from datetime import date

import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from models import AcaoCapacitacao, Licenca, Parcela, Servidor, Solicitacao, Tramitacao, db
from routes import (
    CRUDS,
    atualizar_fluxo,
    cancelar_parcela,
    concluir_parcela,
    criar_tramitacoes,
    etapa_atual,
    iniciar_parcela,
    opcoes,
    parcelas_restantes,
    popular_objeto,
    saldo_licenca,
    validar_item,
    validar_parcela,
)


st.set_page_config(
    page_title="Sistema de Licenca Capacitacao",
    page_icon=":clipboard:",
    layout="wide",
)


class DatabaseConfig:
    config = {
        "SQLALCHEMY_DATABASE_URI": Config.SQLALCHEMY_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": Config.SQLALCHEMY_TRACK_MODIFICATIONS,
    }


@st.cache_resource
def iniciar_banco():
    db.init_app(DatabaseConfig())
    return db


iniciar_banco()


PAGINAS = {
    "Dashboard": "dashboard",
    "Servidores": "servidores",
    "Afastamentos Vigentes": "afastamentos",
    "Solicitacoes": "solicitacoes",
    "Aprovacoes": "aprovacoes",
    "Licencas": "licencas",
}

CAMPOS_SOLICITACAO = [campo for campo in CRUDS["solicitacoes"]["fields"] if campo[0] not in {"data_solicitacao", "status"}]
CAMPOS_ACAO = [campo for campo in CRUDS["acoes"]["fields"] if campo[0] != "id_solicitacao"]


def limpar_formulario(chave):
    st.session_state[f"{chave}_form_nonce"] = st.session_state.get(f"{chave}_form_nonce", 0) + 1


def valor_padrao(item, nome, tipo):
    valor = getattr(item, nome, None)
    if valor is None and tipo == "date":
        return date.today()
    if valor is None and tipo in {"number", "fk"}:
        return 1
    if valor is None:
        return ""
    return valor


def campo_formulario(campo, item, prefixo):
    nome, tipo, rotulo = campo[0], campo[1], campo[2]
    chave_widget = f"{prefixo}_{nome}"
    valor = valor_padrao(item, nome, tipo)

    if tipo == "select":
        alternativas = campo[3]
        indice = alternativas.index(valor) if valor in alternativas else 0
        return st.selectbox(rotulo, alternativas, index=indice, key=chave_widget)
    if tipo == "fk":
        alternativas = opcoes(campo[3], campo[4], campo[5])
        if not alternativas:
            st.warning(f"Cadastre um registro em {rotulo} antes de continuar.")
            return None
        ids = [item_opcao[0] for item_opcao in alternativas]
        textos = {item_opcao[0]: f"{item_opcao[0]} - {item_opcao[1]}" for item_opcao in alternativas}
        indice = ids.index(valor) if valor in ids else 0
        return st.selectbox(rotulo, ids, index=indice, format_func=lambda item_id: textos[item_id], key=chave_widget)
    if tipo == "date":
        return st.date_input(rotulo, value=valor, key=chave_widget)
    if tipo == "number":
        numero = int(valor) if valor not in ("", None) else 1
        return st.number_input(rotulo, min_value=0, step=1, value=numero, key=chave_widget)
    if tipo == "textarea":
        return st.text_area(rotulo, value=valor or "", key=chave_widget)
    return st.text_input(rotulo, value=valor or "", key=chave_widget)


def campo_preenchido(campo, valor):
    if campo[1] in {"text", "textarea"}:
        return bool(str(valor or "").strip())
    return True


def dados_tabela(chave):
    cfg = CRUDS[chave]
    linhas = []
    for item in cfg["model"].query.all():
        linha = {col: getattr(item, col) for col in cfg["cols"]}
        if chave == "licencas":
            linha["saldo_dias"] = saldo_licenca(item)
        linhas.append(linha)
    return linhas


def salvar_registro(chave, item, dados, editando=False):
    cfg = CRUDS[chave]
    popular_objeto(item, cfg, dados)
    erro = validar_item(item, chave, editando=editando)
    if erro:
        return False, erro

    try:
        if not editando:
            db.session.add(item)
        db.session.commit()
        return True, "Registro salvo com sucesso."
    except SQLAlchemyError as exc:
        db.session.rollback()
        return False, f"Erro ao salvar: {exc}"
    except Exception as exc:
        db.session.rollback()
        return False, f"Erro ao salvar: {exc}"


