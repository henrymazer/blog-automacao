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
    
    # Get state creation date
    creation_year = api_client.get_state_creation_date()
    if not creation_year:
        return None
        
    # Format values
    formatted_population = formatter.format_number(int(first_population))
    creation_year_int = int(creation_year)
    first_year_int = int(first_year)
    
    if creation_year_int > first_year_int:
        return (
            f"O estado foi criado em {creation_year}, mas o IBGE estimou a população "
            f"para {first_year} em {formatted_population} habitantes."
        )
    else:
        return (
            f"O estado foi criado em {creation_year}, e no Censo de {first_year} "
            f"a população era de {formatted_population} habitantes."
        )
