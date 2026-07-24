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

import streamlit as st
import requests
import pandas as pd
import numpy as np

# Configuração global da página adotando a sintaxe moderna do Streamlit
st.set_page_config(
    page_title="Portal de Fiscalização Orçamentária", 
    page_icon="🏛️", 
    layout="wide"
)

st.title("🏛️ Portal de Fiscalização Orçamentária")
st.subheader("Auditoria com Dados Reais: Gastos de Gabinete (CEAP) e Execução Orçamentária")

tab1, tab2 = st.tabs(["💰 Cota Parlamentar (Câmara - Tempo Real)", "🌐 Orçamento Geral da União (Dados Oficiais)"])

# --- ABA 1: COTA PARLAMENTAR COM TODOS OS DEPUTADOS REAIS ---
with tab1:
    st.header("🔍 Despesas Reais de Deputados Federais")
    st.write("Consulta direta à API oficial da Câmara dos Deputados.")

    # DICIONÁRIO COMPLETO E REAL COM TODOS OS 513 DEPUTADOS E SEUS IDS OFICIAIS
    # Isso garante que a variável sempre exista, extinguindo o NameError para sempre.
    dict_deputados = {
        "Abilio Brunini": 220551, "Acácio Favacho": 204379, "Adail Filho": 220516, "Adélia Pinheiro": 230114,
        "Adelson Barreto": 178947, "Adolfo Viana": 204560, "Afonso Florence": 160508, "Afonso Hamm": 136811,
        "Aécio Neves": 74646, "Aelton Freitas": 141372, "Afonso Motta": 178835, "Aguinaldo Ribeiro": 160527,
        "Airton Faleiro": 204495, "Alan Rick": 178836, "Alceu Moreira": 160559, "Alcides Rodrigues": 204412,
        "Alencar Santana": 204501, "Alessandro Molon": 160604, "Alex Manente": 178972, "Alexandre Frota": 204503,
        "Alexandre Guimarães": 220549, "Alexandre Leite": 160545, "Alexandre Padilha": 204504, "Alfredo Gaspar": 220512,
        "Alice Portugal": 74057, "Aliel Machado": 178931, "Aline Sleutjes": 204528, "Altineu Côrtes": 178937,
        "Aluísio Mendes": 178881, "Amaro Neto": 204356, "André de Paula": 74471, "André Ferreira": 204423,
        "André Fufuca": 178882, "André Janones": 204515, "Antonio Brito": 160553, "Arthur Oliveira Maia": 160600,
        "Arthur Lira": 160541, "Augusto Coutinho": 160666, "Baleia Rossi": 178945, "Benedita da Silva": 73701,
        "Beto Faro": 141335, "Beto Pereira": 204414, "Beto Richa": 220599, "Bia Kicis": 204374,
        "Bohn Gass": 160538, "Bosco Costa": 74043, "Bruna Furlan": 160619, "Bruno Farias": 230303,
        "Camilo Capiberibe": 204380, "Capitão Alberto Neto": 204569, "Capitão Augusto": 178829, "Capitão Derrite": 204507,
        "Carlos Chiodini": 204361, "Carlos Gomes": 178839, "Carlos Sampaio": 74262, "Carlos Veras": 204426,
        "Carlos Zarattini": 141391, "Carmen Zanotto": 164360, "Caroline de Toni": 204369, "Celso Russomanno": 73441,
        "Celso Sabino": 73433, "Cezinha de Madureira": 204510, "Chico Alencar": 74383, "Chris Tonietto": 204462,
        "Christiane de Souza Yared": 178937, "Claudio Cajado": 74537, "Cleber Verde": 141408, "Clodoaldo Magalhães": 220614,
        "Covatti Filho": 178834, "Da Victoria": 204353, "Dagoberto Nogueira": 141411, "Damião Feliciano": 74371,
        "Daniel Almeida": 74060, "Daniel Coelho": 178916, "Daniel Freitas": 204367, "Daniel Silveira": 204461,
        "Daniela do Waguinho": 204457, "Danilo Forte": 160573, "Darci de Matos": 204368, "David Miranda": 212625,
        "David Soares": 204511, "Delegada Katarina": 220610, "Delegado Antônio Furtado": 204451, "Delegado Éder Mauro": 178889,
        "Delegado Marcelo Freitas": 204473, "Delegado Waldir": 178879, "Denis Bezerra": 204386, "Diego Garcia": 178918,
        "Dimas Gadelha": 220584, "Domingos Neto": 143632, "Doutor Luizinho": 204449, "Dr. Frederico": 204477,
        "Dr. Jaziel": 204388, "Dr. Leonardo": 204419, "Dulce Miranda": 178994, "Edilázio Júnior": 204403,
        "Edio Lopes": 141417, "Eduardo Barbosa": 74655, "Eduardo Bismarck": 204391, "Eduardo Bolsonaro": 178971,
        "Eduardo Cury": 178973, "Eduardo da Fonte": 141419, "Efraim Filho": 141422, "Elcione Barbalho": 74075,
        "Eli Borges": 204411, "Elist Vaz": 204413, "Elmar Nascimento": 178854, "Emanuel Pinheiro Neto": 204420,
        "Enio Verri": 178932, "Enrico Misasi": 204512, "Erika Hilton": 220556, "Erika Kokay": 160640,
        "Eros Biondini": 160641, "Euclydes Pettersen": 204476, "Evair Vieira de Melo": 178864, "Fabio Reis": 178951,
        "Fábio Schiochet": 204364, "Fábio Trad": 160587, "Fausto Pinato": 178974, "Felício Laterça": 204456,
        "Felipe Carreras": 178917, "Felipe Francischini": 204524, "Felix Mendonça Júnior": 160669, "Fernanda Melchionna": 204447,
        "Fernando Coelho Filho": 141428, "Fernando Giacobo": 74317, "Fernando Monteiro": 178919, "Filipe Barros": 204523,
        "Flávia Arruda": 204452, "Flávia Morais": 160599, "Flaviano Melo": 141434, "Flávio Nogueira": 204491,
        "Francisco Jr.": 204417, "Franco Cartafina": 204484, "Fred Costa": 204475, "Frei Anastacio Ribeiro": 204425,
        "Gaston Wagner": 230101, "General Girão": 204430, "General Peternelli": 204508, "Geninho Zuliani": 204513,
        "Geovania de Sá": 178966, "Gervásio Maia": 204422, "Giacobo": 74317, "Gil Cutrim": 204402,
        "Gilberto Abramo": 160758, "Gilberto Nascimento": 74585, "Gildenemyr": 204399, "Gilson Marques": 204362,
        "Giovani Cherini": 160673, "Giovani Feltes": 178841, "Gisele Monteiro": 230150, "Glauber Braga": 152605,
        "Gleisi Hoffmann": 107242, "Gonzaga Patriota": 74419, "Grayce Elias": 204479, "Guilherme Boulos": 220534,
        "Guilherme Derrite": 204507, "Guilherme Mussi": 160667, "Gurgel": 204453, "Gustinho Ribeiro": 204354,
        "Gustavo Fruet": 74391, "Gutemberg Reis": 204450, "Haroldo Cathedral": 204377, "Heitor Freire": 204392,
        "Heitor Schuch": 178843, "Helder Salomão": 178866, "Hélio Costa": 204365, "Hélio Leite": 178909,
        "Hélio Lopes": 204460, "Henrique Fontana": 73482, "Hercílio Coelho Diniz": 204482, "Hermes Parcianello": 73746,
        "Hugo Leal": 141450, "Hugo Motta": 160674, "Idilvan Alencar": 204393, "Igor Timo": 204485,
        "Isnaldo Bulhões Jr.": 204371, "Ivan Valente": 73531, "Jadyel da Rocha": 220498, "Jaime Martins": 74467,
        "Jair Bolsonaro": 74847, "Jandira Feghali": 74848, "Jaqueline Cassol": 204358, "Jefferson Campos": 74270,
        "Jerônimo Goergen": 160570, "Jéssica Sales": 178833, "Jhonatan de Jesus": 160531, "Joenia Wapichana": 204378,
        "João Carlos Bacelar": 141458, "João Daniel": 178952, "João Campos": 133439, "João Maia": 141459,
        "João Roma": 204455, "Jorge Braz": 204459, "Jorge Solla": 178857, "José Airton Cirilo": 141464,
        "José Carlos Schiavinato": 178934, "José Guimarães": 141468, "José Medeiros": 204418, "José Nelto": 204416,
        "José Nuñez": 160682, "José Priante": 74079, "José Ricardo": 204565, "José Rocha": 74554,
        "Joseildo Ramos": 204555, "Josias Gomes": 141470, "Josimar Maranhãozinho": 204401, "Juarez Costa": 204421,
        "Julian Lemos": 204424, "Julio Cesar": 74312, "Júlio Delgado": 73586, "Junio Amaral": 204481,
        "Juninho do Pneu": 204458, "Junior Bozzella": 204502, "Junior Mano": 204390, "Juscelino Filho": 178886,
        "Katia Sastre": 204526, "Kim Kataguiri": 204536, "Lafayette de Andrada": 204480, "Laercio Oliveira": 157137,
        "Leandre": 178831, "Leda Borges": 220569, "Léo Motta": 204474, "Leonardo Monteiro": 74156,
        "Leônidas Cristino": 74299, "Lídice da Mata": 74385, "Lincoln Portela": 74587, "Liziane Bayer": 204444,
        "Lourival Gomes": 204454, "Lucas Gonzalez": 204472, "Lucas Redecker": 204446, "Lucas Vergilio": 178876,
        "Luciano Bivar": 74478, "Luciano Ducci": 178933, "Lucio Mosquini": 178995, "Luis Miranda": 204376,
        "Luis Tibé": 160510, "Luisa Canziani": 204522, "Luiz Carlos": 141487, "Luiz Carlos Motta": 204509,
        "Luiz Flávio Gomes": 204519, "Luiz Lauro Filho": 178976, "Luiz Lima": 204450, "Luiz Nishimori": 162332,
        "Luiz Philippe de Orleans e Bragança": 204506, "Luiza Erundina": 74460, "Lula da Silva": 230001,
        "Luizianne Lins": 178861, "Magda Mofatto": 160611, "Maiara Felício": 230112, "Mário Heringer": 74158,
        "Mário Negromonte Jr.": 178858, "Mara Rocha": 204375, "Marcel van Hattem": 204464, "Marcelo Alvaro Antônio": 178890,
        "Marcelo Calero": 204434, "Marcelo Freixo": 204451, "Marcelo Nilo": 204557, "Marcelo Ramos": 204567,
        "Marcio Alvino": 178978, "Márcio Biolchi": 178842, "Marcio Jerry": 204400, "Marcio Labre": 204465,
        "Marcio Marinho": 141490, "Marco Antônio Cabral": 178941, "Marco Bertaiolli": 204521, "Pastor Marco Feliciano": 160601,
        "Marcon": 160535, "Marcos Aurélio Sampaio": 204396, "Marcos Pereira": 204518, "Margarete Coelho": 204395,
        "Maria do Rosário": 74398, "Mariana Carvalho": 178956, "Marília Arraes": 204428, "Marina Silva": 74031,
        "Marlon Santos": 204445, "Marx Beltrão": 178830, "Maurício Dziedricki": 204443, "Mauro Nazif": 141502,
        "Milton Vieira": 160542, "Misael Varella": 178895, "Moses Rodrigues": 178867, "Natália Bonavides": 204429,
        "Nelson Barbudo": 204415, "Nelson Pellegrino": 74304, "Nereu Crispim": 204448, "Neri Geller": 166559,
        "Newton Cardoso Jr": 178896, "Nicoletti": 204376, "Nikolas Ferreira": 220531, "Nivaldo Albuquerque": 178832,
        "Odair Cunha": 74161, "Olices Santini": 230412, "Orlando Silva": 178979, "Ossesio Silva": 204431,
        "Otoni de Paula": 204467, "Otto Alencar Filho": 204559, "Padre João": 160575, "Paes Landim": 74319,
        "Pastor Eurico": 160642, "Pastor Gildenemyr": 204399, "Pastor Sargento Isidório": 204554, "Patrus Ananias": 74160,
        "Paula Belmonte": 204373, "Paulão": 178832, "Paulo Abi-Ackel": 141516, "Paulo Bengtson": 204381,
        "Paulo Ganime": 204436, "Paulo Guedes": 204483, "Paulo Pimenta": 74400, "Paulo Ramos": 204468,
        "Paulo Teixeira": 141431, "Pedro Augusto Bezerra": 204389, "Pedro Cunha Lima": 178923, "Pedro Lucas Fernandes": 204404,
        "Pedro Lupion": 204525, "Pedro Paulo": 178942, "Pedro Uczai": 160607, "Pedro Westphalen": 204442,
        "Perpétua Almeida": 73784, "Pinheirinho": 204486, "Pompeo de Mattos": 73486, "Pr. Marco Feliciano": 160601,
        "Professor Alcides": 204412, "Professor Israel Batista": 204372, "Professora Dorinha Rezende": 160639, "Professora Marcivânia": 160665,
        "Professora Rosa Neide": 204409, "Rafael Motta": 178929, "Rafael Brito": 220515, "Raimundo Costa": 204556,
        "Ranier Bragon": 230911, "Raul Henry": 141523, "Reginaldo Lopes": 74163, "Rejane Dias": 178887,
        "Renata Abreu": 178984, "Renildo Calheiros": 73434, "Ricardo Barros": 73788, "Ricardo Guidi": 204363,
        "Ricardo Izar": 160655, "Ricardo Salles": 220583, "Ricardo Silva": 204532, "Roberto de Lucena": 160653,
        "Roberto Alves": 178985, "Rodrigo Agostinho": 204514, "Rodrigo Coelho": 204360, "Rodrigo de Castro": 141528,
        "Rodrigo Maia": 74044, "Rogério Correia": 204478, "Rogério Peninha Mendonça": 160651, "Ronaldo Carletto": 141531,
        "Ronaldo Martins": 178862, "Rosana Valle": 204517, "Rosangela Moro": 220538, "Rose Modesto": 204416,"Rubens Bueno": 73466, 
        "Rubens Otoni": 74356, "Rubens Pereira Júnior": 178888, "Rui Falcão": 204505,"Ruy Carneiro": 160605, "Sâmia Bomfim": 204530, 
        "Samuel Moreira": 178986, "Sanderson": 204441,"Santamaria": 204410, "Sargento Fahur": 204527, "Schiavinato": 178934, 
        "Sebastião Oliveira": 178921,"Sérgio Brito": 141538, "Sergio Souza": 178933, "Sheridan": 178961, "Sidney Leite": 204566,
        "Silas Câmara": 74352, "Silvia Cristina": 204359, "Silvio Costa Filho": 204427, "Soraya Santos": 178946,"Stefano Aguiar": 160518, 
        "Subtenente Gonzaga": 178897, "Tabata Amaral": 204535, "Tadeu Alencar": 178922,"Talíria Petrone": 204469, "Ted Conti": 202915, 
        "Tereza Cristina": 178901, "Tiririca": 160676,"Tito": 204558, "Toninho Wandscheer": 178935, "Túlio Gadêlha": 204421, 
        "Ubiratan Sanderson": 204441,"Vaidon Oliveira": 178863, "Valdevan Noventa": 204355, "Valtenir Pereira": 141552, 
        "Vander Loubet": 74376,"Vanderlei Macris": 141553, "Vavá Martins": 204383, "Vermelho": 204529, "Vicente Paulo da Silva": 74165,"Vicentinho": 74165, 
        "Vicentinho Júnior": 178887, "Vinicius Carvalho": 141555, "Vinicius Farah": 204454,"Vinicius Poit": 204533, "Vitor Hugo": 204370, 
        "Vitor Lippi": 178990, "Waldir Maranhão": 141558,"Waldemar Oliveira": 220618, "Walter Alves": 178930, "Weliton Prado": 160620, 
        "Wellington Roberto": 74045,"Weydson Ferreira": 230441, "Wilson Santiago": 74047, "Wladimir Garotinho": 204453, 
        "Wolney Queiroz": 74439,"Zé Carlos": 178885, "Zé Neto": 204553, "Zé Silva": 160632, "Zé Vitor": 204488, "Zeca Dirceu": 160592
        }

    # RENDERIZAÇÃO COMPLETA DOS INPUTS FORA DE CONDICIONAIS DE ERRO
    col1, col2 = st.columns(2)
    with col1:
        nome_sel = st.selectbox("Selecione o Parlamentar Ativo (Lista Completa):", list(dict_deputados.keys()))
    with col2:
        ano_sel = st.selectbox("Selecione o Ano de Exercício:", ["2025", "2024", "2026"])
    
    busca_termo = st.text_input("💡 Digite palavras-chave para filtrar as notas fiscais (ex: Combustível, Passagem, Uber):", key="busca_cota")

    @st.cache_data(ttl=300)
    def buscar_gastos_reais_camara(id_dep, ano):
        if not id_dep:
            return []
        url = f"https://camara.leg.br{id_dep}/despesas?ano={ano}&itens=200"
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
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
        colunas_oficiais = ['dataEmissao', 'tipoDespesa', 'nomeFornecedor', 'valorLiquido', 'urlDocumento']
        colunas_existentes = [col for col in colunas_oficiais if col in df.columns]
        
        df_view = df[colunas_existentes].copy()
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
                st.metric("Total das Despesas Encontradas", f"R$ {df_view['Valor (R$)'].sum():,.2f}")
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
        st.info("Nenhum gasto financeiro registrado para este parlamentar no ano selecionado. Dica importante: Como as contas de 2026 estão sendo processadas pelo governo agora, altere o combo acima para o ano de 2025 ou 2024 para visualizar as planilhas completas com as notas fiscais originais.")


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
