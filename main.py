# Sistema para cadastro de vendas.

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Etapa 1: Preparar a tela com cadastro na lateral e vendas na area principal.


# Etapa 2: Criar o formulario com data, nome do vendedor, produto,
#          quantidade e valor unitario.
# Etapa 3: Validar os campos e garantir que a quantidade seja positiva.

st.set_page_config(
    page_title="Sistema de Vendas",
    layout="wide",
)

st.title("Sistema de Cadastro de Vendas")

# Etapa 4: Carregar vendas.csv ou criar a base com as colunas esperadas.
COLUNAS_VENDAS = ["data", "vendedor", "produto", "quantidade", "valor"]
CAMINHO_VENDAS = Path(__file__).resolve().parent / "vendas.csv"

try:
    if CAMINHO_VENDAS.exists():
        tabela = pd.read_csv(CAMINHO_VENDAS)
    else:
        tabela = pd.DataFrame(columns=COLUNAS_VENDAS)
        tabela.to_csv(CAMINHO_VENDAS, index=False)
except (OSError, UnicodeError, pd.errors.EmptyDataError, pd.errors.ParserError) as erro:
    st.error(f"Não foi possível carregar a base de vendas: {erro}")
    st.stop()

colunas_ausentes = [coluna for coluna in COLUNAS_VENDAS if coluna not in tabela.columns]
if colunas_ausentes:
    st.error(
        "A base de vendas não contém as colunas obrigatórias: "
        + ", ".join(colunas_ausentes)
    )
    st.stop()

# Etapa 5: Salvar cada venda sem substituir os registros existentes.
with st.sidebar:
    with st.container(border=True):
        st.header("Cadastrar venda")
        with st.form("formulario_cadastro_venda"):
            data = st.date_input(
                "Data da venda",
                value=None,
                label_visibility="collapsed",
            )
            vendedor = st.selectbox(
                "Vendedor",
                ["Ana", "Bruno", "Carla"],
                index=None,
                placeholder="Selecione o vendedor",
                label_visibility="collapsed",
            )
            produto = st.selectbox(
                "Produto",
                ["Notebook", "Celular", "Fone"],
                index=None,
                placeholder="Selecione o produto",
                label_visibility="collapsed",
            )
            quantidade = st.number_input(
                "Quantidade",
                step=1,
                value=None,
                placeholder="Digite a quantidade",
                label_visibility="collapsed",
            )
            valor = st.number_input(
                "Valor unitário",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                value=None,
                placeholder="Digite o valor unitário",
                label_visibility="collapsed",
            )
            enviado = st.form_submit_button("Cadastrar venda")

        if enviado:
            erros = []
            if data is None:
                erros.append("Informe a data da venda.")
            if vendedor is None:
                erros.append("Selecione o vendedor.")
            if produto is None:
                erros.append("Selecione o produto.")
            if quantidade is None or quantidade <= 0:
                erros.append("A quantidade deve ser maior que zero.")
            if valor is None or valor < 0:
                erros.append("Informe um valor unitário igual ou maior que zero.")

            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                nova_venda = {coluna: None for coluna in tabela.columns}
                nova_venda.update(
                    {
                        "data": data.isoformat(),
                        "vendedor": vendedor,
                        "produto": produto,
                        "quantidade": quantidade,
                        "valor": valor,
                    }
                )
                tabela_atualizada = pd.concat(
                    [tabela, pd.DataFrame([nova_venda])],
                    ignore_index=True,
                )
                try:
                    tabela_atualizada.to_csv(CAMINHO_VENDAS, index=False)
                except OSError as erro:
                    st.error(f"Não foi possível salvar a venda: {erro}")
                else:
                    tabela = tabela_atualizada
                    st.success("Venda cadastrada com sucesso!")

# Etapa 6: Exibir as vendas cadastradas e confirmar o resultado do cadastro.
st.header("Vendas cadastradas")
if tabela.empty:
    st.info("Nenhuma venda cadastrada ainda.")
else:
    st.dataframe(tabela, use_container_width=True, hide_index=True)

# Etapa 7: Criar um dashboard com indicadores e graficos de vendas.
st.header("Dashboard")
if tabela.empty:
    st.info("Cadastre vendas para visualizar os indicadores e gráficos.")
else:
    quantidade_numerica = pd.to_numeric(tabela["quantidade"], errors="coerce")
    valor_unitario = pd.to_numeric(tabela["valor"], errors="coerce")

    if quantidade_numerica.isna().any() or valor_unitario.isna().any():
        st.error(
            "Não foi possível calcular o dashboard: há quantidade ou valor "
            "inválido na base de vendas."
        )
    else:
        dados_dashboard = tabela.copy()
        dados_dashboard["quantidade"] = quantidade_numerica
        dados_dashboard["faturamento"] = quantidade_numerica * valor_unitario

        faturamento_total = dados_dashboard["faturamento"].sum()
        faturamento_formatado = (
            f"R$ {faturamento_total:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        metrica_faturamento, metrica_vendas, metrica_itens = st.columns(3)
        metrica_faturamento.metric("Faturamento total", faturamento_formatado)
        metrica_vendas.metric("Vendas cadastradas", len(dados_dashboard))
        metrica_itens.metric(
            "Unidades vendidas",
            f"{int(dados_dashboard['quantidade'].sum())}",
        )

        faturamento_vendedor = (
            dados_dashboard.groupby(["vendedor", "produto"], as_index=False)[
                "faturamento"
            ].sum()
        )
        faturamento_produto = (
            dados_dashboard.groupby("produto", as_index=False)["faturamento"].sum()
        )

        coluna_grafico_vendedor, coluna_grafico_produto = st.columns(2)
        with coluna_grafico_vendedor:
            grafico_vendedor = px.bar(
                faturamento_vendedor,
                x="vendedor",
                y="faturamento",
                color="produto",
                title="Faturamento por vendedor e produto",
                labels={
                    "vendedor": "Vendedor",
                    "faturamento": "Faturamento (R$)",
                    "produto": "Produto",
                },
            )
            st.plotly_chart(grafico_vendedor, use_container_width=True)

        with coluna_grafico_produto:
            grafico_produto = px.pie(
                faturamento_produto,
                names="produto",
                values="faturamento",
                title="Participação no faturamento por produto",
                labels={"produto": "Produto", "faturamento": "Faturamento (R$)"},
            )
            st.plotly_chart(grafico_produto, use_container_width=True)
