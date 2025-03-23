def generate_children_population_change_paragraph(data_loader, formatter, state_code: str = 'AC') -> str:
    """Generate paragraph about change in children population.
    
    Args:
        data_loader: DataLoader instance
        formatter: BrazilianFormatter instance for number formatting
        state_code: Two-letter state code
        
    Returns:
        Formatted paragraph about children population change
    """
    # Get state info
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    # Get age group data
    age_data = data_loader.get_age_group_data(state_name)
    
    # Format population numbers using Brazilian formatter
    pop_2024 = formatter.format_population(int(age_data['pop_0_4_2024']))
    pop_2070 = formatter.format_population(int(age_data['pop_0_4_2070']))
    
    # Get percentage change as integer
    percent_change = int(age_data['change_percent'])
    
    return (
        f"O número de crianças entre 0 e 4 anos cairá dos atuais {pop_2024} "
        f"para {pop_2070} em 2070. Uma queda de {percent_change}%."
    )
