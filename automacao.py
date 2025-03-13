import pandas as pd
import numpy as np
import requests
import json
import locale
from src.paragraphs.peak_growth import get_peak_growth_period, generate_peak_growth_paragraph
from src.paragraphs.peak_comparison import generate_peak_comparison_paragraph
from src.paragraphs.chart_intro import generate_chart_intro_paragraph
from src.paragraphs.graph_image import generate_graph_image_paragraph
from src.paragraphs.future_header import generate_future_header
from src.paragraphs.population_peak import generate_population_peak_paragraph
from src.paragraphs.projection_graph import generate_projection_graph_paragraph
from src.paragraphs.graph_description import generate_graph_description_paragraph

# Set locale for number formatting
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_number(num):
    try:
        return locale.format_string("%d", num, grouping=True)
    except:
        return format(num, ",").replace(",", ".")

def format_historical_info(content):
    if not content:
        return None
    
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    formatted = []
    
    for p in paragraphs:
        p = ' '.join(p.split())  # Remove extra spaces
        p = p.replace('[1][3]', ' [Fonte: História do Acre](https://www.historia.acre.gov.br)')
        p = p.replace('[[', '[')
        p = p.replace('o[', 'o [')
        formatted.append(p)
    
    return '\n\n'.join(formatted)

def get_state_creation_date():
    api_key = "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"
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": "When was the state of Acre created in Brazil? Return only the year."
            }
        ],
        "max_tokens": 123,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error getting state creation date: {e}")
        return None

def get_historical_info(year):
    api_key = "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"
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "Write a brief, concise response in Portuguese with exactly two short sentences. Write each sentence on a single line, followed by its source link. Keep sentences short and simple."
            },
            {
                "role": "user",
                "content": f"What was the main economic activity and political organization of Acre, Brazil in {year}? Write two short sentences in Portuguese, first about economic activity, second about political organization. Start each with 'Em {year}'. After each sentence, add a source like '[História do Acre](https://www.historia.acre.gov.br)'. Keep sentences brief."
            }
        ],
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        # Clean up response and ensure proper formatting
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        return '\n\n'.join(paragraphs)
    except Exception as e:
        print(f"Error getting historical information: {e}")
        return None

# Ler o primeiro arquivo CSV
df = pd.read_csv(r"D:\jornalera-marista\censo-2022\dados\estados\Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv")

# Ler o segundo arquivo CSV com os dados de crescimento
df_crescimento = pd.read_csv(r"D:\jornalera-marista\censo-2022\dados\estados\compilado_estados.csv")

# Pegar a primeira linha (Acre) do primeiro arquivo
primeira_linha = df.iloc[0]

# Pegar o nome do estado
nome_estado = primeira_linha['LOCAL']
regiao = primeira_linha['Grande-regiao']

# Lista de colunas para verificar (filtrar apenas as que existem no arquivo)
colunas_censo = [col for col in ['1872', '1890', '1900', '1910', '1920', '1940', '1950', '1960'] 
                 if col in df.columns]

# Encontrar a primeira coluna com dados
primeiro_ano = None
primeiro_valor = None
for coluna in colunas_censo:
    valor = primeira_linha[coluna]
    # Verificar se o valor não é nulo ou vazio
    if pd.notna(valor) and valor != 0:
        primeiro_ano = coluna
        primeiro_valor = valor
        break

# Pegar o valor de crescimento do Acre
crescimento = df_crescimento.loc[df_crescimento['Estado'] == 'AC', 'x_crescimento'].iloc[0]

# Primeira frase - dados históricos
if primeiro_ano:
    print(f"Desde {primeiro_ano} até 2024 o {nome_estado} cresceu {int(crescimento)} vezes.")

# Ordenar estados por crescimento e encontrar posição do Acre
df_ranking = df_crescimento.sort_values('x_crescimento', ascending=False).reset_index(drop=True)
posicao = df_ranking[df_ranking['Estado'] == 'AC'].index[0] + 1
total_estados = len(df_crescimento)

# Função para converter número em posição por extenso
def numero_para_extenso(num):
    extenso = {
        1: "primeiro",
        2: "segundo",
        3: "terceiro",
        4: "quarto",
        5: "quinto"
    }
    return extenso.get(num, str(num))

# Função para posições inversas
def posicao_inversa(pos, total):
    if pos == total:
        return "último"
    elif pos == total - 1:
        return "penúltimo"
    elif pos == total - 2:
        return "antepenúltimo"
    return str(pos)

# Segunda frase - verificar condições de ranking
if posicao <= 5:
    # Top 5 nacional
    pos_texto = numero_para_extenso(posicao)
    print(f"Foi o {pos_texto} que mais cresceu no Brasil nesse período, proporcionalmente.")
elif posicao >= total_estados - 2:
    # Bottom 3 nacional
    pos_texto = posicao_inversa(posicao, total_estados)
    print(f"Foi o {pos_texto} estado em crescimento no Brasil nesse período, proporcionalmente.")
else:
    # Posição regional
    df_regiao = df_crescimento[df_crescimento['Grande-regiao'] == regiao].sort_values('x_crescimento', ascending=False).reset_index(drop=True)
    posicao_regiao = df_regiao[df_regiao['Estado'] == 'AC'].index[0] + 1
    print(f"Foi o {posicao_regiao} estado que mais cresceu na região {regiao} nesse período, proporcionalmente.")

# Terceira frase - data de criação do estado e população
creation_year = get_state_creation_date()
if creation_year and primeiro_ano and primeiro_valor:
    creation_year = int(creation_year)
    primeiro_ano_int = int(primeiro_ano)
    
    if creation_year > primeiro_ano_int:
        print(f"O estado foi criado em {creation_year}, mas o IBGE estimou a população para {primeiro_ano} em {format_number(int(primeiro_valor))} habitantes.")
    else:
        print(f"O estado foi criado em {creation_year}, e no Censo de {primeiro_ano} a população era de {format_number(int(primeiro_valor))} habitantes.")

# Quarta frase - informações históricas
if primeiro_ano:
    historical_info = get_historical_info(primeiro_ano)
    if historical_info:
        formatted_info = format_historical_info(historical_info)
print(f"\n{formatted_info}")

# Quinta frase - período de maior crescimento
peak_period = get_peak_growth_period(df_crescimento, 'AC')
if peak_period:
    start_year, end_year, growth_rate = peak_period
    peak_growth_text = generate_peak_growth_paragraph('Acre', start_year, end_year, growth_rate)
    print(f"\n{peak_growth_text}")
    
    # Sexta frase - comparação do crescimento no período de pico
    comparison_text = generate_peak_comparison_paragraph(df_crescimento, 'AC', start_year, end_year)
    print(f"\n{comparison_text}")

# Sétima frase - introdução do gráfico
chart_intro_text = generate_chart_intro_paragraph('Acre', primeiro_ano)
print(f"\n{chart_intro_text}")

# Oitava frase - imagem do gráfico
graph_image = generate_graph_image_paragraph(nome_estado)
print(f"\n{graph_image}")

# Nona frase - título da seção futura
future_header = generate_future_header()
print(f"\n\n{future_header}")

# Décima frase - projeção do pico populacional
peak_projection = generate_population_peak_paragraph(df, 'Acre')
print(f"\n{peak_projection}")

# Décima primeira frase - gráfico de projeção populacional
projection_graph = generate_projection_graph_paragraph('Acre')
print(f"\n{projection_graph}")

# Décima segunda frase - descrição do gráfico de projeção
graph_description = generate_graph_description_paragraph('Acre')
print(f"\n{graph_description}")
