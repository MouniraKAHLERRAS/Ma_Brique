from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connexion à ta base PostgreSQL (à faire UNE SEULE FOIS ici)
conn = psycopg2.connect(
    host="localhost",
    database="My_Bdd",
    user="postgres",
    password="12345678"
)
cursor = conn.cursor()

# Route de test
@app.route('/')
def home():
    return "Backend connecté avec succès à PostgreSQL 🎉"

# Route de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    mot_de_passe = data['mot_de_passe']

    cur = conn.cursor()
    cur.execute(
        "SELECT id_employe, nom, prenom FROM Employe WHERE email = %s AND mot_de_passe = %s",
        (email, mot_de_passe)
    )
    result = cur.fetchone()

    if result:
        id_employe, nom, prenom = result
        return jsonify({
            "status": "success",
            "message": "Connexion réussie",
            "id": id_employe,
            "nom": nom,
            "prenom": prenom
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Email ou mot de passe incorrect"
        }), 401

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
            SELECT organisme, periode, niveau_etude, diplome
            FROM formation_base
            WHERE id_employe = %s
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        formations = []
        for row in rows:
            formations.append({
                'organisme': row[0],
                'periode': row[1],
                'niveau_etude': row[2],
                'diplome': row[3]
            })

        return jsonify(formations)
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
        cur.execute("""
            SELECT designation, date_debut, date_fin, nombre_jours
            FROM absence
            WHERE id_employe = %s
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        absences = []
        for row in rows:
            absences.append({
                'designation': row[0],
                'date_debut': row[1].strftime('%Y-%m-%d'),
                'date_fin': row[2].strftime('%Y-%m-%d'),
                'nombre_jours': row[3]
            })

        return jsonify(absences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/formations_complementaires/<int:id_employe>', methods=['GET'])
def get_formations_complementaires(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT intitule, date_debut, date_fin, lieu
            FROM formation_complementaire
            WHERE id_employe = %s
            ORDER BY date_debut DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        formations = []
        for row in rows:
            formations.append({
                'intitule': row[0],
                'date_debut': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'date_fin': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'lieu': row[3]
            })

        return jsonify(formations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anciennete/<int:id_employe>', methods=['GET'])
def get_anciennete(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT fonction, echelle, echelon, date_effet, structure, classification
            FROM anciennete_sonatrach
            WHERE id_employe = %s
            ORDER BY date_effet DESC
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        anciennetes = []
        for row in rows:
            anciennetes.append({
                'fonction': row[0],
                'echelle': row[1],
                'echelon': row[2],
                'date_effet': row[3].strftime('%Y-%m-%d') if row[3] else '',
                'structure': row[4],
                'classification': row[5],
            })

        return jsonify(anciennetes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/infos_generales/<int:id_employe>', methods=['GET'])
def get_infos_generales(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                e.nom, e.prenom, e.date_naissance, e.lieu_naissance, e.sexe, e.email,
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
                "date_naissance": row[2].strftime('%Y-%m-%d') if row[2] else '',
                "lieu_naissance": row[3],
                "sexe": row[4],
                "email": row[5],
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
            SELECT nom_realisation, date_debut, lieu
            FROM realisation
            WHERE id_employe = %s
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        realisations = []
        for row in rows:
            realisations.append({
                'nom': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'lieu': row[2],
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
@app.route('/anciennete_sonatrach/<int:id_employe>', methods=['GET'])
def get_anciennete_sonatrach(id_employe):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT fonction, echelle, echelon, date_effet, structure, classification
            FROM anciennete_sonatrach
            WHERE id_employe = %s
        """, (id_employe,))
        rows = cur.fetchall()
        cur.close()

        anciennetes = []
        for row in rows:
            anciennetes.append({
                'fonction': row[0],
                'echelle': row[1],
                'echelon': row[2],
                'date_effet': row[3].strftime('%Y-%m-%d') if row[3] else '',
                'structure': row[4],
                'classification': row[5],
            })

        return jsonify(anciennetes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)