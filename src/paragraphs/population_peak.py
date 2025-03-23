def generate_population_peak_paragraph(data_loader, formatter, state_code: str = 'AC') -> str:
    """Generate paragraph about the state's projected population peak.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        formatter: BrazilianFormatter instance for number formatting
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph about population peak
    """
    # Get state info
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    # Get peak data from ranking DataFrame
    state_data = data_loader.df_ranking[data_loader.df_ranking['LOCAL'] == state_name]
    peak_year = state_data['Ano_Auge_Populacao'].iloc[0]
    peak_population = state_data[str(peak_year)].iloc[0]
    
    # Format the population number
    formatted_pop = formatter.format_population(int(peak_population))
    
    return (
        f"Segundo as projeções do IBGE, em {peak_year} o {state_name} "
        f"chegará no auge da sua população, com {formatted_pop} habitantes, "
        f"e após isso sua população começará a diminuir."
    )
