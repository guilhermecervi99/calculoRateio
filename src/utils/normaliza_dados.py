import pandas as pd

def parse_date(x):
    x = str(x).strip()
    x = x.replace('/', '-')


    if len(x) >= 10:
        # Se os 4 primeiros caracteres forem dígitos, assume formato YYYY-MM-DD
        if x[:4].isdigit():
            return pd.to_datetime(x, format='%Y-%m-%d', errors='coerce')
        else:
            # Caso contrário, assume formato DD-MM-YYYY
            return pd.to_datetime(x, format='%d-%m-%Y', errors='coerce')
    else:
        return pd.NaT

def normalizar_dados(df: pd.DataFrame, metadados: dict) -> pd.DataFrame:
    """
    Aplica tipagem de acordo com os metadados, normalizando também os formatos de data.
    """
    for col in metadados.get("colunas_int", []):
        df[col] = df[col].astype("Int64")

    for col in metadados.get("colunas_float", []):
        df[col] = df[col].astype(float)

    for col in metadados.get("colunas_data", []):
        df[col] = df[col].apply(parse_date)

    df.drop_duplicates(inplace=True)
    return df
