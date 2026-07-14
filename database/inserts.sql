USE sistema_licenca_capacitacao;

INSERT INTO SERVIDOR (nome, siape, data_posse, lotacao, status_funcional) VALUES
('Ana Paula Souza', '100001', '2010-01-10', 'Tecnologia da Informacao', 'ativo'),
('Bruno Costa Lima', '100002', '2011-03-15', 'Administracao', 'ativo'),
('Carla Mendes Rocha', '100003', '2012-05-20', 'Ensino', 'ativo'),
('Diego Araujo Silva', '100004', '2013-07-02', 'Pesquisa', 'ativo'),
('Elisa Nunes Prado', '100005', '2014-09-11', 'Extensao', 'ativo'),
('Fabio Henrique Reis', '100006', '2015-02-28', 'Biblioteca', 'ativo'),
('Gabriela Torres Alves', '100007', '2016-04-18', 'Registro Academico', 'ativo'),
('Henrique Lopes Martins', '100008', '2017-06-22', 'Compras', 'ativo'),
('Isabela Ferreira Gomes', '100009', '2018-08-30', 'Patrimonio', 'ativo'),
('Joao Victor Santos', '100010', '2019-10-05', 'Direcao Geral', 'ativo');

INSERT INTO AFASTAMENTO_VIGENTE (id_servidor, tipo, data_inicio, data_fim, status) VALUES
(1, 'licenca_medica', '2023-01-02', '2023-01-20', 'encerrado'),
(2, 'atestado', '2023-02-03', '2023-02-18', 'encerrado'),
(3, 'licenca_maternidade', '2023-03-01', '2023-06-29', 'encerrado'),
(4, 'afastamento_acidente', '2023-04-10', '2023-05-10', 'encerrado'),
(5, 'licenca_capacitacao', '2023-05-15', '2023-06-15', 'encerrado'),
(6, 'licenca_medica', '2023-06-20', '2023-07-08', 'encerrado'),
(7, 'atestado', '2023-07-10', '2023-07-26', 'encerrado'),
(8, 'licenca_capacitacao', '2023-08-01', '2023-08-31', 'encerrado'),
(9, 'licenca_medica', '2023-09-04', '2023-09-22', 'encerrado'),
(10, 'atestado', '2023-10-02', '2023-10-18', 'encerrado');

INSERT INTO SOLICITACAO (id_servidor, data_solicitacao, status, justificativa, qtd_parcelas) VALUES
(1, '2026-01-05', 'aprovada', 'Curso de aperfeicoamento em gestao publica.', 1),
(2, '2026-01-06', 'aprovada', 'Capacitacao em processos administrativos.', 1),
(3, '2026-01-07', 'aprovada', 'Atualizacao pedagogica para o setor de ensino.', 1),
(4, '2026-01-08', 'aprovada', 'Programa de pesquisa aplicada.', 1),
(5, '2026-01-09', 'aprovada', 'Formacao em extensao institucional.', 1),
(6, '2026-01-10', 'aprovada', 'Capacitacao em biblioteconomia digital.', 1),
(7, '2026-01-11', 'aprovada', 'Curso sobre registros academicos.', 1),
(8, '2026-01-12', 'aprovada', 'Capacitacao em compras publicas.', 1),
(9, '2026-01-13', 'aprovada', 'Curso de controle patrimonial.', 1),
(10, '2026-01-14', 'aprovada', 'Formacao em governanca institucional.', 1);

