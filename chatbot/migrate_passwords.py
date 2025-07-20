import psycopg2
import bcrypt

conn = psycopg2.connect(
    host="localhost",
    database="Ma_Bdd_sql",
    user="postgres",
    password="admin"
)
cur = conn.cursor()
cur.execute("SELECT id_employe, mot_de_passe FROM employe")
rows = cur.fetchall()

for id_employe, mot_de_passe in rows:
    # Si ce n'est PAS déjà hashé, on le hash
    if not mot_de_passe.startswith('$2'):
        hashed = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur.execute(
            "UPDATE employe SET mot_de_passe = %s WHERE id_employe = %s",
            (hashed, id_employe)
        )
        print(f"Employé {id_employe} : hashé !")
    else:
        print(f"Employé {id_employe} : déjà hashé")

conn.commit()
cur.close()
conn.close()
print("Migration terminée.")
