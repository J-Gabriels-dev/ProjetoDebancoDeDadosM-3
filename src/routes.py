from datetime import date, datetime
from math import ceil

from models import (
    AcaoCapacitacao,
    AfastamentoVigente,
    Licenca,
    Parcela,
    Servidor,
    Solicitacao,
    Tramitacao,
    db,
)


ETAPAS = ["chefia_imediata", "gestao_de_pessoas", "autoridade_maxima"]


def parse_date(value):
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None


def dias_entre(inicio, fim):
    return (fim - inicio).days


def completou_quinquenio(servidor):
    try:
        data_direito = servidor.data_posse.replace(year=servidor.data_posse.year + 5)
    except ValueError:
        data_direito = servidor.data_posse.replace(year=servidor.data_posse.year + 5, day=28)
    return date.today() >= data_direito


def periodo_sobrepoe(inicio_a, fim_a, inicio_b, fim_b):
    return inicio_a <= fim_b and fim_a >= inicio_b


def validar_parcela(parcela, ignorar_id=None):
    if parcela.data_fim <= parcela.data_inicio:
        return "A data final deve ser maior que a data inicial."
    if dias_entre(parcela.data_inicio, parcela.data_fim) < 15:
        return "Cada parcela deve ter no minimo 15 dias."
    if not 1 <= parcela.numero_parcela <= 6:
        return "O numero da parcela deve estar entre 1 e 6."

    licenca = Licenca.query.get(parcela.id_licenca)
    if not licenca:
        return "Licenca nao encontrada."
    servidor = licenca.solicitacao.servidor

    conflito = AfastamentoVigente.query.filter(
        AfastamentoVigente.id_servidor == servidor.id_servidor,
        AfastamentoVigente.status == "ativo",
        AfastamentoVigente.data_inicio <= parcela.data_fim,
        AfastamentoVigente.data_fim >= parcela.data_inicio,
    ).first()
    if conflito:
        return "Existe afastamento vigente do servidor no periodo informado."

    outras = Parcela.query.join(Licenca).join(Solicitacao).filter(
        Solicitacao.id_servidor == servidor.id_servidor,
        Parcela.status != "cancelada",
        Parcela.data_inicio <= parcela.data_fim,
        Parcela.data_fim >= parcela.data_inicio,
    )
    if ignorar_id:
        outras = outras.filter(Parcela.id_parcela != ignorar_id)
    if outras.first():
        return "Existe conflito com outra parcela do mesmo servidor."

    parcelas = Parcela.query.filter(Parcela.id_licenca == parcela.id_licenca)
    if ignorar_id:
        parcelas = parcelas.filter(Parcela.id_parcela != ignorar_id)
    lista = parcelas.all() + [parcela]
    lista.sort(key=lambda item: item.data_inicio)
    for atual, proxima in zip(lista, lista[1:]):
        if dias_entre(atual.data_fim, proxima.data_inicio) < 60:
            return "Deve haver intervalo minimo de 60 dias entre parcelas."

    total = sum(dias_entre(p.data_inicio, p.data_fim) for p in lista if p.status != "cancelada")
    if total > licenca.total_dias_aprovados or total > 90:
        return "A soma das parcelas nao pode ultrapassar 90 dias."

    ativos = Servidor.query.filter_by(status_funcional="ativo").count()
    limite = ceil(ativos * 0.05) if ativos else 0
    afastados = set(
        row[0]
        for row in db.session.query(AfastamentoVigente.id_servidor)
        .filter(
            AfastamentoVigente.status == "ativo",
            AfastamentoVigente.data_inicio <= parcela.data_fim,
            AfastamentoVigente.data_fim >= parcela.data_inicio,
        )
        .all()
    )
    parcelas_afastadas = (
        db.session.query(Solicitacao.id_servidor)
        .join(Licenca, Licenca.id_solicitacao == Solicitacao.id_solicitacao)
        .join(Parcela, Parcela.id_licenca == Licenca.id_licenca)
        .filter(
            Parcela.status.in_(["agendada", "em_andamento", "concluida"]),
            Parcela.data_inicio <= parcela.data_fim,
            Parcela.data_fim >= parcela.data_inicio,
        )
    )
    if ignorar_id:
        parcelas_afastadas = parcelas_afastadas.filter(Parcela.id_parcela != ignorar_id)
    afastados.update(row[0] for row in parcelas_afastadas.all())
    if servidor.id_servidor not in afastados and len(afastados) >= limite:
        return "O limite de 5% de servidores afastados simultaneamente foi atingido."
    return None


