import os
import yaml

def carregar_config(caminho: str) -> dict:
    """
    Função que carrega e retorna informações de um arquivo yaml em uma variável
    """
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(diretorio_atual, '..', '..', caminho)

    with open(caminho_completo, 'r') as f:
        config = yaml.safe_load(f)
    return config
