from sqlalchemy import create_engine
import os

def criar_conexao():
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError("Uma ou mais variáveis de ambiente do banco de dados não foram definidas corretamente.")

    url_conexao = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(url_conexao)


def salvar_no_postgresql(df, nome_tabela):
    conexao = criar_conexao()

    df.to_sql(nome_tabela, conexao, if_exists="replace", index=False)
