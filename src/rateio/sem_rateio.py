import pandas as pd

def filtrar_nao_rateados(df_lancamentos: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna os lançamentos que não pertencem aos centros de rateio (100, 204, 268, 288).
    """

    return df_lancamentos[~df_lancamentos['id_centro_resultado'].isin([100, 204, 268, 288])].copy()
