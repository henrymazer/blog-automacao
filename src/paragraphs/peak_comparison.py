import pandas as pd
from ..utils.text_utils import numero_para_extenso, posicao_inversa

def get_period_ranking(df, state, period_start, period_end):
    """
    Get ranking information for a specific period's growth rate.
    
    Args:
        df (pd.DataFrame): DataFrame with census data
        state (str): State code (e.g., 'AC')
        period_start (str): Start year of the period
        period_end (str): End year of the period
        
    Returns:
        dict: Dictionary with ranking information
    """
    column = f"Taxa_Crescimento_Geometrico_{period_start}_{period_end}"
    
    # Get all states' growth rates for this period and sort
    state_data = df[df['Estado'] == state]
    regiao = state_data['Grande-regiao'].iloc[0]
    
    # Create ranking based on the specific period
    period_ranking = df.sort_values(column, ascending=False).reset_index(drop=True)
    posicao = period_ranking[period_ranking['Estado'] == state].index[0] + 1
    total_estados = len(period_ranking)
    
    # Get regional position if needed
    df_regiao = df[df['Grande-regiao'] == regiao].sort_values(column, ascending=False).reset_index(drop=True)
    posicao_regiao = df_regiao[df_regiao['Estado'] == state].index[0] + 1
    
    return {
        'posicao': posicao,
        'total_estados': total_estados,
        'posicao_regiao': posicao_regiao,
        'regiao': regiao,
        'taxa': state_data[column].iloc[0] * 100  # Convert to percentage
    }

def generate_peak_comparison_paragraph(df, state, period_start, period_end):
    """
    Generate paragraph comparing state's growth with others for the peak period.
    
    Args:
        df (pd.DataFrame): DataFrame with census data
        state (str): State code (e.g., 'AC')
        period_start (str): Start year of the period
        period_end (str): End year of the period
        
    Returns:
        str: Formatted paragraph text
    """
    ranking_data = get_period_ranking(df, state, period_start, period_end)
    posicao = ranking_data['posicao']
    total_estados = ranking_data['total_estados']
    regiao = ranking_data['regiao']
    
    state_names = {
        'AC': 'Acre',
        # Add other states as needed
    }
    state_name = state_names.get(state, state)
    
    if posicao <= 5:
        # Top 5 nacional
        pos_texto = numero_para_extenso(posicao)
        return (
            f"Neste período entre {period_start} e {period_end}, o {state_name} foi "
            f"o {pos_texto} estado que mais cresceu no Brasil."
        )
    elif posicao >= total_estados - 2:
        # Bottom 3 nacional
        pos_texto = posicao_inversa(posicao, total_estados)
        return (
            f"Neste período entre {period_start} e {period_end}, o {state_name} foi "
            f"o {pos_texto} estado em crescimento populacional no Brasil."
        )
    else:
        # Posição regional
        posicao_regiao = ranking_data['posicao_regiao']
        return (
            f"Neste período entre {period_start} e {period_end}, o {state_name} foi "
            f"o {posicao_regiao}º estado que mais cresceu na região {regiao}."
        )
