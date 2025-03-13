from src.data.loader import get_first_census_data, get_growth_data, get_state_data

def generate_growth_paragraph(df, df_crescimento, state_code='AC'):
    """Generate the first paragraph about population growth."""
    # Get state data
    state_data = get_state_data(df, state_code)
    nome_estado = state_data['nome_estado']
    
    # Get first census data
    census_data = get_first_census_data(df, state_code)
    primeiro_ano = census_data['ano'] if census_data else None
    
    # Get growth data
    crescimento = get_growth_data(df_crescimento, state_code)
    
    if primeiro_ano:
        return f"Desde {primeiro_ano} até 2024 o {nome_estado} cresceu {int(crescimento)} vezes."
    
    return None
