import locale
from typing import Optional

class BrazilianFormatter:
    """Handles formatting of numbers and text according to Brazilian standards."""
    
    def format_population(self, value: int) -> str:
        """Format population value in thousands or millions.
        
        Args:
            value: Population value to format
            
        Returns:
            Formatted value with appropriate unit (mil or milhões)
        """
        if value < 1_000_000:  # Less than 1 million
            return f"{value/1000:.0f} mil"
        else:  # 1 million or more
            return f"{value/1_000_000:.2f} milhões".replace('.', ',')
            
    
    def __init__(self):
        """Initialize formatter with Brazilian locale settings."""
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            self.locale_set = True
        except locale.Error:
            print("Warning: Brazilian locale not available. Using fallback formatting.")
            self.locale_set = False
    
    def format_number(self, num: float) -> str:
        """Format a number according to Brazilian standards.
        
        Args:
            num: Number to format
            
        Returns:
            Formatted number string with proper thousands separator
        """
        try:
            if self.locale_set:
                return locale.format_string("%d", num, grouping=True)
            else:
                # Fallback formatting: Use period for thousands
                return format(num, ",").replace(",", ".")
        except:
            # If all else fails, return simple string representation
            return str(int(num))
    
    def format_percentage(self, value: float, decimal_places: int = 1) -> str:
        """Format a percentage value according to Brazilian standards.
        
        Args:
            value: Decimal value to format as percentage
            decimal_places: Number of decimal places to display
            
        Returns:
            Formatted percentage string
        """
        try:
            if self.locale_set:
                format_str = f"%.{decimal_places}f%%"
                return locale.format_string(format_str, value * 100)
            else:
                # Fallback formatting
                return f"{value * 100:.{decimal_places}f}%".replace(".", ",")
        except:
            return f"{value * 100:.{decimal_places}f}%"
    
    def format_year_range(self, start_year: str, end_year: str) -> str:
        """Format a year range for display.
        
        Args:
            start_year: Starting year
            end_year: Ending year
            
        Returns:
            Formatted year range string
        """
        return f"{start_year}-{end_year}"
    
    def format_growth_rate(self, rate: float) -> str:
        """Format a growth rate with appropriate multiplier.
        
        Args:
            rate: Growth rate multiplier
            
        Returns:
            Formatted growth rate string in Portuguese
        """
        if rate < 2:
            return f"{self.format_percentage(rate - 1)} de aumento"
        else:
            return f"{self.format_number(int(rate))} vezes"
