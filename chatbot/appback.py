from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import requests
from mail_utils import envoyer_email
from mail_utils import envoyer_email
import random
from mail_utils import envoyer_email
import random
import bcrypt
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify
import traceback
import requests
from cryptography.fernet import Fernet

# Mets ici la clé générée à l’étape précédente
SECRET_KEY = b'zVH9eG61j_XNupj28w7dMaV6RNYBfHgzidFNSJBkO1k='
fernet = Fernet(SECRET_KEY)

# Expressions régulières pour valider email/mot de passe
def email_valide(email):
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(regex, email) is not None



def mot_de_passe_valide(mdp):
    # Mot de passe : au moins 8 caractères, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial
    if not mdp:
        return False
    if len(mdp) < 8:
        return False
    if not re.search(r"[A-Z]", mdp):
        return False
    if not re.search(r"[a-z]", mdp):
        return False
    if not re.search(r"\d", mdp):
        return False
    if not re.search(r"[^A-Za-z0-9]", mdp):
        return False
    return True

codes_reset = {}  # stock temporaire pour les codes, à améliorer pour la prod

app = Flask(__name__)
CORS(app)

# Limite chaque IP à 10 requêtes par minute (tu peux ajuster)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# --- Configuration PostgreSQL ---
conn = psycopg2.connect(
    host="localhost",
    database="Ma_Bdd_sql",
    user="postgres",
    password="admin"
)
cursor = conn.cursor()

# --- Configuration GPT-4o (OpenRouter) ---
api_key = "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"
modell = "openai/gpt-4o"

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="Ma_Bdd_sql",
        user="postgres",
        password="admin"
    )


schema_bdd = """
apprentis(id_apprents, nom, specialite, organisme, date_debut, date_fin, observation, id_employe, departement)
carriere(id_carriere, duree, debut, structure, echelle, classification, medailles, id_employe)
categorie(id_categorie, nom, date_ajouter, id_employe)
conge(id_conge, designation, date_depart, date_reprise, id_employe, est_conge)
droit_conge(id_d_conge, conge_annuelle, conge_recup, conge_scev, id_employe)
employe(id_employe, nom, prenom, date_naissance, lieu_naissance, sexe, adresse, numero_telephone, email, nss, nationalite, groupe_sanguin, situation_familiale, date_recrutement, retenu_panier, benification_transport, is_manager, nb_enfants, reset_code, reset_code_expiration, email_public, telephone_public)
experience(id_experience, poste, employeur, date_debut, date_fin, is_secteur, id_employe)
formation(id_formation, description, date_debut, date_fin, id_employe, type)
inscription_social(id_inscription, sejour, date, type, id_employe)
manager(id_employe, collaborateurs)
mes_prets(id_prets, numero_contract, date_depot, is_accorde, motif_response, motif_prets, montant, duree, rembourse, id_employe, date_debut_remboursement)
message(id_message, expediteur_id, destinataire_id, contenue, date_envoi, lu)
mission(id_mission, objet, lieu, date_debut, date_fin, itineraire, id_employe)
notification(id_notification, date, titre, description, document, est_lue, id_employe)
pointage(id_pointage, heure_arrive, heure_depart, date, id_employe, est_jour_ferie)
poste(code_poste, intitule, service, niveau, echelle, date_recrutement, departement, departement_arrive, diplome_secteur, experience_secteur, experience_hors_secteur, direction, id_employe)
realisation(id_realisation, description, id_employe, date)
remboursement(id_remboursement, id_employe, montant, date_remboursement, type)
retraite(id_retraite, date_depart, date_previsionnelle_retraite, demande_poursuivre, id_employe)
sanction_discipline(id_sanction, date, designation, snc, dnc, id_employe)
"""




# --- Routes ---
@app.route('/')
def home():
    return "Backend connecté avec succès à PostgreSQL 🎉"

# Route de login

