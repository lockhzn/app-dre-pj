import streamlit as st
import pandas as pd

# Configuração
st.set_page_config(page_title="Dashboard DRE PJ 2026", layout="wide", page_icon="🏫")

# Função de carregamento "Inteligente"
@st.cache_data
def get_data():
    # Tenta detectar automaticamente se é vírgula ou ponto e vírgula
    return pd.read_csv("escolas.csv", sep=None, engine='python', encoding='utf-8-sig')

st.title("🏫 Sistema de Gestão Educacional - DRE PJ")

try:
    df = get_data()
    
    # Filtro de Unidade
    unidade = st.selectbox("Selecione a Unidade Escolar:", df['Unidade'].unique())
    d = df[df['Unidade'] == unidade].iloc[0]

    # --- Layout ---
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### 📍 Identificação")
        st.info(f"**Tipo:** {d['Tipo']} \n\n **EOL:** {d['EOL']}")
        st.write(f"**Equipe Gestora:**\n{d['Equipe']}")

    with col2:
        st.markdown("### 📊 Demanda e Inclusão")
        # Tratando caso o valor não seja número
        mat = pd.to_numeric(d['Matriculas'], errors='coerce') or 0
        vag = pd.to_numeric(d['Vagas'], errors='coerce') or 1
        st.metric("Matrículas", f"{int(mat)} / {int(vag)}")
        st.progress(min(float(mat/vag), 1.0))

    with col3:
        st.markdown("### 💰 Financeiro (PTRF)")
        valor_ptrf = pd.to_numeric(d['PTRF'], errors='coerce') or 0
        st.metric("Saldo Atual", f"R$ {valor_ptrf:,.2f}")

    st.divider()
    st.markdown("### ⚖️ Assessoria Jurídica e Supervisão")
    st.warning(d['Processos'])

except Exception as e:
    st.error(f"⚠️ Erro ao ler os dados: {e}")
    st.info("Dica: Verifique se o nome das colunas no Excel está exatamente igual ao original.")
