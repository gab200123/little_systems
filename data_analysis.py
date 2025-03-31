import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_table
import io
import base64
from dash.exceptions import PreventUpdate

# Inicializando o aplicativo
app = dash.Dash(__name__)

app.layout = html.Div([
    # Upload do arquivo .xlsx
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Excel File'),
        multiple=False
    ),
    
    # Dropdown para selecionar as colunas para os eixos X e Y
    dcc.Dropdown(
        id='column-selector',
        multi=True,
        placeholder="Selecione as colunas",  # Placeholder para seleção de colunas
    ),
    
    # Dropdown para selecionar a coluna para filtrar
    dcc.Dropdown(
        id='filter-column',
        placeholder="Selecione a coluna para filtrar",  # Placeholder para filtro
    ),
    
    # Input para inserir o valor para filtrar
    dcc.Input(
        id='filter-value',
        type='text',
        placeholder="Digite o valor para filtrar",
    ),
    
    # Exibição do gráfico de dispersão
    dcc.Graph(id='graph'),
])

# Função para carregar e processar o arquivo Excel
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Converting binary data to DataFrame
        df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return None, str(e)
    return df, None

# Callback para processar o upload e atualizar as opções de colunas
@app.callback(
    [Output('column-selector', 'options'),
     Output('filter-column', 'options'),
     Output('column-selector', 'value')],
    [Input('upload-data', 'contents')]
)
def update_columns(contents):
    if contents is None:
        raise PreventUpdate

    # Carregar o arquivo Excel
    df, error = parse_contents(contents)

    if df is None:
        return [], [], []

    # Gerar as opções de dropdown com base nas colunas do DataFrame
    options = [{'label': col, 'value': col} for col in df.columns]
    
    return options, options, []

# Callback para atualizar o gráfico
@app.callback(
    Output('graph', 'figure'),
    [Input('column-selector', 'value'),
     Input('filter-column', 'value'),
     Input('filter-value', 'value'),
     Input('upload-data', 'contents')]
)
def update_graph(columns, filter_col, filter_value, contents):
    if columns is None or len(columns) < 2 or contents is None:
        raise PreventUpdate

    # Carregar o arquivo Excel
    df, error = parse_contents(contents)

    if df is None:
        return {}

    # Aplicando filtro se a coluna de filtro e o valor de filtro forem selecionados
    filtered_df = df.copy()
    if filter_col and filter_value:
        # Verificando o tipo da coluna e filtrando de acordo
        if filter_col in df.select_dtypes(include=['number']).columns:  # Colunas numéricas
            filtered_df = filtered_df[filtered_df[filter_col] == float(filter_value)]
        else:  # Colunas de texto
            filtered_df = filtered_df[filtered_df[filter_col] == filter_value]
    
    # Se o filtro resultar em um DataFrame vazio, exibir uma mensagem
    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'title': 'Nenhum dado disponível após o filtro',
            }
        }

    # Criando o gráfico de dispersão com as colunas selecionadas para X e Y
    fig = px.scatter(
        filtered_df,
        x=columns[0],  # Eixo X
        y=columns[1],  # Eixo Y
        title=f"Gráfico de Dispersão: {columns[0]} vs {columns[1]}",
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

