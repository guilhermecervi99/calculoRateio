import pandas as pd

def processar_etapa1(df_lancamentos: pd.DataFrame, df_met2: pd.DataFrame) -> pd.DataFrame:
    """
    Processa o rateio para os centros 100 e 204 utilizando os canais canalA e canalB.
    """
    # Filtra as métricas para os canais canalA e canalB
    df_met2_e1 = df_met2[df_met2['ds_canal_aquisicao'].isin(['canalA', 'canalB'])].copy()

    # Agrupa as métricas por ano_mes, ds_canal_aquisicao e ds_segmento
    df_met2_e1_grouped = (
        df_met2_e1
        .groupby(['ano_mes', 'ds_canal_aquisicao', 'ds_segmento'], as_index=False)['total']
        .sum()
        .rename(columns={'total': 'total_parcial'})
    )

    # Calcula o total das métricas por mês
    df_met2_e1_total = (
        df_met2_e1
        .groupby('ano_mes', as_index=False)['total']
        .sum()
        .rename(columns={'total': 'total_mes'})
    )

    # Junta os totais parciais com o total do mês
    df_metricas_merged = pd.merge(df_met2_e1_grouped, df_met2_e1_total, on='ano_mes', how='left')

    # Filtra os lançamentos para os centros 100 e 204
    df_e1 = df_lancamentos[df_lancamentos['id_centro_resultado'].isin([100, 204])].copy()

    # Junta os lançamentos com as métricas agregadas
    df_rateio = pd.merge(df_e1, df_metricas_merged, on='ano_mes', how='left')

    # Calcula o valor rateado
    df_rateio['valor_rateado'] = df_rateio['valor'] * (df_rateio['total_parcial'] / df_rateio['total_mes'])

    # Seleciona as colunas desejadas
    colunas = [
        'id_lancamento', 'id_centro_custo', 'id_centro_resultado',
        'dt_competencia', 'valor', 'ds_canal_aquisicao', 'ds_segmento',
        'ano_mes', 'valor_rateado'
    ]
    return df_rateio[colunas]
