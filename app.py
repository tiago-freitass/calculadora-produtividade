# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Configuração inicial do Streamlit
st.set_page_config(page_title="Calculadora de Produtividade", page_icon="📈", layout="wide")

# Média base de produtividade
MEDIA_BASE = 2.5  # 2,5 peças por minuto por colaborador

# Função para formatar números no padrão brasileiro
def formatar_numero(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função para calcular a produtividade
def calcular_produtividade(itens, tempo_minutos, colaboradores):
    if tempo_minutos <= 0 or colaboradores <= 0 or itens <= 0:
        return None, "Erro: Itens, tempo e colaboradores devem ser maiores que zero."
    
    # Cálculos de produtividade individual
    prod_ind_minuto = (itens / tempo_minutos) / colaboradores
    prod_ind_hora = (itens / (tempo_minutos / 60)) / colaboradores
    prod_ind_dia = (itens / (tempo_minutos / (60 * 8))) / colaboradores
    
    # Cálculos de produtividade geral (equipe)
    prod_eq_minuto = itens / tempo_minutos
    prod_eq_hora = itens / (tempo_minutos / 60)
    prod_eq_dia = itens / (tempo_minutos / (60 * 8))
    
    # Comparativo com a média base
    diff_pecas = prod_ind_minuto - MEDIA_BASE
    diff_percentual = ((prod_ind_minuto - MEDIA_BASE) / MEDIA_BASE) * 100 if MEDIA_BASE != 0 else 0
    
    # Resultados formatados
    resultados_ind = {
        "Métrica": ["Produtividade por minuto", "Produtividade por hora", "Produtividade por dia (8h)"],
        "Valor": [
            f"{formatar_numero(prod_ind_minuto)} itens/minuto/colaborador",
            f"{formatar_numero(prod_ind_hora)} itens/hora/colaborador",
            f"{formatar_numero(prod_ind_dia)} itens/dia/colaborador"
        ]
    }
    
    resultados_eq = {
        "Métrica": ["Produtividade por minuto", "Produtividade por hora", "Produtividade por dia (8h)"],
        "Valor": [
            f"{formatar_numero(prod_eq_minuto)} itens/minuto/equipe",
            f"{formatar_numero(prod_eq_hora)} itens/hora/equipe",
            f"{formatar_numero(prod_eq_dia)} itens/dia/equipe"
        ]
    }
    
    comparativo = {
        "Métrica": [
            "Média Base (peças/min/colaborador)",
            "Produtividade Atual (peças/min/colaborador)",
            "Diferença (peças/min/colaborador)",
            "Diferença Percentual"
        ],
        "Valor": [
            f"{formatar_numero(MEDIA_BASE)}",
            f"{formatar_numero(prod_ind_minuto)}",
            f"{formatar_numero(diff_pecas)}",
            f"{diff_percentual:+.2f}%"
        ]
    }
    
    return {
        "ind": resultados_ind,
        "eq": resultados_eq,
        "comparativo": comparativo,
        "graficos": {
            "prod_ind_minuto": prod_ind_minuto,
            "prod_eq_minuto": prod_eq_minuto,
            "prod_eq_hora": prod_eq_hora,
            "prod_eq_dia": prod_eq_dia,
            "diff_percentual": diff_percentual
        }
    }, None

# Função para exportar tabelas como CSV
def exportar_csv(ind, eq, comparativo):
    buffer = io.StringIO()
    pd.concat([
        pd.DataFrame(ind).assign(Tabela="Individual"),
        pd.DataFrame(eq).assign(Tabela="Equipe"),
        pd.DataFrame(comparativo).assign(Tabela="Comparativo")
    ]).to_csv(buffer, index=False, encoding='utf-8')
    return buffer.getvalue()

# Layout Streamlit
st.title("📈 Calculadora de Produtividade")
st.markdown("**Insira os dados abaixo para calcular a produtividade da equipe.**")

# Instruções rápidas
with st.expander("ℹ️ Como usar"):
    st.markdown("""
    1. Insira a **quantidade de itens separados** (ex.: 1000).
    2. Informe o **tempo em minutos** (ex.: 120).
    3. Digite o **número de colaboradores** (ex.: 5).
    4. Clique em **Calcular** para ver os resultados.
    5. Use o botão **Download** para exportar as tabelas em CSV.
    """)

# Campos de entrada em colunas
col1, col2, col3 = st.columns(3)
with col1:
    itens = st.number_input("Itens Separados", min_value=0, step=1, format="%d", help="Quantidade total de itens separados.")
with col2:
    tempo = st.number_input("Tempo (minutos)", min_value=0.0, step=0.1, format="%.1f", help="Tempo total em minutos.")
with col3:
    colaboradores = st.number_input("Colaboradores", min_value=0, step=1, format="%d", help="Número de colaboradores envolvidos.")

# Botão para calcular
if st.button("Calcular", use_container_width=True):
    with st.spinner("Calculando..."):
        try:
            resultados, erro = calcular_produtividade(itens, tempo, colaboradores)
            if erro:
                st.error(erro)
            else:
                st.success("✅ Cálculo concluído!")
                
                # Exibir tabelas
                st.subheader("🧍‍♂️ Produtividade Individual")
                df_ind = pd.DataFrame(resultados["ind"])
                st.table(df_ind.style.set_properties(**{'text-align': 'left'}).hide(axis='index'))
                
                st.subheader("👥 Produtividade da Equipe")
                df_eq = pd.DataFrame(resultados["eq"])
                st.table(df_eq.style.set_properties(**{'text-align': 'left'}).hide(axis='index'))
                
                st.subheader("📊 Comparativo com Média Base")
                df_comparativo = pd.DataFrame(resultados["comparativo"])
                st.table(df_comparativo.style.set_properties(**{'text-align': 'left'}).hide(axis='index'))
                
                # Botão de download
                csv = exportar_csv(resultados["ind"], resultados["eq"], resultados["comparativo"])
                st.download_button(
                    label="📥 Baixar Tabelas (CSV)",
                    data=csv,
                    file_name="produtividade_resultados.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Gráficos
                sns.set_style("whitegrid")
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                # Gráfico Individual
                prod_ind_minuto = resultados["graficos"]["prod_ind_minuto"]
                diff_percentual = resultados["graficos"]["diff_percentual"]
                barras_ind = ax1.bar(
                    ["Média Base", "Produtividade Atual"],
                    [MEDIA_BASE, prod_ind_minuto],
                    color=['#1f77b4', '#ff7f0e'],
                    edgecolor='black',
                    linewidth=1.2
                )
                ax1.set_ylabel("Peças por Minuto por Colaborador", fontsize=12)
                ax1.set_title("⚖️ Comparativo de Produtividade (Individual)", fontsize=14, pad=15)
                ax1.grid(True, axis='y', linestyle='--', alpha=0.5)
                for i, barra in enumerate(barras_ind):
                    altura = barra.get_height()
                    texto = f"{formatar_numero(altura)}\n({diff_percentual:+.2f}%)" if i == 1 else formatar_numero(altura)
                    ax1.text(barra.get_x() + barra.get_width()/2., altura + 0.05 * altura, texto, ha='center', va='bottom', fontsize=10, fontweight='bold')
                
                # Gráfico Equipe
                metricas = ["Minuto", "Hora", "Dia (8h)"]
                valores = [
                    resultados["graficos"]["prod_eq_minuto"],
                    resultados["graficos"]["prod_eq_hora"],
                    resultados["graficos"]["prod_eq_dia"]
                ]
                barras_eq = ax2.bar(
                    metricas,
                    valores,
                    color=['#2ca02c', '#d62728', '#9467bd'],
                    edgecolor='black',
                    linewidth=1.2
                )
                ax2.set_ylabel("Peças por Equipe", fontsize=12)
                ax2.set_title("👥 Produtividade da Equipe", fontsize=14, pad=15)
                ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
                max_valor = max(valores)
                for i, barra in enumerate(barras_eq):
                    altura = barra.get_height()
                    ax2.text(barra.get_x() + barra.get_width()/2., altura + 0.05 * max_valor, formatar_numero(altura), ha='center', va='bottom', fontsize=10, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                
        except ValueError:
            st.error("🚨 Erro: Insira valores numéricos válidos para itens, tempo e colaboradores.")

# Rodapé
st.markdown("---")
st.markdown("**Desenvolvido para Perim Distribuidora | Contato: tiago.freitas@perimdistribuidora.com.br**", unsafe_allow_html=True)
