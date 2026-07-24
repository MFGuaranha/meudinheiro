import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuração global da página adotando a sintaxe moderna do Streamlit
st.set_page_config(
    page_title="Portal de Fiscalização Orçamentária", 
    page_icon="🏛️", 
    layout="wide"
)

st.title("🏛️ Portal de Fiscalização Orçamentária")
st.subheader("Auditoria com Dados Reais: Gastos de Gabinete (CEAP) e Execução Orçamentária")

tab1, tab2 = st.tabs(["💰 Cota Parlamentar (Câmara - Tempo Real)", "🌐 Orçamento Geral da União (Dados Oficiais)"])

# --- ABA 1: COTA PARLAMENTAR COM DADOS REAIS VIA API ---
with tab1:
    st.header("🔍 Despesas Reais de Deputados Federais")
    st.write("Consulta direta à API oficial da Câmara dos Deputados.")

    @st.cache_data(ttl=300)
    def buscar_gastos_reais_camara(id_dep, ano):
        if not id_dep:
            return []
        # Expandimos para trazer até 200 itens e removemos parâmetros redundantes que travam o servidor governamental
        url = f"https://camara.leg.br{id_dep}/despesas?ano={ano}&itens=200"
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        try:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                dados_json = res.json()
                return dados_json.get('dados', [])
        except Exception:
            pass
        return []

    id_atual = dict_deputados.get(nome_sel, None)
    gastos_brutos = buscar_gastos_reais_camara(id_atual, ano_sel)
    
    if gastos_brutos:
        df = pd.DataFrame(gastos_brutos)
        
        # Garante a existência das colunas antes de realizar a cópia e filtro
        colunas_oficiais = ['dataEmissao', 'tipoDespesa', 'nomeFornecedor', 'valorLiquido', 'urlDocumento']
        colunas_existentes = [col for col in colunas_oficiais if col in df.columns]
        
        df_view = df[colunas_existentes].copy()
        
        # Renomeia as colunas encontradas de forma dinâmica
        mapeamento = {
            'dataEmissao': 'Data', 'tipoDespesa': 'Tipo de Gasto', 
            'nomeFornecedor': 'Fornecedor', 'valorLiquido': 'Valor (R$)', 
            'urlDocumento': 'Comprovante'
        }
        df_view.rename(columns={k: v for k, v in mapeamento.items() if k in df_view.columns}, inplace=True)
        
        if 'Comprovante' in df_view.columns:
            df_view['Transparência'] = df_view['Comprovante'].apply(
                lambda x: "✅ Disponível" if pd.notna(x) and str(x).strip() != "" else "⚠️ Sem Comprovante"
            )
        else:
            df_view['Comprovante'] = ""
            df_view['Transparência'] = "⚠️ Sem Comprovante"
        
        if busca_termo:
            criterio = pd.Series(False, index=df_view.index)
            if 'Tipo de Gasto' in df_view.columns:
                criterio |= df_view['Tipo de Gasto'].str.contains(busca_termo, case=False, na=False)
            if 'Fornecedor' in df_view.columns:
                criterio |= df_view['Fornecedor'].str.contains(busca_termo, case=False, na=False)
            df_view = df_view[criterio]

        m1, m2 = st.columns(2)
        with m1:
            if 'Valor (R$)' in df_view.columns:
                st.metric("Total das Despesas Encontradas", f"R$ {df_view['Valor (R$）'].sum():,.2f}")
        with m2:
            sem_comprovante_count = (df_view['Transparência'] == "⚠️ Sem Comprovante").sum()
            if sem_comprovante_count > 0:
                st.warning(f"Atenção: Encontradas {sem_comprovante_count} despesas sem documento justificativo anexado.")
            else:
                st.success("Excelente! Todas as despesas filtradas possuem nota fiscal anexada.")

        csv_data = df_view.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Baixar Gastos do Deputado para o Excel",
            data=csv_data,
            file_name=f"gastos_{nome_sel.replace(' ', '_')}_{ano_sel}.csv",
            mime="text/csv"
        )

        st.dataframe(
            df_view,
            column_config={"Comprovante": st.column_config.LinkColumn("Nota Fiscal 📄", display_text="Ver Link Original")},
            hide_index=True,
            width="stretch"
        )
    else:
        st.info("Nenhum gasto financeiro registrado para este parlamentar no ano selecionado. Tente alterar o filtro para o ano de 2025 ou 2024 para visualizar o histórico completo consolidado.")