# Route : informations employé
@app.route('/employe/<int:id>', methods=['GET'])
def get_employe(id):
    try:
        cursor.execute(
            "SELECT id_employe, nom, prenom, date_naissance, lieu_naissance, sexe, email FROM Employe WHERE id_employe = %s",
            (id,)
        )
        employe = cursor.fetchone()

        if employe:
            return jsonify({
                'id': employe[0],
                'nom': employe[1],
                'prenom': employe[2],
                'date_naissance': employe[3],
                'lieu_naissance': employe[4],
                'sexe': employe[5],
                'email': employe[6],
            })
        else:
            return jsonify({'message': 'Employé non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route : formations de base
@app.route('/formation_base/<int:id_employe>', methods=['GET'])
def get_formation_base(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT description, date_debut, date_fin
            FROM formation
            WHERE id_employe = %s AND (type = 'base' OR type = 'diplome')
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        result = []
        for row in rows:
            result.append({
                'description': row[0],
                'date_debut': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'date_fin': row[2].strftime('%Y-%m-%d') if row[2] else '',
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/missions/<int:id_employe>', methods=['GET'])
def get_missions(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT objet, lieu, date_debut, date_fin, itineraire
            FROM mission
            WHERE id_employe = %s
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        missions = []
        for row in rows:
            missions.append({
                'objet': row[0],
                'lieu': row[1],
                'date_debut': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'date_fin': row[3].strftime('%Y-%m-%d') if row[3] else '',
                'itineraire': row[4]
            })

        return jsonify(missions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conges/<int:id_employe>', methods=['GET'])
def get_conges(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT designation, date_depart, date_reprise
            FROM conge
            WHERE id_employe = %s
            ORDER BY date_depart DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        conges = []
        for row in rows:
            conges.append({
                'designation': row[0],
                'date_depart': row[1].strftime('%Y-%m-%d'),
                'date_reprise': row[2].strftime('%Y-%m-%d'),
            })

        return jsonify(conges)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pointage/<int:id_employe>', methods=['GET'])
def get_pointage(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT date, heure_arrive, heure_depart
            FROM pointage
            WHERE id_employe = %s
            ORDER BY date DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        pointages = []
        for row in rows:
            pointages.append({
                'date': row[0].strftime('%Y-%m-%d'),
                'heure_arrive': row[1],
                'heure_depart': row[2],
            })

        return jsonify(pointages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/absences/<int:id_employe>', methods=['GET'])
def get_absences(id_employe):
    try:
        cur = conn.cursor()
        # On cherche les jours (parmi ceux où il y a un pointage) où le pointage est incomplet ou inexistant
        # 1. Récupérer toutes les dates potentielles de travail (par exemple sur 30 derniers jours)
        cur.execute("""
            SELECT DISTINCT date
            FROM pointage
            WHERE id_employe = %s
              AND (EXTRACT(DOW FROM date) NOT IN (0, 6)) -- Pas week-end (0=dimanche, 6=samedi)
            ORDER BY date DESC
            LIMIT 30
        """, (id_employe,))
        dates_pointage = [row[0] for row in cur.fetchall()]

        absences = []

        for d in dates_pointage:
            # 2. Vérifier si c'est un jour férié
            cur.execute("""
                SELECT est_jour_ferie, heure_arrive, heure_depart
                FROM pointage
                WHERE id_employe = %s AND date = %s
            """, (id_employe, d))
            rows = cur.fetchall()
            if not rows:
                heure_arrive = heure_depart = None
                est_jour_ferie = False
            else:
                est_jour_ferie = any(r[0] for r in rows)
                heure_arrive = rows[0][1]
                heure_depart = rows[0][2]

            if est_jour_ferie:
                continue  # pas une absence, jour férié

            # 3. Vérifier si en congé ce jour-là
            cur.execute("""
                SELECT 1 FROM conge
                WHERE id_employe = %s
                  AND %s BETWEEN date_depart AND date_reprise
            """, (id_employe, d))
            if cur.fetchone():
                continue  # pas une absence, il est en congé

            # 4. Tester absence (pas de pointage OU pointage incomplet)
            absence = False
            details = ""
            if not rows or ((not heure_arrive or heure_arrive.strip() == "") and (not heure_depart or heure_depart.strip() == "")):
                absence = True
                details = "Aucun pointage (ni arrivée ni départ)"
            elif not heure_arrive or heure_arrive.strip() == "":
                absence = True
                details = "Aucune heure d'arrivée marquée"
            elif not heure_depart or heure_depart.strip() == "":
                absence = True
                details = "Aucune heure de départ marquée"

            if absence:
                absences.append({
                    "date": d.strftime('%Y-%m-%d'),
                    "details": details,
                    "heure_arrive": heure_arrive if heure_arrive else "Aucune",
                    "heure_depart": heure_depart if heure_depart else "Aucune"
                })

        cur.close()
        return jsonify(absences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500






    
@app.route('/formations_complementaires/<int:id_employe>', methods=['GET'])
def get_formations_complementaires(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT description, date_debut, date_fin
            FROM formation
            WHERE id_employe = %s AND type = 'complémentaire'
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        formations = []
        for row in rows:
            formations.append({
                'intitule': row[0],
                'date_debut': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'date_fin': row[2].strftime('%Y-%m-%d') if row[2] else ''
            })

        return jsonify(formations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/infos_generales/<int:id_employe>', methods=['GET'])
def get_infos_generales(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                e.nom, e.prenom, e.email, e.numero_telephone,
                e.email_public, e.telephone_public,
                p.intitule, p.service, p.niveau, p.echelle, p.direction,
                c.structure, c.classification, c.debut
            FROM employe e
            LEFT JOIN poste p ON e.id_employe = p.id_employe
            LEFT JOIN carriere c ON e.id_employe = c.id_employe
            WHERE e.id_employe = %s
            LIMIT 1
        """, (id_employe,))
        row = cur.fetchone()
        cur.close()

        if row:
            infos = {
                "nom": row[0],
                "prenom": row[1],
                "email": row[2],
                "numero_telephone": row[3],
                "email_public": row[4],
                "telephone_public": row[5],
                "poste": row[6],
                "service": row[7],
                "niveau": row[8],
                "echelle": row[9],
                "direction": row[10],
                "structure": row[11],
                "classification": row[12],
                "debut_carriere": row[13].strftime('%Y-%m-%d') if row[13] else ''
            }
            return jsonify(infos)
        else:
            return jsonify({"message": "Aucune information trouvée."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/realisations/<int:id_employe>', methods=['GET'])
def get_realisations(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT description, date
            FROM realisation
            WHERE id_employe = %s
            ORDER BY date DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        realisations = []
        for row in rows:
            realisations.append({
                'description': row[0] if row[0] else 'Sans description',
                'date': row[1].strftime('%Y-%m-%d') if row[1] else '-',
            })

        return jsonify(realisations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/experience_hors_secteur/<int:id_employe>', methods=['GET'])
def get_experience_hors_secteur(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT poste, employeur, date_debut, date_fin
            FROM experience_hors_secteur
            WHERE id_employe = %s
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        experiences = []
        for row in rows:
            experiences.append({
                'poste': row[0],
                'employeur': row[1],
                'date_debut': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'date_fin': row[3].strftime('%Y-%m-%d') if row[3] else '',
            })

        return jsonify(experiences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from datetime import date

@app.route('/anciennete_sonatrach/<int:id_employe>', methods=['GET'])
def get_anciennete_sonatrach(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT date_recrutement, intitule, service, niveau, echelle, departement
            FROM poste
            WHERE id_employe = %s
            ORDER BY date_recrutement ASC
            LIMIT 1
        """, (id_employe,))
        row = cur.fetchone()
        cur.close()

        if not row or not row[0]:
            return jsonify([])  # Aucun poste trouvé

        date_recrutement = row[0]
        aujourd_hui = date.today()
        # Calculer l'ancienneté en années et mois
        nb_annees = aujourd_hui.year - date_recrutement.year
        nb_mois = aujourd_hui.month - date_recrutement.month
        if nb_mois < 0:
            nb_annees -= 1
            nb_mois += 12

        anciennete_str = f"{nb_annees} ans, {nb_mois} mois"

        result = [{
            "date_recrutement": date_recrutement.strftime('%Y-%m-%d'),
            "anciennete": anciennete_str,
            "intitule": row[1],
            "service": row[2],
            "niveau": row[3],
            "echelle": row[4],
            "departement": row[5]
        }]

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def est_manager(id_employe):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Manager WHERE Id_Manager = %s", (id_employe,))
    result = cur.fetchone()
    cur.close()
    return result is not None

@app.route('/question', methods=['POST'])
def repondre_question():
    try:
        data = request.get_json()
        question = data['question']
        id_employe = data['id_employe']

        conn = connect_db()
        cursor = conn.cursor()

        # Vérification employé et statut manager
        cursor.execute("SELECT is_manager FROM employe WHERE id_employe = %s", (id_employe,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Employé introuvable."}), 404

        is_manager = result[0]

        collaborateurs_ids = []
        if is_manager:
            cursor.execute("SELECT collaborateurs FROM manager WHERE id_employe = %s", (id_employe,))
            row = cursor.fetchone()
            collaborateurs_ids = [int(id_) for id_ in row[0]] if row and row[0] else []

        prompt = f"""
Tu es un expert SQL assistant d'une application RH.

Voici la structure complète de la base de données :
{schema_bdd}

Utilisateur connecté : id_employe = {id_employe}, is_manager = {is_manager}.

Règles très strictes à respecter :

1. Ne jamais retourner : mot_de_passe, nss.
2. Employé simple (is_manager=False) :
   - Accès strictement à ses propres données : ajouter systématiquement WHERE id_employe = {id_employe}.
   - Refuse immédiatement tout accès aux données d'autres employés.
   - La table formation a trois type de formation : base, complémentaire, previsionnelle.
3. Manager (is_manager=True) :
   - Accès libre à ses propres données.
   - Accès limité aux collaborateurs ({collaborateurs_ids}) UNIQUEMENT pour ces requêtes :
     - "Cite-moi mes collaborateurs" → SELECT id_employe, nom, prenom, email, numero_telephone FROM employe WHERE id_employe IN ({','.join(map(str, collaborateurs_ids))})
     - "Recherche mon collaborateur par id, nom ou prenom" → SELECT id_employe, nom, prenom, adresse, numero_telephone, email, date_recrutement, retenu_panier, groupe_sanguin, situation_familiale FROM employe WHERE id_employe IN ({','.join(map(str, collaborateurs_ids))}) ET filtrer par nom, prenom ou id.
     - Formations prévisionnelles : table formation (type='previsionnelle')
     - Droits à congés : table droit_conge
     - Sanctions disciplinaires : table sanction_discipline
     - Assiduité (pointage) : table pointage
     - Apprentis du département TI : table apprentis (departement='TI' ou 'technologie de l''information' ou 'technologie information' ou 'technologie informatique') qui contient tous les employés pas seulement les collaborateurs ou bien seulement les collaborateurs selon la question posé mais seulement (departement='TI' ou 'technologie de l''information' ou 'technologie information' ou 'technologie informatique') .

- Toute autre requête concernant les collaborateurs doit être explicitement refusée.

**Consignes techniques PostgreSQL à respecter impérativement** :
- Si la question nécessite de filtrer par année sur une colonne de type date, utilise toujours la syntaxe PostgreSQL EXTRACT(YEAR FROM nom_colonne) = année au lieu de YEAR(nom_colonne).
- Si la question nécessite de faire une opération entre une date et un nombre de jours (par exemple : "cette semaine", "7 derniers jours"), utilise la syntaxe PostgreSQL : date_colonne BETWEEN CURRENT_DATE - INTERVAL '1 day' * nombre_de_jours AND CURRENT_DATE.

Analyse précisément cette question, applique ces règles strictement, et génère UNIQUEMENT la requête SQL finale sans explication ni markdown :

"{question}"
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://chat.openrouter.ai/",
                "Content-Type": "application/json"
            },
            json={
                "model": modell,
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        result = response.json()

        if "error" in result:
            return jsonify({"error": result["error"]["message"]}), 500

        sql_query = result["choices"][0]["message"]["content"].strip()

        # Nettoyage éventuel du résultat
        if sql_query.startswith("```"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        colonnes_interdites = ["mot_de_passe", "nss"]
        if any(col.lower() in sql_query.lower() for col in colonnes_interdites):
            return jsonify({"error": "Accès interdit à une colonne sensible détecté!"}), 403

        # Affichage clair pour debug
        print("\n✅ SQL exécutée :\n", sql_query, "\n")

        # Exécution sécurisée
                # Exécution sécurisée
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # ✅ Récupère les noms des colonnes AVANT de fermer le curseur
        col_names = [desc[0] for desc in cursor.description]
        result_dicts = [dict(zip(col_names, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify({"query": sql_query, "result": result_dicts})



    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500






@app.route('/recherche_employe', methods=['POST'])
def recherche_employe():
    try:
        data = request.get_json()
        nom = data.get('nom', '').strip()
        prenom = data.get('prenom', '').strip()
        matricule = data.get('matricule', '').strip()
        departement = data.get('departement', '').strip()

        query = """
            SELECT nom, prenom, adresse, numero_telephone, email, date_recrutement,
                   retenu_panier, groupe_sanguin, situation_familiale
            FROM employe
            WHERE 1=1
        """
        params = []

        if nom:
            query += " AND LOWER(nom) = LOWER(%s)"
            params.append(nom)
        if prenom:
            query += " AND LOWER(prenom) = LOWER(%s)"
            params.append(prenom)
        if matricule:
            query += " AND CAST(id_employe AS TEXT) = %s"
            params.append(matricule)
        if departement:
            query += """
                AND id_employe IN (
                    SELECT id_employe FROM poste WHERE LOWER(departement) = LOWER(%s)
                )
            """
            params.append(departement)

        cur = conn.cursor()
        cur.execute(query, tuple(params))
        row = cur.fetchone()
        cur.close()

        if row:
            return jsonify({
                'nom': row[0],
                'prenom': row[1],
                'adresse': row[2],
                'numero_telephone': row[3],
                'email': row[4],
                'date_recrutement': row[5].strftime('%Y-%m-%d') if row[5] else '',
                'retenu_panier': row[6],
                'groupe_sanguin': row[7],
                'situation_familiale': row[8]
            })
        else:
            return jsonify({'message': 'Aucun collaborateur trouvé'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/liste_collaborateurs/<int:id_employe>', methods=['GET'])
def liste_collaborateurs(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_employe, nom, prenom, email, numero_telephone, date_recrutement
            FROM employe
            WHERE id_employe != %s
            ORDER BY nom
        """, (id_employe,))  # ✅ ici tu passes l'id
        rows = cur.fetchall()
        cur.close()

        collaborateurs = []
        for row in rows:
            collaborateurs.append({
                'id': row[0],
                'nom': row[1],
                'prenom': row[2],
                'email': row[3],
                'telephone': row[4],
                'date_recrutement': row[5].strftime('%Y-%m-%d') if row[5] else ''
            })

        return jsonify(collaborateurs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/collaborateur/<int:id_employe>', methods=['GET'])
def detail_collaborateur(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT nom, prenom, email, numero_telephone, adresse,
                   date_recrutement, groupe_sanguin, situation_familiale
            FROM employe
            WHERE id_employe = %s
        """, (id_employe,))
        row = cur.fetchone()
        cur.close()

        if row:
            return jsonify({
                'nom': row[0],
                'prenom': row[1],
                'email': row[2],
                'telephone': row[3],
                'adresse': row[4],
                'date_recrutement': row[5].strftime('%Y-%m-%d') if row[5] else '',
                'groupe_sanguin': row[6],
                'situation_familiale': row[7]
            })
        else:
            return jsonify({'message': 'Employé introuvable'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/assiduite_collaborateurs/<int:id_manager>', methods=['GET'])
def assiduite_collaborateurs(id_manager):
    try:
        cur = conn.cursor()
        # Vérifier que l'employé est bien manager
        cur.execute("SELECT is_manager FROM employe WHERE id_employe = %s", (id_manager,))
        row = cur.fetchone()
        if not row or not row[0]:
            cur.close()
            return jsonify({'error': "Accès refusé : vous n'êtes pas un manager."}), 403

        # Récupérer la liste des collaborateurs
        cur.execute("SELECT collaborateurs FROM manager WHERE id_employe = %s", (id_manager,))
        row = cur.fetchone()
        if not row or not row[0]:
            cur.close()
            return jsonify([])  # Pas de collaborateurs

        collaborateurs_ids = [int(x) for x in row[0]]  # Array d'ids

        # Chercher le pointage des collaborateurs (par date décroissante)
        cur.execute("""
            SELECT e.nom, e.prenom, p.date, p.heure_arrive, p.heure_depart
            FROM employe e
            JOIN pointage p ON e.id_employe = p.id_employe
            WHERE e.id_employe = ANY(%s)
            ORDER BY p.date DESC, e.nom
        """, (collaborateurs_ids,))
        rows = cur.fetchall()
        cur.close()

        result = []
        for row in rows:
            result.append({
                'nom': row[0],
                'prenom': row[1],
                'date': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'heure_arrive': row[3],
                'heure_depart': row[4],
            })

        return jsonify(result)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/formations_previsionnelles/<int:id_employe>', methods=['GET'])
def get_formations_previsionnelles(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT description, date_debut, date_fin, type
            FROM formation
            WHERE id_employe = %s AND LOWER(type) = 'previsionnelle'
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        formations = []
        for row in rows:
            formations.append({
                'description': row[0],
                'date_debut': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'date_fin': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'type': row[3],
            })

        return jsonify(formations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sanctions/<int:id_employe>', methods=['GET'])
def get_sanctions(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT date, designation, snc, dnc
            FROM sanction_discipline
            WHERE id_employe = %s
            ORDER BY date DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        sanctions = []
        for row in rows:
            sanctions.append({
                'date': row[0].strftime('%Y-%m-%d') if row[0] else '',
                'designation': row[1],
                'snc': row[2],
                'dnc': row[3],
            })

        return jsonify(sanctions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/droits_conge/<int:id_employe>', methods=['GET'])
def get_droits_conge(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT conge_annuelle, conge_recup, conge_scev
            FROM droit_conge
            WHERE id_employe = %s
        """, (id_employe,))
        row = cur.fetchone()
        cur.close()

        if row:
            return jsonify({
                'conge_annuelle': row[0].strftime('%Y-%m-%d') if row[0] else '',
                'conge_recup': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'conge_scev': row[2].strftime('%Y-%m-%d') if row[2] else '',
            })
        else:
            return jsonify({'message': 'Aucun droit à congé trouvé'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/plannings_conge/<int:id_employe>', methods=['GET'])
def get_plannings_conge(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT designation, date_depart, date_reprise
            FROM conge
            WHERE id_employe = %s
            ORDER BY date_depart DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        plannings = []
        for row in rows:
            plannings.append({
                'designation': row[0],
                'date_depart': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'date_reprise': row[2].strftime('%Y-%m-%d') if row[2] else ''
            })

        return jsonify(plannings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/weekends_feries/<int:id_employe>', methods=['GET'])
def get_weekends_feries(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT date, heure_arrive, heure_depart, est_jour_ferie
            FROM pointage
            WHERE id_employe = %s
              AND (
                est_jour_ferie = TRUE
                OR EXTRACT(DOW FROM date) IN (5,6)
              )
            ORDER BY date DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        jours = []
        for row in rows:
            # Jour de la semaine (0=dimanche ... 5=vendredi, 6=samedi)
            day = row[0].strftime('%A')  # en français, installer locale si besoin
            type_jour = "Jour Férié" if row[3] else "Weekend"
            # Compensation: c'est un exemple, tu peux adapter le texte
            compensation = "Récupération" if row[3] else "Prime Weekend"
            jours.append({
                "date": row[0].strftime('%Y-%m-%d'),
                "heure_arrive": row[1] if row[1] else 'Non renseignée',
                "heure_depart": row[2] if row[2] else 'Non renseignée',
                "type_jour": type_jour,
                "compensation": compensation
            })
        return jsonify(jours)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sejour_asl/<int:id_employe>', methods=['GET'])
def get_sejour_asl(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT sejour, date
            FROM inscription_social
            WHERE id_employe = %s AND type = 'ASL'
            ORDER BY date DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        sejours = []
        for row in rows:
            sejours.append({
                'sejour': row[0] if row[0] else '-',
                'date': row[1].strftime('%Y-%m-%d') if row[1] else '-',
            })

        return jsonify(sejours)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sejours_mip/<int:id_employe>', methods=['GET'])
def get_sejours_mip(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT sejour, date
            FROM inscription_social
            WHERE id_employe = %s AND type = 'MIP'
            ORDER BY date DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        sejours = []
        for row in rows:
            sejours.append({
                'sejour': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else '',
            })

        return jsonify(sejours)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/mes_prets_en_cours/<int:id_employe>', methods=['GET'])
def get_mes_prets_en_cours(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_prets, numero_contract, date_depot, is_accorde, motif_response,
                   motif_prets, montant, duree, rembourse
            FROM mes_prets
            WHERE id_employe = %s AND rembourse = FALSE
            ORDER BY date_depot DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        prets = []
        for row in rows:
            prets.append({
                'id_prets': row[0],
                'numero_contract': row[1],
                'date_depot': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'is_accorde': row[3],
                'motif_response': row[4],
                'motif_prets': row[5],
                'montant': float(row[6]) if row[6] is not None else 0.0,
                'duree': row[7],
                'rembourse': row[8]
            })

        return jsonify(prets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/mes_courants_prets/<int:id_employe>', methods=['GET'])
def get_mes_courants_prets(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_contract, montant, duree, date_depot, rembourse
            FROM mes_prets
            WHERE id_employe = %s
            ORDER BY date_depot DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        result = []
        for row in rows:
            numero_contract = row[0]
            montant = float(row[1]) if row[1] is not None else 0.0
            duree = row[2]
            date_depot = row[3].strftime('%Y-%m-%d') if row[3] else ""
            rembourse = row[4]
            date_debut_remboursement = date_depot if rembourse else "-----"

            result.append({
                "numero_contract": numero_contract,
                "montant": montant,
                "duree": duree,
                "date_debut_remboursement": date_debut_remboursement,
                "rembourse": rembourse
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/etat_civil/<int:id_employe>', methods=['GET'])
def get_etat_civil(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_employe, nom, prenom, date_naissance, lieu_naissance, situation_familiale, 
                   nb_enfants, adresse
            FROM employe
            WHERE id_employe = %s
        """, (id_employe,))
        row = cur.fetchone()
        cur.close()

        if row:
            data = {
                "matricule": row[0],
                "nom": row[1],
                "prenom": row[2],
                "date_naissance": row[3].strftime('%Y-%m-%d') if row[3] else "",
                "lieu_naissance": row[4] or "",
                "situation_familiale": row[5] or "",
                "nb_enfants": row[6] if row[6] is not None else "",
                "adresse": row[7] or ""
            }
            return jsonify(data)
        else:
            return jsonify({"error": "Employé introuvable"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/experience_secteur/<int:id_employe>', methods=['GET'])
def get_experience_secteur(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT poste, employeur, date_debut, date_fin
            FROM experience
            WHERE id_employe = %s AND is_secteur = TRUE
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        experiences = []
        for row in rows:
            experiences.append({
                'poste': row[0],
                'employeur': row[1],
                'date_debut': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'date_fin': row[3].strftime('%Y-%m-%d') if row[3] else '',
            })

        return jsonify(experiences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/exp_hors_secteur/<int:id_employe>', methods=['GET'])
def get_exp_hors_secteur_employe(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT poste, employeur, date_debut, date_fin
            FROM experience
            WHERE id_employe = %s AND is_secteur = FALSE
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        experiences = []
        for row in rows:
            experiences.append({
                'poste': row[0],
                'employeur': row[1],
                'date_debut': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'date_fin': row[3].strftime('%Y-%m-%d') if row[3] else '',
            })

        return jsonify(experiences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/remboursements_mip_cnas/<int:id_employe>', methods=['GET'])
def get_remboursements_mip_cnas(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT type, montant, date_remboursement
            FROM remboursement
            WHERE id_employe = %s
            ORDER BY date_remboursement DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        remboursements = []
        for row in rows:
            remboursements.append({
                'type': row[0],  # 'MIP' ou 'CNAS'
                'montant': float(row[1]) if row[1] else 0,
                'date_remboursement': row[2].strftime('%Y-%m-%d') if row[2] else '',
            })
        return jsonify(remboursements)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from flask import jsonify

@app.route('/listing_collaborateurs/<int:id_employe>', methods=['GET'])
def listing_collaborateurs(id_employe):
    import traceback
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT collaborateurs
            FROM manager
            WHERE id_employe = %s
        """, (id_employe,))
        row = cur.fetchone()
        if not row or not row[0]:
            cur.close()
            return jsonify([])

        collaborateurs_ids = row[0]
        # On convertit tous les IDs en INT (ils viennent comme str depuis character varying[])
        collaborateurs_ids_int = [int(x) for x in collaborateurs_ids]

        cur.execute("""
            SELECT id_employe, nom, prenom, email, numero_telephone
            FROM employe
            WHERE id_employe = ANY(%s)
        """, (collaborateurs_ids_int,))
        collaborateurs = [
            {
                'id_employe': c[0],
                'nom': c[1],
                'prenom': c[2],
                'email': c[3],
                'numero_telephone': c[4]
            }
            for c in cur.fetchall()
        ]
        cur.close()
        return jsonify(collaborateurs)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/droits_conge_collaborateurs/<int:id_employe_manager>', methods=['GET'])
def droits_conge_collaborateurs(id_employe_manager):
    try:
        cur = conn.cursor()
        # 1. Récupérer les IDs collaborateurs du manager
        cur.execute("""
            SELECT collaborateurs FROM manager WHERE id_employe = %s
        """, (id_employe_manager,))
        row = cur.fetchone()
        if not row or not row[0]:
            cur.close()
            return jsonify([])

        collaborateurs_ids = [int(x) for x in row[0]]

        # 2. Récupérer les droits à congé de ces collaborateurs
        cur.execute("""
            SELECT dc.id_employe, e.nom, e.prenom,
                   dc.conge_annuelle, dc.conge_recup, dc.conge_scev
            FROM droit_conge dc
            JOIN employe e ON dc.id_employe = e.id_employe
            WHERE dc.id_employe = ANY(%s)
            ORDER BY e.nom, e.prenom
        """, (collaborateurs_ids,))
        rows = cur.fetchall()
        cur.close()

        droits = []
        for r in rows:
            droits.append({
                'id_employe': r[0],
                'nom': r[1],
                'prenom': r[2],
                'conge_annuelle': r[3].strftime('%Y-%m-%d') if r[3] else None,
                'conge_recup': r[4].strftime('%Y-%m-%d') if r[4] else None,
                'conge_scev': r[5].strftime('%Y-%m-%d') if r[5] else None,
            })

        return jsonify(droits)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
@app.route('/formations_previsionnelles_collaborateurs/<int:id_employe_manager>', methods=['GET'])
def formations_previsionnelles_collaborateurs(id_employe_manager):
    try:
        cur = conn.cursor()
        # 1. Récupérer les ID des collaborateurs du manager
        cur.execute("""
            SELECT collaborateurs
            FROM manager
            WHERE id_employe = %s
        """, (id_employe_manager,))
        row = cur.fetchone()
        if not row or not row[0]:
            cur.close()
            return jsonify([])

        collaborateurs_ids = [int(x) for x in row[0]]  # Convert to int

        # 2. Chercher les formations prévisionnelles des collaborateurs
        cur.execute("""
            SELECT f.id_formation, f.description, f.date_debut, f.date_fin, f.id_employe, e.nom, e.prenom
            FROM formation f
            JOIN employe e ON f.id_employe = e.id_employe
            WHERE f.id_employe = ANY(%s)
              AND f.type = 'previsionnelle'
            ORDER BY f.date_debut DESC
        """, (collaborateurs_ids,))
        rows = cur.fetchall()
        cur.close()

        formations = []
        for row in rows:
            formations.append({
                'id_formation': row[0],
                'description': row[1],
                'date_debut': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'date_fin': row[3].strftime('%Y-%m-%d') if row[3] else '',
                'id_employe': row[4],
                'nom': row[5],
                'prenom': row[6],
            })

        return jsonify(formations)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/recherche_collaborateur_manager/<int:id_manager>', methods=['POST'])
def recherche_collaborateur_manager(id_manager):
    try:
        data = request.get_json()
        nom = data.get('nom', '').strip()
        prenom = data.get('prenom', '').strip()
        matricule = data.get('matricule', '').strip()

        cur = conn.cursor()

        # Récupérer la liste des IDs collaborateurs du manager
        cur.execute("""
            SELECT collaborateurs
            FROM manager
            WHERE id_employe = %s
        """, (id_manager,))
        row = cur.fetchone()

        if not row or not row[0] or len(row[0]) == 0:
            cur.close()
            return jsonify({'message': 'Aucun collaborateur trouvé.'}), 404

        collaborateurs_ids = row[0]  # ARRAY de string (ex: ['1','2','3','5'])
        # Si le champ id_employe est de type integer, on convertit les valeurs en int
        collaborateurs_ids_int = [int(i) for i in collaborateurs_ids]

        # Construction dynamique de la requête
        query = """
            SELECT id_employe, nom, prenom, adresse, numero_telephone, email,
                   date_recrutement, retenu_panier, groupe_sanguin, situation_familiale
            FROM employe
            WHERE id_employe = ANY(%s)
        """
        params = [collaborateurs_ids_int]

        if matricule:
            query += " AND CAST(id_employe AS TEXT) = %s"
            params.append(matricule)
        if nom:
            query += " AND LOWER(nom) = LOWER(%s)"
            params.append(nom)
        if prenom:
            query += " AND LOWER(prenom) = LOWER(%s)"
            params.append(prenom)

        cur.execute(query, tuple(params))
        result = cur.fetchone()
        cur.close()

        if result:
            return jsonify({
                'id_employe': result[0],
                'nom': result[1],
                'prenom': result[2],
                'adresse': result[3],
                'numero_telephone': result[4],
                'email': result[5],
                'date_recrutement': result[6].strftime('%Y-%m-%d') if result[6] else '',
                'retenu_panier': result[7],
                'groupe_sanguin': result[8],
                'situation_familiale': result[9]
            })
        else:
            return jsonify({'message': 'Aucun collaborateur trouvé.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/achats_vehicule/<int:id_employe>', methods=['GET'])
def achats_vehicule(id_employe):
    try:
        cur = conn.cursor()
        # On utilise ILIKE pour matcher 'vehicule' ou 'voiture' peu importe la casse
        cur.execute("""
            SELECT numero_contract, date_depot, montant, duree, motif_prets
            FROM mes_prets
            WHERE id_employe = %s
              AND rembourse = TRUE
              AND (
                motif_prets ILIKE '%%vehicule%%'
                OR motif_prets ILIKE '%%voiture%%'
              )
            ORDER BY date_depot DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        result = []
        for row in rows:
            result.append({
                'numero_contract': row[0],
                'date_depot': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'montant': float(row[2]),
                'duree': row[3],
                'motif_prets': row[4]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Backend Flask (ajoute cette route)
@app.route('/prets_sociaux/<int:id_employe>', methods=['GET'])
def get_prets_sociaux(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_contract, date_depot, montant, duree, motif_prets
            FROM mes_prets
            WHERE id_employe = %s
              AND LOWER(motif_prets) LIKE '%%social%%'
              AND rembourse = true
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        prets = []
        for row in rows:
            prets.append({
                'numero_contract': row[0],
                'date_depot': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'montant': row[2],
                'duree': row[3],
                'motif_prets': row[4],
            })
        return jsonify(prets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/prets_logement_cal/<int:id_employe>', methods=['GET'])
def get_prets_logement_cal(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_contract, date_depot, montant, duree, motif_prets
            FROM mes_prets
            WHERE id_employe = %s
              AND (
                  LOWER(motif_prets) LIKE '%%cal%%'
                  OR LOWER(motif_prets) LIKE '%%logement%%'
                  OR LOWER(motif_prets) LIKE '%%immobilier%%'
              )
              AND rembourse = true
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        prets = []
        for row in rows:
            prets.append({
                'numero_contract': row[0],
                'date_depot': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'montant': row[2],
                'duree': row[3],
                'motif_prets': row[4],
            })
        return jsonify(prets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/suspensions_collaborateurs/<int:id_employe_manager>', methods=['GET'])
def suspensions_collaborateurs(id_employe_manager):
    try:
        cur = conn.cursor()
        # 1. Récupérer les ID des collaborateurs du manager
        cur.execute("""
            SELECT collaborateurs
            FROM manager
            WHERE id_employe = %s
        """, (id_employe_manager,))
        row = cur.fetchone()
        if not row or not row[0]:
            cur.close()
            return jsonify([])

        # ➜ Eliminer les doublons de la liste d'ID collaborateurs
        collaborateurs_ids = list(set([int(x) for x in row[0]]))

        # 2. Chercher les suspensions (sanctions disciplinaires) des collaborateurs
        cur.execute("""
            SELECT DISTINCT s.id_sanction, s.date, s.designation, s.snc, s.dnc, s.id_employe, e.nom, e.prenom
            FROM sanction_discipline s
            JOIN employe e ON s.id_employe = e.id_employe
            WHERE s.id_employe = ANY(%s)
            ORDER BY s.date DESC
        """, (collaborateurs_ids,))
        rows = cur.fetchall()
        cur.close()

        suspensions = []
        for row in rows:
            suspensions.append({
                'id_sanction': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'designation': row[2],
                'snc': row[3],
                'dnc': row[4],
                'id_employe': row[5],
                'nom': row[6],
                'prenom': row[7],
            })

        return jsonify(suspensions)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/apprentis_departement_ti', methods=['GET'])
def apprentis_departement_ti():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_apprents, nom, specialite, organisme, date_debut, date_fin, observation, departement
            FROM apprentis
            WHERE LOWER(departement) IN ('ti', 'technologie information', 'technologie de l''information','technologie informatique')
            ORDER BY date_debut DESC
        """)
        rows = cur.fetchall()
        cur.close()

        apprentis = []
        for row in rows:
            apprentis.append({
                'id_apprents': row[0],
                'nom': row[1],
                'specialite': row[2],
                'organisme': row[3],
                'date_debut': row[4].strftime('%Y-%m-%d') if row[4] else '',
                'date_fin': row[5].strftime('%Y-%m-%d') if row[5] else '',
                'observation': row[6],
                'departement': row[7],
            })
        return jsonify(apprentis)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/modifier_mot_de_passe/<int:id_employe>', methods=['POST'])
def modifier_mot_de_passe(id_employe):
    try:
        data = request.get_json()
        ancien = data.get("ancien")
        nouveau = data.get("nouveau")

        cur = conn.cursor()
        cur.execute("SELECT mot_de_passe FROM employe WHERE id_employe = %s", (id_employe,))
        row = cur.fetchone()
        if not row or not bcrypt.checkpw(ancien.encode('utf-8'), row[0].encode('utf-8')):
            cur.close()
            return jsonify({'error': "Ancien mot de passe incorrect."}), 400

        # Vérification de la sécurité du nouveau mot de passe
        if not mot_de_passe_valide(nouveau):
            cur.close()
            return jsonify({'error': "Le nouveau mot de passe n'est pas assez sécurisé (8 caractères, majuscule, minuscule, chiffre, spécial)."}), 400

        # Hash le nouveau mot de passe
        hashed = bcrypt.hashpw(nouveau.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur.execute("UPDATE employe SET mot_de_passe = %s WHERE id_employe = %s", (hashed, id_employe))
        conn.commit()
        cur.close()
        return jsonify({"message": "Mot de passe changé avec succès."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/demander_code_reset', methods=['POST'])
def demander_code_reset():
    try:
        data = request.get_json()
        email = data.get('email')
        cur = conn.cursor()
        cur.execute("SELECT id_employe FROM employe WHERE email = %s", (email,))
        row = cur.fetchone()
        if not row:
            return jsonify({'error': 'Email inconnu'}), 404
        id_employe = row[0]
        code = str(random.randint(100000, 999999))
        codes_reset[email] = code

        envoyer_email(
            email,
            "Votre code de réinitialisation de mot de passe",
            f"Votre code de vérification est : {code}"
        )
        return jsonify({'message': 'Code envoyé à votre adresse email.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. Vérifier le code et changer le mot de passe
@app.route('/reset_mot_de_passe', methods=['POST'])
def reset_mot_de_passe():
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        nouveau_mdp = data.get('nouveau_mdp')

        if codes_reset.get(email) != code:
            return jsonify({'error': 'Code invalide'}), 400

        # Vérification de la sécurité du mot de passe
        if not mot_de_passe_valide(nouveau_mdp):
            return jsonify({'error': "Le nouveau mot de passe n'est pas assez sécurisé (8 caractères, majuscule, minuscule, chiffre, spécial)."}), 400

        hashed = bcrypt.hashpw(nouveau_mdp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur = conn.cursor()
        cur.execute("UPDATE employe SET mot_de_passe = %s WHERE email = %s", (hashed, email))
        conn.commit()
        cur.close()
        codes_reset.pop(email, None)
        return jsonify({'message': 'Mot de passe modifié avec succès !'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# --- messagerie ---
# ENVOYER UN MESSAGE
@app.route('/messages/envoyer', methods=['POST'])
def envoyer_message():
    data = request.get_json()
    expediteur_id = data.get('expediteur_id')
    destinataire_id = data.get('destinataire_id')
    contenu = data.get('contenu')

    if not expediteur_id or not destinataire_id or not contenu:
        return jsonify({'error': 'Champs manquants'}), 400

    # Chiffrement du message
    contenu_crypte = fernet.encrypt(contenu.encode()).decode()

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO message (expediteur_id, destinataire_id, contenu)
        VALUES (%s, %s, %s)
    """, (expediteur_id, destinataire_id, contenu_crypte))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Message envoyé !'})

@app.route('/messages/conversation', methods=['GET'])
def get_conversation():
    expediteur_id = request.args.get('expediteur_id')
    destinataire_id = request.args.get('destinataire_id')
    cur = conn.cursor()
    cur.execute("""
        SELECT id_message, expediteur_id, destinataire_id, contenu, date_envoi, lu
        FROM message
        WHERE (expediteur_id = %s AND destinataire_id = %s)
           OR (expediteur_id = %s AND destinataire_id = %s)
        ORDER BY date_envoi ASC
    """, (expediteur_id, destinataire_id, destinataire_id, expediteur_id))
    rows = cur.fetchall()
    cur.close()
    messages = []
    for r in rows:
        try:
            contenu_dechiffre = fernet.decrypt(r[3].encode()).decode()
        except Exception:
            contenu_dechiffre = "[Message illisible]"
        messages.append({
            'id_message': r[0],
            'expediteur_id': r[1],
            'destinataire_id': r[2],
            'contenu': contenu_dechiffre,
            'date_envoi': r[4].strftime('%Y-%m-%d %H:%M:%S'),
            'lu': r[5]
        })
    return jsonify(messages)

@app.route('/messages/conversations/<int:id_employe>', methods=['GET'])
def liste_conversations(id_employe):
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id_employe, e.nom, e.prenom,
            (SELECT contenu FROM message m2 
             WHERE ((m2.expediteur_id = e.id_employe AND m2.destinataire_id = %s)
                 OR (m2.destinataire_id = e.id_employe AND m2.expediteur_id = %s))
             ORDER BY date_envoi DESC LIMIT 1) AS dernier_message,
            (SELECT date_envoi FROM message m2 
             WHERE ((m2.expediteur_id = e.id_employe AND m2.destinataire_id = %s)
                 OR (m2.destinataire_id = e.id_employe AND m2.expediteur_id = %s))
             ORDER BY date_envoi DESC LIMIT 1) AS date_envoi,
            (SELECT COUNT(*) FROM message m3 
             WHERE m3.expediteur_id = e.id_employe AND m3.destinataire_id = %s AND m3.lu = FALSE) AS non_lus
        FROM employe e
        WHERE e.id_employe != %s
        ORDER BY date_envoi DESC NULLS LAST
    """, (id_employe, id_employe, id_employe, id_employe, id_employe, id_employe))
    rows = cur.fetchall()
    cur.close()
    conversations = []
    for r in rows:
        if r[3]:  # dernier_message non NULL hadi li dechifri les messages
            try:
                dernier_message = fernet.decrypt(r[3].encode()).decode()
            except Exception:
                dernier_message = "[MESSAGE ILLISIBLE]"
            conversations.append({
                'autre_id': r[0],
                'nom': r[1],
                'prenom': r[2],
                'dernier_message': dernier_message,
                'date_envoi': r[4].strftime('%Y-%m-%d %H:%M') if r[4] else '',
                'non_lus': r[5]
            })
    return jsonify(conversations)


# RECHERCHE D'EMPLOYÉS (pour la barre de recherche)
@app.route('/employes/recherche', methods=['GET'])
def rechercher_employes():
    query = request.args.get('query', '')
    cur = conn.cursor()
    cur.execute("""
        SELECT id_employe, nom, prenom
        FROM employe
        WHERE LOWER(nom) LIKE %s OR LOWER(prenom) LIKE %s OR CAST(id_employe AS TEXT) LIKE %s
        LIMIT 20
    """, (f'%{query.lower()}%', f'%{query.lower()}%', f'%{query}%'))
    rows = cur.fetchall()
    cur.close()
    employes = [{'id_employe': r[0], 'nom': r[1], 'prenom': r[2]} for r in rows]
    return jsonify(employes)
@app.route('/messages/lire', methods=['POST'])
def marquer_lus():
    data = request.get_json()
    expediteur_id = data.get('expediteur_id')
    destinataire_id = data.get('destinataire_id')
    cur = conn.cursor()
    cur.execute("""
        UPDATE message SET lu = TRUE
        WHERE expediteur_id = %s AND destinataire_id = %s AND lu = FALSE
    """, (expediteur_id, destinataire_id))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Messages marqués comme lus'})

###########################
@app.route('/notifications/<int:id_employe>', methods=['GET'])
def get_notifications(id_employe):
    conn = psycopg2.connect(
        host="localhost",
        database="Ma_Bdd_sql",
        user="postgres",
        password="admin"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT id_notification, date, titre, description, document, est_lue
        FROM notification
        WHERE id_employe = %s
        ORDER BY date DESC
    """, (id_employe,))
    rows = cur.fetchall()
    notifs = []
    for r in rows:
        notifs.append({
            "id_notification": r[0],
            "date": r[1].strftime('%Y-%m-%d %H:%M'),
            "titre": r[2],
            "description": r[3],
            "document": r[4],
            "est_lue": r[5]
        })
    cur.close()
    conn.close()
    return jsonify(notifs)

@app.route('/notifications/non_lues/<int:id_employe>', methods=['GET'])
def get_non_lues(id_employe):
    conn = psycopg2.connect(
        host="localhost",
        database="Ma_Bdd_sql",
        user="postgres",
        password="admin"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM notification
        WHERE id_employe = %s AND est_lue = FALSE
    """, (id_employe,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"non_lues": count})

@app.route('/notifications/lire/<int:id_notification>', methods=['POST'])
def lire_notification(id_notification):
    conn = psycopg2.connect(
        host="localhost",
        database="Ma_Bdd_sql",
        user="postgres",
        password="admin"
    )
    cur = conn.cursor()
    cur.execute("""
        UPDATE notification
        SET est_lue = TRUE
        WHERE id_notification = %s
    """, (id_notification,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Notification marquée comme lue"})

##################################
from flask import Flask, request, jsonify
from datetime import date

@app.route('/retraite/<int:id_employe>')
def get_retraite(id_employe):
    cur = conn.cursor()
    # Récupérer la date de naissance de l'employé
    cur.execute("SELECT date_naissance FROM employe WHERE id_employe = %s", (id_employe,))
    emp = cur.fetchone()
    if not emp:
        cur.close()
        return jsonify({'error': 'Employé non trouvé'}), 404
    date_naissance = emp[0]

    # Calcul de l'âge
    from datetime import datetime
    today = datetime.today().date()
    age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))

    # Récupérer l'info retraite s'il a 60 ans ou plus
    cur.execute("SELECT date_depot, date_previsionnelle_retraite, demande_poursuivre FROM retraite WHERE id_employe = %s", (id_employe,))
    retraite = cur.fetchone()
    cur.close()

    # Génère la réponse selon l'âge
    if age < 60:
        return jsonify({'age': age, 'status': 'non_concerne', 'message': 'Vous n\'êtes pas concerné(e) par la retraite pour le moment.'})
    
    # Le reste de la logique retraite (comme avant)
    if not retraite:
        return jsonify({'age': age, 'status': 'pas_de_dossier', 'message': "Vous n'avez pas déposé un dossier retraite."})
    date_depot, date_prev, demande_poursuivre = retraite

    if date_depot and date_prev and (not demande_poursuivre):
        return jsonify({
            'age': age,
            'status': 'retraite_normale',
            'message': "Votre dossier retraite est en cours pour un départ à 60 ans.",
            'date_depot': str(date_depot),
            'date_previsionnelle': str(date_prev)
        })
    elif not date_depot and not date_prev and demande_poursuivre:
        return jsonify({
            'age': age,
            'status': 'poursuite',
            'message': "Vous avez choisi de poursuivre le travail après 60 ans."
        })
    else:
        return jsonify({
            'age': age,
            'status': 'incomplet',
            'message': "Merci de déposer une demande (Départ à la retraite ou Poursuite du travail)."
        })

################################################
@app.route('/employes/recherche_global', methods=['GET'])
def rechercher_employes_global():
    query = request.args.get('query', '')
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            e.id_employe, e.nom, e.prenom, e.adresse, e.email, e.email_public, 
            e.numero_telephone, e.telephone_public,
            p.intitule AS poste, p.service, p.direction, p.departement
        FROM employe e
        LEFT JOIN poste p ON e.id_employe = p.id_employe
        WHERE 
            LOWER(e.nom) LIKE %s
            OR LOWER(e.prenom) LIKE %s
            OR LOWER(COALESCE(p.departement, '')) LIKE %s
            OR LOWER(COALESCE(p.service, '')) LIKE %s
            OR LOWER(COALESCE(p.direction, '')) LIKE %s
    """, (
        f'%{query.lower()}%',
        f'%{query.lower()}%',
        f'%{query.lower()}%',
        f'%{query.lower()}%',
        f'%{query.lower()}%',
    ))
    rows = cur.fetchall()
    cur.close()
    employes = []
    for r in rows:
        email = r[4] if r[5] else "Privé"
        numero_telephone = r[6] if r[7] else "Privé"
        employes.append({
            'id_employe': r[0],
            'nom': r[1],
            'prenom': r[2],
            'adresse': r[3],
            'email': email,
            'numero_telephone': numero_telephone,
            'poste': r[8],
            'service': r[9],
            'direction': r[10],
            'departement': r[11]
        })
    return jsonify(employes)

@app.route('/employe/modifier_visibilite', methods=['POST'])
def modifier_visibilite():
    data = request.get_json()
    id_employe = data.get('id_employe')
    email_public = data.get('email_public')
    telephone_public = data.get('telephone_public')

    cur = conn.cursor()
    cur.execute("""
        UPDATE employe SET email_public = %s, telephone_public = %s WHERE id_employe = %s
    """, (email_public, telephone_public, id_employe))
    conn.commit()
    cur.close()
    return jsonify({'status': 'ok'})

@app.route('/documents', methods=['GET'])
def get_documents():
    cur = conn.cursor()
    cur.execute("SELECT id_document, titre, chemin FROM document")
    rows = cur.fetchall()
    cur.close()
    docs = [{"id": r[0], "titre": r[1], "chemin": r[2]} for r in rows]
    return jsonify(docs)

@app.route('/notifications/dernieres/<int:id_employe>', methods=['GET'])
def get_last_notifications(id_employe):
    cur = conn.cursor()
    cur.execute("""
        SELECT id_notification, titre, description, date, document, est_lue
        FROM notification
        WHERE id_employe = %s
        ORDER BY date DESC
        LIMIT 2
    """, (id_employe,))
    rows = cur.fetchall()
    cur.close()
    notifs = []
    for r in rows:
        notifs.append({
            "id_notification": r[0],
            "titre": r[1],
            "description": r[2],
            "date": r[3].strftime('%d/%m/%Y %H:%M'),
            "document": r[4],
            "est_lue": r[5]
        })
    return jsonify(notifs)
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import spacy
import logging
from typing import Dict, List, Tuple, Optional
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from spellchecker import SpellChecker
import unicodedata
from datetime import date
import pandas as pd
from collections import Counter
from decimal import Decimal



import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DB_URL',
    'postgresql://postgres:admin@localhost:5432/Ma_Bdd_sql'  # Valeur par défaut (PC)
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Chargement modèles NLP
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    raise RuntimeError("Modèle Spacy non trouvé. Exécutez: python -m spacy download fr_core_news_sm")



device = 0 if torch.cuda.is_available() else -1
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
flan_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

trained_model_path = r"C:\Users\WINDOWS 10\Desktop\Ma_Brique\try_1 - Copie (3)\chatbot\fichier_generer"

finetuned_tokenizer = AutoTokenizer.from_pretrained(trained_model_path)
finetuned_model = AutoModelForSeq2SeqLM.from_pretrained(trained_model_path)

# ✅ Forcé sur CPU
finetuned_pipeline = pipeline(
    "text2text-generation",
    model=finetuned_model,
    tokenizer=finetuned_tokenizer,
    device=-1  # -1 = CPU
)


# 🔹 Correcteur orthographique (langue française)
spell = SpellChecker(language='fr')
##############################
# MODÈLES SQLALCHEMY
##############################

class Employe(db.Model):
    __tablename__ = 'employe'
    id_employe = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    date_naissance = db.Column(db.Date)
    lieu_naissance = db.Column(db.String(100))
    sexe = db.Column(db.String(10))
    adresse = db.Column(db.String(255))
    numero_telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    nss = db.Column(db.String(50))
    nationalite = db.Column(db.String(50))
    groupe_sanguin = db.Column(db.String(10))
    situation_familiale = db.Column(db.String(50))
    date_recrutement = db.Column(db.Date)
    retenu_panier = db.Column(db.Boolean)
    benification_transport = db.Column(db.Boolean)
    mot_de_passe = db.Column(db.Text)
    is_manager = db.Column(db.Boolean, default=False)
    nb_enfants = db.Column(db.Integer, default=0)
    email_public = db.Column(db.Boolean, default=True)
    telephone_public = db.Column(db.Boolean, default=True)

class Apprentis(db.Model):
    __tablename__ = 'apprentis'
    id_apprentis = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    specialite = db.Column(db.String(100))
    organisme = db.Column(db.String(100))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    observation = db.Column(db.String(255))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    departement = db.Column(db.String(100))

class Carriere(db.Model):
    __tablename__ = 'carriere'
    id_carriere = db.Column(db.Integer, primary_key=True)
    duree = db.Column(db.String(50))
    debut = db.Column(db.Date)
    structure = db.Column(db.String(100))
    echelle = db.Column(db.String(50))
    classification = db.Column(db.String(50))
    medailles = db.Column(db.String(100))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Categorie(db.Model):
    __tablename__ = 'categorie'
    id_categorie = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    date_ajouter = db.Column(db.Date)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Conge(db.Model):
    __tablename__ = 'conge'
    id_conge = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(100))
    date_depart = db.Column(db.Date)
    date_reprise = db.Column(db.Date)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class DroitConge(db.Model):
    __tablename__ = 'droit_conge'
    id_d_conge = db.Column(db.Integer, primary_key=True)
    conge_annuelle = db.Column(db.Integer)  # Changé de Date à Integer
    conge_recup = db.Column(db.Integer)    # Changé de Date à Integer
    conge_scev = db.Column(db.Integer)    # Changé de Date à Integer
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Experience(db.Model):
    __tablename__ = 'experience'
    id_experience = db.Column(db.Integer, primary_key=True)
    poste = db.Column(db.String(100))
    employeur = db.Column(db.String(100))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    is_secteur = db.Column(db.Boolean)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Formation(db.Model):
    __tablename__ = 'formation'
    id_formation = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    type = db.Column(db.String(100))

class InscriptionSocial(db.Model):
    __tablename__ = 'inscription_social'
    id_inscription = db.Column(db.Integer, primary_key=True)
    sejour = db.Column(db.String(100))
    date = db.Column(db.Date)
    type = db.Column(db.String(100))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Manager(db.Model):
    __tablename__ = 'manager'
    id_employe = db.Column(db.Integer, primary_key=True)
    collaborateurs = db.Column(db.ARRAY(db.String))

class MesPrets(db.Model):
    __tablename__ = 'mes_prets'
    id_prets = db.Column(db.Integer, primary_key=True)
    numero_contract = db.Column(db.String(50))
    date_depot = db.Column(db.Date)
    is_accorde = db.Column(db.Boolean)
    motif_response = db.Column(db.String(200))
    motif_prets = db.Column(db.String(200))
    montant = db.Column(db.Numeric(10, 2))
    duree = db.Column(db.Integer)
    rembourse = db.Column(db.Boolean)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    date_debut_remboursement = db.Column(db.Date)

class Mission(db.Model):
    __tablename__ = 'mission'
    id_mission = db.Column(db.Integer, primary_key=True)
    objet = db.Column(db.String(100))
    lieu = db.Column(db.String(100))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    itineraire = db.Column(db.String(255))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Pointage(db.Model):
    __tablename__ = 'pointage'
    id_pointage = db.Column(db.Integer, primary_key=True)
    heure_arrive = db.Column(db.String(20))
    heure_depart = db.Column(db.String(20))
    date = db.Column(db.Date)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    est_jour_ferie = db.Column(db.Boolean, default=False)

class Poste(db.Model):
    __tablename__ = 'poste'
    code_poste = db.Column(db.Integer, primary_key=True)
    intitule = db.Column(db.String(100))
    service = db.Column(db.String(100))
    niveau = db.Column(db.Integer)
    echelle = db.Column(db.Integer)
    date_recrutement = db.Column(db.Date)
    departement = db.Column(db.String(100))
    departement_arrive = db.Column(db.String(100))
    diplome_secteur = db.Column(db.String(100))
    experience_secteur = db.Column(db.String(100))
    experience_hors_secteur = db.Column(db.String(100))
    direction = db.Column(db.String(100))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Realisation(db.Model):
    __tablename__ = 'realisation'
    id_realisation = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    date = db.Column(db.Date)

class SanctionDiscipline(db.Model):
    __tablename__ = 'sanction_discipline'
    id_sanction = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    designation = db.Column(db.String(100))
    snc = db.Column(db.String(50))
    dnc = db.Column(db.String(50))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Notification(db.Model):
    __tablename__ = 'notification'
    id_notification = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    titre = db.Column(db.String(100))
    description = db.Column(db.String(255))
    document = db.Column(db.String(255))
    est_lue = db.Column(db.Boolean, default=False)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Message(db.Model):
    __tablename__ = 'message'
    id_message = db.Column(db.Integer, primary_key=True)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    destinataire_id = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))
    contenu = db.Column(db.Text)
    date_envoi = db.Column(db.Date)
    lu = db.Column(db.Boolean, default=False)

class Documents(db.Model):
    __tablename__ = 'document'
    id_document = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    chemin = db.Column(db.String(255))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Retraite(db.Model):
    __tablename__ = 'retraite'
    id_retraite = db.Column(db.Integer, primary_key=True)
    date_depot = db.Column(db.Date)
    date_previsionnelle_retraite = db.Column(db.Date)
    demande_poursuivre = db.Column(db.Boolean)
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

class Remboursement(db.Model):
    __tablename__ = 'remboursement'
    id_remboursement = db.Column(db.Integer, primary_key=True)
    montant = db.Column(db.Numeric(10, 2))
    date_remboursement = db.Column(db.Date)
    type = db.Column(db.String(50))
    id_employe = db.Column(db.Integer, db.ForeignKey('employe.id_employe'))

KEYWORD_SYNONYMS = {
    # --- employe ---
    ("coordonnées", "informations", "infos", "informations personnelles", "profil", "mes infos", "mes coordonnées", "mes données personnelles", "données personnelles", "fiche employé", "état civil", "dossier personnel"): ("employe", [
        "nom", "prenom", "date_naissance", "lieu_naissance", "adresse", "numero_telephone",
        "email", "nss", "nationalite", "groupe_sanguin", "situation_familiale", "nb_enfants",
        "sexe", "date_recrutement", "retenu_panier", "benification_transport", 
        "is_manager", "email_public", "telephone_public"
    ]),
    ("nom", "noms", "nom complet", "noms complets", "nom de famille", "noms de famille", "identité", "identités", "appelation", "appelations", "nom patronymique", "nom usuel"): ("employe", ["nom"]),
    ("prénom", "prénoms", "prenom", "prenoms", "first name", "first names", "prénom usuel", "prénoms usuels", "prénom courant", "nom de jeune fille"): ("employe", ["prenom"]),
    ("date de naissance", "dates de naissance", "naissance", "naissances", "mon age", "ages", "date naissance", "dates naissance", "anniversaire", "anniversaires", "birthdate", "birthdates", "dob", "date anniversaire"): ("employe", ["date_naissance"]),
    ("lieu de naissance", "lieux de naissance", "ville de naissance", "villes de naissance", "endroit naissance", "endroits naissance", "commune naissance", "communes naissance", "pays natal", "localité de naissance"): ("employe", ["lieu_naissance"]),
    ("adresse", "adresses", "domicile", "domiciles", "résidence", "résidences", "logement", "logements", "lieu d'habitation", "lieux d'habitation", "adresse postale", "habitation", "lieu de résidence"): ("employe", ["adresse"]),
    ("téléphone", "téléphones", "tel", "tels", "portable", "portables", "numéro de téléphone", "numéros de téléphone", "gsm", "gsms", "num tel", "nums tel", "contact", "contacts", "mobile", "numéro portable", "contact téléphonique"): ("employe", ["numero_telephone"]),
    ("email", "emails", "courriel", "courriels", "adresse mail", "adresses mail", "mail", "mails", "e-mail", "e-mails", "boîte mail", "boîtes mail", "mél", "adresse électronique", "courrier électronique"): ("employe", ["email"]),
    ("nss", "sécurité sociale", "sécurités sociales", "numéro sécurité sociale", "numéros sécurité sociale", "numéro de sécurité sociale", "numéros de sécurité sociale", "num ss", "nums ss", "numero ss", "matricule ss", "numéro d'assuré social"): ("employe", ["nss"]),
    ("nationalité", "nationalités", "citoyenneté", "citoyennetés", "origine", "origines", "pays d'origine", "pays natal", "pays de citoyenneté"): ("employe", ["nationalite"]),
    ("groupe sanguin", "groupes sanguins", "type sanguin", "types sanguins", "sang", "sangs", "rhésus", "groupe rh", "rh", "blood type"): ("employe", ["groupe_sanguin"]),
    ("situation familiale", "situations familiales", "état civil", "états civils", "famille", "familles", "marié", "mariés", "célibataire", "célibataires", "statut marital", "situation matrimoniale", "vie maritale"): ("employe", ["situation_familiale"]),
    ("nombre d'enfants", "nombres d'enfants", "enfants", "nb enfants", "nbs enfants", "combien d'enfants", "kids", "descendants", "nombre de descendants", "charge familiale"): ("employe", ["nb_enfants"]),
    ("sexe", "sexes", "genre", "genres", "masculin", "masculins", "féminin", "féminins", "identité de genre", "sexe biologique"): ("employe", ["sexe"]),
    ("date de recrutement", "dates de recrutement", "embauche", "embauches", "entrée", "entrées", "date d'entrée", "dates d'entrée", "date début", "dates début", "début travail", "débuts travail", "date d'embauche", "ancienneté", "date d'incorporation"): ("employe", ["date_recrutement"]),
    ("retenu panier", "retenus panier", "panier repas", "paniers repas", "retenue repas", "retenues repas", "avantage repas", "avantages repas", "ticket resto", "bon repas", "allocation repas"): ("employe", ["retenu_panier"]),
    ("transport", "transports", "bénéfice transport", "bénéfices transport", "prime transport", "primes transport", "avantage transport", "avantages transport", "frais transport", "indemnité transport", "remboursement transport", "titre de transport"): ("employe", ["benification_transport"]),
    
    ("manager", "managers", "responsable", "responsables", "supérieur", "supérieurs", "chef", "chefs", "encadreur", "encadreurs", "superviseur", "superviseurs", "directeur", "hierarchie", "n+1"): ("employe", ["is_manager"]),
    ("email public", "emails publics", "email visible", "emails visibles", "email partagé", "contact public", "email professionnel visible"): ("employe", ["email_public"]),
    ("téléphone public", "téléphones publics", "téléphone visible", "téléphones visibles", "contact téléphonique public", "numéro partagé"): ("employe", ["telephone_public"]),

    # --- conge ---
    ("vacances","planning","plannings","absences","conges", "vacance", "permission", "permissions", "repos", "absence autorisée", "absences autorisées", "pause", "pauses", "jours off", "j'ai pris","pris", "absence", "jours de congé", "demande de congé", "autorisation d'absence", "jours de repos", "congé payé"): ("conge", ["designation", "date_depart", "date_reprise"]),
    ("type de congé", "types de congé", "motif congé", "motifs congé", "nature congé", "natures congé", "raison absence", "raisons absence", "cause congé", "causes congé"): ("conge", ["designation"]),
    ("départ en congé", "départs en congé", "début congé", "débuts congé", "date de départ", "dates de départ", "commencement congé"): ("conge", ["date_depart"]),
    ("retour de congé", "retours de congé", "fin congé", "fins congé", "reprise travail", "reprises travail", "date de reprise", "dates de reprise", "retour au travail"): ("conge", ["date_reprise"]),

    # --- droit_conge ---
    ("congés restants", "congé restant","restant" "me restent", "jours restants", "jours disponibles", "droit à congé", "droits à congé","droits à congés","droit à congés", "congés à venir", "jours à venir", "solde congé", "soldes congé", "encore", "je peux prendre", "prochain congé", "prochains congés", "solde de congés", "reliquat congé", "jours acquis", "droits congés", "quotité congé"): ("droit_conge", ["conge_annuelle", "conge_recup", "conge_scev"]),
    ("congé annuel", "congés annuels", "congé principal", "congés principaux", "vacances annuelles", "congé ordinaire", "congés ordinaires"): ("droit_conge", ["conge_annuelle"]),
    ("congé de récupération", "congés de récupération", "récup", "récups", "jours de récupération", "congé compensatoire", "congés compensatoires"): ("droit_conge", ["conge_recup"]),
    ("congé sans solde", "congés sans solde", "congé exceptionnel", "congés exceptionnels", "congé non payé", "congés non payés", "autorisation spéciale"): ("droit_conge", ["conge_scev"]),

    # --- experience ---
    ("expérience", "expériences", "poste précédent", "postes précédents", "ancien poste", "anciens postes", "ancien employeur", "anciens employeurs", "ancien job", "anciens jobs", "carrière passée", "carrières passées", "emploi antérieur", "emplois antérieurs", "secteur", "secteurs", "expérience pro", "expériences pro", "historique professionnel", "parcours pro", "cv", "curriculum vitae", "antécédents professionnels", "emplois précédents"): ("experience", ["poste", "employeur", "date_debut", "date_fin", "is_secteur"]),
    ("poste occupé", "postes occupés", "fonction précédente", "fonctions précédentes", "ancienne position", "anciennes positions", "rôle précédent", "rôles précédents"): ("experience", ["poste"]),
    ("ancien employeur", "anciens employeurs", "entreprise précédente", "entreprises précédentes", "boîte précédente", "boîtes précédentes", "ex-employeur", "ex-employeurs"): ("experience", ["employeur"]),
    ("début expérience", "débuts expérience", "date commencement", "dates commencement", "début emploi", "débuts emploi", "entrée en poste"): ("experience", ["date_debut"]),
    ("fin expérience", "fins expérience", "date de fin", "dates de fin", "sortie poste", "sorties poste", "terminaison emploi"): ("experience", ["date_fin"]),
    ("expérience secteur", "expériences secteur", "secteur d'activité", "secteurs d'activité", "même domaine", "mêmes domaines", "secteur similaire", "secteurs similaires"): ("experience", ["is_secteur"]),

    # --- formation ---
    ("formations","formations de mes collaborateurs",  "cours", "stage", "stages", "apprentissage", "apprentissages", "diplôme", "diplômes", "études", "enseignement", "enseignements", "programme de formation", "programmes de formation", "apprentissage professionnel", "qualification", "certification", "compétence acquise", "parcours académique", "éducation", "training"): ("formation", ["description", "date_debut", "date_fin", "type"]),
    ("description formation", "descriptions formation", "contenu formation", "contenus formation", "programme", "programmes", "détails cours"): ("formation", ["description"]),
    ("début formation", "débuts formation", "date commencement", "dates commencement", "début stage", "débuts stage", "entrée en formation"): ("formation", ["date_debut"]),
    ("fin formation", "fins formation", "date de fin", "dates de fin", "terminaison", "terminaisons", "clôture formation"): ("formation", ["date_fin"]),
    ("type formation", "types formation", "nature formation", "natures formation", "catégorie cours", "catégories cours", "domaine étude", "domaines étude"): ("formation", ["type"]),

    # --- realisation ---
    ("réalisation", "réalisations", "projet accompli", "projets accomplis", "succès", "tâche accomplie", "tâches accomplies", "résultat", "résultats", "mission réussie", "missions réussies", "accomplissement", "accomplissements", "projets réalisés", "travaux effectués", "réussites professionnelles", "fait marquant", "performance", "exploit professionnel"): ("realisation", ["description", "date"]),
    ("description réalisation", "descriptions réalisation", "détails projet", "détails projets", "explication succès", "contenu accomplissement", "contenus accomplissement"): ("realisation", ["description"]),
    ("date réalisation", "dates réalisation", "quand réalisé", "période accomplissement", "périodes accomplissement", "moment succès"): ("realisation", ["date"]),

    # --- sanction_discipline ---
    ("sanction", "sanctions", "punition", "punitions", "avertissement", "avertissements", "blâme", "blâmes", "réprimande", "réprimandes", "mesure disciplinaire", "mesures disciplinaires", "remarque", "remarques", "pénalité", "pénalités", "mise à pied", "avertissement écrit", "faute professionnelle", "procédure disciplinaire", "retenue sur salaire"): ("sanction_discipline", ["designation", "date", "snc", "dnc"]),
    ("type sanction", "types sanction", "nature punition", "natures punition", "motif sanction", "motifs sanction", "raison blâme", "raisons blâme"): ("sanction_discipline", ["designation"]),
    ("date sanction", "dates sanction", "quand punition", "moment avertissement", "période blâme"): ("sanction_discipline", ["date"]),
    ("sanction avec notification", "sanctions avec notification", "notification écrite", "avertissement formel", "documentation sanction"): ("sanction_discipline", ["snc"]),
    ("sanction sans notification", "sanctions sans notification", "avertissement verbal", "remarque informelle", "sanction orale"): ("sanction_discipline", ["dnc"]),

    # --- poste ---
    ("poste", "postes", "fonction", "fonctions", "emploi", "emplois", "position", "positions", "rôle", "rôles", "travail", "travaux", "intitulé poste", "intitulés poste", "job", "jobs", "occupation", "occupations", "mission professionnelle", "missions professionnelles", "tâche assignée", "tâches assignées", "responsabilités", "poste occupé", "postes occupés", "grade", "grades"): ("poste", ["intitule", "service", "niveau", "echelle", "departement", "departement_arrive", "diplome_secteur", "experience_secteur", "experience_hors_secteur", "direction"]),
    ("intitulé poste", "intitulés poste", "libellé fonction", "libellés fonction", "désignation poste", "désignations poste", "titre professionnel", "titres professionnels"): ("poste", ["intitule"]),
    ("service", "services", "unité", "unités", "division", "divisions", "branche", "branches", "secteur", "secteurs", "département", "départements", "équipe", "équipes"): ("poste", ["service"]),
    ("niveau poste", "niveaux poste", "grade", "grades", "niveau hiérarchique", "niveaux hiérarchiques", "échelon", "échelons", "niveau professionnel", "niveaux professionnels"): ("poste", ["niveau"]),
    ("échelle salariale", "échelles salariales", "grille salariale", "grilles salariales", "niveau rémunération", "niveaux rémunération", "classe salariale", "classes salariales"): ("poste", ["echelle"]),
    ("département", "départements", "direction", "directions", "service d'affectation", "services d'affectation", "unité de rattachement", "unités de rattachement"): ("poste", ["departement"]),
    ("département d'arrivée", "départements d'arrivée", "nouvelle affectation", "nouvelles affectations", "service destination", "services destination", "future unité", "futures unités"): ("poste", ["departement_arrive"]),
    ("diplôme secteur", "diplômes secteur", "formation requise", "formations requises", "qualification nécessaire", "qualifications nécessaires", "certification métier", "certifications métier"): ("poste", ["diplome_secteur"]),
    ("expérience secteur", "expériences secteur", "ancienneté domaine", "anciennetés domaine", "expérience métier", "expériences métier", "pratique professionnelle", "pratiques professionnelles"): ("poste", ["experience_secteur"]),
    ("expérience hors secteur", "expériences hors secteur", "expérience externe", "expériences externes", "pratique autre domaine", "pratiques autres domaines", "compétences transverses"): ("poste", ["experience_hors_secteur"]),
    ("direction", "directions", "management", "managements", "encadrement", "encadrements", "supervision", "supervisions", "hiérarchie", "hiérarchies"): ("poste", ["direction"]),

    # --- carriere ---
    ("carrière", "carrières", "évolution", "évolutions", "parcours professionnel", "parcours professionnels", "historique postes", "historiques postes", "progression", "progressions", "trajet pro", "trajets pro", "promotions", "avancement", "cheminement professionnel", "développement de carrière", "mobilité interne", "promotion", "évolution professionnelle"): ("carriere", ["structure", "echelle", "classification", "debut", "duree", "medailles"]),
    ("structure", "structures", "organisation", "organisations", "entreprise", "entreprises", "institution", "institutions", "établissement", "établissements"): ("carriere", ["structure"]),
    ("échelle", "échelles", "niveau hiérarchique", "niveaux hiérarchiques", "grade professionnel", "grades professionnels", "palier carrière", "paliers carrière"): ("carriere", ["echelle"]),
    ("classification", "classifications", "catégorie professionnelle", "catégories professionnelles", "classement", "classements", "groupe métier", "groupes métier"): ("carriere", ["classification"]),
    ("début carrière", "débuts carrière", "date commencement", "dates commencement", "début professionnel", "débuts professionnels", "premier emploi", "premiers emplois"): ("carriere", ["debut"]),
    ("durée carrière", "durées carrière", "ancienneté", "anciennetés", "temps service", "période activité", "périodes activité"): ("carriere", ["duree"]),
    ("médailles", "distinctions", "récompenses", "honneurs", "titres", "reconnaissance professionnelle"): ("carriere", ["medailles"]),

    # --- apprentis ---
    ("apprenti", "apprentis", "apprentissage", "apprentissages", "stagiaire", "stagiaires", "formation alternée", "formations alternées", "élève en stage", "élèves en stage", "alternant", "alternants", "apprenant", "apprenants", "jeune professionnel", "jeunes professionnels", "stagiaire en formation", "stagiaires en formation", "étudiant salarié", "étudiants salariés"): ("apprentis", ["nom", "specialite", "organisme", "date_debut", "date_fin", "observation"]),
    ("spécialité apprentissage", "spécialités apprentissage", "domaine formation", "domaines formation", "métier appris", "métiers appris", "filière apprentissage", "filières apprentissage"): ("apprentis", ["specialite"]),
    ("organisme formation", "organismes formation", "centre apprentissage", "centres apprentissage", "école", "écoles", "établissement formateur", "établissements formateurs", "institut", "instituts"): ("apprentis", ["organisme"]),
    ("début apprentissage", "débuts apprentissage", "date commencement", "dates commencement", "début stage", "débuts stage", "entrée en formation"): ("apprentis", ["date_debut"]),
    ("fin apprentissage", "fins apprentissage", "date de fin", "dates de fin", "terminaison", "terminaisons", "clôture stage"): ("apprentis", ["date_fin"]),
    ("observation apprentissage", "observations apprentissage", "remarques", "commentaires", "évaluation", "évaluations", "suivi", "suivis"): ("apprentis", ["observation"]),

    # --- mission ---
    ("mission", "missions", "déplacement", "déplacements", "voyage professionnel", "voyages professionnels", "tâche externe", "tâches externes", "affectation temporaire", "affectations temporaires", "projet externe", "projets externes", "délégation", "délégations", "travail sur site", "travaux sur site", "intervention externe", "interventions externes", "déplacement professionnel", "déplacements professionnels"): ("mission", ["objet", "lieu", "date_debut", "date_fin", "itineraire"]),
    ("objet mission", "objets mission", "but", "buts", "objectif", "objectifs", "raison déplacement", "raisons déplacement", "motif mission", "motifs mission"): ("mission", ["objet"]),
    ("lieu mission", "lieux mission", "destination", "destinations", "ville", "villes", "pays", "site d'intervention", "sites d'intervention", "localisation", "localisations"): ("mission", ["lieu"]),
    ("début mission", "débuts mission", "date départ", "dates départ", "commencement", "commencements", "début affectation", "débuts affectation"): ("mission", ["date_debut"]),
    ("fin mission", "fins mission", "date retour", "dates retour", "terminaison", "terminaisons", "clôture", "clôtures"): ("mission", ["date_fin"]),
    ("itinéraire", "itinéraires", "trajet", "trajets", "parcours", "voyage", "voyages", "chemin", "chemins", "déroulement déplacement", "déroulements déplacement"): ("mission", ["itineraire"]),

    # --- mes_prets ---
    ("prêt", "prêts", "emprunt", "emprunts", "avance", "avances", "demande de prêt", "demandes de prêt", "demande financière", "demandes financières", "crédit", "crédits", "aide financière", "aides financières", "avance sur salaire", "avances sur salaire", "prêt personnel", "prêts personnels", "financement", "financements", "acompte", "acomptes", "prêt salarial", "prêts salariaux"): ("mes_prets", [
        "numero_contract", "montant", "date_depot", "duree", "is_accorde", "motif_response", "motif_prets", "rembourse", "date_debut_remboursement"
    ]),
    ("numéro contrat", "numéros contrat", "référence prêt", "références prêt", "identifiant emprunt", "identifiants emprunt", "code prêt", "codes prêt"): ("mes_prets", ["numero_contract"]),
    ("montant prêt", "montants prêt", "somme", "sommes", "capital emprunté", "capitaux empruntés", "valeur prêt", "valeurs prêt", "total", "totaux"): ("mes_prets", ["montant"]),
    ("date demande", "dates demande", "dépôt dossier", "dépôts dossier", "soumission", "soumissions", "date requête", "dates requête"): ("mes_prets", ["date_depot"]),
    ("durée prêt", "durées prêt", "période remboursement", "périodes remboursement", "terme", "termes", "échéance", "échéances"): ("mes_prets", ["duree"]),
    ("statut demande", "statuts demande", "accordé", "accordés", "refusé", "refusés", "réponse", "réponses", "décision", "décisions", "état demande", "états demande"): ("mes_prets", ["is_accorde"]),
    ("motif refus", "motifs refus", "raison rejet", "raisons rejet", "explication négative", "explications négatives", "cause refus", "causes refus"): ("mes_prets", ["motif_response"]),
    ("motif prêt", "motifs prêt", "raison emprunt", "raisons emprunt", "utilisation fonds", "utilisations fonds", "objectif financement", "objectifs financement"): ("mes_prets", ["motif_prets"]),
    ("remboursé", "remboursés", "solde", "soldes", "acquitté", "acquittés", "dette réglée", "dettes réglées", "prêt terminé", "prêts terminés"): ("mes_prets", ["rembourse"]),
    ("début remboursement", "débuts remboursement", "date première échéance", "dates première échéance", "commencement paiement", "commencements paiement", "échéancier", "échéanciers"): ("mes_prets", ["date_debut_remboursement"]),

    # --- pointage ---
    ("pointage","absences", "pointages", "heures de travail", "présence", "présences", "horaires", "temps de travail", "heures", "arrivée", "arrivées", "départ", "départs", "pointé", "pointés", "enregistrement horaire", "badgeage", "fichage", "contrôle présence", "suivi temps"): ("pointage", ["heure_arrive", "heure_depart", "date", "est_jour_ferie"]),
    ("heure arrivée", "heures arrivée", "début journée", "débuts journée", "heure entrée", "heures entrée", "premier badgeage", "premiers badgeages"): ("pointage", ["heure_arrive"]),
    ("heure départ", "heures départ", "fin journée", "fins journée", "heure sortie", "heures sortie", "dernier badgeage", "derniers badgeages"): ("pointage", ["heure_depart"]),
    ("date pointage", "dates pointage", "journée", "journées", "date travail", "dates travail", "période", "périodes"): ("pointage", ["date"]),
    ("jour férié", "weekends","jours fériés", "férié", "fériés", "congé légal", "congés légaux", "jour chômé", "jours chômés", "repos légal", "repos légaux"): ("pointage", ["est_jour_ferie"]),

    # --- inscription_social ---
    ("inscription sociale", "inscriptions sociales", "sécurité sociale", "sécurités sociales", "enregistrement cnas", "enregistrements cnas", "séjour", "séjours", "cotisation", "cotisations", "type d'inscription", "types d'inscription", "affiliation sociale", "affiliations sociales", "protection sociale", "protections sociales", "couverture sociale", "couvertures sociales", "adhésion cnas", "adhésions cnas", "dossier cnas", "dossiers cnas"): ("inscription_social", ["sejour", "date", "type"]),
    ("séjour", "séjours", "période", "périodes", "durée", "durées", "intervalle", "intervalles", "temps couvert", "temps couverts"): ("inscription_social", ["sejour"]),
    ("date inscription", "dates inscription", "enregistrement", "enregistrements", "date adhésion", "dates adhésion", "moment affiliation", "moments affiliation"): ("inscription_social", ["date"]),
    ("type inscription", "types inscription", "catégorie", "catégories", "nature affiliation", "natures affiliation", "genre couverture", "genres couverture"): ("inscription_social", ["type"]),

    # --- manager ---
    ("collaborateurs", "équipe", "équipes", "membres supervisés", "personnes encadrées", "subordonnés", "employés sous responsabilité", "équipe managée", "ressources humaines encadrées", "personnel sous direction"): ("manager", ["collaborateurs"]),

    # --- notification ---
    ("notification", "notifications", "alerte", "alertes", "message système", "messages système", "info reçue", "infos reçues", "avis", "avis", "communication interne", "communications internes", "information", "informations", "rappel", "rappels", "annonce", "annonces", "message administratif", "messages administratifs"): ("notification", ["date", "titre", "description", "document", "est_lue"]),
    ("titre notification", "titres notification", "sujet", "sujets", "objet", "objets", "intitulé message", "intitulés message"): ("notification", ["titre"]),
    ("description notification", "descriptions notification", "contenu", "contenus", "détails", "explication", "explications", "message complet", "messages complets"): ("notification", ["description"]),
    ("document joint", "documents joints", "fichier attaché", "fichiers attachés", "pièce jointe", "pièces jointes", "annexe", "annexes", "support", "supports"): ("notification", ["document"]),
    ("lu", "lus", "vue", "vues", "consultée", "consultées", "ouverte", "ouvertes", "prise connaissance", "prises connaissance"): ("notification", ["est_lue"]),

    # --- message ---
    ("message", "messages", "messagerie", "messageries", "communication", "communications", "conversation", "conversations", "sms", "chat", "échange", "échanges", "correspondance", "correspondances", "discussion", "discussions", "courrier interne", "courriers internes", "memo", "memos", "note interne", "notes internes"): ("message", ["expediteur_id", "destinataire_id", "contenu", "date_envoi", "lu"]),
    ("expéditeur", "expéditeurs", "envoyeur", "envoyeurs", "auteur", "auteurs", "émetteur", "émetteurs", "personne qui envoie", "personnes qui envoient"): ("message", ["expediteur_id"]),
    ("destinataire", "destinataires", "récepteur", "récepteurs", "receveur", "receveurs", "personne qui reçoit", "personnes qui reçoivent"): ("message", ["destinataire_id"]),
    ("contenu message", "contenus message", "texte", "textes", "corps", "corps", "détails", "communication écrite", "communications écrites"): ("message", ["contenu"]),
    ("date envoi", "dates envoi", "moment expédition", "moments expédition", "heure message", "heures message", "quand envoyé"): ("message", ["date_envoi"]),
    ("message lu", "messages lus", "vu", "vus", "consulté", "consultés", "ouvert", "ouverts", "pris connaissance", "prises connaissance"): ("message", ["lu"]),

    # --- documents ---
    ("document", "documents", "fichier", "fichiers", "pièce jointe", "pièces jointes", "ressource", "ressources", "pdf", "pdfs", "téléchargement", "téléchargements", "fichier joint", "fichiers joints", "archive", "archives", "dossier", "dossiers", "support", "supports", "pièce administrative", "pièces administratives", "justificatif", "justificatifs"): ("document", ["titre", "chemin"]),
    ("titre document", "titres document", "nom fichier", "noms fichier", "intitulé", "intitulés", "description fichier", "descriptions fichier"): ("document", ["titre"]),
    ("chemin document", "chemins document", "emplacement", "emplacements", "lien", "liens", "url", "urls", "adresse fichier", "adresses fichier", "répertoire", "répertoires"): ("document", ["chemin"]),

    # --- categorie ---
    ("catégorie", "catégories", "groupe", "groupes", "classification", "classifications", "type d'employé", "types d'employé", "niveau", "niveaux", "classe", "classes", "catégorie professionnelle", "catégories professionnelles", "groupe hiérarchique", "groupes hiérarchiques", "classification métier", "classifications métier"): ("categorie", ["nom", "date_ajouter"]),
    ("nom catégorie", "noms catégorie", "libellé", "libellés", "désignation", "désignations", "intitulé groupe", "intitulés groupe"): ("categorie", ["nom"]),
    ("date ajout", "dates ajout", "date création", "dates création", "moment enregistrement", "moments enregistrement", "date incorporation", "dates incorporation"): ("categorie", ["date_ajouter"]),

    # --- retraite ---
    ("retraite", "retraites", "départ à la retraite", "départs à la retraite", "cessation activité", "cessations activité", "fin carrière", "fins carrière", "pension", "pensions", "préretraite", "préretraites", "demande retraite", "demandes retraite", "dossier retraite", "dossiers retraite", "cessation service", "cessations service"): ("retraite", ["date_depot", "date_previsionnelle_retraite", "demande_poursuivre"]),
    ("date dépôt demande", "dates dépôt demande", "soumission dossier", "soumissions dossier", "date requête", "dates requête", "enregistrement demande", "enregistrements demande"): ("retraite", ["date_depot"]),
    ("date prévisionnelle", "dates prévisionnelles", "date départ", "dates départ", "moment cessation", "moments cessation", "échéance retraite", "échéances retraite"): ("retraite", ["date_previsionnelle_retraite"]),
    ("poursuite activité", "poursuites activité", "demande prolongation", "demandes prolongation", "continuation travail", "continuations travail", "maintien poste", "maintiens poste"): ("retraite", ["demande_poursuivre"]),

    # --- remboursement ---
    ("remboursement", "remboursements", "récupération frais", "récupérations frais", "indemnisation", "indemnisations", "compensation", "compensations", "remboursement dépenses", "remboursements dépenses", "règlement", "règlements", "recouvrement", "recouvrements", "remboursement CNAS", "remboursements CNAS", "remboursement MIP", "remboursements MIP"): ("remboursement", ["montant", "date_remboursement", "type"]),
    ("montant remboursé", "montants remboursés", "somme", "sommes", "total", "totaux", "valeur", "valeurs", "capital", "capitaux"): ("remboursement", ["montant"]),
    ("date remboursement", "dates remboursement", "moment paiement", "moments paiement", "échéance", "échéances", "date versement", "dates versement"): ("remboursement", ["date_remboursement"]),
    ("type remboursement", "types remboursement", "nature", "natures", "catégorie", "catégories", "genre", "genres", "CNAS", "MIP"): ("remboursement", ["type"]),

    # --- Mots invariables ---
    ("premier", "première", "premiers", "premières", "1er", "1ère", "1ers", "1ères", "ancien", "anciens", "plus ancien", "plus anciens"): ("", []),
    ("dernier", "dernière", "derniers", "dernières", "récent", "récents", "plus récent", "plus récents", "actuel", "actuelle", "actuels", "actuelles", "en cours"): ("", []),
    ("tous", "tout", "toutes", "l'ensemble de", "chaque", "la totalité de"): ("", []),
    ("date inscription sociale", "dates inscription sociale", "date inscription social", "dates inscription social", "date d'inscription sociale", "dates d'inscription sociale", "date d'inscription", "dates d'inscription", "quand me suis-je inscrit"): ("inscription_social", ["date"]),
     ("collaborateurs", "équipe", "subordonnés", "membres de mon équipe", "mon équipe", 
     "employés sous ma responsabilité", "mes employés", "mon personnel", "ressources managées"): 
    ("manager", ["collaborateurs"]),

    ("liste collaborateurs", "liste des employés", "fiches collaborateurs", "tableau équipe", 
     "annuaire interne", "répertoire du service"): 
    ("employe", ["id_employe", "nom", "prenom", "poste.intitule", "poste.direction"]),

    ("congés équipe", "absences de mon équipe", "congés des collaborateurs", "départs en vacances équipe"): 
    ("conge", ["id_employe", "employe.nom", "employe.prenom", "designation", "date_depart", "date_reprise"]),

    ("formations équipe", "cours suivis par mon équipe", "apprentissages collaborateurs"): 
    ("formation", ["id_employe", "employe.nom", "employe.prenom", "description", "date_debut", "type"]),

    ("missions équipe", "déplacements collaborateurs", "voyages professionnels équipe"): 
    ("mission", ["id_employe", "employe.nom", "employe.prenom", "objet", "lieu", "date_debut"]),

    # --- Jointures implicites ---
    ("coordonnées collaborateurs", "contacts équipe", "annuaire téléphonique service"): 
    ("employe", ["nom", "prenom", "numero_telephone", "email", "poste.service"]),

    ("expérience équipe", "parcours professionnel collaborateurs", "CV équipe"): 
    ("experience", ["id_employe", "employe.nom", "employe.prenom", "poste", "employeur", "date_debut"])
}

corrections = {
    "conte": "congé",
    "contes": "congés",
    "conge": "congé",
    "conges": "congés",
    "pret": "prêt",
    "prets": "prêts",
    # Variantes de "coordonnées"
        "mes coordonnees": "mes coordonnées",
        "mes coordonnes": "mes coordonnées",
        "coordonnees": "coordonnées",
        "coordonnes": "coordonnées",
        
        # Autres exemples
        "mes donnees": "mes données",
        "telephone": "téléphone",
        "prenom": "prénom",
        "conte": "congé",
            # Format: "terme_sans_accents": "forme_canonique"
        "é": "e",
    "è": "e",
    "ê": "e",
    "ë": "e",
    "à": "a",
    "â": "a",
    "ä": "a",
    "î": "i",
    "ï": "i",
    "ô": "o",
    "ö": "o",
    "ù": "u",
    "û": "u",
    "ü": "u",
    "ç": "c",
    
    # Formes accentuées courantes
    "prénom": "prenom",
    "prenom": "prenom",
    "nom": "nom",
    "coordonnées": "coordonnees",
    "informations": "informations",
    "données": "donnees",
    "téléphone": "telephone",
    "email": "email",
    "courriel": "courriel",
    "adresse": "adresse",
    "date": "date",
    "naissance": "naissance",
    "âge": "age",
    "anniversaire": "anniversaire",
    "situation": "situation",
    "familiale": "familiale",
    "nationalité": "nationalite",
    "groupe": "groupe",
    "sanguin": "sanguin",
    "sexe": "sexe",
    "genre": "genre",
    "recrutement": "recrutement",
    "mot": "mot",
    "passe": "passe",
    "manager": "manager",
    "congé": "conge",
    "congés": "conges",
    "vacances": "vacances",
    "expérience": "experience",
    "formation": "formation",
    "diplôme": "diplome",
    "poste": "poste",
    "mission": "mission",
    "sanction": "sanction",
    "notification": "notification",
    "message": "message",
    "document": "document",
    "prêt": "pret",
    "remboursement": "remboursement",
    "catégorie": "categorie",
    "réussite": "reussite",
    "projet": "projet",
    "médaille": "medaille",
    
    # Combinaisons courantes
    "informations personnelles": "informations personnelles",
    "données personnelles": "donnees personnelles",
    "date de naissance": "date naissance",
    "lieu de naissance": "lieu naissance",
    "numéro de téléphone": "numero telephone",
    "groupe sanguin": "groupe sanguin",
    "situation familiale": "situation familiale",
    "date de recrutement": "date recrutement",
    
    "email public": "email public",
    "téléphone public": "telephone public",
    "jours restants": "jours restants",
    "congés restants": "conges restants",
     "congés précédents": "conges precedents",
    "poste précédent": "poste precedent",
    "ancien employeur": "ancien employeur",
    "mesure disciplinaire": "mesure disciplinaire",
    "heure d'arrivée": "heure arrivee",
    "heure de départ": "heure depart",
    "pièce jointe": "piece jointe",
    
    # Mots fréquents avec apostrophes
    "l'employé": "employe",
    "d'emploi": "emploi",
    "d'adresse": "adresse",
    "l'information": "information",
    "d'expérience": "experience",
    
    # Variantes contractées
    "aujourd'hui": "aujourdhui",
    "prud'homme": "prudhomme",
    "quelqu'un": "quelqun",

    
    # Singulier/Pluriel
    "apprentis": "apprenti",
    "stagiaires": "stagiaire",
    "formations": "formation",
    "cours": "cours",
    "diplômes": "diplôme",
    "études": "étude",
    "expériences": "expérience",
    "postes": "poste",
    "emplois": "emploi",
    "missions": "mission",
    "sanctions": "sanction",
    "punitions": "punition",
    "avertissements": "avertissement",
    "congés": "congé",
    "vacances": "vacance",
    "jours": "jour",
    "notifications": "notification",
    "alertes": "alerte",
    "messages": "message",
    "documents": "document",
    "fichiers": "fichier",
    "prêts": "prêt",
    "emprunts": "emprunt",
    "remboursements": "remboursement",
    "catégories": "catégorie",
    "grades": "grade",
    "niveaux": "niveau",
    "réalisations": "réalisation",
    "projets": "projet",
    "succès": "succès",
    "médaille": "médaille",
    "distinctions": "distinction",

    # Masculin/Féminin
    "employés": "employé",
    "employées": "employé",
    "collaborateurs": "collaborateur",
    "collaboratrices": "collaborateur",
    "managers": "manager",
    "chefs": "chef",
    "superviseurs": "superviseur",
    "directeurs": "directeur",
    "directrices": "directeur",

    # Variantes orthographiques
    "prénoms": "prénom",
    "noms": "nom",
    "adresses": "adresse",
    "téléphones": "téléphone",
    "emails": "email",
    "courriels": "courriel",
    "mails": "mail",
    "e-mails": "e-mail",
    
    "passwords": "password",
    "mdps": "mdp",
    "dates": "date",
    "lieux": "lieu",
    "villes": "ville",
    "groupes sanguins": "groupe sanguin",
    "types sanguins": "type sanguin",
    "situations familiales": "situation familiale",
    "états civils": "état civil",
    "nationalités": "nationalité",
    "sexes": "sexe",
    "genres": "genre",

    # Verbes conjugués
    "a pris": "prendre",
    "prendre": "prendre",
    "prend": "prendre",
    "pouvez prendre": "pouvoir prendre",
    "peux prendre": "pouvoir prendre",
    "peut prendre": "pouvoir prendre",
    "a déposé": "déposer",
    "déposer": "déposer",
    "dépose": "déposer",
    "a accordé": "accorder",
    "accorder": "accorder",
    "accorde": "accorder",
    "a remboursé": "rembourser",
    "rembourser": "rembourser",
    "rembourse": "rembourser",
    "a pointé": "pointer",
    "pointer": "pointer",
    "pointe": "pointer",
    "a envoyé": "envoyer",
    "envoyer": "envoyer",
    "envoie": "envoyer",
    "a reçu": "recevoir",
    "recevoir": "recevoir",
    "reçoit": "recevoir",
    "a lu": "lire",
    "lire": "lire",
    "lit": "lire",
    "a vu": "voir",
    "voir": "voir",
    "voit": "voir",

    # Mots composés
    "mes infos": "information",
    "mes coordonnées": "coordonnée",
    "mes données": "donnée",
    "données personnelles": "donnée personnelle",
    "informations personnelles": "information personnelle",
    "numéro de téléphone": "numéro téléphone",
    "numéro tel": "numéro téléphone",
    "date de naissance": "date naissance",
    "lieu de naissance": "lieu naissance",
    "groupe sanguin": "groupe sanguin",
    "situation familiale": "situation familiale",
    "nombre d'enfants": "nombre enfants",
    "date de recrutement": "date recrutement",
   
    "email public": "email public",
    "téléphone public": "téléphone public",
    "jours restants": "jour restant",
    "jours disponibles": "jour disponible",
    "congés restants": "congé restant",
    "poste précédent": "poste précédent",
    "ancien poste": "ancien poste",
    "ancien employeur": "ancien employeur",
    "date de début": "date début",
    "date de fin": "date fin",
    "projet accompli": "projet accompli",
    "tâche accomplie": "tâche accomplie",
    "mission réussie": "mission réussie",
    "mesure disciplinaire": "mesure disciplinaire",
    "heure d'arrivée": "heure arrivée",
    "heure de départ": "heure départ",
    "jour férié": "jour férié",
    "date d'envoi": "date envoi",
    "pièce jointe": "pièce jointe",
    "date d'ajout": "date ajout",

    # Singulier/Pluriel
    "apprentis": "apprenti",
    "conges": "congé",
    "coordonnees": "coordonnées",
    "donnees": "données",
    "benes": "béné",  # pour "bénification"
    "employes": "employé",
    
    # Accents manquants
    "benification": "bénification",
    "prenom": "prénom",
    "telephone": "téléphone",
    "numero": "numéro",
    "profil": "profil",  # déjà correct
    "infos": "infos",  # forme courte acceptée
    "adresse": "adresse",  # déjà correct
    "mail": "mail",  # forme courte acceptée
    "e-mail": "e-mail",  # forme correcte
    "nationalite": "nationalité",
    "groupe": "groupe",  # déjà correct
    "sanguin": "sanguin",  # déjà correct
    "situation": "situation",  # déjà correct
    "familiale": "familiale",  # déjà correct
    "enfants": "enfants",  # pluriel correct
    "sexe": "sexe",  # déjà correct
    "recrutement": "recrutement",  # déjà correct
    "retenu": "retenu",  # déjà correct
    "panier": "panier",  # déjà correct
    "transport": "transport",  # déjà correct
    
    
    "manager": "manager",  # mot anglais accepté
    "public": "public",  # déjà correct
    
    # Mots composés
    "mes infos": "mes infos",  # correct
    "mes coordonnees": "mes coordonnées",
    "mes donnees": "mes données",
    "nom complet": "nom complet",  # correct
    "nom de famille": "nom de famille",  # correct
    "date de naissance": "date de naissance",  # correct
    "lieu de naissance": "lieu de naissance",  # correct
    "numero de telephone": "numéro de téléphone",
    "securite sociale": "sécurité sociale",
    "groupe sanguin": "groupe sanguin",  # correct
    "situation familiale": "situation familiale",  # correct
    "nombre d'enfants": "nombre d'enfants",  # correct
    "date de recrutement": "date de recrutement",  # correct
    "retenu panier": "retenu panier",  # correct
    "benification transport": "bénification transport",
    
    "email public": "email public",  # correct
    "telephone public": "téléphone public",
    
    # Formes alternatives
    "infos": "informations",  # forme complète
    "tel": "téléphone",
    "mail": "courriel",
    "e-mail": "courriel",
    "nb": "nombre",
    
    
    # Corrections supplémentaires trouvées dans les valeurs
    "scev": "SCEV",  # sigle
    "nss": "NSS",  # sigle
    "cnas": "CNAS",  # sigle
    "mip": "MIP" ,  # sigle

    "conte": "congé",
    "contes": "congés",
    "conge": "congé",
    "congés": "conges",
    "conges": "congés",
    "pret": "prêt", 
    "prets": "prêts",
    "coordonnees": "coordonnées",
    "infos": "informations",
    "donnees": "données",
    "prenom": "prénom",
    "naissance": "date de naissance",
    "telephone": "téléphone",
    "numero": "numéro",
    "email": "courriel",
    "nss": "numéro sécurité sociale",
    "nationalite": "nationalité",
    "groupe": "groupe sanguin",
    "sanguin": "groupe sanguin",
    "familiale": "situation familiale",
    "recrutement": "date recrutement",
    "panier": "retenu panier",
    "transport": "bénéfice transport",
    
    "manager": "responsable",
    "public": "visible",
    "conges": "congés",
    "vacances": "congés",
    "repos": "congés",
    "droits": "droit à congé",
    "annuelle": "congé annuelle",
    "recup": "congé récupération",
    "scev": "congé sans solde",
    "experience": "expérience",
    "poste": "emploi",
    "employeur": "entreprise",
    "formation": "apprentissage",
    "stage": "formation",
    "realisation": "réalisation",
    "projet": "réalisation",
    "sanction": "punition",
    "discipline": "sanction",
    "poste": "fonction",
    "service": "département",
    "echelle": "niveau",
    "departement": "service",
    "direction": "management",
    "carriere": "carrière",
    "structure": "entreprise",
    "medailles": "récompenses",
    "apprenti": "stagiaire",
    "specialite": "domaine",
    "organisme": "centre formation",
    "mission": "déplacement",
    "objet": "but",
    "lieu": "destination",
    "prets": "prêts",
    "montant": "somme",
    "duree": "durée",
    "rembourse": "remboursé",
    "pointage": "présence",
    "arrive": "arrivée",
    "depart": "départ",
    "ferie": "férié",
    "sociale": "sécurité sociale",
    "sejour": "période",
    "collaborateurs": "équipe",
    "notification": "alerte",
    "titre": "sujet",
    "document": "fichier",
    "lue": "vue",
    "message": "communication",
    "expediteur": "envoyeur",
    "destinataire": "receveur",
    "contenu": "texte",
    "envoi": "envoie",
    "documents": "fichiers",
    "chemin": "lien",
    "categorie": "type",
    "retraite": "pension",
    "previsionnelle": "prévue",
    "poursuivre": "continuer",
    "remboursement": "récupération",
    "montant": "somme",
    "type": "nature",
    "departement": "département",
    "dept": "département",
    "département": "departement",
    "departement": "dept"
}
# Dictionnaire pour faire le lien entre phrases naturelles et colonnes précises
expression_to_column = {
    "date d'inscription": ("inscription_social", "date"),
    "date de mission": ("mission", "date_debut"),
    "date de remboursement": ("remboursement", "date"),
    "date d'absence": ("absence", "date_debut"),
    "date de formation": ("formation", "date_debut"),
    "date de sanction": ("sanction_discipline", "date"),
    "date de pointage": ("pointage", "date"),
    "date de prêt": ("mes_prets", "date_depot"),
    "date de carrière": ("carriere", "debut"),
    "date de réalisation": ("realisation", "date")
}
##############################
# FONCTIONS UTILITAIRES
##############################

def remove_accents(text: str) -> str:
    """Normalise et supprime les accents d'un texte."""
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def normalize_text(text: str) -> str:
    """Normalise le texte pour la recherche."""
    text = remove_accents(text).lower()
    return re.sub(r'[^\w\s]', '', text)

def corriger_texte(texte: str) -> str:
    texte = texte.lower()
    texte = re.sub(r"[']", "'", texte)
    texte = re.sub(r"ç", "c", texte)

    mots = texte.split()
    mots_corriges = []
    for mot in mots:
        mot_corrige = corrections.get(mot, mot)
        mots_corriges.append(mot_corrige)

    return " ".join(mots_corriges)

def corriger_fautes(text: str) -> str:
    mots = text.split()
    mots_corriges = []
    for mot in mots:
        correction = spell.correction(mot)
        mots_corriges.append(correction if correction else mot)
    return ' '.join(mots_corriges)

def preprocess_question(question: str) -> str:
    return question.lower().strip()

def clean_sql_response(sql_response: str) -> str:
    # Suppression des commentaires
    sql = re.sub(r'--.*?$', '', sql_response, flags=re.MULTILINE)
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    
    # Extraction de la première requête SELECT
    match = re.search(r'(SELECT.*?)(?=;|$)', sql, flags=re.IGNORECASE|re.DOTALL)
    if match:
        sql = match.group(1)
    
    # Correction des noms de tables courants
    replacements = {
        r'\bemploy\b': 'employe',
        r'\bconges\b': 'conge',
        r'\bformations\b': 'formation',
        r'\bpret\b': 'mes_prets'
    }
    
    for pattern, replacement in replacements.items():
        sql = re.sub(pattern, replacement, sql, flags=re.IGNORECASE)
    
    # Suppression des clauses problématiques
    sql = re.sub(r'\b(LIMIT \d+|ORDER BY .*?|GROUP BY .*?|HAVING .*?)(?=;|$)', '', sql, flags=re.IGNORECASE)
    
    return sql.strip()

def extract_lemmas(text: str) -> List[str]:
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

def fix_sql_query(query: str) -> str:
    """
    Valide et nettoie la requête SQL :
    - Supprime les espaces superflus
    - S'assure qu'elle commence par SELECT
    - Enlève le point-virgule final si présent
    """
    import re

    query = query.strip()
    query = re.sub(r'\s+', ' ', query)  # compresser les espaces
    query = query.rstrip(';')

    if not re.match(r'^SELECT\s', query, re.IGNORECASE):
        raise ValueError("La requête ne commence pas par SELECT")

    return query

def find_best_match_table(question: str) -> Tuple[Optional[str], Optional[List[str]]]:
    """Trouve la table et colonnes correspondant à la question."""
    question_norm = normalize_text(question)
    
    # D'abord vérifier les correspondances exactes
    for synonyms, (table, cols) in KEYWORD_SYNONYMS.items():
        for synonym in synonyms:
            synonym_norm = normalize_text(synonym)
            if re.search(rf'\b{synonym_norm}\b', question_norm):
                logger.debug(f"Match exact: {synonym} -> {table}")
                return table, cols
                
    # Ensuite utiliser spaCy pour une analyse plus fine
    doc = nlp(question_norm)
    nouns = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    
    for noun in nouns:
        for synonyms, (table, cols) in KEYWORD_SYNONYMS.items():
            if any(normalize_text(synonym) == noun for synonym in synonyms):
                return table, cols
                
    return None, None


def generate_sql_query(table: str, columns: List[str], id_employe: int) -> str:
    cols_str = ", ".join(columns)
    sql = f"SELECT {cols_str} FROM {table} WHERE id_employe = :id_employe"
    logger.debug(f"Requête SQL générée: {sql}")
    return sql

def execute_sql(sql: str, params: Dict) -> List[Dict]:
    try:
        # Validation de sécurité
        if not sql.strip().upper().startswith('SELECT'):
            raise ValueError("Seules les requêtes SELECT sont autorisées")
            
        result = db.session.execute(text(sql), params)
        return [dict(row) for row in result]
    except Exception as e:
        logger.error(f"Erreur exécution SQL: {e}")
        return []

def detect_colonne_date(question: str):
    for expression, (table, colonne) in expression_to_column.items():
        if expression in question.lower():
            return table, colonne
    return None, None

def lemmatize_question(question: str) -> str:
    doc = nlp(question)
    lemmatized = ' '.join([token.lemma_ for token in doc])
    return lemmatized

def fetch_data(sql: str, params: Dict) -> List[Dict]:
    try:
        # Validation de sécurité
        if not sql.strip().upper().startswith('SELECT'):
            raise ValueError("Seules les requêtes SELECT sont autorisées")
            
        if any(keyword in sql.upper() for keyword in ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER']):
            raise ValueError("Opération non autorisée")

        # Correction des noms de tables
        sql = sql.replace("employ ", "employe ").replace("employ,", "employe,")
        
        # Exécution avec timeout
        with db.engine.connect().execution_options(statement_timeout=30) as connection:
            result = connection.execute(text(sql), params)
            rows = [dict(row._mapping) for row in result]
            
            # Formatage des dates et autres types spéciaux
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, date):
                        row[key] = value.isoformat()
                    elif isinstance(value, Decimal):
                        row[key] = float(value)
                        
            return rows
            
    except Exception as e:
        logger.error(f"Erreur fetch_data: {e}\nRequête: {sql}")
        return []

from typing import List, Dict
import pandas as pd

def post_process_answer(rows: List[Dict], question: str):
    """Retourne uniquement les données utiles sans clé superflue."""

    if not rows:
        return "Aucune donnée trouvée pour votre requête."

    question_lower = question.lower().strip()
    first_row = rows[0]

    # 1. Réponse simple à une seule colonne
    if len(first_row) == 1 and len(rows) == 1:
        return list(first_row.values())[0]

    # 2. Questions de comptage
    if any(q in question_lower for q in ["combien", "nombre", "count"]):
        try:
            count = list(first_row.values())[0]
            return int(count)
        except:
            return len(rows)

    # 3. Questions oui/non
    if question_lower.startswith(("ai-je", "suis-je", "est-ce que", "avez-vous", "as-tu")):
        exists = bool(list(first_row.values())[0]) if len(first_row) == 1 else bool(rows)
        return "Oui" if exists else "Non"

    # 4. Formater les dates si applicable
    for row in rows:
        for k, v in row.items():
            if "date" in k.lower() and v:
                try:
                    row[k] = pd.to_datetime(v).strftime('%d/%m/%Y')
                except Exception:
                    pass

    # 5. Calcul durée si date_debut/date_fin
    if "durée" in question_lower:
        for row in rows:
            if 'date_debut' in row and 'date_fin' in row:
                try:
                    debut = pd.to_datetime(row['date_debut'])
                    fin = pd.to_datetime(row['date_fin'])
                    row['durée_jours'] = (fin - debut).days
                except Exception:
                    pass

    # 6. Si trop de lignes → échantillon
    if len(rows) > 5:
        return rows[:3]

    # 7. Résultat complet
    return rows



def get_all_table_and_column_names():
    """Retourne la liste de tous les noms de tables et de colonnes de la BDD."""
    table_names = set()
    column_names = set()
    # Compatible SQLAlchemy 1.x et 2.x
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        if hasattr(cls, '__tablename__'):
            table_names.add(cls.__tablename__)
            for col in cls.__table__.columns:
                column_names.add(col.name)
    return table_names, column_names
   
def question_contains_table_or_column(question: str) -> bool:
    tables, columns = get_all_table_and_column_names()
    question_norm = normalize_text(question)
    for name in tables.union(columns):
        if name.lower() in question_norm:
            return True
    return False
import re
import logging
import psycopg2


logger = logging.getLogger(__name__)
import re
import logging

logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)

import re

import re
from typing import Optional

import re

import re

import re
from typing import List
import re
import logging

logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)



import re
import logging

logger = logging.getLogger(__name__)

def extract_best_sql(output: str) -> str:
    """
    Extrait la meilleure requête SQL complète depuis un texte généré.
    Elle commence par SELECT, contient FROM, éventuellement WHERE/ORDER/LIMIT,
    et ne contient pas de texte parasite.
    """
    try:
        # Nettoyer le texte brut (enlever répétitions de schema)
        cleaned = re.sub(r"(Table\s+\w+\s*:\s*-.*?)(\n|$)", "", output, flags=re.IGNORECASE | re.DOTALL)

        # Cherche toutes les requêtes valides
        candidates = re.findall(
            r"(?i)(?<![a-z])select\s+.+?\s+from\s+.+?(?:\s+where\s+.+?)?(?:\s+order\s+by\s+.+?)?(?:\s+limit\s+\d+)?(?:\s*;|\Z)",
            cleaned,
            flags=re.DOTALL
        )

        if not candidates:
            raise ValueError("Aucune requête SQL détectée.")

        # Nettoyage de la première requête
        sql = candidates[0].strip()
        sql = re.sub(r'\s+', ' ', sql)
        if not sql.lower().startswith("select"):
            raise ValueError("La sortie ne commence pas par SELECT")
        return sql.rstrip(';')

    except Exception as e:
        logger.error(f"[extract_best_sql ERROR] : {e}")
        return ""

def clean_sql_columns(sql: str) -> str:
    """Nettoie les colonnes dupliquées dans un SELECT SQL."""
    try:
        match = re.search(r"(SELECT\s+)(.*?)(\s+FROM\s+)", sql, re.IGNORECASE | re.DOTALL)
        if not match:
            return sql  # Rien à nettoyer

        prefix, column_block, suffix = match.groups()
        columns = [col.strip() for col in column_block.split(',')]
        seen = set()
        cleaned_columns = []
        for col in columns:
            norm = col.lower()
            if norm not in seen:
                seen.add(norm)
                cleaned_columns.append(col)

        cleaned_sql = prefix + ', '.join(cleaned_columns) + suffix + sql[match.end():]
        return cleaned_sql.strip()
    except Exception as e:
        logger.warning(f"[clean_sql_columns ERROR] : {e}")
        return sql

import logging
from collections import defaultdict
from typing import Tuple

# Configuration du logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import re
import logging

logger = logging.getLogger(__name__)

import re
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

logger = logging.getLogger(__name__)

# Chargement du modèle fine-tuné RH sur CPU
trained_model_path = r"C:\Users\WINDOWS 10\Desktop\Ma_Brique\try_1 - Copie (3)\chatbot\fichier_generer"
finetuned_tokenizer = AutoTokenizer.from_pretrained(trained_model_path)
finetuned_model = AutoModelForSeq2SeqLM.from_pretrained(trained_model_path)

finetuned_pipeline = pipeline(
    "text2text-generation",
    model=finetuned_model,
    tokenizer=finetuned_tokenizer,
    device=-1  # CPU
)

import re
import logging

logger = logging.getLogger(__name__)

# Chargement du tokenizer Flan-T5 pour le tronquage
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

def truncate_prompt(prompt: str, max_tokens: int = 500) -> str:
    tokens = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)



import re
import logging

logger = logging.getLogger(__name__)

# Dictionnaire de colonnes autorisées par table
allowed_columns = {
    "formation": {"description", "date_debut", "date_fin", "type"},
    "realisation": {"description", "date"},
    "mission": {"objet", "lieu", "date_debut", "date_fin", "itineraire"},
    "mes_prets": {"montant", "date_depot", "rembourse"},
    "pointage": {"heure_arrive", "heure_depart", "date", "est_jour_ferie"},
    "conge": {"designation", "date_depart", "date_reprise"},
    "droit_conge": {"conge_annuelle", "conge_recup", "conge_scev"}
}

import re
import logging
def handle_next_query(match: re.Match, question: str, id_employe: int,
                    tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'prochain congé'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None
        
    columns = get_relevant_columns(question, table, tables_columns)
    
    return f"""SELECT {', '.join(columns)} 
              FROM {table} 
              WHERE id_employe = {id_employe} 
              AND {date_col} > CURRENT_DATE
              ORDER BY {date_col} ASC 
              LIMIT 1"""

def handle_count_query(match: re.Match, question: str, id_employe: int,
                     tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'combien de missions'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    return f"""SELECT COUNT(*) as count 
              FROM {table} 
              WHERE id_employe = {id_employe}"""


def handle_today_query(match: re.Match, question: str, id_employe: int,
                      tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'pointages aujourd'hui'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None
        
    columns = get_relevant_columns(question, table, tables_columns)
    
    return f"""SELECT {', '.join(columns)} 
              FROM {table} 
              WHERE id_employe = {id_employe} 
              AND {date_col} = CURRENT_DATE"""




def handle_date_range_query(match: re.Match, question: str, id_employe: int,
                          tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'entre date1 et date2'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None
        
    date1 = match.group(2)  # Première date
    date2 = match.group(3)  # Deuxième date
    columns = get_relevant_columns(question, table, tables_columns)
    
    return f"""SELECT {', '.join(columns)} 
              FROM {table} 
              WHERE id_employe = {id_employe} 
              AND {date_col} BETWEEN TO_DATE('{date1}', 'DD/MM/YYYY') 
              AND TO_DATE('{date2}', 'DD/MM/YYYY')"""
def handle_first_query(match: re.Match, question: str, id_employe: int,
                     tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'première mission'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None
        
    columns = get_relevant_columns(question, table, tables_columns)
    
    return f"""SELECT {', '.join(columns)} 
              FROM {table} 
              WHERE id_employe = {id_employe} 
              ORDER BY {date_col} ASC 
              LIMIT 1"""
def handle_current_month_query(match: re.Match, question: str, id_employe: int,
                             tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'ce mois'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None
        
    columns = get_relevant_columns(question, table, tables_columns)
    
    return f"""SELECT {', '.join(columns)} 
              FROM {table} 
              WHERE id_employe = {id_employe} 
              AND EXTRACT(MONTH FROM {date_col}) = EXTRACT(MONTH FROM CURRENT_DATE)
              AND EXTRACT(YEAR FROM {date_col}) = EXTRACT(YEAR FROM CURRENT_DATE)"""
def handle_last_query(match: re.Match, question: str, id_employe: int,
                     tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """
    Gère les requêtes du type 'dernier X' ou 'last X'.
    Exemples:
    - "Ma dernière mission"
    - "Last formation"
    - "Dernier pointage"
    
    Args:
        match: Objet de correspondance regex
        question: Question posée par l'utilisateur
        id_employe: ID de l'employé
        tables_columns: Dictionnaire de configuration des tables
        table_mapping: Mapping des termes vers les tables
        
    Returns:
        str: Requête SQL formatée ou None si non applicable
    """
    try:
        # 1. Détection de la table
        table = detect_table_from_question(question, table_mapping)
        if not table or table not in tables_columns:
            logger.debug(f"Table non trouvée pour: {question}")
            return None

        # 2. Récupération de la colonne de date
        date_col = get_primary_date_column(table, tables_columns)
        if not date_col:
            logger.debug(f"Aucune colonne de date trouvée dans {table}")
            # Fallback sur l'ID si pas de date
            date_col = "id"

        # 3. Sélection des colonnes pertinentes
        columns = get_relevant_columns(question, table, tables_columns) or ["*"]
        
        # 4. Sécurisation des noms de colonnes/tables
        safe_columns = ', '.join([f'"{col}"' for col in columns])
        safe_table = f'"{table}"'
        safe_date_col = f'"{date_col}"'

        # 5. Construction de la requête
        query = f"""
            SELECT {safe_columns}
            FROM {safe_table}
            WHERE id_employe = {id_employe}
            ORDER BY {safe_date_col} DESC
            LIMIT 1
        """
        
        logger.debug(f"Requête 'last' générée: {query}")
        return query.strip()

    except Exception as e:
        logger.error(f"Erreur dans handle_last_query: {str(e)}", exc_info=True)
        return None
def ask_flan(question: str, id_employe: int) -> str:
    """Génère des requêtes SQL RH robustes avec validation complète des schémas."""
    try:
        # 1. Configuration complète du schéma
        tables_columns = {
            "formation": {
                "columns": ["id_formation", "description", "date_debut", "date_fin", "type"],
                "date_columns": ["date_debut", "date_fin"],
                "text_columns": ["description", "type"]
            },
            "realisation": {
                "columns": ["id_realisation", "description", "date"],
                "date_columns": ["date"],
                "text_columns": ["description"]
            },
            "mission": {
                "columns": ["id_mission", "objet", "lieu", "date_debut", "date_fin", "itineraire"],
                "date_columns": ["date_debut", "date_fin"],
                "text_columns": ["objet", "lieu", "itineraire"]
            },
            "mes_prets": {
                "columns": ["id_prets", "montant", "date_depot", "rembourse", "numero_contract", 
                          "is_accorde", "motif_prets", "duree", "date_debut_remboursement"],
                "date_columns": ["date_depot", "date_debut_remboursement"],
                "text_columns": ["numero_contract", "motif_prets"],
                "numeric_columns": ["montant", "duree"],
                "boolean_columns": ["rembourse", "is_accorde"]
            },
            "pointage": {
                "columns": ["id_pointage", "heure_arrive", "heure_depart", "date", "est_jour_ferie"],
                "date_columns": ["date"],
                "time_columns": ["heure_arrive", "heure_depart"],
                "boolean_columns": ["est_jour_ferie"]
            },
            "conge": {
                "columns": ["id_conge", "designation", "date_depart", "date_reprise"],
                "date_columns": ["date_depart", "date_reprise"],
                "text_columns": ["designation"]
            },
            "droit_conge": {
                "columns": ["id_d_conge", "conge_annuelle", "conge_recup", "conge_scev"],
                "numeric_columns": ["conge_annuelle", "conge_recup", "conge_scev"]
            }
        }

        # 2. Mapping des termes courants vers les tables réelles
        table_mapping = {
    # Employé
    "employe": "employe",
    "employés": "employe",
    "employee": "employe",
    "employees": "employe",

    # Congé
    "conge": "conge",
    "conges": "conge",
    "congé": "conge",
    "congés": "conge",
    "vacation": "conge",
    "leave": "conge",

    # Droit de congé
    "droit": "droit_conge",
    "droits": "droit_conge",
    "droit_conge": "droit_conge",
    "droits_conge": "droit_conge",
    "right": "droit_conge",
    "rights": "droit_conge",

    # Formation
    "formation": "formation",
    "formations": "formation",
    "training": "formation",
    "trainings": "formation",

    # Expérience
    "experience": "experience",
    "expériences": "experience",
    "experiences": "experience",

    # Réalisation
    "realisation": "realisation",
    "réalisation": "realisation",
    "realisations": "realisation",
    "réalisations": "realisation",
    "achievement": "realisation",
    "accomplishment": "realisation",

    # Mission
    "mission": "mission",
    "missions": "mission",
    "assignment": "mission",
    "assignments": "mission",

    # Sanction
    "sanction": "sanction_discipline",
    "sanctions": "sanction_discipline",
    "discipline": "sanction_discipline",
    "disciplinary": "sanction_discipline",

    # Prêt
    "pret": "mes_prets",
    "prets": "mes_prets",
    "prêt": "mes_prets",
    "prêts": "mes_prets",
    "loan": "mes_prets",
    "loans": "mes_prets",

    # Pointage
    "pointage": "pointage",
    "pointages": "pointage",
    "attendance": "pointage",

    # Carrière
    "carriere": "carriere",
    "carrière": "carriere",
    "carrieres": "carriere",
    "carrières": "carriere",
    "career": "carriere",

    # Poste
    "poste": "poste",
    "postes": "poste",
    "position": "poste",
    "positions": "poste",

    # Apprenti
    "apprenti": "apprentis",
    "apprentis": "apprentis",
    "apprents": "apprentis",
    "trainee": "apprentis",
    "trainees": "apprentis",

    # Inscription sociale
    "inscription": "inscription_social",
    "inscriptions": "inscription_social",
    "social": "inscription_social",
    "social_inscription": "inscription_social",

    # Retraite
    "retraite": "retraite",
    "retraites": "retraite",
    "retirement": "retraite"
}


        # 3. Détection des requêtes spéciales (temporelles/agrégations)
        special_patterns = [
            # Dernier/dernière
            (r"\b(dernier|dernière|last)\b\s+(.*?)\b", handle_last_query),


            #Premiere
            (r"(première|premier|first)\s+(.*)", handle_first_query),
            # Cette année
            (r"(cette année|cette année|année en cours|this year)", handle_current_year_query),
            # Prochain/prochaine
            (r"(prochain|prochaine|next)\s+(.*)", handle_next_query),
            # Combien de/nombre
            (r"(combien de|nombre|count|how many)\s+(.*)", handle_count_query),
            # Entre dates
            (r"(entre|between)\s+(\d{2}/\d{2}/\d{4})\s+et\s+(\d{2}/\d{2}/\d{4})", handle_date_range_query),
            # Mois courant
            (r"(ce mois|mois en cours|current month)", handle_current_month_query),
             # Aujourd'hui
            (r"(aujourd'hui|today)", handle_today_query),
            (r"(en|le)?\s*(\d{2}/\d{2}/\d{4}|\d{2}/\d{4}|\d{4}|janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)", handle_explicit_date_query)
            
        ]

        # 4. Vérification des requêtes spéciales en premier
        for pattern, handler in special_patterns:
            match = re.search(pattern, question.lower())
            if match:
                result = handler(match, question, id_employe, tables_columns, table_mapping)
                if result:
                    return result

        # 5. Génération standard si pas une requête spéciale
        return generate_standard_query(question, id_employe, tables_columns, table_mapping)

    except Exception as e:
        logger.error(f"Erreur dans ask_flan: {str(e)}", exc_info=True)
        return "Aucune réponse trouvée."


# Fonctions helper définies comme fonctions autonomes

def handle_explicit_date_query(match: re.Match, question: str, id_employe: int,
                                tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """
    Gère les requêtes contenant une date explicite : année, mois, jour.
    Exemple : "les missions en juin", "mes absences le 15/06/2025", "congé en 2024",
    "ma mission de juin", "mon absence le 15/06/2025", "congé en 2024"
    """
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None

    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None

    # Extraire une date complète ou partielle
    patterns = [
        (r"\b(\d{2})/(\d{2})/(\d{4})\b", "%d/%m/%Y"),
        (r"\b(\d{2})/(\d{4})\b", "%m/%Y"),
        (r"\b(\d{4})\b", "%Y"),
        (r"\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\b", "mois")
    ]

    date_filter = ""
    mois_map = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04",
        "mai": "05", "juin": "06", "juillet": "07", "août": "08",
        "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
    }

    for p, fmt in patterns:
        m = re.search(p, question.lower())
        if m:
            if fmt == "%d/%m/%Y":
                jour, mois, annee = m.groups()
                date_filter = f"DATE_TRUNC('day', {date_col}) = TO_DATE('{jour}/{mois}/{annee}', 'DD/MM/YYYY')"
            elif fmt == "%m/%Y":
                mois, annee = m.groups()
                date_filter = f"EXTRACT(MONTH FROM {date_col}) = {int(mois)} AND EXTRACT(YEAR FROM {date_col}) = {int(annee)}"
            elif fmt == "%Y":
                annee = m.group(1)
                date_filter = f"EXTRACT(YEAR FROM {date_col}) = {int(annee)}"
            elif fmt == "mois":
                mois_str = m.group(1)
                mois_num = mois_map.get(mois_str)
                if mois_num:
                    date_filter = f"EXTRACT(MONTH FROM {date_col}) = {int(mois_num)}"
            break

    if not date_filter:
        return None

    sql = f"""
    SELECT {', '.join(col for col in tables_columns[table]["columns"] if col != 'id_' + table)}
    FROM {table}
    WHERE id_employe = :id_employe AND {date_filter}
    ORDER BY {date_col} ASC
    """
    return sql.strip()

def handle_current_year_query(match: re.Match, question: str, id_employe: int,
                           tables_columns: Dict, table_mapping: Dict) -> Optional[str]:
    """Gère les requêtes du type 'cette année'."""
    table = detect_table_from_question(question, table_mapping)
    if not table:
        return None
        
    date_col = get_primary_date_column(table, tables_columns)
    if not date_col:
        return None
        
    columns = get_relevant_columns(question, table, tables_columns)
    
    return f"""SELECT {', '.join(columns)} 
              FROM {table} 
              WHERE id_employe = {id_employe} 
              AND EXTRACT(YEAR FROM {date_col}) = EXTRACT(YEAR FROM CURRENT_DATE)
              ORDER BY {date_col}"""

def detect_table_from_question(question: str, table_mapping: Dict) -> Optional[str]:
    """Détecte la table la plus pertinente d'après la question."""
    question_lower = question.lower()
    
    # Recherche directe par nom de table
    for table in table_mapping.values():
        if table in question_lower:
            return table
            
    # Recherche par termes mappés
    for term, table in table_mapping.items():
        if term in question_lower:
            return table
            
    return None

def get_primary_date_column(table: str, tables_columns: Dict) -> Optional[str]:
    """Retourne la colonne de date principale d'une table."""
    if table not in tables_columns:
        return None
        
    date_cols = tables_columns[table].get("date_columns", [])
    if not date_cols:
        return None
        
    # Préfère les colonnes 'date_' ou 'fin'
    for col in date_cols:
        if col.startswith("date_") or "fin" in col:
            return col
            
    return date_cols[0]

def get_relevant_columns(question: str, table: str, tables_columns: Dict) -> List[str]:
    """Sélectionne les colonnes les plus pertinentes selon la question."""
    if table not in tables_columns:
        return ["*"]
        
    cols = tables_columns[table]["columns"]
    question_lower = question.lower()
    
    # Filtre les colonnes pertinentes
    relevant_cols = []
    for col in cols:
        if col == "id_employe":
            continue
        if col in question_lower:
            relevant_cols.append(col)
            
    # Si aucune correspondance, prend les colonnes principales
    if not relevant_cols:
        if "date_columns" in tables_columns[table]:
            relevant_cols = tables_columns[table]["date_columns"][:1]
        if "text_columns" in tables_columns[table]:
            relevant_cols += tables_columns[table]["text_columns"][:1]
        if not relevant_cols and len(cols) > 1:
            relevant_cols = cols[1:2]
            
    return relevant_cols or ["*"]

def generate_standard_query(question: str, id_employe: int,
                          tables_columns: Dict, table_mapping: Dict) -> str:
    """Génère une requête standard pour les questions non spéciales."""
    prompt = build_prompt(question, id_employe, tables_columns)
    raw_sql = get_raw_sql_from_flan(prompt)
    return validate_and_fix_sql(raw_sql, id_employe, tables_columns, table_mapping)

def build_prompt(question: str, id_employe: int, tables_columns: Dict) -> str:
    """Construit le prompt pour le modèle FLAN."""
    tables_info = []
    for table, config in tables_columns.items():
        cols = ", ".join(config["columns"])
        tables_info.append(f"{table}({cols})")
    
    return f"""
Schéma de la base de données RH:
{'\n'.join(tables_info)}

Règles STRICTES:
1. Utiliser exclusivement les tables et colonnes ci-dessus
2. Toujours inclure WHERE id_employe = {id_employe}
3. Ne pas inventer de colonnes
4. Pour les dates, utiliser le format DATE 'YYYY-MM-DD'
5. n'utilise aucune colonne et aucune table n'est pas dans le shéma.
6. si vous ne trouve pas la reponse return "Aucune réponse trouvée.".
Exemples:
Question: Quels sont mes weekends ou jours feriés travaillés?
Réponse:  SELECT date, heure_arrive, heure_depart, est_jour_ferie
            FROM pointage
            WHERE id_employe = %s
              AND (
                est_jour_ferie = TRUE
                OR EXTRACT(DOW FROM date) IN (5,6)
              )
            ORDER BY date DESC

Question: Quelles sont mes formations cette année?
Réponse: SELECT description, date_debut, date_fin FROM formation WHERE id_employe = {id_employe} AND EXTRACT(YEAR FROM date_debut) = EXTRACT(YEAR FROM CURRENT_DATE)


Question: {question}
Réponse:
"""

def get_raw_sql_from_flan(prompt: str) -> str:
    """Obtient la requête SQL brute depuis le modèle FLAN."""
    outputs = flan_pipeline(
        prompt.strip(),
        max_new_tokens=200,
        do_sample=False,
        num_beams=5,
        temperature=0.1
    )
    return outputs[0]["generated_text"].strip()

def validate_and_fix_sql(raw_sql: str, id_employe: int,
                        tables_columns: Dict, table_mapping: Dict) -> str:
    """Valide et corrige la requête SQL générée."""
    # Extraction de la partie SELECT ... WHERE
    sql_match = re.search(r'(SELECT\s+.+?\s+FROM\s+.+?WHERE\s+.+?)(?:ORDER BY|GROUP BY|LIMIT|$)', 
                         raw_sql, re.IGNORECASE | re.DOTALL)
    if not sql_match:
        return "Aucune réponse trouvée."
    
    sql = sql_match.group(1).strip()
    sql = re.sub(r'\s+', ' ', sql)
    
    # Correction du nom de la table
    table_match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
    if not table_match:
        return "Aucune réponse trouvée."
    
    table = table_match.group(1).lower()
    table = table_mapping.get(table, table)
    
    if table not in tables_columns:
        return "Aucune réponse trouvée."
    
    # Validation des colonnes
    cols_match = re.search(r'SELECT\s+(.+?)\s+FROM', sql, re.IGNORECASE)
    if not cols_match:
        return "Aucune réponse trouvée."
    
    selected_cols = [c.strip().split(' ')[0].lower() for c in cols_match.group(1).split(',')]
    valid_cols = [col for col in selected_cols if col in tables_columns[table]["columns"]]
    
    if not valid_cols:
        valid_cols = tables_columns[table]["columns"][1:4]  # Exclut l'ID
    
    # Reconstruction de la requête
    where_match = re.search(r'WHERE\s+.+', sql, re.IGNORECASE)
    where_clause = where_match.group(0) if where_match else f"WHERE id_employe = {id_employe}"
    
    # S'assure que le WHERE contient la condition id_employe
    if f"id_employe = {id_employe}" not in where_clause.lower():
        where_clause = f"WHERE id_employe = {id_employe} AND {where_clause[6:]}" if where_match else f"WHERE id_employe = {id_employe}"
    
    return f"SELECT {', '.join(valid_cols)} FROM {table} {where_clause} LIMIT 100"














def requete_valide(requete: str) -> bool:
    requete = requete.strip().lower()
    return (
        requete.startswith("select") and
        "from" in requete and
        ";" in requete and
        re.match(r"^select\s.+\sfrom\s.+;", requete, re.DOTALL) is not None
    )











##############################
# DICTIONNAIRES ET CONFIGURATIONS
##############################

# (Conserver les dictionnaires KEYWORD_SYNONYMS et corrections existants)

##############################
# ROUTES API
##############################



from flask import request, jsonify
import logging

# Assure-toi que ces fonctions sont bien définies quelque part :
# preprocess_question, find_best_match_table, generate_sql_query,
# ask_flan, clean_sql_response, fix_sql_query,
# fetch_data, post_process_answer

from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)
from flask import Flask, request, jsonify
from sqlalchemy.sql import text
def is_manager_question(question: str) -> bool:
    """Détecte si la question concerne les collaborateurs d'un manager."""
    manager_keywords = [
        "mes collaborateurs", "mon équipe", "mes employés", 
        "personnel sous ma responsabilité", "subordonnés",
        "collaborateur", "collaborateurs", "équipe",
        "collaborateur smith", "collaborateur id", "employé id"
    ]
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in manager_keywords)

def extract_collaborator_info(question: str) -> tuple:
    """Extrait le nom ou l'ID du collaborateur de la question."""
    question_lower = question.lower()
    
    # Détection d'un ID (ex: "collaborateur id 2")
    id_match = re.search(r'collaborateur id (\d+)', question_lower)
    if id_match:
        return ('id', int(id_match.group(1)))
    
    # Détection d'un nom (ex: "collaborateur smith")
    name_match = re.search(r'collaborateur (\w+)', question_lower)
    if name_match:
        return ('nom', name_match.group(1))
    
    return (None, None)
from typing import List

def get_collaborateurs_ids(id_manager: int) -> List[int]:
    """
    Retourne la liste des IDs des collaborateurs d’un manager donné.
    """
    try:
        result = db.session.execute(text("""
            SELECT unnest(collaborateurs)::integer AS id_collaborateur
            FROM manager
            WHERE id_employe = :id_manager
        """), {"id_manager": id_manager})
        return [row["id_collaborateur"] for row in result]
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des collaborateurs : {e}")
        return []

def generate_manager_sql(question: str, id_employe: int) -> str:
    """Génère une requête SQL pour les questions sur les collaborateurs."""
    # Détection de la table concernée
    table, columns = find_best_match_table(question)
    if not table:
        table = "employe"  # Table par défaut
        
    # Construction de la requête de base
    cols_str = ", ".join(columns) if columns else "*"
    sql = f"""
    SELECT {cols_str} 
    FROM {table} 
    WHERE id_employe = ANY(
        SELECT unnest(collaborateurs)::integer 
        FROM manager 
        WHERE id_employe = {id_employe}
    )
    """
    
    # Ajout de filtres spécifiques pour un collaborateur particulier
    collab_type, collab_value = extract_collaborator_info(question)
    
    if collab_type == 'id':
        sql += f" AND id_employe = {collab_value}"
    elif collab_type == 'nom':
        sql += f" AND id_employe IN (SELECT id_employe FROM employe WHERE nom ILIKE '%{collab_value}%')"
    
    # Gestion des requêtes temporelles
    question_lower = question.lower()
    if "dernier" in question_lower or "récent" in question_lower:
        sql += " ORDER BY date DESC LIMIT 1"
    elif "ancien" in question_lower or "premier" in question_lower:
        sql += " ORDER BY date ASC LIMIT 1"
        
    return sql

def handle_manager_question(question: str, id_employe: int) -> Dict:
    """Traite une question concernant les collaborateurs d'un manager."""
    if not is_manager_question(question):
        return None
        
    # Vérification que l'utilisateur est bien un manager
    user = Employe.query.get(id_employe)
    if not user or not user.is_manager:
        return {"error": "Vous n'êtes pas manager ou n'avez pas de collaborateurs"}
    
    # Génération de la requête SQL
    sql = generate_manager_sql(question, id_employe)
    rows = fetch_data(sql, {})
    
    # Post-traitement des résultats
    response = post_process_answer(rows, question)
    
    return {
        "question": question,
        "sql_query": sql,
        "response": response,
        "is_manager_query": True
    }




def detect_custom_sql(question: str, id_employe: int):
    if "collaborateurs" in question.lower():
        return text("""
            SELECT e.id_employe, e.nom, e.prenom
            FROM employe e
            WHERE e.id_employe = ANY (
              SELECT unnest(collaborateurs)::integer
              FROM manager
              WHERE id_employe = :id_employe
            )
        """), {"id_employe": id_employe}
    return None, None


@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Données JSON requises"}), 400

        question = data.get("question", "").strip()
        id_employe = data.get("id_employe")

        if not question:
            return jsonify({"success": False, "message": "Question requise"}), 400

        try:
            id_employe = int(id_employe)
        except (TypeError, ValueError):
            return jsonify({"success": False, "message": "ID employé valide requis"}), 400

        # Si c'est une question manager
        manager_response = handle_manager_question(question, id_employe)
        if manager_response:
            if "error" in manager_response:
                return jsonify({"success": False, "message": manager_response["error"]}), 403
            return jsonify({
                "success": True,
                "question": question,
                "response": manager_response["response"],
                "sql_query": manager_response["sql_query"],
                "is_manager_query": True
            })

        # Prétraitement question
        question_corrigée = corriger_texte(question)
        question_corrigée = corriger_fautes(question_corrigée)
        question_clean = preprocess_question(question_corrigée)

        
        sql_query = ask_flan(question_clean, id_employe)

        
        if sql_query.strip().lower() == "aucune réponse trouvée.":
            table, columns = find_best_match_table(question_clean)
            if table and columns:
                sql_query = generate_sql_query(table, columns, id_employe)

        # Nettoyage
        sql_query = clean_sql_response(sql_query)

        # ✅ Sécurité : requête doit commencer par SELECT
        if not sql_query.strip().lower().startswith("select"):
            logger.warning(f"⚠️ Requête IA invalide (non-SELECT) : {sql_query}")
            return jsonify({
                "success": False,
                "message": "La requête générée est invalide (elle ne commence pas par SELECT)."
            }), 422

        # Validation stricte
        sql_query = fix_sql_query(sql_query)

        # Exécution
        rows = fetch_data(sql_query, {"id_employe": id_employe})
        response = post_process_answer(rows, question_clean)

        return jsonify({
            "success": True,
            "question": question,
            "sql_query": sql_query,
            "response": response,
            "is_manager_query": False
        })

    except Exception as e:
        logger.exception("Erreur interne dans /api/ask")
        return jsonify({"success": False, "message": "Erreur interne du serveur"}), 500




@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')

    if not email_valide(email):
        return jsonify({"status": "error", "message": "Format email non valide."}), 400

    cur = conn.cursor()
    cur.execute(
        "SELECT id_employe, nom, prenom, is_manager, mot_de_passe FROM employe WHERE email = %s",
        (email,)
    )
    result = cur.fetchone()
    cur.close()

    if result:
        id_employe, nom, prenom, is_manager, mot_de_passe_hash = result

        if not mot_de_passe_hash or not mot_de_passe_hash.startswith('$2'):
            return jsonify({
                "status": "error",
                "message": "Connexion impossible : mot de passe non sécurisé. Contactez l'administrateur."
            }), 401

        try:
            if bcrypt.checkpw(mot_de_passe.encode('utf-8'), mot_de_passe_hash.encode('utf-8')):
                return jsonify({
                    "status": "success",
                    "message": "Connexion réussie",
                    "id": id_employe,
                    "nom": nom,
                    "prenom": prenom,
                    "is_manager": is_manager
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Email ou mot de passe incorrect."
                }), 401
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Erreur serveur lors de la vérification du mot de passe."
            }), 500

    return jsonify({
        "status": "error",
        "message": "Email ou mot de passe incorrect."
    }), 401

print(">>> Flask backend démarré depuis appback.py <<<")
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "routes": [str(rule) for rule in app.url_map.iter_rules()]
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
