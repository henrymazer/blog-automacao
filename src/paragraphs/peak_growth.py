import pandas as pd
from src.utils.formatting import BrazilianFormatter

def generate_peak_growth_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph about the period of highest growth for a state.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph text describing peak growth period
    """
    # Get state info
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    # Get growth data from DataFrame
    df = data_loader.df_growth
    state_data = df[df['Estado'] == state_code]
    if state_data.empty:
        return None
    
    # Find peak growth period
    growth_cols = [col for col in df.columns if col.startswith("Taxa_Crescimento_Geometrico_")]
    max_rate = float('-inf')
    max_period = None
    
    for col in growth_cols:
        # Extract years from column name
        _, start_year, end_year = col.split('_')[-3:]
        
        # Get growth rate value
        rate = state_data[col].iloc[0]
        
        # Check if rate is valid (not NaN or null)
        if pd.notna(rate) and rate > max_rate:
            max_rate = rate
            max_period = (start_year, end_year, rate)
    
    if not max_period:
        return None
        
    start_year, end_year, growth_rate = max_period
    
    # Format the growth rate using Brazilian standards
    formatter = BrazilianFormatter()
    formatted_rate = formatter.format_percentage(growth_rate)
    
    return f"O período de maior crescimento populacional do {state_name} foi entre os censos de {start_year} e {end_year}, quando o estado registrou uma taxa de crescimento geométrico de {formatted_rate}."
