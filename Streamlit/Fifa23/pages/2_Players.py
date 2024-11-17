import streamlit as st

# Carregar os dados da página 'home'
df_data = st.session_state['data']

# Page_Config
st.set_page_config(
    page_title='Players',
    layout='wide'
)


# Filtros - Player e Club
clubes = df_data['Club'].value_counts().index
club = st.sidebar.selectbox('Clubes', clubes)
df_players = df_data[(df_data['Club'] == club)]

players = df_players['Name'].value_counts().index
player = st.sidebar.selectbox('Jogador', players)

# Construindo o layout
player_stats = df_data[df_data['Name'] == player].iloc[0] # iloc[n] -> Vai retornar a primeira aparição do jogador no dataset

st.image(player_stats['Photo']) # Imagem do jogador
st.title(player_stats['Name']) # Nome do jogador como título
st.markdown(f'**Clube:** {player_stats['Club']}') # Nome do clube
st.markdown(f'**Posição:** {player_stats['Position']}') # Posição do jogador

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'**Idade:** {player_stats['Age']}')
col2.markdown(f'**Altura:** {player_stats['Height(cm.)'] /100}')
col3.markdown(f'**Peso:** {player_stats['Weight(lbs.)'] *0.453:.2f}')
st.divider() # Linha para dividir a página

st.subheader(f'Overall {player_stats['Overall']}')
st.progress(int(player_stats['Overall'])) # Medida de 0 a 100

col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Valor de mercado', value=f'£ {player_stats['Value(£)']:,}')
col2.metric(label='Remuneração semanal', value=f'£ {player_stats['Wage(£)']:,}')
col3.metric(label='Cláusula de rescião', value=f'£ {player_stats['Release Clause(£)']:,}')