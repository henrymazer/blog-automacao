from src.utils.text_utils import format_historical_info

def generate_historical_paragraph(data_loader, api_client, state_code: str = 'AC') -> str:
    """Generate paragraph about historical information.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        api_client: PerplexityAPI instance for historical queries
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph text with historical information
    """
    # Get first census data to get the year
    first_census = data_loader.get_first_census_data(state_code)
    if not first_census:
        return None
        
    first_year, _ = first_census
    
    # Get state info
    try:
        state_data, _, _, _ = data_loader.get_state_data(state_code)
        if not state_data:
            return None
        
        state_name = state_data['name']
    except Exception:
        return None
    
    # Get historical information via API
    historical_info = api_client.get_historical_info(first_year, state_name)
    if not historical_info:
        return None
        
    # Format the response
    return format_historical_info(historical_info)
