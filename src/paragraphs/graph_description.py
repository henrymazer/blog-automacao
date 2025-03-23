def generate_graph_description_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate description text for the population projection graph.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Description text for population projection graph
    """
    # Get state info and first census year
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    first_census = data_loader.get_first_census_data(state_code)
    
    if not first_census:
        return None
        
    first_year, _ = first_census
    state_name = state_info['name']
    
    # Get state creation year
    creation_year = data_loader.get_state_creation_year(state_code)
    
    # Generate appropriate text based on the relationship between creation year and census year
    if creation_year and int(creation_year) < int(first_year):
        return (
            f"O gráfico acima mostra a população do Censo {first_year}, primeiro ano que o Brasil "
            f"teve um Censo Demográfico, para a população do {state_name}, até a projeção de 2070."
        )
    else:
        return (
            f"O gráfico acima mostra a população desde {first_year}, primeiro ano que o IBGE estimou "
            f"a população do {state_name}, até a projeção de 2070."
        )
