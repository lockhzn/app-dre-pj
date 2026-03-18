import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard DRE PJ 2026", layout="wide", page_icon="🏫")

# 2. Função Inteligente para ler o Excel/CSV brasileiro
@st.cache_data
def get_data():
    try:
        # Tenta ler com codificação do Windows (Latin-1) e detecta se é vírgula ou ponto e vírgula
        return pd.read_csv("escolas.csv", sep=None, engine='python', encoding='latin-1')
    except:
        # Se falhar, tenta o padrão internacional (UTF-8)
        return pd.read_csv("escolas.csv", sep=None, engine='python', encoding='utf-8-sig')

# 3. Início do App
st.title("🏫 Sistema de Gestão Educacional - DRE PJ")

try:
    df = get_data()
    
    # Criar a barra de seleção
    unidades_disponiveis = df['Unidade'].unique()
    unidade = st.selectbox("Selecione a Unidade Escolar:", unidades_disponiveis)
    
    # Filtrar os dados da unidade escolhida
    d = df[df['Unidade'] == unidade].iloc[0]

    # --- Organização Visual em Colunas ---
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### 📍 Identificação")
        st.info(f"**Tipo:** {d.get('Tipo', 'N/A')} \n\n **EOL:** {d.get('EOL', 'N/A')}")
        st.write(f"**Equipe Gestora:**\n{d.get('Equipe', 'Não informada')}")

    with col2:
        st.markdown("### 📊 Demanda e Inclusão")
        # Converte para número e evita erro se estiver vazio
        mat = pd.to_numeric(d['Matriculas'], errors='coerce') or 0
        vag = pd.to_numeric(d['Vagas'], errors='coerce') or 1
        st.metric("Matrículas Atuais", f"{int(mat)} / {int(vag)}")
        
        # Barra de progresso (limita entre 0 e 1 para não dar erro)
        percentual = min(max(float(mat/vag), 0.0), 1.0)
        st.progress(percentual)
        st.write(f"**Alunos com Deficiência:** {d.get('CEFAI_Deficiencia', 0)}")

    with col3:
        st.markdown("### 💰 Financeiro (PTRF)")
        valor_ptrf = pd.to_numeric(d['PTRF'], errors='coerce') or 0
        st.metric("Saldo Atual", f"R$ {valor_ptrf:,.2f}")
        if valor_ptrf == 0:
            st.warning("Unidade com saldo zerado.")

    st.divider()
    
    # 4. Área de Alertas
    st.markdown("### ⚖️ Assessoria Jurídica e Supervisão")
    processos = d.get('Processos', 'Sem informações registradas')
    if "Sem" in str(processos) or str(processos) == "nan":
        st.success("Nenhuma pendência crítica encontrada.")
    else:
        st.error(f"**Ocorrências:** {processos}")

except Exception as erro_geral:
    st.error(f"⚠️ Ocorreu um problema ao carregar os dados.")
    st.write(f"Detalhes técnicos: {erro_geral}")
    st.info("Dica: Verifique se a planilha 'escolas.csv' tem a coluna chamada 'Unidade'.")

# Rodapé
st.markdown("<br><hr><center><small>DRE PJ 2026 | Gestão de Dados</small></center>", unsafe_allow_html=True)
