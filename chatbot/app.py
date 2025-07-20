from flask import Flask, request, jsonify
import psycopg2
import requests

app = Flask(__name__)

# Configuration de l'API GPT-4o (OpenRouter)
api_key = "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"
model = "openai/gpt-4o"

# Connexion à PostgreSQL
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="Ma_Bdd",
        user="postgres",
        password="admin"
    )

# Schéma de ta base pour aider GPT à comprendre
schema_bdd = """
Employe(Id_Employe, Nom, Prenom, Date_naissance, Lieu_naissance, Sexe, Adresse, Numero_telephone, Email, NSS, Nationalite, Groupe_sanguin, Situation_familiale, Date_recrutement, Retenu_panier, Benification_transport, mot_de_passe)
Manager(Id_Manager, mot_de_passe)
Poste(Code_Poste, Intitule, Service, Niveau, Echelle, Date_recrutement, Departement, Departement_arrive, Diplome_secteur, Experience_secteur, Experience_hors_secteur, Direction, Id_Employe)
Carriere(Id_Carriere, Duree, Debut, Structure, Echelle, Classification, Medailles, Id_Employe)
Conge(Id_Conge, Designation, Date_depart, Date_reprise, Id_Employe)
Droit_Conge(Id_D_Congé, Conge_annuelle, Conge_recup, Conge_scev, Id_Employe)
Formation(Id_Formation, Description, Date_debut, Date_fin, Id_Employe)
Mission(Id_Mission, Objet, Lieu, Date_debut, Date_fin, Itineraire, Id_Employe)
Sanction_deceplinaire(Id_Sanction_deceplinaire, Date, Designation, SNC, DNC, Id_Employe)
Pointage(Id_Pointage, Heure_arrive, Heure_depart, Date, Id_Employe)
Mouvements(Id_mouvement, Date_depart, Date_retour, Motif, Id_Employe)
Realisation(Id_Realisation, Intitule, Date_debut, Date_fin, Description, Id_Employe)
Categorie(Id_Categorie, Nom, Date, Id_Employe)
Apprents(Id_Apprents, Nom, Specialite, Organisme, Date_debut, Date_fin, Observation, Id_Employe)
Remboursement_Social(Id_Remboursement, Prix, Date_Remboursement, Id_Employe)
Inscription_Social(Id_Inscription, Sejour, Date, Type, Id_Employe)
"""

@app.route('/question', methods=['POST'])
def repondre_question():
    try:
        data = request.get_json()
        question = data['question']
        id_employe = data['id_employe']

        # Création du prompt pour GPT
        prompt = f"""
Voici la structure de la base :
{schema_bdd}

L'utilisateur est connecté avec Id_Employe = {id_employe}.

Génère une requête SQL PostgreSQL qui répond à la question :
"{question}"

Retourne uniquement la requête SQL sans explication.
"""

        # Envoi à GPT-4o
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://chat.openrouter.ai/",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        result = response.json()
        sql_query = result["choices"][0]["message"]["content"].strip()

        # Nettoyage du format ```sql ... ```
        if sql_query.startswith("```"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        # Remplacement des paramètres
        sql_query = sql_query.replace(":Id_Employe", str(id_employe)).replace("?", str(id_employe))

        # 🔐 Sécurité : interdire l'accès aux données sensibles
        colonnes_interdites = ["mot_de_passe", "password", "email", "nss", "numero_telephone"]
        for colonne in colonnes_interdites:
            if colonne.lower() in sql_query.lower():
                return jsonify({
                    "error": f"⚠️ Accès non autorisé à la donnée sensible : '{colonne}'"
                }), 403

        print("📤 Requête SQL exécutée :")
        print(sql_query)

        # Exécution de la requête
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"query": sql_query, "result": rows})

    except Exception as e:
        return jsonify({"error": str(e), "details": response.text}), 500

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)