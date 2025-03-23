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
    _, _, position, total_states = data_loader.get_state_data(state_code)
    
    # Generate description using updated get_ranking_description
    description = get_ranking_description(position, total_states)
    
    # Capitalize first letter since this is a standalone paragraph
    return description[0].upper() + description[1:]
