def generate_chart_intro_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate the introductory text for the state's growth chart.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted text introducing the chart
    """
    # Get state info and first census year
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    first_census = data_loader.get_first_census_data(state_code)
    
    if not first_census:
        return None
        
    first_year, _ = first_census
    state_name = state_info['name']
    
    return f"Veja abaixo o gráfico de crescimento do {state_name} entre {first_year} e 2024:"
