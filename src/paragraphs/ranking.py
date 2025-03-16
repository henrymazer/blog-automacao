from src.utils.text_utils import get_ranking_description

def generate_ranking_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph about state's growth ranking.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph text describing growth ranking
    """
    # Get state info and basic data
    state_info, _, position, total_states = data_loader.get_state_data(state_code)
    region = state_info['region']
    
    if position <= 5 or position >= total_states - 2:
        # Top 5 or Bottom 3 nationally
        return get_ranking_description(position, total_states)
    else:
        # Regional position
        regional_position = data_loader.get_regional_ranking(state_code, region)
        return get_ranking_description(position, total_states, regional_position, region)
