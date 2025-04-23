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
        "ind": {
            "Minuto": round(prod_ind_minuto, 1),
            "Hora": round(prod_ind_hora, 3),
            "Dia": round(prod_ind_dia, 3)
        },
        "eq": {
            "Minuto": round(prod_eq_minuto, 1),
            "Hora": round(prod_eq_hora, 3),
            "Dia": round(prod_eq_dia, 3)
        },
        "comparativo": {
            "Média Base": round(MEDIA_BASE, 1),
            "Produtividade Atual": round(prod_ind_minuto, 1),
            "Diferença": round(diff_pecas, 1),
            "Diferença (%)": round(diff_percentual, 1)
        }
    }

# Layout Streamlit
st.title("📊 Calculadora de Produtividade")

itens = st.number_input("Itens Separados", min_value=0)
tempo = st.number_input("Tempo (minutos)", min_value=1, format="%d")  # Inteiro, sem vírgula
colaboradores = st.number_input("Colaboradores", min_value=1)

if st.button("Calcular"):
    resultados = calcular_produtividade(itens, tempo, colaboradores)
    if resultados:
        # Tabelas com texto centralizado e formato limpo
        st.subheader("🧍‍♂️ Produtividade Individual")
        st.dataframe(
            pd.DataFrame(resultados["ind"], index=["Valor"]).T.style
                .set_properties(**{'text-align': 'center'})
                .format(precision=3),
            use_container_width=True
        )

        st.subheader("👥 Produtividade da Equipe")
        st.dataframe(
            pd.DataFrame(resultados["eq"], index=["Valor"]).T.style
                .set_properties(**{'text-align': 'center'})
                .format(precision=3),
            use_container_width=True
        )

        st.subheader("📈 Comparativo com Média Base")
        st.dataframe(
            pd.DataFrame(resultados["comparativo"], index=["Valor"]).T.style
                .set_properties(**{'text-align': 'center'})
                .format(precision=1),
            use_container_width=True
        )

        # Gráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        prod_ind_minuto = resultados["comparativo"]["Produtividade Atual"]
        ax1.bar(["Média Base", "Produtividade Atual"], [MEDIA_BASE, prod_ind_minuto], color=['#00BFFF', '#FFA500'])
        ax1.set_title("⚖️ Comparativo de Produtividade (Individual)")
        ax1.set_ylabel("Peças/min/colaborador")
        ax1.grid(True, axis='y', linestyle='--', alpha=0.5)
        for i, valor in enumerate([MEDIA_BASE, prod_ind_minuto]):
            ax1.text(i, valor + 0.05, f"{valor:.1f}", ha='center', va='bottom', fontsize=10)

        eq_vals = resultados["eq"]
        cores_eq = ['#4CAF50', '#FF7043', '#7E57C2']
        ax2.bar(eq_vals.keys(), eq_vals.values(), color=cores_eq)
        ax2.set_title("👥 Produtividade da Equipe")
        ax2.set_ylabel("Peças")
        ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
        for i, valor in enumerate(eq_vals.values()):
            ax2.text(i, valor + 0.05, f"{valor:.3f}", ha='center', va='bottom', fontsize=10)

        st.pyplot(fig)
    else:
        st.error("🚨 Erro: valores inválidos.")

