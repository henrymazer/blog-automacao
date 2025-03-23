import pandas as pd
from typing import List
from src.utils.formatting import BrazilianFormatter

def _get_same_year_states(df: pd.DataFrame, state_code: str, state_name: str, peak_year: int, use_national: bool = True) -> str:
    """Get formatted text for states peaking in the same year.
    
    Args:
        df: DataFrame with state data
        state_code: Current state code
        state_name: Current state name
        peak_year: Year to check for
        use_national: Whether to use national or regional comparison
        
    Returns:
        Formatted text for states peaking in same year, or empty string
    """
    # Get states with same peak year
    same_year_states = df[df['Ano_Auge_Populacao'] == peak_year]
    
    if len(same_year_states) <= 1:
        return ""
        
    # Filter states by position to ensure they share same ranking
    current_state_data = df[df['LOCAL'] == state_name].iloc[0]
    if use_national:
        position = current_state_data['Posição_Auge']
        same_year_states = same_year_states[same_year_states['Posição_Auge'] == position]
    else:
        position = current_state_data['Posição_Auge_Região']
        region = current_state_data['Grande-regiao']
        same_year_states = same_year_states[
            (same_year_states['Posição_Auge_Região'] == position) & 
            (same_year_states['Grande-regiao'] == region)
        ]
    
    # Remove current state from list
    other_states = same_year_states[same_year_states['LOCAL'] != state_name]
    
    if len(other_states) == 0:
        return ""
        
    state_names = other_states['LOCAL'].tolist()
    if len(state_names) == 1:
        return f", junto com {state_names[0]},"
    else:
        return f", junto com {', '.join(state_names[:-1])} e {state_names[-1]},"

def _get_position_text(position: int, total_positions: int) -> str:
    """Convert numeric position to text with suffix.
    
    Args:
        position: Numeric position
        total_positions: Total number of positions
        
    Returns:
        Position with appropriate suffix
    """
    if position == 1:
        return "primeiro"
    elif position == 2:
        return "segundo"
    elif position == 3:
        return "terceiro"
    elif position == 4:
        return "quarto"
    elif position == 5:
        return "quinto"
    elif position == total_positions - 1:
        return "penúltimo"
    elif position == total_positions - 2:
        return "antepenúltimo"
    else:
        return f"{position}º"

def generate_population_peak_comparison(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph comparing when state will reach peak population vs others.
    
    Args:
        data_loader: DataLoader instance
        state_code: Two-letter state code
        
    Returns:
        Formatted paragraph about peak population timing comparison
    """
    # Get state info and DataFrame
    state_info, _, _, total_states = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    region = state_info['region']
    
    df = data_loader.df_ranking
    state_data = df[df['LOCAL'] == state_name].iloc[0]
    
    # Get position and peak year
    national_pos = int(state_data['Posição_Auge'])
    regional_pos = int(state_data['Posição_Auge_Região'])
    peak_year = int(state_data['Ano_Auge_Populacao'])
    
    # Determine if we use national or regional comparison
    use_national = (national_pos <= 5) or (national_pos >= total_states - 2)
    
    # Get other states' info based on comparison scope
    if use_national:
        sorted_states = df.sort_values('Posição_Auge')
        first_state = sorted_states.iloc[0]['LOCAL']
        first_year = int(sorted_states.iloc[0]['Ano_Auge_Populacao'])
        last_state = sorted_states.iloc[-1]['LOCAL']
        last_year = int(sorted_states.iloc[-1]['Ano_Auge_Populacao'])
        position_text = _get_position_text(national_pos, 18)  # Brazil has 18 positions
        scope = "no Brasil"
    else:
        region_states = df[df['Grande-regiao'] == region].sort_values('Posição_Auge_Região')
        first_state = region_states.iloc[0]['LOCAL']
        first_year = int(region_states.iloc[0]['Ano_Auge_Populacao'])
        last_state = region_states.iloc[-1]['LOCAL']
        last_year = int(region_states.iloc[-1]['Ano_Auge_Populacao'])
        region_size = len(df[df['Grande-regiao'] == region])
        position_text = _get_position_text(regional_pos, region_size)
        scope = f"na região {region}"
    
    # Get text for states peaking in same year
    same_year_text = _get_same_year_states(df, state_code, state_name, peak_year, use_national)
    
    # Generate appropriate text based on position
    if use_national:
        if national_pos == 1:
            return (
                f"O {state_name} será o primeiro estado a parar de crescer populacionalmente "
                f"{scope}{same_year_text}, no ano de {peak_year}. "
                f"{last_state} será o último, somente em {last_year}."
            )
        elif national_pos == total_states:
            return (
                f"O {state_name} será o último estado a parar de crescer populacionalmente "
                f"{scope}{same_year_text}, no ano de {peak_year}. "
                f"{first_state} será o primeiro em {first_year}."
            )
        else:
            return (
                f"O {state_name} será o {position_text} estado a parar de crescer populacionalmente "
                f"{scope}{same_year_text}, no ano de {peak_year}. "
                f"{first_state} será o primeiro em {first_year} e "
                f"{last_state} o último, somente em {last_year}."
            )
    else:
        region_size = len(df[df['Grande-regiao'] == region])
        if regional_pos == 1:
            return (
                f"O {state_name} será o primeiro estado a parar de crescer populacionalmente "
                f"{scope}{same_year_text}, no ano de {peak_year}. "
                f"{last_state} será o último, somente em {last_year}."
            )
        elif regional_pos == region_size:
            return (
                f"O {state_name} será o último estado a parar de crescer populacionalmente "
                f"{scope}{same_year_text}, no ano de {peak_year}. "
                f"{first_state} será o primeiro em {first_year}."
            )
        else:
            return (
                f"O {state_name} será o {position_text} estado a parar de crescer populacionalmente "
                f"{scope}{same_year_text}, no ano de {peak_year}. "
                f"{first_state} será o primeiro em {first_year} e "
                f"{last_state} o último, somente em {last_year}."
            )
