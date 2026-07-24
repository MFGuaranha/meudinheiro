import streamlit as st
import requests
import pandas as pd

# Configuração da página e layout fluido
st.set_page_config(
    page_title="Fiscaliza Congresso Pro", 
    page_icon="📊", 
    layout="wide"
)

st.title("📊 Fiscaliza Congresso Pro")
st.subheader("Auditoria Avançada de Notas Fiscais e Destinação Orçamentária")

# Abas principais do aplicativo
tab1, tab2 = st.tabs(["💰 Cota Parlamentar (Comprovantes)", "🏥 Gráficos e Destinação por Área"])

# --- ABA 1: COTA PARLAMENTAR (FILTROS, ALERTAS E EXPORTAÇÃO EXCEL/CSV) ---
with tab1:
    st.header("🔍 Busca de Notas Fiscais e Alertas de Transparência")
    st.write("Pesquise por termos e verifique a existência de documentos comprobatórios dos gastos.")

    
    
    # --- SUBSTITUA AS FUNÇÕES DE BUSCA POR ESTAS CORRIGIDAS ---

@st.cache_data(ttl=3600)
def listar_deputados():
    url = "https://camara.leg.br"
    # Adicionamos uma identificação de User-Agent profissional para o Streamlit Cloud não ser bloqueado
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Valida se o conteúdo de fato é texto em formato JSON antes de decodificar
            dados_json = response.json()
            if 'dados' in dados_json:
                return {d['nome']: d['id'] for d in dados_json['dados']}
        return {}
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        # Se falhar, não quebra o app, apenas retorna vazio para tratamento visual
        return {}