def excluir_registro(chave, item_id):
    cfg = CRUDS[chave]
    item = cfg["model"].query.get(item_id)
    if not item:
        st.error("Registro nao encontrado.")
        return
    try:
        db.session.delete(item)
        db.session.commit()
        st.success("Registro excluido com sucesso.")
        st.rerun()
    except Exception as exc:
        db.session.rollback()
        st.error(f"Erro ao excluir: {exc}")


def pagina_dashboard():
    st.title("Dashboard")
    st.caption("Resumo do controle de licenca capacitacao.")

    metricas = [
        ("Total de servidores", Servidor.query.count()),
        ("Total de solicitacoes", Solicitacao.query.count()),
        ("Total de licencas", Licenca.query.count()),
        ("Total de parcelas", Parcela.query.count()),
        ("Solicitacoes pendentes", Tramitacao.query.filter_by(decisao="pendente").count()),
    ]
    colunas = st.columns(len(metricas))
    for coluna, (titulo, valor) in zip(colunas, metricas):
        with coluna:
            st.metric(titulo, valor)


def formulario_crud(chave, item=None):
    cfg = CRUDS[chave]
    editando = item is not None
    item = item or cfg["model"]()
    nonce = st.session_state.get(f"{chave}_form_nonce", 0)
    item_id = getattr(item, cfg["pk"], "novo")
    prefixo = f"{chave}_{'editar' if editando else 'novo'}_{item_id}_{nonce}"
    titulo = "Editar registro" if editando else "Novo registro"

    with st.form(f"form_{prefixo}"):
        st.subheader(titulo)
        dados = {}
        campos_validos = True
        for campo in cfg["fields"]:
            valor = campo_formulario(campo, item, prefixo)
            if valor is None or not campo_preenchido(campo, valor):
                campos_validos = False
            dados[campo[0]] = valor
        enviado = st.form_submit_button("Salvar")

    if enviado and not campos_validos:
        st.error("Preencha todos os campos obrigatorios.")
    elif enviado and campos_validos:
        sucesso, mensagem = salvar_registro(chave, item, dados, editando=editando)
        if sucesso:
            st.success(mensagem)
            limpar_formulario(chave)
            st.rerun()
        else:
            st.error(mensagem)


