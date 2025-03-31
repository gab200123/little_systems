import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_uploader as du
import os
from flask import Flask
from google.colab.output import eval_js
from pyngrok import ngrok

# Configurar Flask e Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Configuração do diretório de upload
UPLOAD_FOLDER = "./uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

du.configure_upload(app, UPLOAD_FOLDER)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Análise de Dados com Dash"),
    du.Upload(id='upload-data', text='Arraste e solte ou clique para fazer upload',
              text_completed='Upload completo: {filename}', max_files=1),
    dcc.Dropdown(id='column-selector', multi=True, placeholder="Selecione as colunas"),
    dcc.Dropdown(id='filter-column', placeholder="Selecione a coluna para filtrar"),
    dcc.Input(id='filter-value', type='text', placeholder='Valor do filtro'),
    html.Button('Aplicar Filtro', id='apply-filter', n_clicks=0),
    dash_table.DataTable(id='data-table', page_size=10),
    dcc.Graph(id='data-graph')
])

# Callback para carregar o arquivo e popular as colunas
@app.callback(
    [Output('column-selector', 'options'), Output('filter-column', 'options')],
    Input('upload-data', 'isCompleted'),
    prevent_initial_call=True
)
def load_file(is_completed):
    if is_completed:
        # Filtrar apenas arquivos Excel no diretório de uploads
        excel_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.xlsx')]
        if not excel_files:
            return [], []
        
        file_path = os.path.join(UPLOAD_FOLDER, excel_files[0])
        df = pd.read_excel(file_path)
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options
    return [], []

# Callback para aplicar filtro e atualizar gráficos
@app.callback(
    [Output('data-table', 'data'), Output('data-graph', 'figure')],
    [Input('apply-filter', 'n_clicks')],
    [dash.dependencies.State('filter-column', 'value'), dash.dependencies.State('filter-value', 'value'),
     dash.dependencies.State('upload-data', 'isCompleted')],
    prevent_initial_call=True
)
def filter_data(n_clicks, column, value, is_completed):
    if is_completed:
        excel_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.xlsx')]
        if not excel_files:
            return [], {}
        
        file_path = os.path.join(UPLOAD_FOLDER, excel_files[0])
        df = pd.read_excel(file_path)

        if column and value:
            df = df[df[column].astype(str).str.contains(value, case=False, na=False)]

        fig = px.histogram(df, x=column) if column else px.histogram(df)
        return df.to_dict('records'), fig
    return [], {}

# Iniciar ngrok e rodar o servidor
public_url = ngrok.connect(8050).public_url
print(f"Acesse o app aqui: {public_url}")
app.run(host='0.0.0.0', port=8050, debug=True)
