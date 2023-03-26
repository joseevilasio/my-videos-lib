import pytest
from sqlalchemy import create_engine

from api.app import create_app


@pytest.fixture(scope="module")
def app():
    """Instace of Main flask app"""
    return create_app()


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False)

    # Define o comando SQL para criar a tabela
    create_table_sql = """\
        CREATE TABLE if not exists video (
            id integer PRIMARY KEY AUTOINCREMENT,
            title varchar UNIQUE NOT NULL,
            description varchar NOT NULL,
            url varchar NOT NULL
        );
        """

    # Executa o comando SQL para criar a tabela
    with engine.connect() as conn:
        conn.exec_driver_sql(create_table_sql)

    # Retorna o engine para utilização nos testes
    yield engine

    # Fecha a conexão com o engine e limpa o
    # banco de dados de teste após os testes
    with engine.connect() as conn:
        conn.exec_driver_sql("DROP TABLE video")
