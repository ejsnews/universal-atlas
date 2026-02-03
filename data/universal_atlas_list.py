import mysql.connector
import os
import zipfile

def export_for_google_index():
    # En-tête reflétant vos 10 ans de travail
    header_text = (
        "================================================================================\n"
        "UNIVERSAL ATLAS OF GEOMETRIC CONSTANTS - Index Fragment\n"
        "--------------------------------------------------------------------------------\n"
        "AUTHOR: Eric Jacob Simon (ejsnews) - Independent Researcher\n"
        "RESEARCH BACKGROUND: 10 years of fundamental research.\n"
        "  - 4 years: Prime Number Theory & Infinite Sequences (Forest Structures).\n"
        "  - 6 years: Linear Recurrences & Geometric Constants Algorithm.\n"
        "--------------------------------------------------------------------------------\n"
        "PURPOSE: Search index for reverse engineering.\n"
        "VALUES: 50 digits (original 100 digits).\n"
        "FULL SYMBOLIC DATA: Private server access only.\n"
        "CONTACT: https://github.com/ejsnews\n"
        "================================================================================\n\n"
    )
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="", database="universalatlas", port="3306")
        cursor = db.cursor()
    except Exception as e:
        print(f"Erreur connexion : {e}")
        return
    query = "SELECT LEFT(constanteFloat, 50), CTEname FROM geometricconstants ORDER BY constanteFloat ASC"
    cursor.execute(query)
    # Paramètres de fragmentation
    lines_per_file = 6000  # Environ 500 Ko par fichier
    file_count = 1
    current_line_count = 0
    # Création du dossier de sortie
    output_dir = "C:\\THEORIES\\github ejsnews\\data\\universal_atlas_index"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    f = open(f"{output_dir}/atlas_index_{file_count:03d}.txt", "w", encoding="utf-8")
    f.write(header_text)
    print("Extraction en cours...")
    for (val_float, name) in cursor:
        # Écriture de la ligne (Format optimisé pour Google)
        f.write(f"{name:29} : {val_float}\n")
        current_line_count += 1
        # Si on atteint la limite du fichier, on en ouvre un nouveau
        if current_line_count >= lines_per_file:
            f.close()
            print(f"Fichier {file_count} créé.")
            file_count += 1
            current_line_count = 0
            f = open(f"{output_dir}/atlas_index_{file_count:03d}.txt", "w", encoding="utf-8")
            f.write(header_text)
    f.close()
    cursor.close()
    db.close()

    # Création du fichier ZIP global
    zip_name = f"{output_dir}\\FULL_ATLAS_INDEX_50_DIGITS_03_02_2026.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as atlas_zip:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                atlas_zip.write(os.path.join(root, file), file)

    print(f"Terminé ! {file_count} fichiers créés dans le dossier '{output_dir}'.")

if __name__ == "__main__":
    export_for_google_index()

