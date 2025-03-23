import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict, Any

class DataLoader:
    # State code to name mapping
    STATE_NAMES = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }
    
    # State creation years mapping
    STATE_CREATION_YEARS = {
        'AC': 1962,  # Acre
        'AL': 1817,  # Alagoas
        'AP': 1988,  # Amapá
        'AM': 1850,  # Amazonas
        'BA': 1549,  # Bahia
        'CE': 1822,  # Ceará
        'DF': 1960,  # Distrito Federal
        'ES': 1822,  # Espírito Santo
        'GO': 1748,  # Goiás
        'MA': 1621,  # Maranhão
        'MT': 1748,  # Mato Grosso
        'MS': 1979,  # Mato Grosso do Sul
        'MG': 1720,  # Minas Gerais
        'PA': 1616,  # Pará
        'PB': 1585,  # Paraíba
        'PR': 1853,  # Paraná
        'PE': 1534,  # Pernambuco
        'PI': 1811,  # Piauí
        'RJ': 1565,  # Rio de Janeiro
        'RN': 1599,  # Rio Grande do Norte
        'RS': 1807,  # Rio Grande do Sul
        'RO': 1981,  # Rondônia
        'RR': 1988,  # Roraima
        'SC': 1738,  # Santa Catarina
        'SP': 1554,  # São Paulo
        'SE': 1820,  # Sergipe
        'TO': 1988   # Tocantins
    }
    
    def get_state_creation_year(self, state_code: str) -> Optional[int]:
        """Get the creation year for a specific state.
        
        Args:
            state_code: Two-letter state code
            
        Returns:
            Year of state creation or None if state code is invalid
        """
        return self.STATE_CREATION_YEARS.get(state_code)
    
    def __init__(self, ranking_file: str, growth_file: str, age_data_file: str = None):
        """Initialize DataLoader with file paths.
        
        Args:
            ranking_file: Path to ranking CSV file
            growth_file: Path to growth data CSV file
            age_data_file: Path to age group data CSV file
        """
        self.ranking_file = ranking_file
        self.growth_file = growth_file
        self.age_data_file = age_data_file
        self.df_ranking = None
        self.df_growth = None
        self.df_age_data = None
        
    def load_data(self) -> None:
        """Load CSV files into DataFrames."""
        self.df_ranking = pd.read_csv(self.ranking_file)
        self.df_growth = pd.read_csv(self.growth_file)
        if self.age_data_file:
            self.df_age_data = pd.read_csv(self.age_data_file)
    
    def get_state_data(self, state_code: str) -> Tuple[Dict[str, Any], float, int, int]:
        """Get comprehensive data for a specific state.
        
        Args:
            state_code: Two-letter state code (e.g., 'AC' for Acre)
            
        Returns:
            Tuple containing:
            - Dictionary with state basic info (name, region)
            - Growth multiplier
            - National ranking position
            - Total number of states
            
        Raises:
            ValueError: If state data cannot be found
        """
        if self.df_ranking is None or self.df_growth is None:
            self.load_data()
            
        # Get state name from code
        state_name = self.STATE_NAMES.get(state_code)
        if not state_name:
            raise ValueError(f"Invalid state code: {state_code}")
            
        # Get state info from ranking DataFrame
        state_mask = self.df_ranking['LOCAL'] == state_name
        if not state_mask.any():
            raise ValueError(f"No data found for state: {state_name}")
            
        state_info = self.df_ranking[state_mask].iloc[0]
        
        # Get growth data
        growth_mask = self.df_growth['Estado'] == state_code
        if not growth_mask.any():
            raise ValueError(f"No growth data found for state: {state_name}")
            
        growth = self.df_growth.loc[growth_mask, 'x_crescimento'].iloc[0]
        
        # Calculate ranking
        df_ranking = self.df_growth.sort_values('x_crescimento', ascending=False).reset_index(drop=True)
        position = df_ranking[df_ranking['Estado'] == state_code].index[0] + 1
        total_states = len(self.df_growth)
        
        return {
            'name': state_name,
            'region': state_info['Grande-regiao']
        }, growth, position, total_states
    
    def get_first_census_data(self, state_code: str) -> Optional[Tuple[str, float]]:
        """Get the first available census data for a state.
        
        Args:
            state_code: Two-letter state code
            
        Returns:
            Tuple of (year, population) or None if no data found
        """
        if self.df_ranking is None:
            self.load_data()
        
        # Get state name from code
        state_name = self.STATE_NAMES.get(state_code)
        if not state_name:
            return None
            
        state_mask = self.df_ranking['LOCAL'] == state_name
        if not state_mask.any():
            return None
            
        state_data = self.df_ranking[state_mask].iloc[0]
        
        # List of census years to check
        census_years = ['1872', '1890', '1900', '1910', '1920', '1940', '1950', '1960']
        
        # Find first year with data
        for year in census_years:
            if year in state_data.index:
                value = state_data[year]
                if pd.notna(value) and value != 0:
                    return year, value
        
        return None
    
    def get_regional_ranking(self, state_code: str, region: str) -> int:
        """Get state's ranking within its region.
        
        Args:
            state_code: Two-letter state code
            region: Region name
            
        Returns:
            Regional ranking position
            
        Raises:
            ValueError: If regional ranking cannot be determined
        """
        if self.df_growth is None:
            self.load_data()
            
        df_region = self.df_growth[self.df_growth['Grande-regiao'] == region]
        if df_region.empty:
            raise ValueError(f"No data found for region: {region}")
            
        region_mask = df_region['Estado'] == state_code
        if not region_mask.any():
            raise ValueError(f"State {state_code} not found in region {region}")
            
        df_region = df_region.sort_values('x_crescimento', ascending=False).reset_index(drop=True)
        return df_region[df_region['Estado'] == state_code].index[0] + 1
        
    def get_age_group_data(self, state_name: str) -> Dict[str, float]:
        """Get age group data for a specific state.
        
        Args:
            state_name: Full state name
            
        Returns:
            Dictionary with age group data including:
            - Population 0-4 years (2024)
            - Population 0-4 years (2070)
            - % Change 0-4 years
            
        Raises:
            ValueError: If age group data cannot be found
        """
        if self.df_age_data is None:
            if not self.age_data_file:
                raise ValueError("Age data file not provided")
            self.df_age_data = pd.read_csv(self.age_data_file)
            
        state_mask = self.df_age_data['Local'] == state_name
        if not state_mask.any():
            raise ValueError(f"No age group data found for state: {state_name}")
            
        state_data = self.df_age_data[state_mask].iloc[0]
        
        return {
            'pop_0_4_2024': state_data['População 0-4 anos (2024)'],
            'pop_0_4_2070': state_data['População 0-4 anos (2070)'],
            'change_percent': abs(state_data['% Mudança 0-4 anos']),
            'pop_65_2024': state_data['População acima de 65 anos (2024)'],
            'pop_65_2070': state_data['População acima de 65 anos (2070)'],
            'change_factor_65': round(state_data['Fator de Mudança acima de 65 anos'].astype(float), 1)
        }
