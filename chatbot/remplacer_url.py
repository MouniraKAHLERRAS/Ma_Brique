import os
import re

# 📁 Chemin vers le dossier lib de ton projet Flutter
project_dir = r"C:\Users\WINDOWS 10\Desktop\Ma_Brique\try_1 - Copie (3)\lib"



# 🧠 Les modèles à remplacer : remplace toutes les IP locales ou localhost
urls = [
    r"Uri\.parse\('http://10\.0\.2\.2:5000(.*?)'\)",
    r"Uri\.parse\('http://127\.0\.0\.1:5000(.*?)'\)",
    r"Uri\.parse\('http://192\.168\.\d+\.\d+:5000(.*?)'\)",
]

# 🔁 Balaye tous les fichiers .dart et remplace les URL par getUri(...)
for root, _, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".dart"):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            original = content
            for pattern in urls:
                content = re.sub(pattern, r"getUri('\1')", content)
            if content != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✔️ Modifié : {path}")

print("✅ Remplacement terminé dans tous les fichiers .dart.")
