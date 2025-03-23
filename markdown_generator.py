import os
import sys
from typing import Optional, List, Tuple
import logging
from datetime import datetime

from src.data.loader import DataLoader
from src.utils.api import PerplexityAPI
from src.utils.formatting import BrazilianFormatter

# Importar todas as funções de geração de parágrafos
from automacao import generate_article

# Configuração
RANKING_FILE = r"D:\jornalera-marista\censo-2022\dados\estados\Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv"
GROWTH_FILE = r"D:\jornalera-marista\censo-2022\dados\estados\compilado_estados.csv"
AGE_DATA_FILE = r"D:\jornalera-marista\censo-2022\dados\estados\Tabela_Popula__o_por_Faixa_Et_ria_e_Anos.csv"
OUTPUT_DIR = "artigos"  # Diretório local do projeto

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("estados_processing.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def simplify_source_links(text: str) -> str:
    """Simplifica os links de fonte no texto, substituindo [Fonte: texto] por [Fonte]."""
    import re
    return re.sub(r'\[Fonte:(.*?)\]', r'[Fonte]', text)

def normalize_sources(text: str) -> str:
    """Normaliza a formatação das fontes para garantir padrão consistente.
    
    Regras:
    1. Move o ponto final para depois do parênteses de fechamento do link
    2. Garante espaço entre a palavra anterior e o início da fonte
    3. Coloca fontes isoladas na mesma linha do parágrafo anterior
    
    Args:
        text: Texto original do artigo
        
    Returns:
        Texto com fontes normalizadas
    """
    import re
    
    # Primeiro: fontes isoladas em suas próprias linhas
    text = re.sub(r'\.?\n\n(\[Fonte.*?\]\(.*?\)\.?)', r' \1', text)
    
    # Segundo: garante espaço entre texto e fonte na mesma linha
    text = re.sub(r'([^\s])(\[Fonte)', r'\1 \2', text)
    
    # Terceiro: move pontos finais antes da fonte para depois dela
    text = re.sub(r'\.(\s*\[Fonte.*?\]\(.*?\))', r'\1.', text)
    
    # Quarto: se a fonte não termina com ponto, adiciona um
    text = re.sub(r'(\[Fonte.*?\]\(.*?\))([^\.])', r'\1. \2', text)
    
    # Quinto: remove pontos duplicados que possam ter sido gerados
    text = re.sub(r'\.\s*\.', r'.', text)
    
    return text

def split_long_paragraphs(text: str) -> str:
    """Divide parágrafos longos em múltiplos parágrafos quando contêm várias frases,
    ignorando pontos em links e abreviações.
    
    Args:
        text: Texto original do artigo
        
    Returns:
        Texto com parágrafos divididos por frases
    """
    import re
    lines = text.split('\n')
    result_lines = []
    
    for line in lines:
        if line.strip():
            # Dividir frases por ponto final, excluindo links e abreviações
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', line)
            result_lines.extend(sentences)
        else:
            result_lines.append(line)
    
    return '\n\n'.join(result_lines)

def normalize_blank_lines(text: str) -> str:
    """Normaliza linhas em branco entre parágrafos.
    
    Args:
        text: Texto original do artigo
        
    Returns:
        Texto com espaçamento consistente entre parágrafos
    """
    lines = text.split('\n')
    normalized_lines = []
    
    for line in lines:
        if line.strip():  # Linha não vazia
            normalized_lines.append(line)
        elif normalized_lines and normalized_lines[-1] != '':  # Adicionar linha vazia apenas se necessário
            normalized_lines.append('')
    
    return '\n'.join(normalized_lines)

def setup_output_directory() -> None:
    """Cria o diretório de saída se não existir."""
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
            logging.info(f"Diretório de saída criado: {OUTPUT_DIR}")
        except Exception as e:
            logging.error(f"Erro ao criar diretório de saída: {e}")
            sys.exit(1)
    else:
        logging.info(f"Diretório de saída já existe: {OUTPUT_DIR}")

def ensure_proper_punctuation(text: str) -> str:
    """Garante que todos os parágrafos terminem com pontuação adequada.
    
    Args:
        text: Texto original do artigo
        
    Returns:
        Texto com pontuação corrigida
    """
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.rstrip()
        if line and not line.startswith('#') and not line.startswith('!') and not line.startswith('---'):
            # Verifica se a linha não termina com pontuação
            if line and not line[-1] in ['.', '!', '?', ':', ';', '"', "'", ')']:
                line += '.'
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def capture_article_output(state_code: str) -> str:
    """Captura a saída do artigo gerado para um estado.
    
    Args:
        state_code: Código de duas letras do estado
        
    Returns:
        Conteúdo completo do artigo em formato markdown
    """
    import io
    from contextlib import redirect_stdout
    
    # Redirecionar stdout para um buffer
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        generate_article(state_code)
    
    # Retornar o conteúdo capturado
    return buffer.getvalue()

def generate_markdown_file(state_code: str) -> Tuple[bool, Optional[str]]:
    """Gera um arquivo markdown para um estado específico.
    
    Args:
        state_code: Código de duas letras do estado
        
    Returns:
        Tupla (sucesso: bool, caminho_arquivo: str ou None)
    """
    # Garantir que o diretório de saída existe
    setup_output_directory()
    
    state_name = DataLoader.STATE_NAMES.get(state_code)
    if not state_name:
        logging.error(f"Código de estado inválido: {state_code}")
        return False, None
    
    output_file = os.path.join(OUTPUT_DIR, f"estado_{state_code}.md")
    
    try:
        # Capturar a saída do artigo
        article_content = capture_article_output(state_code)
        
        # Adicionar título no início do arquivo
        header = f"# {state_name}: Análise Demográfica\n\n"
        article_content = header + article_content
        
        # 1. Primeiro, normalizar as fontes
        article_content = normalize_sources(article_content)
        
        # 2. Simplificar os links de fonte
        article_content = simplify_source_links(article_content)
        
        # 3. Garantir pontuação adequada em todos os parágrafos
        article_content = ensure_proper_punctuation(article_content)
        
        # 3. Dividir parágrafos longos em frases individuais
        article_content = split_long_paragraphs(article_content)
        
        # 4. Normalizar linhas em branco entre os parágrafos
        article_content = normalize_blank_lines(article_content)
        
        # Remover metadados e data de geração do final do arquivo
        
        # Escrever no arquivo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(article_content)
        
        logging.info(f"Arquivo gerado com sucesso: {output_file}")
        return True, output_file
        
    except Exception as e:
        logging.error(f"Erro ao gerar arquivo para {state_name} ({state_code}): {str(e)}")
        return False, None

def process_all_states(start_from: Optional[str] = None) -> List[Tuple[str, bool]]:
    """Processa todos os estados, gerando arquivos markdown para cada um.
    
    Args:
        start_from: Opcional, código do estado para começar (continuar processamento)
        
    Returns:
        Lista de tuplas (código_estado, sucesso)
    """
    # Lista de códigos de todos os estados brasileiros em ordem alfabética
    state_codes = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    # Se especificado um estado para começar, ajustar a lista
    if start_from and start_from in state_codes:
        start_index = state_codes.index(start_from)
        state_codes = state_codes[start_index:]
    
    # Preparar diretório de saída
    setup_output_directory()
    
    # Resultados
    results = []
    
    # Processar cada estado
    total_states = len(state_codes)
    for i, state_code in enumerate(state_codes, 1):
        state_name = DataLoader.STATE_NAMES.get(state_code)
        logging.info(f"Processando {i}/{total_states}: {state_name} ({state_code})")
        
        success, filepath = generate_markdown_file(state_code)
        results.append((state_code, success))
        
        if success:
            logging.info(f"Concluído {i}/{total_states}: {state_name} - Arquivo: {filepath}")
        else:
            logging.warning(f"Falha {i}/{total_states}: {state_name} - Continuando processamento...")
    
    # Relatório final
    successful = sum(1 for _, success in results if success)
    logging.info(f"Processamento concluído: {successful}/{total_states} estados processados com sucesso")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gera arquivos markdown para estados brasileiros")
    parser.add_argument("--start", help="Código do estado para iniciar/continuar processamento")
    parser.add_argument("--state", help="Gerar apenas para um estado específico")
    args = parser.parse_args()
    
    if args.state:
        # Processar apenas um estado
        state_code = args.state.upper()
        logging.info(f"Gerando arquivo apenas para o estado: {state_code}")
        success, filepath = generate_markdown_file(state_code)
        if success:
            print(f"Arquivo gerado com sucesso: {filepath}")
        else:
            print(f"Falha ao gerar arquivo para {state_code}")
    else:
        # Processar todos os estados (ou a partir de um específico)
        start_from = args.start.upper() if args.start else None
        results = process_all_states(start_from)
        
        # Exibir resumo
        print("\nResumo do processamento:")
        for state_code, success in results:
            state_name = DataLoader.STATE_NAMES.get(state_code)
            status = "✅ Sucesso" if success else "❌ Falha"
            print(f"{state_code} - {state_name}: {status}")