def pagina_crud(chave):
    cfg = CRUDS[chave]
    st.title(cfg["titulo"])

    linhas = dados_tabela(chave)
    if linhas:
        st.dataframe(linhas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado.")

    abas = st.tabs(["Novo", "Editar", "Excluir"])
    with abas[0]:
        formulario_crud(chave)

    with abas[1]:
        itens = cfg["model"].query.order_by(getattr(cfg["model"], cfg["pk"])).all()
        if not itens:
            st.info("Nao ha registros para editar.")
        else:
            opcoes_edicao = [getattr(item, cfg["pk"]) for item in itens]
            selecionado = st.selectbox("Registro", opcoes_edicao, key=f"{chave}_item_edicao")
            item = cfg["model"].query.get(selecionado)
            formulario_crud(chave, item)

    with abas[2]:
        itens = cfg["model"].query.order_by(getattr(cfg["model"], cfg["pk"])).all()
        if not itens:
            st.info("Nao ha registros para excluir.")
        else:
            opcoes_exclusao = [getattr(item, cfg["pk"]) for item in itens]
            selecionado = st.selectbox("Registro", opcoes_exclusao, key=f"{chave}_item_exclusao")
            st.warning("A exclusao e definitiva.")
            if st.button("Excluir registro", type="primary", key=f"{chave}_excluir"):
                excluir_registro(chave, selecionado)


def criar_solicitacao(dados_solicitacao, dados_acao):
    solicitacao = Solicitacao(data_solicitacao=date.today(), status="pendente")
    popular_objeto(solicitacao, {"fields": CAMPOS_SOLICITACAO}, dados_solicitacao)
    erro = validar_item(solicitacao, "solicitacoes")
    if erro:
        return False, erro

    acao = AcaoCapacitacao()
    popular_objeto(acao, {"fields": CAMPOS_ACAO}, dados_acao)
    erro = validar_item(acao, "acoes")
    if erro:
        return False, erro

    try:
        db.session.add(solicitacao)
        db.session.flush()
        acao.id_solicitacao = solicitacao.id_solicitacao
        db.session.add(acao)
        criar_tramitacoes(solicitacao)
        db.session.commit()
        return True, "Solicitacao enviada com sucesso."
    except SQLAlchemyError as exc:
        db.session.rollback()
        return False, f"Erro ao salvar: {exc}"


def cancelar_solicitacao(solicitacao):
    try:
        solicitacao.status = "cancelada"
        db.session.commit()
        st.success("Solicitacao cancelada.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        st.error(f"Erro ao cancelar: {exc}")


def agendar_parcela(licenca, data_inicio, data_fim):
    parcela = Parcela(
        id_licenca=licenca.id_licenca,
        numero_parcela=len(licenca.parcelas) + 1,
        data_inicio=data_inicio,
        data_fim=data_fim,
        status="agendada",
    )
    erro = validar_parcela(parcela)
    if erro:
        return False, erro

    try:
        db.session.add(parcela)
        db.session.commit()
        return True, "Parcela agendada com sucesso."
    except SQLAlchemyError as exc:
        db.session.rollback()
        return False, f"Erro ao salvar: {exc}"


def transicionar_parcela(parcela, acao):
    try:
        if acao == "iniciar":
            iniciar_parcela(parcela)
        elif acao == "concluir":
            concluir_parcela(parcela)
        elif acao == "cancelar":
            cancelar_parcela(parcela)
        db.session.commit()
        st.success("Parcela atualizada.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        st.error(f"Erro ao atualizar parcela: {exc}")


def pagina_solicitacoes():
    st.title("Solicitacoes")

    linhas = []
    for solicitacao in Solicitacao.query.order_by(Solicitacao.id_solicitacao).all():
        etapa = etapa_atual(solicitacao)
        linhas.append(
            {
                "id_solicitacao": solicitacao.id_solicitacao,
                "servidor": solicitacao.servidor.nome,
                "data_solicitacao": solicitacao.data_solicitacao,
                "status": solicitacao.status,
                "etapa_atual": etapa.etapa if etapa else "-",
            }
        )
    if linhas:
        st.dataframe(linhas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado.")

    st.subheader("Nova solicitacao")
    nonce = st.session_state.get("solicitacoes_form_nonce", 0)
    prefixo = f"solicitacoes_nova_{nonce}"

    with st.form(f"form_{prefixo}"):
        solicitacao_nova = Solicitacao()
        acao_nova = AcaoCapacitacao()
        dados_solicitacao = {}
        dados_acao = {}
        campos_validos = True

        for campo in CAMPOS_SOLICITACAO:
            valor = campo_formulario(campo, solicitacao_nova, prefixo)
            if valor is None or not campo_preenchido(campo, valor):
                campos_validos = False
            dados_solicitacao[campo[0]] = valor

        st.markdown("**Acao de Capacitacao**")
        for campo in CAMPOS_ACAO:
            valor = campo_formulario(campo, acao_nova, prefixo)
            if valor is None or not campo_preenchido(campo, valor):
                campos_validos = False
            dados_acao[campo[0]] = valor

        enviado = st.form_submit_button("Enviar solicitacao")

    if enviado and not campos_validos:
        st.error("Preencha todos os campos obrigatorios.")
    elif enviado and campos_validos:
        sucesso, mensagem = criar_solicitacao(dados_solicitacao, dados_acao)
        if sucesso:
            st.success(mensagem)
            limpar_formulario("solicitacoes")
            st.rerun()
        else:
            st.error(mensagem)

    st.subheader("Acompanhamento")
    pendentes = Solicitacao.query.filter_by(status="pendente").order_by(Solicitacao.id_solicitacao).all()
    if not pendentes:
        st.info("Nenhuma solicitacao pendente.")
    for solicitacao in pendentes:
        with st.expander(f"Solicitacao #{solicitacao.id_solicitacao} - {solicitacao.servidor.nome}"):
            etapa = etapa_atual(solicitacao)
            st.write(f"Etapa atual: {etapa.etapa if etapa else '-'}")
            if st.button("Cancelar solicitacao", key=f"cancelar_{solicitacao.id_solicitacao}"):
                cancelar_solicitacao(solicitacao)
                st.rerun()

    st.subheader("Agendar parcelas")
    aprovadas = [s for s in Solicitacao.query.filter_by(status="aprovada").all() if s.licenca]
    if not aprovadas:
        st.info("Nenhuma solicitacao aprovada aguardando parcelas.")
    for solicitacao in aprovadas:
        licenca = solicitacao.licenca
        restantes = parcelas_restantes(licenca, solicitacao)
        titulo = f"Solicitacao #{solicitacao.id_solicitacao} - {solicitacao.servidor.nome} (saldo: {saldo_licenca(licenca)} dias)"
        with st.expander(titulo):
            for parcela in licenca.parcelas:
                col_info, col_acao = st.columns([3, 1])
                with col_info:
                    st.write(
                        f"Parcela {parcela.numero_parcela}: {parcela.data_inicio} a {parcela.data_fim} - {parcela.status}"
                    )
                with col_acao:
                    if parcela.status == "agendada":
                        if st.button("Iniciar", key=f"iniciar_{parcela.id_parcela}"):
                            transicionar_parcela(parcela, "iniciar")
                            st.rerun()
                        if st.button("Cancelar", key=f"cancelar_parcela_{parcela.id_parcela}"):
                            transicionar_parcela(parcela, "cancelar")
                            st.rerun()
                    elif parcela.status == "em_andamento":
                        if st.button("Concluir", key=f"concluir_{parcela.id_parcela}"):
                            transicionar_parcela(parcela, "concluir")
                            st.rerun()

            if restantes == 0:
                st.success("Todas as parcelas ja foram agendadas.")
                continue

            chave_parcela = f"parcela_{solicitacao.id_solicitacao}"
            nonce_parcela = st.session_state.get(f"{chave_parcela}_form_nonce", 0)
            prefixo_parcela = f"{chave_parcela}_{nonce_parcela}"
            with st.form(f"form_{prefixo_parcela}"):
                data_inicio = st.date_input("Data inicial", value=date.today(), key=f"{prefixo_parcela}_inicio")
                data_fim = st.date_input("Data final", value=date.today(), key=f"{prefixo_parcela}_fim")
                enviado_parcela = st.form_submit_button("Agendar parcela")

            if enviado_parcela:
                sucesso, mensagem = agendar_parcela(licenca, data_inicio, data_fim)
                if sucesso:
                    st.success(mensagem)
                    limpar_formulario(chave_parcela)
                    st.rerun()
                else:
                    st.error(mensagem)


def decidir_tramitacao(tramitacao, decisao, observacao):
    try:
        tramitacao.decisao = decisao
        tramitacao.observacao = observacao
        tramitacao.data_decisao = date.today()
        atualizar_fluxo(tramitacao)
        db.session.commit()
        st.success("Decisao registrada.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        st.error(f"Erro ao registrar decisao: {exc}")


def pagina_aprovacoes():
    st.title("Aprovacoes")

    solicitacoes = Solicitacao.query.filter_by(status="pendente").order_by(Solicitacao.id_solicitacao).all()
    pendentes = [(solicitacao, etapa_atual(solicitacao)) for solicitacao in solicitacoes]
    pendentes = [(solicitacao, etapa) for solicitacao, etapa in pendentes if etapa]

    if not pendentes:
        st.info("Nenhuma solicitacao aguardando decisao.")
        return

    for solicitacao, tramitacao in pendentes:
        titulo_acao = solicitacao.acao.titulo if solicitacao.acao else "-"
        titulo = f"Solicitacao #{solicitacao.id_solicitacao} - {solicitacao.servidor.nome} - Etapa: {tramitacao.etapa}"
        with st.expander(titulo):
            st.write(f"Acao de capacitacao: {titulo_acao}")
            st.write(f"Responsavel: {tramitacao.responsavel}")
            observacao = st.text_area("Observacao", key=f"obs_{tramitacao.id_tramitacao}")
            coluna_aprovar, coluna_negar = st.columns(2)
            with coluna_aprovar:
                if st.button("Aprovar", key=f"aprovar_{tramitacao.id_tramitacao}", type="primary"):
                    decidir_tramitacao(tramitacao, "aprovado", observacao)
                    st.rerun()
            with coluna_negar:
                if st.button("Negar", key=f"negar_{tramitacao.id_tramitacao}"):
                    decidir_tramitacao(tramitacao, "negado", observacao)
                    st.rerun()


def pagina_licencas():
    st.title("Licencas")
    linhas = dados_tabela("licencas")
    if linhas:
        st.dataframe(linhas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado.")


with st.sidebar:
    st.header("Menu")
    pagina = st.radio("Navegacao", list(PAGINAS.keys()), label_visibility="collapsed")

chave_pagina = PAGINAS[pagina]
if chave_pagina == "dashboard":
    pagina_dashboard()
elif chave_pagina == "solicitacoes":
    pagina_solicitacoes()
elif chave_pagina == "aprovacoes":
    pagina_aprovacoes()
elif chave_pagina == "licencas":
    pagina_licencas()
else:
    pagina_crud(chave_pagina)
