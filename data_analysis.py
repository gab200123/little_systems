import os
import glob
import pandas as pd
from datetime import datetime
from google.colab import files

def obter_data_hoje():
    return datetime.today().strftime("%d-%m-%Y")

data_hoje = obter_data_hoje()
uploaded = files.upload()

# Mover o arquivo para a pasta 'uploads'
for filename in uploaded.keys():
    os.rename(filename, os.path.join("uploads", filename))

print("Arquivo(s) movido(s) para 'uploads/'!")
print("Arquivos na pasta 'uploads/':")
print(os.listdir("uploads/"))

# Diretórios de entrada e saída
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Criar diretórios se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Parâmetros permitidos
COLUNAS_PERMITIDAS = [
    "cliente_id", "chamado_id", "cidade", "carimbo_baixa_problema",
    "onu_substituida", "roteador_substituido", "modelo_roteador",
    "PROTOCOLO", "CONTRATO INTERNET", "CIDADE", "MODELO ONU",
    "MODELO CPE", "ETIQUETAS", "CATEGORIAS DE ETIQUETA"
]

CATEGORIAS_PERMITIDAS = [
    "Instabilidade na conexão", "Roteador com defeito",
    "Equipamento brisanet sem gerência/sem acesso", "Sem WIFI",
    "Velocidade abaixo da contratada", "Quantidade de pontos WIFI insuficientes"
]

# Buscar arquivo XLSX na pasta de upload
file_list = glob.glob(os.path.join(UPLOAD_FOLDER, "*.xlsx"))
if not file_list:
    print("❌ Erro: Nenhum arquivo XLSX encontrado na pasta de uploads.")
    exit()

file_path = file_list[0]
print(f"📂 Processando arquivo: {file_path}")

try:
    xls = pd.ExcelFile(file_path)
    sheets = {}

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)

        # Manter apenas as colunas desejadas
        colunas_validas = [col for col in df.columns if col in COLUNAS_PERMITIDAS]
        df = df[colunas_validas]

        # Filtrar categorias desejadas, se a coluna existir
        if "carimbo_baixa_problema" in df.columns:
            df = df[df["carimbo_baixa_problema"].isin(CATEGORIAS_PERMITIDAS)]

        sheets[sheet_name] = df

    # Salvar novo arquivo XLSX
    output_path = os.path.join(OUTPUT_FOLDER, f"dados_tratados_{data_hoje}.xlsx")
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        for sheet, data in sheets.items():
            data.to_excel(writer, sheet_name=sheet, index=False)

    print(f"✅ Processamento concluído. Arquivo salvo em: {output_path}")


    # Caminho do arquivo tratado
    output_file = f"outputs/dados_tratados_{data_hoje}.xlsx"

    # Baixar o arquivo
    files.download(output_file)


except Exception as e:
    print(f"⚠️ Erro ao processar o arquivo: {str(e)}")
