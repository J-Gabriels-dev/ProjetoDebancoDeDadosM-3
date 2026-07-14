from datetime import date

import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from models import Licenca, Parcela, Servidor, Solicitacao, Tramitacao, db
from routes import (
    CRUDS,
    atualizar_fluxo,
    criar_tramitacoes,
    opcoes,
    popular_objeto,
    saldo_licenca,
    validar_item,
    validar_tramitacao,
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
    "Acoes de Capacitacao": "acoes",
    "Tramitacoes": "tramitacoes",
    "Licencas": "licencas",
    "Parcelas": "parcelas",
}


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
    if chave == "tramitacoes" and not erro:
        erro = validar_tramitacao(item)
    if erro:
        return False, erro

    try:
        if not editando:
            db.session.add(item)
            db.session.flush()
            if chave == "solicitacoes":
                criar_tramitacoes(item)
        if chave == "tramitacoes":
            atualizar_fluxo(item)
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
            if valor is None:
                campos_validos = False
            dados[campo[0]] = valor
        enviado = st.form_submit_button("Salvar")

    if enviado and campos_validos:
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


with st.sidebar:
    st.header("Menu")
    pagina = st.radio("Navegacao", list(PAGINAS.keys()), label_visibility="collapsed")

chave_pagina = PAGINAS[pagina]
if chave_pagina == "dashboard":
    pagina_dashboard()
else:
    pagina_crud(chave_pagina)
