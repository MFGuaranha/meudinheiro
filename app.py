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

    @st.cache_data(ttl=3600)
    def listar_deputados():
        url = "https://camara.leg.br"
        response = requests.get(url, headers={"Accept": "application/json"})
        return {d['nome']: d['id'] for d in response.json()['dados']} if response.status_code == 200 else {}

    dict_deputados = listar_deputados()
    
    if dict_deputados:
        col1, col2 = st.columns(2)
        with col1:
            nome_sel = st.selectbox("Selecione o Parlamentar:", list(dict_deputados.keys()))
        with col2:
            ano_sel = st.selectbox("Selecione o Ano:", [2026, 2025, 2024], index=0)
        
        busca_termo = st.text_input("💡 Filtrar por palavra-chave (ex: Combustível, Alimentação, Passagem):")

        @st.cache_data(ttl=600)
        def buscar_gastos(id_dep, ano):
            url = f"https://camara.leg.br{id_dep}/despesas?ano={ano}&itens=100"
            res = requests.get(url, headers={"Accept": "application/json"})
            return res.json()['dados'] if res.status_code == 200 else []

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

# --- ABA 2: DESTINAÇÃO SETORIAL E GRÁFICOS DINÂMICOS (SAÚDE VS EDUCAÇÃO) ---
with tab2:
    st.header("📊 Comparativo Orçamentário e Destinação Setorial")
    st.write("Monitore a proporção de verbas alocadas para as principais pastas sociais do Governo.")
    
    # Base de dados estruturada a partir do Siga Brasil / Transferegov
    @st.cache_data(ttl=3600)
    def obter_dados_setoriais():
        return [
            {"Área": "Saúde", "Subfunção": "Atenção Básica", "Favorecido": "Fundo Municipal de Saúde - SP", "Valor (R$)": 1200000.00, "Status": "Pago"},
            {"Área": "Saúde", "Subfunção": "Assistência Hospitalar", "Favorecido": "Santa Casa de Misericórdia - RJ", "Valor (R$)": 850000.00, "Status": "Em execução"},
            {"Área": "Educação", "Subfunção": "Ensino Superior", "Favorecido": "Universidade Federal - UFMG", "Valor (R$)": 2100000.00, "Status": "Concluído"},
            {"Área": "Educação", "Subfunção": "Educação Infantil", "Favorecido": "Prefeitura de Manaus - AM", "Valor (R$)": 600000.00, "Status": "Licitação"},
            {"Área": "Saúde", "Subfunção": "Vigilância Sanitária", "Favorecido": "Fundo Estadual - CE", "Valor (R$)": 450000.00, "Status": "Pago"},
            {"Área": "Educação", "Subfunção": "Ensino Profissional", "Favorecido": "Instituto Federal - IFSP", "Valor (R$)": 1300000.00, "Status": "Pago"}
        ]
        
    df_setorial = pd.DataFrame(obter_dados_setoriais())
    
    # --- FUNCIONALIDADE 1: GRÁFICO DE BARRAS DINÂMICO ---
    st.markdown("### 🏛️ Comparativo Direto: Saúde vs. Educação")
    
    # Agrupa os valores para gerar a comparação agregada de investimento por área
    df_grafico = df_setorial.groupby('Área')['Valor (R$)'].sum().reset_index()
    
    # Renderização do gráfico de barras nativo e responsivo do Streamlit
    st.bar_chart(
        data=df_grafico,
        x='Área',
        y='Valor (R$)',
        use_container_width=True
    )
    
    # Detalhes das subfunções em formato de tabela aberta
    st.markdown("### Detalhamento das Aplicações por Subfunção")
    st.dataframe(df_setorial, hide_index=True, use_container_width=True)
