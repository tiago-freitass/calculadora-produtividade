# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

MEDIA_BASE = 2.5

def calcular_produtividade(itens, tempo_minutos, colaboradores):
    if tempo_minutos <= 0 or colaboradores <= 0:
        return None

    prod_ind_minuto = (itens / tempo_minutos) / colaboradores
    prod_ind_hora = (itens / (tempo_minutos / 60)) / colaboradores
    prod_ind_dia = (itens / (tempo_minutos / (60 * 8))) / colaboradores

    prod_eq_minuto = itens / tempo_minutos
    prod_eq_hora = itens / (tempo_minutos / 60)
    prod_eq_dia = itens / (tempo_minutos / (60 * 8))

    diff_pecas = prod_ind_minuto - MEDIA_BASE
    diff_percentual = ((prod_ind_minuto - MEDIA_BASE) / MEDIA_BASE) * 100 if MEDIA_BASE != 0 else 0

    return {
        "ind": {"Minuto": prod_ind_minuto, "Hora": prod_ind_hora, "Dia": prod_ind_dia},
        "eq": {"Minuto": prod_eq_minuto, "Hora": prod_eq_hora, "Dia": prod_eq_dia},
        "comparativo": {
            "Média Base": MEDIA_BASE,
            "Produtividade Atual": prod_ind_minuto,
            "Diferença": diff_pecas,
            "Diferença (%)": diff_percentual
        }
    }

st.set_page_config(page_title="Calculadora de Produtividade", layout="centered")
st.title("📊 Calculadora de Produtividade")

# Entradas
itens = st.number_input("Itens Separados", min_value=0)
tempo = st.number_input("Tempo (minutos)", min_value=1, step=1, format="%d")  # Inteiro
colaboradores = st.number_input("Colaboradores", min_value=1)

if st.button("Calcular"):
    resultados = calcular_produtividade(itens, tempo, colaboradores)
    if resultados:
        st.subheader("🧍‍♂️ Produtividade Individual")
        st.dataframe(
            pd.DataFrame(resultados["ind"], index=["Valor"]).T.style
                .set_properties(**{'text-align': 'center'})
                .format("{:g}"),
            use_container_width=True
        )

        st.subheader("👥 Produtividade da Equipe")
        st.dataframe(
            pd.DataFrame(resultados["eq"], index=["Valor"]).T.style
                .set_properties(**{'text-align': 'center'})
                .format("{:g}"),
            use_container_width=True
        )

        st.subheader("📈 Comparativo com Média Base")
        st.dataframe(
            pd.DataFrame(resultados["comparativo"], index=["Valor"]).T.style
                .set_properties(**{'text-align': 'center'})
                .format("{:g}"),
            use_container_width=True
        )

        # Gráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        # Gráfico Individual
        ax1.bar(
            ["Média Base", "Produtividade Atual"],
            [MEDIA_BASE, resultados["comparativo"]["Produtividade Atual"]],
            color=["#1f77b4", "#ff7f0e"]
        )
        ax1.set_title("Comparativo (Individual)")
        ax1.set_ylabel("Peças/min/colaborador")
        ax1.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Gráfico Equipe
        eq_vals = resultados["eq"]
        ax2.bar(eq_vals.keys(), eq_vals.values(), color=["#2ca02c", "#d62728", "#9467bd"])
        ax2.set_title("Produtividade da Equipe")
        ax2.set_ylabel("Peças")
        ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)
    else:
        st.error("Erro: valores inválidos.")
