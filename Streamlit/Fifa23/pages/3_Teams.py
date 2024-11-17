import streamlit as st

# Carregar os dados da página 'home'
df_data = st.session_state['data']

# Page_Config
st.set_page_config(
    page_title='Players',
    layout='wide'
)

# Filtros - Club
clubes = df_data['Club'].value_counts().index
club = st.sidebar.selectbox('Clubes', clubes)
df_filtered = df_data[(df_data['Club'] == club)].set_index('Name') # Criando o filtro da tabela, onde o indice vai ser os nomes

# Layout da página
st.image(df_filtered.iloc[0]['Club Logo'])
st.markdown(f'## {club}')

# Colunas relevantes
columns = ['Age', 'Photo', 'Flag', 'Overall', 'Value(£)', 'Wage(£)', 'Joined',
    'Height(cm.)', 'Weight(lbs.)', 'Contract Valid Until', 'Release Clause(£)']

st.dataframe(df_filtered[columns], # Utiliza o 'st.dataframe' para poder utilizar as utilidades do streamlit (ajustar as colunas como quiser) 
            column_config={
            'Overall': st.column_config.ProgressColumn('Overall', format='%d', min_value=0, max_value=100),
            'Wage(£)': st.column_config.ProgressColumn('Weekly Wage', format='£%f', min_value=0, max_value=df_filtered['Wage(£)'].max()),
            'Photo': st.column_config.ImageColumn(),
            'Flag': st.column_config.ImageColumn('Country'),
            })