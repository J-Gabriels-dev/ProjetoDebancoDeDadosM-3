# Sistema de Gestão de Licença Capacitação

Sistema web para controle e gerenciamento de solicitações de **Licença Capacitação** de servidores públicos federais, desenvolvido como projeto acadêmico do Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas — **IFPI Campus Angical**.

O projeto automatiza um processo hoje realizado manualmente por planilhas eletrônicas, cobrindo desde a solicitação do servidor até a tramitação, aprovação e controle de parcelas da licença concedida.

## 📋 Base legal

- **Lei nº 8.112/1990** — Regime Jurídico dos Servidores Públicos Civis da União
- **Decreto nº 9.991/2019** — Política Nacional de Desenvolvimento de Pessoas
- **Instrução Normativa SGP-ENAP/SEDGG/ME nº 21/2021**

## ✨ Funcionalidades

- Cadastro, consulta, atualização e exclusão de servidores
- Registro de afastamentos vigentes (com verificação de conflito de datas)
- Abertura de solicitações de Licença Capacitação, vinculadas a uma ação de capacitação
- Fluxo de tramitação com três etapas obrigatórias de aprovação (chefia imediata, gestão de pessoas e autoridade máxima)
- Concessão de licença e controle de parcelas, com cálculo dinâmico do saldo de dias
- Dashboard com indicadores gerais (total de servidores, solicitações, licenças, parcelas e pendências)

> ⚠️ Nesta versão, o sistema contempla apenas o afastamento do tipo **Licença Capacitação** (Art. 18, inciso I, Decreto nº 9.991/2019). Os demais tipos previstos no mesmo artigo (Participação em Treinamento, Pós-graduação *stricto sensu* e Estudo no Exterior) não foram implementados — ver seção de Limitações no relatório técnico.

## 🧱 Arquitetura

O sistema segue uma arquitetura em três camadas, com responsabilidades bem delimitadas:

| Camada | Responsabilidade |
|---|---|
| **Interface** | Streamlit — telas de cadastro, consulta e dashboard |
| **Backend** | Regras de negócio complexas (validação de quinquênio, conflito de datas, interstício entre parcelas, limite de afastamentos simultâneos) |
| **Banco de Dados** | Restrições estruturais simples (integridade referencial, unicidade, validações de domínio via `CHECK`) |

O saldo de dias de capacitação **nunca é armazenado como campo estático** — é sempre calculado dinamicamente a partir da soma das parcelas concluídas (`SUM(DATEDIFF(data_fim, data_inicio))`).

## 🗄️ Modelagem de dados

O banco relacional é composto por **7 entidades principais**:

`SERVIDOR` · `AFASTAMENTO_VIGENTE` · `SOLICITACAO` · `ACAO_CAPACITACAO` · `TRAMITACAO` · `LICENCA` · `PARCELA`

Principais regras de negócio incorporadas como constraints no banco:

- Máximo de **6 parcelas** por licença (Decreto 9.991/2019, Art. 25 §3º)
- Mínimo de **15 dias** por parcela
- Máximo de **90 dias** totais por licença (Lei 8.112/1990, Art. 87)
- Mínimo de **30h semanais** de carga horária na ação de capacitação (Decreto 9.991/2019, Art. 26)
- Exatamente **3 etapas** obrigatórias de tramitação por solicitação (IN 21/2021, Art. 33)

O script de criação das tabelas está disponível em [`modelo_logico_corrigido.sql`](./modelo_logico_corrigido.sql), com 8 chaves estrangeiras e 13 `CHECK constraints`, testado em MySQL/MariaDB.

## 🛠️ Tecnologias

| Categoria | Ferramenta |
|---|---|
| Linguagem | Python |
| Interface | Streamlit |
| Banco de dados | MySQL |
| IDE | Visual Studio Code |
| Controle de versão | Git / GitHub |
| Modelagem | draw.io |
| Documentação | LaTeX (abnTeX2) / Microsoft Word |
| Coleta de requisitos | Google Forms |

## 🚀 Como executar

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd <nome-do-repositorio>

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar o banco de dados
mysql -u root -p < modelo_logico_corrigido.sql

# 4. Configurar a conexão com o banco
# (ajustar host, usuário, senha e nome do banco no arquivo de configuração da aplicação)

# 5. Rodar a aplicação
streamlit run app.py
```

A aplicação ficará disponível em `http://localhost:8501`.

## 👥 Equipe

- João Gabriel Paulino — Modelagem de Banco de Dados
- João Gabriel Pereira
- Alex Pablo
- Carlos Eduardo

**Orientador:** Prof. Me. José Soares da Silva Neto

## 📄 Documentação

O relatório técnico completo (introdução, tecnologias, modelagem, diagramas ER e de classes, testes e considerações finais) está disponível na pasta `docs/` do projeto.

---

*Instituto Federal de Educação, Ciência e Tecnologia do Piauí — Campus Angical*
*Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas — 2026*
