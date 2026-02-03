import os

source = 'universal_atlas_200_geometric_constants_large_0_to_90'
source = 'universal_atlas_200_geometric_constants_large_150_to_200'
source = 'universal_atlas_100_geometric_constants_large_200_to_500'
source = 'universal_atlas_50_geometric_constants_large_500_to_1000'
path = 'C:\\THEORIES\\github ejsnews\\data\\universal_atlas_index\\'


def create_files(input_filename):
    # Utilisation de 'latin-1' pour éviter les erreurs de décodage sur les octets 0xa0
    try:
        with open(input_filename, 'r', encoding='latin-1') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_filename} est introuvable.")
        return

    # Découpage par blocs de constantes (5 retours à la ligne selon votre fichier)
    blocks = content.split('\n\n\n\n\n')
    
    data_rows = []
    
    for block in blocks:
        # Nettoyage des lignes et suppression des espaces insécables
        lines = [l.strip().replace('\xa0', ' ') for l in block.split('\n') if l.strip()]
        
        # On ignore l'en-tête du fichier s'il est présent dans le bloc
        if len(lines) >= 5 and "CTEname" not in lines[0]:
            name = lines[0]
            
            # Formatage du flottant à 20 caractères
            try:
                val_float = lines[1]
                # On s'assure qu'il y a 20 caractères (padding avec des espaces ou troncature)
                f_str = val_float[:20].ljust(20)
            except:
                f_str = " " * 20
                
            brute = lines[2]
            latex = lines[3]
            fibo = lines[4]
            
            data_rows.append({
                'name': name,
                'fibo': fibo,
                'float': f_str,
                'brute': brute,
                'latex': latex
            })

    # --- GÉNÉRATION MARKDOWN ---
    md_header = "| CTEname | Fibovar | constantefloat | constanteSymbols | constanteLatex |\n"
    md_header += "| :--- | :--- | :--- | :--- | :--- |\n"
    md_lines = []
    for row in data_rows:
        # Format Markdown avec double dollar pour le rendu GitHub
        line = f"| {row['name']} | {row['fibo']} | {row['float']} | {row['brute']} | $${row['latex']}$$ |"
        md_lines.append(line)
    
    with open(f'{path}{source}.md', 'w', encoding='utf-8') as fmd:
        fmd.write(md_header + '\n'.join(md_lines))

    # --- GÉNÉRATION HTML ---
    html_rows = ""
    for r in data_rows:
        html_rows += f"""
        <tr>
            <td>{r['name']}</td>
            <td>{r['fibo']}</td>
            <td class="mono">{r['float']}</td>
            <td>\({r['latex']}\)</td>
        </tr>"""

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Constantes Géométriques</title>
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; }}
            table {{ border-collapse: collapse; width: 100%; border: 2px solid #444; }}
            th, td {{ border: 1px solid #888; padding: 10px; text-align: left; }}
            th {{ background-color: #f0f0f0; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .mono {{ font-family: 'Courier New', monospace; white-space: pre; }}
            h1 {{ color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>Échantillon de Constantes Géométriques</h1>
        <table>
            <tr><th>CTEname</th><th>Fibovar</th><th>constantefloat (20)</th><th>Formule</th></tr>
            {html_rows}
        </table>
    </body>
    </html>
    """
    
    with open(f'{path}{source}_2.html', 'w', encoding='utf-8') as fhtml:
        fhtml.write(html_template)

    print(f"Extraction terminée : {len(data_rows)} constantes trouvées.")
    print(f"Fichiers créés : '{path}{source}.md' et '{path}{source}_2.html'")


# Lancement
if __name__ == "__main__":
    # Remplacez par le nom exact de votre fichier sur votre ordinateur
    create_files(f"{path}{source}.txt")
