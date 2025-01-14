import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tenta carregar o arquivo CSV ou cria um DataFrame vazio
#try:
    #dados = pd.read_csv("compras.csv")
#except FileNotFoundError:
dados = pd.DataFrame({"produtos": [], "preços": []})
dados.to_csv("compras.csv", index=False)

st.title("Controle de Compras")

# Entrada de orçamento
orcamento = st.number_input("Orçamento (€):", min_value=0.0)
total = dados["preços"].sum() if not dados.empty else 0.0

# Formulário para adicionar produtos
with st.form("Adicionar item"):
    produto = st.text_input("Adicione produto:")
    preco = st.number_input("Adicione preço (€):", min_value=0.0)
    submit_button = st.form_submit_button("Adicionar")

    if submit_button:
        if preco <= (orcamento - total):
            novo_produto = pd.DataFrame({"produtos": [produto], "preços": [preco]})
            dados = pd.concat([dados, novo_produto], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada com sucesso!")
        else:
            st.error("Sem orçamento disponível para esta compra!")

# Exibir informações e gráficos se orçamento for maior que 0
if orcamento > 0:
    # Criar gráfico de pizza (donut)
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["produtos"].tolist()
        valores = dados["preços"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)

        ax.pie(
            valores,
            labels=produtos,
            autopct='%1.1f%%',
            pctdistance=0.85
        )
        # Criar o centro do gráfico (estilo donut)
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)

    plt.title(f"Orçamento: {orcamento}€")
    st.pyplot(fig)

# Exibir tabela de dados e informações adicionais
st.dataframe(dados)
st.write(f"Total gasto: {total:.2f}€")
st.write(f"Saldo restante: {orcamento - total:.2f}€")
