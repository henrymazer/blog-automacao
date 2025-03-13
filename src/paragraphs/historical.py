from src.data.loader import get_first_census_data
from src.utils.api import get_historical_info
from src.utils.formatting import format_historical_info

def generate_historical_paragraph(df, state_code='AC'):
    """Generate the fourth paragraph about historical information."""
    # Get first census data to get the year
    census_data = get_first_census_data(df, state_code)
    if not census_data:
        return None
        
    primeiro_ano = census_data['ano']
    
    # Get and format historical information
    historical_info = get_historical_info(primeiro_ano)
    if not historical_info:
        return None
        
    formatted_info = format_historical_info(historical_info)
    return formatted_info
