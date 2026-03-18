import streamlit as st
import pandas as pd

# Configuração
st.set_page_config(page_title="Dashboard DRE PJ 2026", layout="wide", page_icon="🏫")

# Carregar Dados
@st.cache_data
def get_data():
    return pd.read_csv("escolas.csv")

try:
    df = get_data()
except:
    st.error("Erro: Certifique-se de que o arquivo 'escolas.csv' está na mesma pasta do código.")
    st.stop()

# Título e Filtro
st.title("🏫 Sistema de Gestão Educacional - DRE PJ")
unidade = st.selectbox("Selecione a Unidade Escolar para análise:", df['Unidade'].unique())

# Filtrar unidade específica
d = df[df['Unidade'] == unidade].iloc[0]

# --- Layout do App ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 📍 Identificação")
    st.info(f"**Tipo:** {d['Tipo']} \n\n **EOL:** {d['EOL']}")
    st.write(f"**Equipe Gestora:**\n{d['Equipe']}")

with col2:
    st.markdown("### 📊 Demanda e Inclusão")
    ocupacao = (d['Matriculas'] / d['Vagas'])
    st.metric("Matrículas", f"{d['Matriculas']} / {d['Vagas']}")
    st.progress(ocupacao)
    st.write(f"**Alunos com Deficiência (CEFAI):** {d['CEFAI_Deficiencia']}")

with col3:
    st.markdown("### 💰 Financeiro (PTRF)")
    if d['PTRF'] > 0:
        st.metric("Saldo Atual", f"R$ {d['PTRF']:,.2f}")
    else:
        st.warning("⚠️ Saldo PTRF Zerado")
        st.metric("Saldo Atual", "R$ 0,00")

st.markdown("---")

# Seção de Alertas Jurídicos/Supervisão
st.markdown("### ⚖️ Assessoria Jurídica e Supervisão")
if "Sem ocorrências" in d['Processos']:
    st.success("✅ Nenhuma pendência ou processo crítico registrado para esta unidade.")
else:
    st.error(f"**Ocorrências Registradas:**\n\n {d['Processos']}")

# Rodapé
st.markdown("<br><br><small>DRE PJ - Dados atualizados para o ciclo 2026</small>", unsafe_allow_html=True)
