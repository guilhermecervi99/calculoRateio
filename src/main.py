import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.utils.carrega_config import carregar_config
from src.utils.db import salvar_no_postgresql
from src.utils.normaliza_dados import normalizar_dados
from src.rateio.etapa1 import processar_etapa1
from src.rateio.etapa2 import processar_etapa2
from src.rateio.sem_rateio import filtrar_nao_rateados


def main():
    config = carregar_config("config/config.yml")
    raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    caminho_lancamentos = os.path.join(raiz_projeto, config["paths"]["lancamentos"])
    caminho_metricas = os.path.join(raiz_projeto, config["paths"]["metricas"])

    df_lancamentos = pd.read_json(caminho_lancamentos, orient='index')
    df_metricas = pd.read_json(caminho_metricas, orient='index')

    df_lancamentos = normalizar_dados(df_lancamentos, config["lancamentos"])
    df_metricas = normalizar_dados(df_metricas, config["metricas"])

    df_lancamentos['dt_competencia'] = pd.to_datetime(
        df_lancamentos['dt_competencia'], errors='coerce', dayfirst=True
    ).values.astype('datetime64[us]')

    df_lancamentos['ano_mes'] = df_lancamentos['dt_competencia'].astype('datetime64[ns]').dt.strftime('%Y-%m')

    df_lancamentos = df_lancamentos[
        (df_lancamentos['ano_mes'] == '2024-10') | (df_lancamentos['ano_mes'] == '2024-11')
    ].copy()

    df_metricas['dt_referencia'] = pd.to_datetime(
        df_metricas['dt_referencia'], errors='coerce'
    )
    df_metricas['ano_mes'] = df_metricas['dt_referencia'].dt.strftime('%Y-%m')

    df_metricas_filtradas = df_metricas[df_metricas['ds_metrica'] == 'metrica_2'].copy()
    df_metricas_filtradas = df_metricas_filtradas[
        (df_metricas_filtradas['ano_mes'] == '2024-10') | (df_metricas_filtradas['ano_mes'] == '2024-11')
    ].copy()

    df_rateio_etapa1 = processar_etapa1(df_lancamentos, df_metricas_filtradas)
    df_rateio_etapa2 = processar_etapa2(df_lancamentos, df_metricas_filtradas)

    df_nao_rateados = filtrar_nao_rateados(df_lancamentos)

    caminho_saida = os.path.join(raiz_projeto, "dados", "delivery")

    if not os.path.exists(caminho_saida):
        os.makedirs(caminho_saida)

    df_rateio_etapa1.to_parquet(os.path.join(caminho_saida, "rateio_etapa1.parquet"), index=False)
    df_rateio_etapa2.to_parquet(os.path.join(caminho_saida, "rateio_etapa2.parquet"), index=False)
    df_nao_rateados.to_parquet(os.path.join(caminho_saida, "nao_rateados.parquet"), index=False)

    salvar_no_postgresql(df_rateio_etapa1, "TbRateioEtapa1")
    salvar_no_postgresql(df_rateio_etapa2, "TbRateioEtapa2")
    salvar_no_postgresql(df_nao_rateados, "TbSemRateio")

if __name__ == "__main__":
    main()