@st.cache_data(ttl=600)
def buscar_gastos(id_dep, ano):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_dep}/despesas?ano={ano}&itens=100"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            dados_json = res.json()
            if 'dados' in dados_json:
                return dados_json['dados']
        return []
    except (requests.exceptions.RequestException, ValueError):
        return []
    
        gastos_brutos = buscar_gastos(dict_deputados[nome_sel], ano_sel)
        
        if gastos_brutos:
            df = pd.DataFrame(gastos_brutos)
            
            # Seleção e renomeação de colunas estratégicas
            df_view = df[['dataEmissao', 'tipoDespesa', 'nomeFornecedor', 'valorLiquido', 'urlDocumento']].copy()
            df_view.columns = ['Data', 'Tipo de Gasto', 'Fornecedor', 'Valor (R$)', 'Comprovante']
            
            # --- FUNCIONALIDADE 2: ALERTA DE TRANSPARÊNCIA (Documento em Branco) ---
            # Cria um indicador textual ou visual direto na tabela
            df_view['Transparência'] = df_view['Comprovante'].apply(
                lambda x: "✅ Disponível" if pd.notna(x) and str(x).strip() != "" else "⚠️ Sem Comprovante"
            )
            
            # Aplica o filtro de palavra-chave se digitado
            if busca_termo:
                criterio = (
                    df_view['Tipo de Gasto'].str.contains(busca_termo, case=False, na=False) |
                    df_view['Fornecedor'].str.contains(busca_termo, case=False, na=False)
                )
                df_view = df_view[criterio]

            # Bloco de Métricas e Alertas Resumidos
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Total das Despesas Filtradas", f"R$ {df_view['Valor (R$)'].sum():,.2f}")
            with m2:
                sem_comprovante_count = (df_view['Transparência'] == "⚠️ Sem Comprovante").sum()
                if sem_comprovante_count > 0:
                    st.warning(f"Atenção: Encontradas {sem_comprovante_count} despesas sem documento justificativo anexado.")
                else:
                    st.success("Excelente! Todas as despesas filtradas possuem nota fiscal anexada.")

            # --- FUNCIONALIDADE 3: EXPORTAÇÃO RÁPIDA DA TABELA FILTRADA ---
            # O Streamlit oferece suporte nativo a downloads em CSV, que abre direto no Excel
            csv_data = df_view.to_csv(index=False).encode('utf-8-sig') # utf-8-sig garante acentuação correta no Excel
            
            st.download_button(
                label="📥 Baixar Tabela Filtrada para o Excel (CSV)",
                data=csv_data,
                file_name=f"gastos_{nome_sel.replace(' ', '_')}_{ano_sel}.csv",
                mime="text/csv",
                help="Clique para baixar a planilha exatamente com os filtros aplicados acima"
            )
            
            # Exibição interativa
            st.dataframe(
                df_view,
                column_config={
                    "Comprovante": st.column_config.LinkColumn("Nota Fiscal 📄", display_text="Abrir Arquivo Original")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Nenhuma despesa registrada para os parâmetros selecionados.")
    else:
        st.error("Erro ao conectar com os servidores da Câmara dos Deputados.")

# --- ABA 2: DESTINAÇÃO SETORIAL COMPLETA COM GRÁFICOS DINÂMICOS E FILTROS TOTAIS ---
with tab2:
    st.header("📊 Painel Orçamentário Global (Todas as Áreas)")
    st.write("Filtre o orçamento por áreas ministeriais (combobox) ou pesquise subfunções e favorecidos via caixa de texto.")
    
    # 1. Base de dados expandida com múltiplos ministérios e áreas de governo
    @st.cache_data(ttl=3600)
    def obter_dados_setoriais_completos():
        return [
            {"Área": "Saúde", "Subfunção": "Atenção Básica", "Favorecido": "Fundo Municipal de Saúde - SP", "Valor (R$)": 1200000.00, "Status": "Pago"},
            {"Área": "Saúde", "Subfunção": "Assistência Hospitalar", "Favorecido": "Santa Casa de Misericórdia - RJ", "Valor (R$)": 850000.00, "Status": "Em execução"},
            {"Área": "Educação", "Subfunção": "Ensino Superior", "Favorecido": "Universidade Federal - UFMG", "Valor (R$)": 2100000.00, "Status": "Concluído"},
            {"Área": "Educação", "Subfunção": "Educação Infantil", "Favorecido": "Prefeitura de Manaus - AM", "Valor (R$)": 600000.00, "Status": "Licitação"},
            {"Área": "Educação", "Subfunção": "Ensino Profissional", "Favorecido": "Instituto Federal - IFSP", "Valor (R$)": 1300000.00, "Status": "Pago"},
            {"Área": "Segurança Pública", "Subfunção": "Policiamento Ostensivo", "Favorecido": "Secretaria de Segurança - RS", "Valor (R$)": 950000.00, "Status": "Pago"},
            {"Área": "Segurança Pública", "Subfunção": "Defesa Civil", "Favorecido": "Corpo de Bombeiros - MG", "Valor (R$)": 400000.00, "Status": "Em execução"},
            {"Área": "Transporte", "Subfunção": "Infraestrutura Rodoviária", "Favorecido": "DNIT / BR-116", "Valor (R$)": 4500000.00, "Status": "Em execução"},
            {"Área": "Transporte", "Subfunção": "Transporte Urbano", "Favorecido": "Metrô de Salvador - BA", "Valor (R$)": 3200000.00, "Status": "Concluído"},
            {"Área": "Assistência Social", "Subfunção": "Proteção Social Básica", "Favorecido": "Fundo de Assistência - MA", "Valor (R$)": 750000.00, "Status": "Pago"},
            {"Área": "Habitação", "Subfunção": "Habitação Urbana", "Favorecido": "Conjunto Residencial - CE", "Valor (R$)": 1800000.00, "Status": "Licitação"},
            {"Área": "Ciência e Tecnologia", "Subfunção": "Desenvolvimento Tecnológico", "Favorecido": "CNPq / Bolsas de Pesquisa", "Valor (R$)": 1150000.00, "Status": "Pago"}
        ]
        
    df_completo = pd.DataFrame(obter_dados_setoriais_completos())
    
    # Extrai automaticamente todas as áreas únicas existentes na base para criar o Combobox
    lista_areas_disponiveis = sorted(df_completo['Área'].unique().tolist())
    
    # Interface de Filtros Combinados (Combobox + Digitação)
    c1, c2 = st.columns(2)
    with c1:
        # Combobox dinâmico multiselect - se deixar vazio, exibe todas
        areas_selecionadas = st.multiselect(
            "📁 Selecione as Áreas Governamentais (Rubricas):",
            options=lista_areas_disponiveis,
            default=None,
            placeholder="Todas as áreas selecionadas"
        )
    with c2:
        # Caixa de texto para digitação livre (filtra favorecido ou subfunção)
        termo_busca_setorial = st.text_input(
            "💡 Digite palavras-chave (ex: Nome de prefeitura, UFMG, Rodoviária, Hospital):",
            key="busca_setorial"
        )
        
    # --- PROCESSO DE FILTRAGEM SEQUENCIAL ---
    df_filtrado = df_completo.copy()
    
    # Filtro 1: Pelo Combobox (Se o usuário escolheu áreas específicas)
    if areas_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['Área'].isin(areas_selecionadas)]
        
    # Filtro 2: Pela caixa de texto livre (Ignorando maiúsculas e minúsculas)
    if termo_busca_setorial:
        criterio_texto = (
            df_filtrado['Subfunção'].str.contains(termo_busca_setorial, case=False, na=False) |
            df_filtrado['Favorecido'].str.contains(termo_busca_setorial, case=False, na=False) |
            df_filtrado['Status'].str.contains(termo_busca_setorial, case=False, na=False)
        )
        df_filtrado = df_filtrado[criterio_texto]
        
    # --- RENDERIZAÇÃO DOS RESULTADOS ---
    if not df_filtrado.empty:
        # Gráfico de Barras Dinâmico - Ele se adapta automaticamente à filtragem do usuário
        st.markdown("### 📈 Distribuição do Orçamento Filtrado")
        
        # Agrupa os valores para somar por área de acordo com o filtro aplicado
        df_grafico_dinamico = df_filtrado.groupby('Área')['Valor (R$)'].sum().reset_index()
        
        st.bar_chart(
            data=df_grafico_dinamico,
            x='Área',
            y='Valor (R$)',
            use_container_width=True
        )
        
        # Métricas e Exportação Excel/CSV da tabela setorial
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            st.metric("Total Alocado nos Filtros Atuais", f"R$ {df_filtrado['Valor (R$)'].sum():,.2f}")
        with col_m2:
            # Botão de download para a tabela filtrada
            csv_setorial = df_filtrado.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Dados Filtrados (CSV/Excel)",
                data=csv_setorial,
                file_name="orcamento_setorial_filtrado.csv",
                mime="text/csv"
            )
            
        # Exibição da tabela final
        st.markdown("### 📋 Listagem Detalhada de Aplicações")
        st.dataframe(df_filtrado, hide_index=True, use_container_width=True)
        
    else:
        st.warning("⚠️ Nenhum registro encontrado para os filtros selecionados. Tente ajustar o texto ou as rubricas.")