def saldo_licenca(licenca):
    usados = 0
    for parcela in licenca.parcelas:
        if parcela.status == "concluida":
            usados += dias_entre(parcela.data_inicio, parcela.data_fim)
    return 90 - usados


def opcoes(modelo, pk, label):
    return [(getattr(item, pk), getattr(item, label)) for item in modelo.query.order_by(getattr(modelo, label)).all()]


CRUDS = {
    "servidores": {
        "titulo": "Servidores",
        "model": Servidor,
        "pk": "id_servidor",
        "fields": [
            ("nome", "text", "Nome"),
            ("siape", "text", "SIAPE"),
            ("data_posse", "date", "Data de posse"),
            ("lotacao", "text", "Lotacao"),
            ("status_funcional", "select", "Status funcional", ["ativo", "aposentado", "exonerado", "disponibilidade"]),
        ],
        "cols": ["id_servidor", "nome", "siape", "data_posse", "lotacao", "status_funcional"],
    },
    "afastamentos": {
        "titulo": "Afastamentos Vigentes",
        "model": AfastamentoVigente,
        "pk": "id_afastamento",
        "fields": [
            ("id_servidor", "fk", "Servidor", Servidor, "id_servidor", "nome"),
            ("tipo", "select", "Tipo", ["licenca_medica", "licenca_maternidade", "afastamento_acidente", "atestado", "licenca_capacitacao"]),
            ("data_inicio", "date", "Data inicial"),
            ("data_fim", "date", "Data final"),
            ("status", "select", "Status", ["ativo", "encerrado", "cancelado"]),
        ],
        "cols": ["id_afastamento", "id_servidor", "tipo", "data_inicio", "data_fim", "status"],
    },
    "solicitacoes": {
        "titulo": "Solicitacoes",
        "model": Solicitacao,
        "pk": "id_solicitacao",
        "fields": [
            ("id_servidor", "fk", "Servidor", Servidor, "id_servidor", "nome"),
            ("data_solicitacao", "date", "Data da solicitacao"),
            ("status", "select", "Status", ["pendente", "aprovada", "concluida", "cancelada"]),
            ("justificativa", "textarea", "Justificativa"),
            ("qtd_parcelas", "number", "Quantidade de parcelas"),
        ],
        "cols": ["id_solicitacao", "id_servidor", "data_solicitacao", "status", "qtd_parcelas"],
    },
    "acoes": {
        "titulo": "Acoes de Capacitacao",
        "model": AcaoCapacitacao,
        "pk": "id_acao",
        "fields": [
            ("id_solicitacao", "fk", "Solicitacao", Solicitacao, "id_solicitacao", "id_solicitacao"),
            ("titulo", "text", "Titulo"),
            ("instituicao", "text", "Instituicao"),
            ("modalidade", "select", "Modalidade", ["presencial", "ead", "hibrido"]),
            ("carga_horaria_semanal", "number", "Carga horaria semanal"),
            ("local", "text", "Local"),
        ],
        "cols": ["id_acao", "id_solicitacao", "titulo", "instituicao", "modalidade", "carga_horaria_semanal", "local"],
    },
    "tramitacoes": {
        "titulo": "Tramitacoes",
        "model": Tramitacao,
        "pk": "id_tramitacao",
        "fields": [
            ("id_solicitacao", "fk", "Solicitacao", Solicitacao, "id_solicitacao", "id_solicitacao"),
            ("etapa", "select", "Etapa", ETAPAS),
            ("responsavel", "text", "Responsavel"),
            ("decisao", "select", "Decisao", ["pendente", "aprovado", "negado"]),
            ("observacao", "textarea", "Observacao"),
            ("data_decisao", "date", "Data da decisao"),
        ],
        "cols": ["id_tramitacao", "id_solicitacao", "etapa", "responsavel", "decisao", "data_decisao"],
    },
    "licencas": {
        "titulo": "Licencas",
        "model": Licenca,
        "pk": "id_licenca",
        "fields": [
            ("id_solicitacao", "fk", "Solicitacao", Solicitacao, "id_solicitacao", "id_solicitacao"),
            ("data_concessao", "date", "Data de concessao"),
            ("status", "select", "Status", ["ativa", "concluida", "cancelada", "interrompida"]),
            ("total_dias_aprovados", "number", "Total de dias aprovados"),
        ],
        "cols": ["id_licenca", "id_solicitacao", "data_concessao", "status", "total_dias_aprovados"],
    },
    "parcelas": {
        "titulo": "Parcelas",
        "model": Parcela,
        "pk": "id_parcela",
        "fields": [
            ("id_licenca", "fk", "Licenca", Licenca, "id_licenca", "id_licenca"),
            ("numero_parcela", "number", "Numero da parcela"),
            ("data_inicio", "date", "Data inicial"),
            ("data_fim", "date", "Data final"),
            ("status", "select", "Status", ["agendada", "em_andamento", "concluida", "cancelada"]),
        ],
        "cols": ["id_parcela", "id_licenca", "numero_parcela", "data_inicio", "data_fim", "status"],
    },
}


