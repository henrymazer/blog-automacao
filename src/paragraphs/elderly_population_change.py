def generate_elderly_population_change_paragraph(data_loader, formatter, state_code: str = 'AC') -> str:
    """Generate paragraph about change in elderly population.
    
    Args:
        data_loader: DataLoader instance
        formatter: BrazilianFormatter instance for number formatting
        state_code: Two-letter state code
        
    Returns:
        Formatted paragraph about elderly population change
    """
    # Get state info
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    # Get age group data
    age_data = data_loader.get_age_group_data(state_name)
    
    # Format population numbers using Brazilian formatter
    pop_2024 = formatter.format_population(int(age_data['pop_65_2024']))
    pop_2070 = formatter.format_population(int(age_data['pop_65_2070']))
    
    # Format change factor (already rounded) with comma decimal separator
    change_factor = str(age_data['change_factor_65']).replace('.', ',')
    
    return (
        f"Essa parte da população sairá de {pop_2024} para {pop_2070}, "
        f"um aumento de {change_factor} vezes."
    )