INSERT INTO ACAO_CAPACITACAO (id_solicitacao, titulo, instituicao, modalidade, carga_horaria_semanal, local) VALUES
(1, 'Gestao Publica Contemporanea', 'Escola Nacional de Administracao Publica', 'ead', 30, 'Ambiente virtual'),
(2, 'Processos Administrativos', 'Instituto Federal', 'hibrido', 32, 'Campus Sede'),
(3, 'Metodologias de Ensino', 'Universidade Federal', 'presencial', 35, 'Centro de Formacao'),
(4, 'Pesquisa Aplicada', 'Fundacao de Apoio', 'ead', 30, 'Ambiente virtual'),
(5, 'Extensao e Comunidade', 'Instituto Federal', 'presencial', 34, 'Campus Sede'),
(6, 'Bibliotecas Digitais', 'Universidade Aberta', 'ead', 30, 'Ambiente virtual'),
(7, 'Gestao Academica', 'Instituto Federal', 'hibrido', 36, 'Campus Sede'),
(8, 'Compras Governamentais', 'Escola de Governo', 'ead', 30, 'Ambiente virtual'),
(9, 'Patrimonio Publico', 'Escola de Governo', 'ead', 30, 'Ambiente virtual'),
(10, 'Governanca no Setor Publico', 'Escola Nacional de Administracao Publica', 'hibrido', 32, 'Brasilia');

INSERT INTO TRAMITACAO (id_solicitacao, etapa, responsavel, decisao, observacao, data_decisao) VALUES
(1, 'chefia_imediata', 'Chefia TI', 'aprovado', 'Compativel com o setor.', '2026-01-15'),
(1, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Requisitos legais atendidos.', '2026-01-16'),
(1, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(2, 'chefia_imediata', 'Chefia Administracao', 'aprovado', 'Compativel.', '2026-01-15'),
(2, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(2, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(3, 'chefia_imediata', 'Chefia Ensino', 'aprovado', 'Compativel.', '2026-01-15'),
(3, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(3, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(4, 'chefia_imediata', 'Chefia Pesquisa', 'aprovado', 'Compativel.', '2026-01-15'),
(4, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(4, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(5, 'chefia_imediata', 'Chefia Extensao', 'aprovado', 'Compativel.', '2026-01-15'),
(5, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(5, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(6, 'chefia_imediata', 'Chefia Biblioteca', 'aprovado', 'Compativel.', '2026-01-15'),
(6, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(6, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(7, 'chefia_imediata', 'Chefia Registro Academico', 'aprovado', 'Compativel.', '2026-01-15'),
(7, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(7, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(8, 'chefia_imediata', 'Chefia Compras', 'aprovado', 'Compativel.', '2026-01-15'),
(8, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(8, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(9, 'chefia_imediata', 'Chefia Patrimonio', 'aprovado', 'Compativel.', '2026-01-15'),
(9, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(9, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17'),
(10, 'chefia_imediata', 'Chefia Direcao', 'aprovado', 'Compativel.', '2026-01-15'),
(10, 'gestao_de_pessoas', 'Gestao de Pessoas', 'aprovado', 'Apto.', '2026-01-16'),
(10, 'autoridade_maxima', 'Diretor Geral', 'aprovado', 'Concedido.', '2026-01-17');

INSERT INTO LICENCA (id_solicitacao, data_concessao, status, total_dias_aprovados) VALUES
(1, '2026-01-17', 'ativa', 90),
(2, '2026-01-17', 'ativa', 90),
(3, '2026-01-17', 'ativa', 90),
(4, '2026-01-17', 'ativa', 90),
(5, '2026-01-17', 'ativa', 90),
(6, '2026-01-17', 'ativa', 90),
(7, '2026-01-17', 'ativa', 90),
(8, '2026-01-17', 'ativa', 90),
(9, '2026-01-17', 'ativa', 90),
(10, '2026-01-17', 'ativa', 90);

INSERT INTO PARCELA (id_licenca, numero_parcela, data_inicio, data_fim, status) VALUES
(1, 1, '2026-03-01', '2026-03-16', 'agendada'),
(2, 1, '2026-04-01', '2026-04-16', 'agendada'),
(3, 1, '2026-05-01', '2026-05-16', 'agendada'),
(4, 1, '2026-06-01', '2026-06-16', 'agendada'),
(5, 1, '2026-07-01', '2026-07-16', 'agendada'),
(6, 1, '2026-08-01', '2026-08-16', 'agendada'),
(7, 1, '2026-09-01', '2026-09-16', 'agendada'),
(8, 1, '2026-10-01', '2026-10-16', 'agendada'),
(9, 1, '2026-11-01', '2026-11-16', 'agendada'),
(10, 1, '2026-12-01', '2026-12-16', 'agendada');
