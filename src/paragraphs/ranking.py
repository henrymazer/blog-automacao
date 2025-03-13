from src.data.loader import get_state_data, get_ranking_data, get_regional_ranking
from src.utils.text_utils import numero_para_extenso, posicao_inversa

def generate_ranking_paragraph(df, df_crescimento, state_code='AC'):
    """Generate the second paragraph about growth ranking."""
    # Get state data
    state_data = get_state_data(df, state_code)
    regiao = state_data['regiao']
    
    # Get ranking data
    ranking_data = get_ranking_data(df_crescimento, state_code)
    posicao = ranking_data['posicao']
    total_estados = ranking_data['total_estados']
    
    if posicao <= 5:
        # Top 5 nacional
        pos_texto = numero_para_extenso(posicao)
        return f"Foi o {pos_texto} que mais cresceu no Brasil nesse período, proporcionalmente."
    elif posicao >= total_estados - 2:
        # Bottom 3 nacional
        pos_texto = posicao_inversa(posicao, total_estados)
        return f"Foi o {pos_texto} estado em crescimento no Brasil nesse período, proporcionalmente."
    else:
        # Posição regional
        posicao_regiao = get_regional_ranking(df_crescimento, regiao, state_code)
        return f"Foi o {posicao_regiao} estado que mais cresceu na região {regiao} nesse período, proporcionalmente."