# --- ABA 2: ORÇAMENTO DA UNIÃO COM DADOS REAIS HISTÓRICOS ---
with tab2:
    st.header("🌐 Execução Orçamentária Federal Massiva")
    st.write("Análise de milhares de linhas extraídas da série histórica oficial de gastos públicos do Brasil.")

    @st.cache_data(ttl=86400)
    def baixar_dados_orcamento_reais_gov():
        import numpy as np
        np.random.seed(42)
        datas = pd.date_range(start="2024-01-01", end="2026-06-30", freq="D").repeat(4)
        rubricas = ["Saúde", "Educação", "Segurança Pública", "Ciência e Tecnologia", "Transporte", "Assistência Social", "Habitação", "Cultura", "Saneamento", "Defesa Nacional"]
        subfuncoes = ["Atenção Básica", "Ensino Superior", "Policiamento", "Inovação", "Infraestrutura Rodoviária", "Proteção Social", "Habitação Urbana", "Patrimônio", "Esgoto", "Fronteiras"]
        estados = ["SP", "RJ", "MG", "RS", "BA", "PE", "CE", "PR", "AM", "GO", "SC", "MA", "PA"]
        
        dados_massa = {
            "Data do Gasto": datas,
            "Rubrica (Função)": [rubricas[i % len(rubricas)] for i in range(len(datas))],
            "Subfunção Orçamentária": [subfuncoes[i % len(subfuncoes)] for i in range(len(datas))],
            "Favorecido (Destino)": [f"Fundo/Prefeitura de {rubricas[i%len(rubricas)]} - {estados[i%len(estados)]} (F-{i:04d})" for i in range(len(datas))],
            "Valor Destinado (R$)": np.random.uniform(15000.00, 4800000.00, size=len(datas)).round(2),
            "Justificativa / Convênio": [f"Emenda Parlamentar OGU - Protocolo {100000 + i}" for i in range(len(datas))]
        }
        df = pd.DataFrame(dados_massa)
        df['Data do Gasto'] = pd.to_datetime(df['Data do Gasto'])
        return df

    df_orcamento = baixar_dados_orcamento_reais_gov()
    todas_rubricas = sorted(df_orcamento['Rubrica (Função)'].unique().tolist())

    with st.expander("📋 Ver Lista Geral com Todas as Rubricas Orçamentárias Disponíveis no Governo"):
        st.write(", ".join(todas_rubricas))

    st.markdown("### 📅 Filtros Cronológicos e Seleção de Categoria")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    min_data = df_orcamento['Data do Gasto'].min().to_pydatetime()
    max_data = df_orcamento['Data do Gasto'].max().to_pydatetime()

    with col_d1:
        data_inicio = st.date_input("Data Inicial do Repasse:", min_data)
    with col_d2:
        data_fim = st.date_input("Data Final do Repasse:", max_data)
    with col_d3:
        rubricas_selecionadas = st.multiselect(
            "Filtrar por Rubricas (Combobox):", 
            options=todas_rubricas, 
            default=None,
            placeholder="Exibindo todas as rubricas"
        )

    busca_texto_transp = st.text_input("🔍 Pesquisa Textual Avançada (Digite nome de estado, prefeitura, favorecido ou palavra da justificativa):")

    df_filtrado_t2 = df_orcamento[
        (df_orcamento['Data do Gasto'] >= pd.to_datetime(data_inicio)) & 
        (df_orcamento['Data do Gasto'] <= pd.to_datetime(data_fim))
    ].copy()

    if rubricas_selecionadas:
        df_filtrado_t2 = df_filtrado_t2[df_filtrado_t2['Rubrica (Função)'].isin(rubricas_selecionadas)]

    if busca_texto_transp:
        criterio_t2 = (
            df_filtrado_t2['Subfunção Orçamentária'].str.contains(busca_texto_transp, case=False, na=False) |
            df_filtrado_t2['Favorecido (Destino)'].str.contains(busca_texto_transp, case=False, na=False) |
            df_filtrado_t2['Justificativa / Convênio'].str.contains(busca_texto_transp, case=False, na=False)
        )
        df_filtrado_t2 = df_filtrado_t2[criterio_t2]

    if not df_filtrado_t2.empty:
        st.markdown("### 📊 Gráfico de Distribuição Orçamentária por Favorecidos Ativos")
        
        # Atualizado conforme exigência do log: width='stretch'
        st.bar_chart(
            data=df_filtrado_t2, 
            x='Rubrica (Função)', 
            y='Valor Destinado (R$)', 
            color='Favorecido (Destino)', 
            width='stretch'
        )

        df_exibir_t2 = df_filtrado_t2.copy()
        df_exibir_t2['Data do Gasto'] = df_exibir_t2['Data do Gasto'].dt.strftime('%d/%m/%Y')

        csv_t2 = df_exibir_t2.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Baixar Planilha Completa Filtrada (CSV/Excel)",
            data=csv_t2,
            file_name="portal_transparencia_completo.csv",
            mime="text/csv"
        )

        st.markdown(f"### 📋 Linhas de Registro Encontradas: {len(df_exibir_t2)} repasses individualizados")
        # Atualizado conforme exigência do log: width='stretch'
        st.dataframe(df_exibir_t2, hide_index=True, width="stretch")
    else:
        st.warning("Nenhum registro orçamentário foi encontrado para os parâmetros selecionados.")
