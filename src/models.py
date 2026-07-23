from datetime import date
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Servidor(db.Model):
    __tablename__ = "SERVIDOR"
    id_servidor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    siape = db.Column(db.String(20), nullable=False, unique=True)
    data_posse = db.Column(db.Date, nullable=False)
    lotacao = db.Column(db.String(255), nullable=False)
    status_funcional = db.Column(db.String(20), nullable=False)


class AfastamentoVigente(db.Model):
    __tablename__ = "AFASTAMENTO_VIGENTE"
    id_afastamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servidor = db.Column(db.Integer, db.ForeignKey("SERVIDOR.id_servidor"), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    servidor = db.relationship("Servidor", backref="afastamentos")


class Solicitacao(db.Model):
    __tablename__ = "SOLICITACAO"
    id_solicitacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servidor = db.Column(db.Integer, db.ForeignKey("SERVIDOR.id_servidor"), nullable=False)
    data_solicitacao = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    justificativa = db.Column(db.Text, nullable=False)
    qtd_parcelas = db.Column(db.Integer, nullable=False)
    servidor = db.relationship("Servidor", backref="solicitacoes")


class AcaoCapacitacao(db.Model):
    __tablename__ = "ACAO_CAPACITACAO"
    id_acao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_solicitacao = db.Column(db.Integer, db.ForeignKey("SOLICITACAO.id_solicitacao"), nullable=False, unique=True)
    titulo = db.Column(db.String(255), nullable=False)
    instituicao = db.Column(db.String(255), nullable=False)
    modalidade = db.Column(db.String(20), nullable=False)
    carga_horaria_semanal = db.Column(db.Integer, nullable=False)
    local = db.Column(db.String(255), nullable=False)
    solicitacao = db.relationship("Solicitacao", backref=db.backref("acao", uselist=False))


class Tramitacao(db.Model):
    __tablename__ = "TRAMITACAO"
    id_tramitacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_solicitacao = db.Column(db.Integer, db.ForeignKey("SOLICITACAO.id_solicitacao"), nullable=False)
    etapa = db.Column(db.String(30), nullable=False)
    responsavel = db.Column(db.String(255), nullable=False)
    decisao = db.Column(db.String(20), nullable=False, default="pendente")
    observacao = db.Column(db.Text)
    data_decisao = db.Column(db.Date)
    solicitacao = db.relationship("Solicitacao", backref="tramitacoes")


class Licenca(db.Model):
    __tablename__ = "LICENCA"
    id_licenca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_solicitacao = db.Column(db.Integer, db.ForeignKey("SOLICITACAO.id_solicitacao"), nullable=False, unique=True)
    data_concessao = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default="ativa")
    total_dias_aprovados = db.Column(db.Integer, nullable=False, default=90)
    solicitacao = db.relationship("Solicitacao", backref=db.backref("licenca", uselist=False))


class Parcela(db.Model):
    __tablename__ = "PARCELA"
    id_parcela = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_licenca = db.Column(db.Integer, db.ForeignKey("LICENCA.id_licenca"), nullable=False)
    numero_parcela = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    licenca = db.relationship("Licenca", backref="parcelas")
