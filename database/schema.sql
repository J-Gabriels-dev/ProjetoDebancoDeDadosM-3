CREATE DATABASE IF NOT EXISTS sistema_licenca_capacitacao
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE sistema_licenca_capacitacao;

DROP TABLE IF EXISTS PARCELA;
DROP TABLE IF EXISTS LICENCA;
DROP TABLE IF EXISTS TRAMITACAO;
DROP TABLE IF EXISTS ACAO_CAPACITACAO;
DROP TABLE IF EXISTS SOLICITACAO;
DROP TABLE IF EXISTS AFASTAMENTO_VIGENTE;
DROP TABLE IF EXISTS SERVIDOR;

CREATE TABLE SERVIDOR (
  id_servidor INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  siape VARCHAR(20) NOT NULL,
  data_posse DATE NOT NULL,
  lotacao VARCHAR(255) NOT NULL,
  status_funcional VARCHAR(20) NOT NULL,
  PRIMARY KEY (id_servidor),
  UNIQUE (siape),
  CONSTRAINT chk_servidor_status CHECK (status_funcional IN ('ativo','aposentado','exonerado','disponibilidade'))
);

CREATE TABLE AFASTAMENTO_VIGENTE (
  id_afastamento INT NOT NULL AUTO_INCREMENT,
  id_servidor INT NOT NULL,
  tipo VARCHAR(30) NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  PRIMARY KEY (id_afastamento),
  FOREIGN KEY (id_servidor) REFERENCES SERVIDOR(id_servidor),
  CONSTRAINT chk_afastamento_tipo CHECK (tipo IN ('licenca_medica','licenca_maternidade','afastamento_acidente','atestado','licenca_capacitacao')),
  CONSTRAINT chk_afastamento_status CHECK (status IN ('ativo','encerrado','cancelado')),
  CONSTRAINT chk_afastamento_datas CHECK (data_fim > data_inicio)
);

CREATE TABLE SOLICITACAO (
  id_solicitacao INT NOT NULL AUTO_INCREMENT,
  id_servidor INT NOT NULL,
  data_solicitacao DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  justificativa TEXT NOT NULL,
  qtd_parcelas INT NOT NULL,
  PRIMARY KEY (id_solicitacao),
  FOREIGN KEY (id_servidor) REFERENCES SERVIDOR(id_servidor),
  CONSTRAINT chk_solicitacao_status CHECK (status IN ('pendente','aprovada','concluida','cancelada')),
  CONSTRAINT chk_solicitacao_parcelas CHECK (qtd_parcelas BETWEEN 1 AND 6)
);

CREATE TABLE ACAO_CAPACITACAO (
  id_acao INT NOT NULL AUTO_INCREMENT,
  id_solicitacao INT NOT NULL,
  titulo VARCHAR(255) NOT NULL,
  instituicao VARCHAR(255) NOT NULL,
  modalidade VARCHAR(20) NOT NULL,
  carga_horaria_semanal INT NOT NULL,
  local VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_acao),
  UNIQUE (id_solicitacao),
  FOREIGN KEY (id_solicitacao) REFERENCES SOLICITACAO(id_solicitacao),
  CONSTRAINT chk_acao_modalidade CHECK (modalidade IN ('presencial','ead','hibrido')),
  CONSTRAINT chk_acao_carga CHECK (carga_horaria_semanal >= 30)
);

CREATE TABLE TRAMITACAO (
  id_tramitacao INT NOT NULL AUTO_INCREMENT,
  id_solicitacao INT NOT NULL,
  etapa VARCHAR(30) NOT NULL,
  responsavel VARCHAR(255) NOT NULL,
  decisao VARCHAR(20) NOT NULL,
  observacao TEXT,
  data_decisao DATE,
  PRIMARY KEY (id_tramitacao),
  FOREIGN KEY (id_solicitacao) REFERENCES SOLICITACAO(id_solicitacao),
  CONSTRAINT chk_tramitacao_etapa CHECK (etapa IN ('chefia_imediata','gestao_de_pessoas','autoridade_maxima')),
  CONSTRAINT chk_tramitacao_decisao CHECK (decisao IN ('pendente','aprovado','negado'))
);

CREATE TABLE LICENCA (
  id_licenca INT NOT NULL AUTO_INCREMENT,
  id_solicitacao INT NOT NULL,
  data_concessao DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  total_dias_aprovados INT NOT NULL,
  PRIMARY KEY (id_licenca),
  UNIQUE (id_solicitacao),
  FOREIGN KEY (id_solicitacao) REFERENCES SOLICITACAO(id_solicitacao),
  CONSTRAINT chk_licenca_status CHECK (status IN ('ativa','concluida','cancelada','interrompida')),
  CONSTRAINT chk_licenca_dias CHECK (total_dias_aprovados BETWEEN 1 AND 90)
);

CREATE TABLE PARCELA (
  id_parcela INT NOT NULL AUTO_INCREMENT,
  id_licenca INT NOT NULL,
  numero_parcela INT NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  PRIMARY KEY (id_parcela),
  FOREIGN KEY (id_licenca) REFERENCES LICENCA(id_licenca),
  CONSTRAINT chk_parcela_numero CHECK (numero_parcela BETWEEN 1 AND 6),
  CONSTRAINT chk_parcela_status CHECK (status IN ('agendada','em_andamento','concluida','cancelada')),
  CONSTRAINT chk_parcela_datas CHECK (data_fim > data_inicio),
  CONSTRAINT chk_parcela_minimo CHECK (data_fim >= DATE_ADD(data_inicio, INTERVAL 15 DAY))
);
