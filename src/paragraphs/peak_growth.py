import pandas as pd
from ..utils.formatting import format_number

def get_peak_growth_period(df, state):
    """
    Find the period of highest geometric growth rate for a given state.
    
    Args:
        df (pd.DataFrame): DataFrame containing the census data
        state (str): Name of the state to analyze
        
    Returns:
        tuple: (start_year, end_year, growth_rate) or None if no valid data
    """
    # Filter state data
    state_data = df[df['Estado'] == state]
    if state_data.empty:
        return None
        
    # Get all growth rate columns (they start with "Taxa_Crescimento_Geometrico_")
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
            max_period = (start_year, end_year, rate * 100)  # Convert to percentage
    
    return max_period if max_rate != float('-inf') else None

def generate_peak_growth_paragraph(state, start_year, end_year, growth_rate):
    """
    Generate a paragraph describing the period of highest growth for a state.
    
    Args:
        state (str): Name of the state
        start_year (str): Starting census year
        end_year (str): Ending census year
        growth_rate (float): Growth rate for the period
        
    Returns:
        str: Formatted paragraph text
    """
    formatted_rate = f"{growth_rate:.1f}".replace('.', ',')
    
    return (
        f"O período de maior crescimento populacional do {state} foi entre os censos de "
        f"{start_year} e {end_year}, quando o estado registrou uma taxa de crescimento "
        f"geométrico de {formatted_rate}%."
    )
