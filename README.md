# Sistema de Controle de Licenca Capacitacao

Sistema web desenvolvido em Python, Streamlit, SQLAlchemy e PyMySQL, usando o mesmo banco MySQL e os mesmos models do projeto original.

## Como executar

1. Abra a pasta `Sistema-Licenca`.
2. Crie e ative um ambiente virtual.
3. Instale as dependencias:

```bash
pip install -r requirements.txt
```

O pacote `cryptography` e necessario para conexoes MySQL com usuarios que usam `sha256_password` ou `caching_sha2_password`.

4. No MySQL, execute os scripts do banco caso ainda nao tenha criado a base:

```sql
SOURCE database/schema.sql;
SOURCE database/inserts.sql;
```

5. Se necessario, ajuste a conexao no arquivo `config.py` ou use a variavel `DATABASE_URL`.

Exemplo no Windows:

```bash
set DATABASE_URL=mysql+pymysql://root:senha@localhost/sistema_licenca_capacitacao
```

6. Inicie o sistema:

```bash
streamlit run app.py
```

O Streamlit exibira a URL local no terminal.

## Paginas

- Dashboard
- Servidores
- Afastamentos Vigentes
- Solicitacoes
- Acoes de Capacitacao
- Tramitacoes
- Licencas
- Parcelas

## Regras preservadas

- Quinquênio: somente servidor ativo com 5 anos completos desde `data_posse` pode criar solicitacao.
- Tramitacao: as etapas seguem a ordem `chefia_imediata`, `gestao_de_pessoas`, `autoridade_maxima`.
- Negativa em qualquer etapa cancela a solicitacao.
- Aprovacao das tres etapas cria automaticamente um registro em `LICENCA`.
- Parcela valida conflito com afastamento vigente e com outra parcela do mesmo servidor.
- Parcela valida intervalo minimo de 60 dias entre parcelas.
- Parcela valida limite de 5% de servidores afastados simultaneamente.
- Licenca valida maximo de 90 dias.
- Saldo de dias e calculado dinamicamente pelas parcelas concluidas.

## Observacao sobre o banco

A migracao troca apenas a interface Flask/Jinja2 por Streamlit. A estrutura das tabelas MySQL, os models e as regras de negocio foram preservados.
