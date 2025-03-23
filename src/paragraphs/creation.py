def generate_creation_paragraph(data_loader, api_client, formatter, state_code: str = 'AC') -> str:
    """Generate paragraph about state creation date and initial population.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        api_client: PerplexityAPI instance for historical queries
        formatter: BrazilianFormatter instance for number formatting
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph about state creation and initial population
    """
    # Get first census data
    first_census = data_loader.get_first_census_data(state_code)
    if not first_census:
        return None
        
    first_year, first_population = first_census
    
    # Get state creation date and name using the new method
    try:
        state_data, _, _, _ = data_loader.get_state_data(state_code)
        if not state_data:
            return None
            
        state_name = state_data['name']
        creation_year = data_loader.get_state_creation_year(state_code)
        if not creation_year:
            return None
    except Exception:
        return None
    
    # Format values
    formatted_population = formatter.format_number(int(first_population))
    creation_year_int = int(creation_year)
    first_year_int = int(first_year)
    
    if creation_year_int > first_year_int:
        return (
            f"Muito embora o estado do {state_name} tenha sido criado apenas em {creation_year}, "
            f"o IBGE estimou a população do território o qual hoje configura o estado em "
            f"{formatted_population} habitantes no ano de {first_year}."
        )
    else:
        return (
            f"O estado do {state_name} foi criado em {creation_year}, e no Censo de {first_year} "
            f"a população do território já era de {formatted_population} habitantes."
        )
