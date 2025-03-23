from src.utils.formatting import BrazilianFormatter

def generate_growth_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate the first paragraph about population growth.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph string about population growth
    """
    # Get state data and growth
    state_info, growth, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    # Get first census data
    first_census = data_loader.get_first_census_data(state_code)
    if not first_census:
        return None
    
    first_year, _ = first_census
    
    # Format the growth number
    formatter = BrazilianFormatter()
    growth_formatted = formatter.format_number(int(growth))
    
    return f"Desde o ano de {first_year} até 2024, a população do estado do {state_name} cresceu em {growth_formatted} vezes."
