def format_population(value):
    """
    Format population value in thousands or millions.
    
    Args:
        value (int): Population value to format
        
    Returns:
        str: Formatted value with appropriate unit (mil or milhões)
    """
    if value < 1_000_000:  # Less than 1 million
        return f"{value/1000:.0f} mil"
    else:  # 1 million or more
        return f"{value/1_000_000:.2f} milhões"

def generate_population_peak_paragraph(df, state_name):
    """
    Generate paragraph about the state's projected population peak.
    
    Args:
        df (pd.DataFrame): DataFrame with population projection data
        state_name (str): Name of the state (e.g., 'Acre')
        
    Returns:
        str: Formatted paragraph about population peak
    """
    state_data = df[df['LOCAL'] == state_name]
    peak_year = state_data['Ano_Auge_Populacao'].iloc[0]
    peak_population = state_data[str(peak_year)].iloc[0]
    formatted_pop = format_population(peak_population)
    
    return (
        f"Segundo as projeções do IBGE, em {peak_year} o {state_name} "
        f"chegará no auge da população, com {formatted_pop} habitantes, "
        f"diminuindo a população a partir desse ano."
    )
