import pandas as pd

def processar_etapa2(df_lancamentos: pd.DataFrame, df_met2: pd.DataFrame) -> pd.DataFrame:
    """
    Processa o rateio para os centros 268 e 288 utilizando somente o segmento.
    """

    df_met2_grouped = (
        df_met2
        .groupby(['ano_mes', 'ds_segmento'], as_index=False)['total']
        .sum()
        .rename(columns={'total': 'total_segmento'})
    )

    df_total = (
        df_met2_grouped
        .groupby('ano_mes', as_index=False)['total_segmento']
        .sum()
        .rename(columns={'total_segmento': 'total_mes'})
    )

    df_metricas_merged = pd.merge(df_met2_grouped, df_total, on='ano_mes', how='left')

    df_e2 = df_lancamentos[df_lancamentos['id_centro_resultado'].isin([268, 288])].copy()

    df_rateio = pd.merge(df_e2, df_metricas_merged, on='ano_mes', how='left')

    df_rateio['valor_rateado'] = df_rateio['valor'] * (df_rateio['total_segmento'] / df_rateio['total_mes'])

    colunas = [
        'id_lancamento', 'id_centro_custo', 'id_centro_resultado',
        'dt_competencia', 'valor', 'ds_segmento', 'ano_mes', 'valor_rateado'
    ]
    return df_rateio[colunas]
