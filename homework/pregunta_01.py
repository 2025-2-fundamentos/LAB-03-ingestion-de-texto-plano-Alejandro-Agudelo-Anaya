import pandas as pd
import re

def pregunta_01():
    file_path = "files/input/clusters_report.txt"

    clusters = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data = lines[4:]

    registros = []
    actual = None

    for linea in data:
        m = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+\s%)\s+(.*)", linea)

        if m:
            if actual:
                texto = " ".join(actual["principales_palabras_clave"])
                texto = re.sub(r"\s+", " ", texto).strip()
                texto = texto.rstrip(",").rstrip(".")
                actual["principales_palabras_clave"] = texto
                registros.append(actual)

            actual = {
                "cluster": int(m.group(1)),
                "cantidad_de_palabras_clave": int(m.group(2)),
                "porcentaje_de_palabras_clave": float(
                    m.group(3).replace("%", "").replace(",", ".").strip()
                ),
                "principales_palabras_clave": [m.group(4)],
            }

        else:
            if actual:
                linea2 = linea.strip()
                if linea2:
                    actual["principales_palabras_clave"].append(linea2)

    if actual:
        texto = " ".join(actual["principales_palabras_clave"])
        texto = re.sub(r"\s+", " ", texto).strip()
        texto = texto.rstrip(",").rstrip(".")
        actual["principales_palabras_clave"] = texto
        registros.append(actual)

    df = pd.DataFrame(registros)

    df.columns = (
        df.columns.str.lower()
        .str.replace(" ", "_")
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    return df
