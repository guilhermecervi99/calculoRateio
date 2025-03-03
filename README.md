# Projeto de Rateio de Lançamentos 🚀

Este projeto tem como objetivo realizar o rateio de lançamentos financeiros com base em métricas SAAS, gerando arquivos .parquet e persistindo os resultados em um banco de dados PostgreSQL.

## 📚 Sumário

- [📖 Descrição Geral](#descricao-geral)
- [📁 Estrutura de Pastas](#estrutura-de-pastas)
- [🔧 Pré-Requisitos](#pre-requisitos)
- [⚙️ Configuração](#configuracao)
- [🏃‍♂️ Execução sem Docker](#execucao-sem-docker)
- [🐳 Execução com Docker](#execucao-com-docker)
- [⚙️ Funcionamento da Aplicação](#funcionamento-da-aplicacao)
- [👤 Autor](#autor)

## <a id="descricao-geral"></a>📖 Descrição Geral

A aplicação realiza as seguintes tarefas:
- **Leitura de dados:** Carrega os arquivos `lancamentos.json` e `metricas.json` (localizados em `dados/raw`).
- **Normalização:** Converte os dados conforme as configurações definidas em `config/config.yml`.
- **Rateio em duas etapas:**
  - **Etapa 1:** Para os centros **100** e **204**, utilizando os canais `canalA` e `canalB`.
  - **Etapa 2:** Para os centros **268** e **288**, utilizando o campo `ds_segmento`.
- **Saída:**
  - Geração de arquivos `.parquet` em `dados/delivery`:
    - `rateio_etapa1.parquet`
    - `rateio_etapa2.parquet`
    - `nao_rateados.parquet`
  - Persistência dos resultados em tabelas no **PostgreSQL**.

## <a id="estrutura-de-pastas"></a>📁 Estrutura de Pastas

<pre>
pythonProject/
├── config/
│   └── config.yml          # Configurações do projeto (colunas, caminhos, etc.)
│
├── dados/
│   ├── raw/                # Dados brutos de entrada
│   │   ├── lancamentos.json
│   │   └── metricas.json
│   └── delivery/           # Arquivos .parquet gerados pela aplicação
│       ├── nao_rateados.parquet
│       ├── rateio_etapa1.parquet
│       └── rateio_etapa2.parquet
│
├── src/
│   ├── main.py             # Script principal para execução da aplicação
│   ├── rateio/
│   │   ├── etapa1.py
│   │   ├── etapa2.py
│   │   └── sem_rateio.py
│   └── utils/
│       ├── carrega_config.py
│       ├── db.py
│       └── normaliza_dados.py
│
├── docker-compose.yml      # Configuração dos serviços Docker
├── Dockerfile              # Definição da imagem Docker
├── requirements.txt        # Dependências Python
└── README.md               # Documentação do projeto
</pre>

## <a id="pre-requisitos"></a>🔧 Pré-Requisitos

### Para execução sem Docker
- **Python 3.12** 🐍
- **pip** para instalar as dependências
- **PostgreSQL** instalado e rodando na máquina ou em um servidor acessível.  
  **O banco de dados e o usuário precisam ser criados** no PostgreSQL. Se o banco não foi criado automaticamente (via Docker), você pode criar o banco de dados e o usuário com os seguintes comandos SQL no PostgreSQL:

  ```sql
  CREATE USER exemplo_user WITH PASSWORD 'exemplo_pass';
  CREATE DATABASE lancamentos;
  GRANT ALL PRIVILEGES ON DATABASE lancamentos TO exemplo_user;
  ```
  
### Docker (Para execução com contêiner)
- **Docker** instalado 🐳

## <a id="configuracao"></a>⚙️ Configuração

1. **Arquivo .env**  
   O arquivo `.env` já está presente na raiz do projeto com as configurações padrão, mas você pode alterá-lo conforme necessário. Exemplo de conteúdo:
   ```
   POSTGRES_USER=exemplo_user
   POSTGRES_PASSWORD=exemplo_pass
   POSTGRES_DB=lancamentos
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   ```
   > **Observação:**  
   > - Para execução sem Docker, verifique se o PostgreSQL está configurado corretamente e ajuste `POSTGRES_HOST` para `localhost` ou para o IP do servidor onde o PostgreSQL está instalado.

2. **Banco de Dados**  
   - **Sem Docker:** Certifique-se de que o banco de dados (por exemplo, `lancamentos`) esteja criado no PostgreSQL instalado localmente.
   - **Com Docker:** O contêiner do PostgreSQL será iniciado automaticamente com as configurações definidas.

3. **Arquivo de Configuração (config/config.yml)**  
   Define:
   - Caminhos dos arquivos de dados (`paths.lancamentos` e `paths.metricas`).
   - Informações para normalização (colunas de int, float, data) para `lancamentos` e `metricas`.

## <a id="execucao-sem-docker"></a>🏃‍♂️ Execução sem Docker

1. **Crie um ambiente virtual** (caso não tenha um ambiente isolado já criado):

   ```bash
   python3 -m venv .venv
   ```

   Isso criará um ambiente virtual na pasta `.venv` do seu projeto.

2. **Ative o ambiente virtual:**
   - **No Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **No macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

3. **Instale as dependências** dentro do ambiente virtual:

   ```bash
   pip install -r requirements.txt
   ```

4. **Verifique o PostgreSQL**  
   Assegure-se de que o PostgreSQL esteja rodando em sua máquina ou servidor. Ajuste o arquivo `.env` se necessário (por exemplo, `POSTGRES_HOST=localhost`).

5. **Execute o script principal**:

   ```bash
   python src/main.py
   ```

6. **Verifique os resultados**:
   - Os arquivos `.parquet` serão gerados na pasta `dados/delivery`.
   - As tabelas `TbRateioEtapa1`, `TbRateioEtapa2` e `TbSemRateio` serão criadas no banco de dados PostgreSQL.

## <a id="execucao-com-docker"></a>🐳 Execução com Docker

1. **Configure o arquivo `.env`**  
   O arquivo `.env` já está presente, mas você pode alterá-lo conforme necessário.

2. **Suba os contêineres com Docker Compose**:
   ```bash
   docker-compose up --build
   ```
   - O serviço **postgres** será iniciado e configurado automaticamente.
   - O serviço **app** executará o `main.py`, realizando o rateio automaticamente.

3. **Acompanhe os logs** no terminal para verificar a execução.

4. **Para parar a aplicação**:
   - Pressione `Ctrl + C` no terminal ou execute:
     ```bash
     docker-compose down
     ```

5. **Arquivos gerados**:
   - Os arquivos `.parquet` estarão disponíveis no contêiner em `/app/dados/delivery` (verifique o mapeamento de volumes para acessá-los no host).
   - As tabelas no PostgreSQL serão criadas no contêiner do banco de dados.

## <a id="funcionamento-da-aplicacao"></a>⚙️ Funcionamento da Aplicação

1. **Leitura de Dados**  
   - O script `main.py` lê os arquivos `lancamentos.json` e `metricas.json` da pasta `dados/raw/` 📥.

2. **Normalização**  
   - A função `normalizar_dados` (em `src/utils/normaliza_dados.py`) ajusta os tipos das colunas (int, float, data) conforme definido em `config/config.yml` 🔄.

3. **Filtragem por Período**  
   - Filtra os dados para os meses de outubro e novembro de 2024 (2024-10 e 2024-11).

4. **Rateio**  
   - **Etapa 1:**
     - Filtra lançamentos para os centros **100** e **204**.
     - Rateia valores considerando os canais `canalA` e `canalB` e `ds_segmento`.
   - **Etapa 2:**
     - Filtra lançamentos para os centros **268** e **288**.
     - Rateia valores com base no `ds_segmento`.
   - **Lançamentos Não Rateados:**
     - Retorna os lançamentos que não se enquadram nas regras de rateio.

5. **Saída**  
   - **Arquivos Parquet:** Salvos em `dados/delivery`:
     - `rateio_etapa1.parquet`
     - `rateio_etapa2.parquet`
     - `nao_rateados.parquet`
   - **Banco de Dados:**  
     - Os resultados são persistidos em tabelas no PostgreSQL: `TbRateioEtapa1`, `TbRateioEtapa2` e `TbSemRateio`.

## <a id="autor"></a>👤 Autor

- **Guilherme Cervi Schwingel**  
  Email: gcervi64@gmail.com

Qualquer dúvida ou sugestão, sinta-se à vontade para entrar em contato! 💬
