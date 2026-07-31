import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Simulador QL & Produção - Aves Jarinu",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# AUTENTICAÇÃO E SESSÃO
# -----------------------------------------------------------------------------
USERS_DB = {
    "admin": {"pass": "admin123", "role": "Administrador", "name": "Gestor Industrial"},
    "planejamento": {"pass": "plan2026", "role": "Planejamento PCP", "name": "Analista de PCP"},
    "consulta": {"pass": "view123", "role": "Consulta", "name": "Visualizador"}
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_role"] = None
    st.session_state["user_name"] = None

def login():
    st.markdown("<h2 style='text-align: center; color: #1a365d;'>🐔 Simulador QL Aves - Unidade Jarinu</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 Autenticação de Acesso")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar", use_container_width=True):
            u = username.strip().lower()
            if u in USERS_DB and USERS_DB[u]["pass"] == password:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = USERS_DB[u]["role"]
                st.session_state["user_name"] = USERS_DB[u]["name"]
                st.success(f"Bem-vindo(a), {USERS_DB[u]['name']}! Perfil: {USERS_DB[u]['role']}")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# Logout na barra lateral
st.sidebar.markdown(f"**Usuário:** {st.session_state['user_name']}")
st.sidebar.markdown(f"**Perfil:** {st.session_state['user_role']}")
if st.sidebar.button("Sair / Logout"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")

# -----------------------------------------------------------------------------
# BANCO DE DADOS DE REFERÊNCIA DE POSTOS E EFICIÊNCIA
# -----------------------------------------------------------------------------
@st.cache_data
def get_initial_data():
    data = [
        # Abate & Pendura
        {"CC": "3481", "Setor": "Pendura/Sangria", "Atividade": "Descarregar Aves - Manual", "Tempo_Padrao_s": 0.56, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Pendura/Sangria", "Atividade": "Pendurar Aves", "Tempo_Padrao_s": 3.42, "Eficiencia_Op": 95.0, "QL_Aprovado": 5, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Pendura/Sangria", "Atividade": "Empilhar Gaiolas", "Tempo_Padrao_s": 0.27, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Pendura/Sangria", "Atividade": "Carregar Caminhão", "Tempo_Padrao_s": 0.30, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Pendura/Sangria", "Atividade": "Lavar Caminhão / Recolher Aves", "Tempo_Padrao_s": 0.14, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Pendura/Sangria", "Atividade": "Repassar Sangria", "Tempo_Padrao_s": 0.05, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Evisceração
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Operador Escalda/Depenadeira", "Tempo_Padrao_s": 0.15, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Revisar Aves Após Depenagem", "Tempo_Padrao_s": 0.54, "Eficiencia_Op": 90.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Rependurar Frango (Transferidor)", "Tempo_Padrao_s": 0.12, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Operador Linha de Evisceração", "Tempo_Padrao_s": 0.22, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Abastecer Máquina de Separar Miúdos", "Tempo_Padrao_s": 2.85, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Repassar Traquéia e Esôfago", "Tempo_Padrao_s": 0.21, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Revisar Frango PCC 2", "Tempo_Padrao_s": 1.20, "Eficiencia_Op": 90.0, "QL_Aprovado": 5, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Cortes Condicionais DIF", "Tempo_Padrao_s": 0.50, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3481", "Setor": "Evisceração/Chiller", "Atividade": "Operador Chiller", "Tempo_Padrao_s": 0.23, "Eficiencia_Op": 100.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Sala de Cortes - Primários
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Abastecer Cone", "Tempo_Padrao_s": 1.20, "Eficiencia_Op": 95.0, "QL_Aprovado": 2, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Deslocar Peito e Retirar Asas (Cone)", "Tempo_Padrao_s": 5.74, "Eficiencia_Op": 90.0, "QL_Aprovado": 12, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Retirar Asas (Cone)", "Tempo_Padrao_s": 2.84, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Retirar Peito (Cone)", "Tempo_Padrao_s": 2.53, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Retirar Pele do Peito (Cone)", "Tempo_Padrao_s": 2.80, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Riscar / Retirar Sassami (Cone)", "Tempo_Padrao_s": 5.20, "Eficiencia_Op": 90.0, "QL_Aprovado": 8, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3482", "Setor": "Cortes Primários", "Atividade": "Rependura Nórea Automática", "Tempo_Padrao_s": 2.15, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Produção de Peito
        {"CC": "3451", "Setor": "Peito", "Atividade": "Refilar Peito", "Tempo_Padrao_s": 9.10, "Eficiencia_Op": 90.0, "QL_Aprovado": 14, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3451", "Setor": "Peito", "Atividade": "Revisar / Classificar Peito Refilado", "Tempo_Padrao_s": 1.70, "Eficiencia_Op": 95.0, "QL_Aprovado": 3, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3451", "Setor": "Peito", "Atividade": "Embalar Peito Bloco", "Tempo_Padrao_s": 28.50, "Eficiencia_Op": 95.0, "QL_Aprovado": 5, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3451", "Setor": "Peito", "Atividade": "Abastecer Máquina Embaladora Contínua", "Tempo_Padrao_s": 1.95, "Eficiencia_Op": 95.0, "QL_Aprovado": 3, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Produção de Perna
        {"CC": "3450", "Setor": "Perna", "Atividade": "Desossar Perna (Manual)", "Tempo_Padrao_s": 32.57, "Eficiencia_Op": 85.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3450", "Setor": "Perna", "Atividade": "Separar Coxa / Sobrecoxa", "Tempo_Padrao_s": 8.50, "Eficiencia_Op": 95.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3450", "Setor": "Perna", "Atividade": "Abastecer Embaladora Contínua", "Tempo_Padrao_s": 1.95, "Eficiencia_Op": 95.0, "QL_Aprovado": 6, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Produção de Asa
        {"CC": "3452", "Setor": "Asa", "Atividade": "Abastecer Máquina Cortar Asas", "Tempo_Padrao_s": 2.09, "Eficiencia_Op": 95.0, "QL_Aprovado": 2, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3452", "Setor": "Asa", "Atividade": "Classificar Asas", "Tempo_Padrao_s": 0.51, "Eficiencia_Op": 95.0, "QL_Aprovado": 1, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3452", "Setor": "Asa", "Atividade": "Embalar Asa Pacote", "Tempo_Padrao_s": 17.88, "Eficiencia_Op": 90.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3452", "Setor": "Asa", "Atividade": "Interfolhar Asa Bloco", "Tempo_Padrao_s": 230.0, "Eficiencia_Op": 90.0, "QL_Aprovado": 2, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Embalagem & Paletização
        {"CC": "3483", "Setor": "Embalagem/Paletização", "Atividade": "Alimentar Esteira do Túnel", "Tempo_Padrao_s": 10.00, "Eficiencia_Op": 95.0, "QL_Aprovado": 2, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3483", "Setor": "Embalagem/Paletização", "Atividade": "Arrumar Pacotes na Caixa", "Tempo_Padrao_s": 3.50, "Eficiencia_Op": 95.0, "QL_Aprovado": 7, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3483", "Setor": "Embalagem/Paletização", "Atividade": "Tampar Caixas de Papelão", "Tempo_Padrao_s": 6.65, "Eficiencia_Op": 95.0, "QL_Aprovado": 2, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "3483", "Setor": "Embalagem/Paletização", "Atividade": "Paletizar Produtos", "Tempo_Padrao_s": 29.57, "Eficiencia_Op": 90.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        
        # Logística / Expedição
        {"CC": "212000", "Setor": "Logística/Expedição", "Atividade": "Carregar Caminhão", "Tempo_Padrao_s": 30.00, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "212000", "Setor": "Logística/Expedição", "Atividade": "Operar Empilhadeira / Paleteira", "Tempo_Padrao_s": 45.00, "Eficiencia_Op": 95.0, "QL_Aprovado": 2, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800},
        {"CC": "212000", "Setor": "Logística/Expedição", "Atividade": "Conferente", "Tempo_Padrao_s": 30.00, "Eficiencia_Op": 95.0, "QL_Aprovado": 4, "AFF_Percent": 7.0, "Volume_Hora_Aves": 4800}
    ]
    return pd.DataFrame(data)

# -----------------------------------------------------------------------------
# MENU LATERAL - NAVEGAÇÃO
# -----------------------------------------------------------------------------
menu = st.sidebar.radio("Navegação do Sistema", [
    "📊 Dashboard Executivo",
    "⚙️ Planejamento de Produção & SKUs",
    "🧮 Simulador de Quadro de Lotação (QL) & Eficiências",
    "❄️ Capacidade de Túneis & Girofreezer",
    "📋 Auditoria & Logs de Acesso"
])

# Load Session Data
if "df_posts" not in st.session_state:
    st.session_state["df_posts"] = get_initial_data()

# -----------------------------------------------------------------------------
# 1. DASHBOARD EXECUTIVO
# -----------------------------------------------------------------------------
if menu == "📊 Dashboard Executivo":
    st.title("📊 Painel Executivo - Simulador Industrial Aves (Jarinu)")
    st.markdown("Visão consolidada de produção, quadro de lotação e eficiências operacionais.")
    
    df = st.session_state["df_posts"].copy()
    
    # Recálculos no DataFrame
    df["Pecas_Hora_Nominal"] = 3600 / df["Tempo_Padrao_s"]
    df["Pecas_Hora_Efetiva"] = df["Pecas_Hora_Nominal"] * (df["Eficiencia_Op"] / 100.0)
    df["Carga_Trabalho"] = df["Volume_Hora_Aves"] / df["Pecas_Hora_Efetiva"]
    df["QL_Base"] = np.ceil(df["Carga_Trabalho"])
    df["QL_Ideal"] = np.ceil(df["QL_Base"] * (1 + df["AFF_Percent"] / 100.0))
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Volume Abate Diário", "45.000 aves/dia")
    col2.metric("Total QL Aprovado", f"{int(df['QL_Aprovado'].sum())} vagas")
    col3.metric("Total QL Ideal Simulada", f"{int(df['QL_Ideal'].sum())} vagas")
    
    desvio = int(df['QL_Ideal'].sum() - df['QL_Aprovado'].sum())
    col4.metric("Desvio de Quadro", f"{desvio:+d} vagas", delta_color="inverse")
    
    st.markdown("---")
    
    st.subheader("📌 Comparativo de Quadro de Lotação por Setor")
    df_setor = df.groupby("Setor")[["QL_Aprovado", "QL_Ideal"]].sum().reset_index()
    st.bar_chart(df_setor.set_index("Setor"))
    
    st.markdown("---")
    st.subheader("💡 Média de Eficiência Operacional por Setor")
    df_ef = df.groupby("Setor")["Eficiencia_Op"].mean().reset_index()
    st.dataframe(df_ef.style.format({"Eficiencia_Op": "{:.1f}%"}), use_container_width=True)

# -----------------------------------------------------------------------------
# 2. PLANEJAMENTO DE PRODUÇÃO & SKUS
# -----------------------------------------------------------------------------
elif menu == "⚙️ Planejamento de Produção & SKUs":
    st.title("⚙️ Parâmetros de Produção & Portfólio de SKUs")
    
    st.subheader("1. Parâmetros Gerais do Abatedouro")
    col1, col2, col3, col4 = st.columns(4)
    vol_dia = col1.number_input("Volume Aves / Dia", value=45000, step=1000)
    vel_linha = col2.number_input("Velocidade da Linha (frangos/hora)", value=4800, step=100)
    hrs_trabalhadas = col3.number_input("Horas Trabalhadas/Dia", value=9.575, step=0.1)
    dias_mes = col4.number_input("Dias Trabalhados / Mês", value=22, step=1)
    
    st.markdown("---")
    st.subheader("2. Distribuição por Família de Produtos & Rendimentos")
    
    skus_data = [
        {"SKU": "18228", "Item": "MOELA FRANGO CG ALM SE", "Família": "MIUDOS", "Subfamília": "MOELA PACOTE 1 KG", "Rendimento_%": 1.06, "Plano_Mensal_kg": 35712.0},
        {"SKU": "18163", "Item": "CORACAO FGO CG ALM SE", "Família": "MIUDOS", "Subfamília": "CORAÇÃO PACOTE 1 KG", "Rendimento_%": 0.47, "Plano_Mensal_kg": 12096.0},
        {"SKU": "209669", "Item": "FIGADO FG CG PCT", "Família": "MIUDOS", "Subfamília": "FÍGADO PACOTE 1 KG", "Rendimento_%": 1.75, "Plano_Mensal_kg": 42336.0},
        {"SKU": "45517", "Item": "PES DE FRANGO", "Família": "MIUDOS", "Subfamília": "PE 10 KG", "Rendimento_%": 2.33, "Plano_Mensal_kg": 68256.0},
        {"SKU": "220359", "Item": "MEIO PEITO S/OPF INTERF", "Família": "PEITO", "Subfamília": "Peito INTERF", "Rendimento_%": 21.70, "Plano_Mensal_kg": 408484.08},
        {"SKU": "990391", "Item": "FILE PTO FG RF BDJ PRM 600G", "Família": "PEITO", "Subfamília": "PEITO BDJ RF", "Rendimento_%": 21.47, "Plano_Mensal_kg": 1453.68},
        {"SKU": "15105", "Item": "FILE PEITO BDJ SE", "Família": "PEITO", "Subfamília": "PEITO BDJ", "Rendimento_%": 21.47, "Plano_Mensal_kg": 58147.20},
        {"SKU": "929883", "Item": "FILE DE PEITO FG CG PCT", "Família": "PEITO", "Subfamília": "Peito WIP", "Rendimento_%": 21.68, "Plano_Mensal_kg": 113387.04},
        {"SKU": "55364", "Item": "REC PEITO FGO CO MPL MP", "Família": "PEITO", "Subfamília": "PEITO 15 KG CG", "Rendimento_%": 21.70, "Plano_Mensal_kg": 11232.0},
        {"SKU": "14567", "Item": "FILE C/TENDAO", "Família": "SASSAMI", "Subfamília": "SASSAMI 1 KG", "Rendimento_%": 5.10, "Plano_Mensal_kg": 120657.60},
        {"SKU": "795259", "Item": "COXA SBCX C/O 15KG CG", "Família": "PERNA", "Subfamília": "Perna C/O WIP", "Rendimento_%": 24.54, "Plano_Mensal_kg": 676854.72},
        {"SKU": "14133", "Item": "ASA INT CG ITF SE", "Família": "ASA", "Subfamília": "ASA INTEIRA INTERF", "Rendimento_%": 7.81, "Plano_Mensal_kg": 87552.0},
        {"SKU": "14290", "Item": "MEIO ASA CG ALM SE", "Família": "ASA", "Subfamília": "MEIO DA ASA PACOTE 1 KG", "Rendimento_%": 2.95, "Plano_Mensal_kg": 56908.80},
        {"SKU": "18244", "Item": "COXINHA ASA CG ALM SE", "Família": "ASA", "Subfamília": "COXA DA ASA PACOTE 1 KG", "Rendimento_%": 4.03, "Plano_Mensal_kg": 73324.80},
        {"SKU": "997653", "Item": "CARNE MS AVES CG BL SE MP", "Família": "OUTROS", "Subfamília": "CMS", "Rendimento_%": 12.00, "Plano_Mensal_kg": 317088.00},
        {"SKU": "12645", "Item": "PELE DE FRANGO CG BL SE MP", "Família": "OUTROS", "Subfamília": "PELE 15KG", "Rendimento_%": 2.61, "Plano_Mensal_kg": 51552.00},
        {"SKU": "32421", "Item": "SAMBIQUIRA CG PCT", "Família": "OUTROS", "Subfamília": "SAMBIQUIRA 1 KG", "Rendimento_%": 0.56, "Plano_Mensal_kg": 20160.00}
    ]
    
    df_skus = pd.DataFrame(skus_data)
    df_skus["Plano_Hora_kg"] = df_skus["Plano_Mensal_kg"] / (dias_mes * hrs_trabalhadas)
    
    st.data_editor(
        df_skus,
        column_config={
            "Rendimento_%": st.column_config.NumberColumn("Rendimento (%)", format="%.2f %%"),
            "Plano_Mensal_kg": st.column_config.NumberColumn("Plano Mensal (kg)", format="%.2f kg"),
            "Plano_Hora_kg": st.column_config.NumberColumn("Plano Hora (kg/h)", format="%.2f kg/h")
        },
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 3. SIMULADOR DE QUADRO DE LOTAÇÃO & EFICIÊNCIA DOS POSTOS
# -----------------------------------------------------------------------------
elif menu == "🧮 Simulador de Quadro de Lotação (QL) & Eficiências":
    st.title("🧮 Simulador de Eficiência & Dimensionamento de Postos de Trabalho")
    st.markdown("""
    **Cálculo da Eficiência do Posto de Trabalho**:
    - **Capacidade Nominal (peças/h)** = $3600 / \text{Tempo Padrão (s)}$
    - **Capacidade Real (peças/h)** = $\text{Capacidade Nominal} \times (\text{Eficiência Operacional \%} / 100)$
    - **Carga de Trabalho** = $\text{Volume Solicitado (aves/h)} / \text{Capacidade Real}$
    - **QL Ideal** = $\lceil \text{Carga de Trabalho} \rceil \times (1 + \text{Fator AFF \%} / 100)$
    """)
    
    df = st.session_state["df_posts"].copy()
    
    # Filtro por Setor
    setores = ["Todos"] + list(df["Setor"].unique())
    setor_sel = st.selectbox("Filtrar por Setor de Produção:", setores)
    
    if setor_sel != "Todos":
        df_sub = df[df["Setor"] == setor_sel]
    else:
        df_sub = df
        
    st.subheader("Inputs de Eficiência & Parâmetros por Posto")
    edited_df = st.data_editor(
        df_sub[["CC", "Setor", "Atividade", "Tempo_Padrao_s", "Eficiencia_Op", "AFF_Percent", "QL_Aprovado", "Volume_Hora_Aves"]],
        column_config={
            "Tempo_Padrao_s": st.column_config.NumberColumn("Tempo Padrão (s)", min_value=0.01, max_value=600.0, format="%.2f s"),
            "Eficiencia_Op": st.column_config.NumberColumn("Eficiência Op. (%)", min_value=10.0, max_value=100.0, format="%.1f %%"),
            "AFF_Percent": st.column_config.NumberColumn("Fator AFF (%)", min_value=0.0, max_value=30.0, format="%.1f %%"),
            "QL_Aprovado": st.column_config.NumberColumn("QL Aprovado", min_value=0, max_value=100),
            "Volume_Hora_Aves": st.column_config.NumberColumn("Volume (aves/h)", min_value=0, max_value=20000)
        },
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Atualiza sessão
    st.session_state["df_posts"].update(edited_df)
    
    # Exibe Resultados Calculados
    st.markdown("---")
    st.subheader("📈 Resultado da Simulação em Tempo Real")
    
    res_df = edited_df.copy()
    res_df["Pecas_Hora_Nominal"] = 3600.0 / res_df["Tempo_Padrao_s"]
    res_df["Pecas_Hora_Real"] = res_df["Pecas_Hora_Nominal"] * (res_df["Eficiencia_Op"] / 100.0)
    res_df["Carga_Trabalho"] = res_df["Volume_Hora_Aves"] / res_df["Pecas_Hora_Real"]
    res_df["QL_Base"] = np.ceil(res_df["Carga_Trabalho"])
    res_df["QL_Ideal"] = np.ceil(res_df["QL_Base"] * (1.0 + res_df["AFF_Percent"] / 100.0))
    res_df["Desvio_QL"] = res_df["QL_Ideal"] - res_df["QL_Aprovado"]
    
    st.dataframe(
        res_df[["CC", "Setor", "Atividade", "Pecas_Hora_Nominal", "Pecas_Hora_Real", "Carga_Trabalho", "QL_Aprovado", "QL_Ideal", "Desvio_QL"]].style.format({
            "Pecas_Hora_Nominal": "{:.0f} pc/h",
            "Pecas_Hora_Real": "{:.0f} pc/h",
            "Carga_Trabalho": "{:.2f}",
            "QL_Aprovado": "{:.0f}",
            "QL_Ideal": "{:.0f}",
            "Desvio_QL": "{:+d}"
        }),
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 4. CAPACIDADE DE TÚNEIS & GIROFREEZER
# -----------------------------------------------------------------------------
elif menu == "❄️ Capacidade de Túneis & Girofreezer":
    st.title("❄️ Ocupação e Capacidade de Congelamento")
    
    st.subheader("Túneis Contínuos, Estáticos e Girofreezer")
    
    tuneis_data = [
        {"Equipamento": "MQ.TUNEL DE CG (CONTINUO) 1", "Tipo": "Contínuo", "Capacidade_Nominal_kg_h": 3000, "Carga_Atual_kg_h": 2272, "Horas_Disponiveis": 17.0},
        {"Equipamento": "MQ.TUNEL DE CG (CONTINUO) 2", "Tipo": "Contínuo", "Capacidade_Nominal_kg_h": 3000, "Carga_Atual_kg_h": 2272, "Horas_Disponiveis": 17.0},
        {"Equipamento": "MQ.TUNEL DE CG (ESTATICO) 1", "Tipo": "Estático", "Capacidade_Nominal_kg_h": 1500, "Carga_Atual_kg_h": 1200, "Horas_Disponiveis": 24.0},
        {"Equipamento": "MQ.GIROFREEZER 1", "Tipo": "Girofreezer/IQF", "Capacidade_Nominal_kg_h": 3500, "Carga_Atual_kg_h": 2286, "Horas_Disponiveis": 17.0},
        {"Equipamento": "MQ.GIROFREEZER 2", "Tipo": "Girofreezer/IQF", "Capacidade_Nominal_kg_h": 3500, "Carga_Atual_kg_h": 2286, "Horas_Disponiveis": 17.0}
    ]
    
    df_tuneis = pd.DataFrame(tuneis_data)
    df_tuneis["Ocupacao_%"] = (df_tuneis["Carga_Atual_kg_h"] / df_tuneis["Capacidade_Nominal_kg_h"]) * 100.0
    df_tuneis["Horas_Ocupadas"] = (df_tuneis["Carga_Atual_kg_h"] * df_tuneis["Horas_Disponiveis"]) / df_tuneis["Capacidade_Nominal_kg_h"]
    
    st.data_editor(
        df_tuneis,
        column_config={
            "Capacidade_Nominal_kg_h": st.column_config.NumberColumn("Capacidade Nominal (kg/h)"),
            "Carga_Atual_kg_h": st.column_config.NumberColumn("Carga Atual (kg/h)"),
            "Ocupacao_%": st.column_config.NumberColumn("Ocupação (%)", format="%.1f %%"),
            "Horas_Ocupadas": st.column_config.NumberColumn("Horas Necessárias", format="%.2f h")
        },
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 5. AUDITORIA & LOGS
# -----------------------------------------------------------------------------
elif menu == "📋 Auditoria & Logs de Acesso":
    st.title("📋 Registro de Logs & Exportação de Dados")
    
    st.markdown("Historico de alterações e exportação dos relatórios da simulação.")
    
    logs = [
        {"Data/Hora": "2026-07-30 02:10:00", "Usuário": "Gestor Industrial", "Perfil": "Administrador", "Ação": "Login Efetuado"},
        {"Data/Hora": "2026-07-30 02:12:15", "Usuário": "Gestor Industrial", "Perfil": "Administrador", "Ação": "Ajuste de Eficiência no Refile de Peito (90%)"},
        {"Data/Hora": "2026-07-30 02:15:30", "Usuário": "Analista de PCP", "Perfil": "Planejamento PCP", "Ação": "Simulação QL Executada"}
    ]
    st.table(pd.DataFrame(logs))
    
    st.markdown("---")
    st.subheader("📥 Exportar Resultados da Simulação")
    
    csv = st.session_state["df_posts"].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Relatório QL em CSV",
        data=csv,
        file_name="Simulacao_QL_Aves_Jarinu.csv",
        mime="text/csv"
    )