def popular_objeto(item, cfg, dados):
    for campo in cfg["fields"]:
        nome, tipo = campo[0], campo[1]
        valor = dados.get(nome)
        if tipo == "date":
            valor = parse_date(valor)
        elif tipo in {"number", "fk"}:
            valor = int(valor) if valor else None
        setattr(item, nome, valor)


def validar_item(item, chave, editando=False):
    if chave == "solicitacoes":
        servidor = Servidor.query.get(item.id_servidor)
        if not servidor or servidor.status_funcional != "ativo":
            return "Somente servidores ativos podem solicitar licenca."
        if not completou_quinquenio(servidor):
            return "O servidor ainda nao completou quinquenio."
        if not 1 <= item.qtd_parcelas <= 6:
            return "A quantidade de parcelas deve estar entre 1 e 6."
    if chave == "acoes" and item.carga_horaria_semanal < 30:
        return "A carga horaria semanal minima e 30h."
    if chave == "afastamentos" and item.data_fim <= item.data_inicio:
        return "A data final deve ser maior que a data inicial."
    if chave == "licencas" and item.total_dias_aprovados > 90:
        return "A licenca nao pode ultrapassar 90 dias."
    if chave == "parcelas":
        return validar_parcela(item, item.id_parcela if editando else None)
    return None


def criar_tramitacoes(solicitacao):
    responsaveis = {
        "chefia_imediata": f"Chefia - {solicitacao.servidor.lotacao}",
        "gestao_de_pessoas": "Gestao de Pessoas",
        "autoridade_maxima": "Autoridade Maxima",
    }
    for etapa in ETAPAS:
        db.session.add(Tramitacao(id_solicitacao=solicitacao.id_solicitacao, etapa=etapa, responsavel=responsaveis[etapa]))


def validar_tramitacao(item):
    indice = ETAPAS.index(item.etapa)
    anteriores = Tramitacao.query.filter_by(id_solicitacao=item.id_solicitacao).all()
    por_etapa = {tr.etapa: tr for tr in anteriores}
    for etapa in ETAPAS[:indice]:
        if por_etapa.get(etapa) and por_etapa[etapa].decisao != "aprovado":
            return f"A etapa {item.etapa} so pode ser decidida depois da aprovacao de {etapa}."
    return None


def atualizar_fluxo(item):
    solicitacao = item.solicitacao
    if item.decisao == "pendente":
        return
    item.data_decisao = item.data_decisao or date.today()
    if item.decisao == "negado":
        solicitacao.status = "cancelada"
        return
    todas = Tramitacao.query.filter_by(id_solicitacao=item.id_solicitacao).all()
    if all(tr.decisao == "aprovado" for tr in todas):
        solicitacao.status = "aprovada"
        if not solicitacao.licenca:
            db.session.add(Licenca(id_solicitacao=solicitacao.id_solicitacao, total_dias_aprovados=90, status="ativa"))
