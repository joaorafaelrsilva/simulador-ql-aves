# Simulador de Quadro de Lotação (QL) & Produção de Aves - Unidade Jarinu


Este é o sistema completo em Python (Streamlit) baseado na planilha de simulação industrial `JAR_Aves&2026Fev.xlsx`.


## 🚀 Como Executar no GitHub Codespaces / Servidor Online


1. Clone ou abra este repositório no **GitHub Codespaces** (`simulador-ql-aves`).
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```
4. O link público em tempo real estará disponível na porta `8501`:
   `https://stunning-waddle-69jrqvj9g59gfrqpp-8501.app.github.dev/`


## 🔑 Credenciais de Acesso
- **Administrador**: Usuário: `admin` | Senha: `admin123`
- **Planejamento PCP**: Usuário: `planejamento` | Senha: `plan2026`
- **Consulta**: Usuário: `consulta` | Senha: `view123`


## 📊 Funcionalidades
- **Dashboard Executivo**: KPIs de abate, desvio de quadro e eficiências por setor.
- **Planejamento de SKUs**: Tabela editável dos 21 SKUs de frango com cálculo de rendimentos e volumes kg/h.
- **Simulador de QL & Eficiência dos Postos**: Inputs de tempo padrão (s), % eficiência operacional, fator AFF (%) e recálculo do QL Ideal em tempo real.
- **Capacidade de Túneis & Girofreezer**: Ocupação de túneis contínuos, estáticos e girofreezers.
- **Logs & Exportação**: Registro de acessos e download de relatórios em CSV/Excel.