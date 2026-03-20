"""Progress Bar Builder Module

This module provides functionality to generate visual progress bars using
high-density Unicode block characters for CLI-style display.
"""


class ProgressBarBuilder:
    """Builds visual progress bars using Unicode block characters.
    
    The progress bar consists of exactly 25 characters total, using:
    - █ (Full Block) for completed progress
    - ▒ (Medium Shade) for remaining progress
    
    Example: ██████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 40%
    """
    
    FILLED_BLOCK = "█"  # Full Block (U+2588)
    EMPTY_BLOCK = "▒"   # Medium Shade (U+2592)
    TOTAL_BLOCKS = 25
    
    @staticmethod
    def build(percentage: float) -> str:
        """Generate a 25-character progress bar based on percentage.
        
        Args:
            percentage: Progress percentage (0-100)
            
        Returns:
            A string containing exactly 25 Unicode block characters
            
        Example:
            >>> ProgressBarBuilder.build(0)
            '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
            >>> ProgressBarBuilder.build(40)
            '██████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
            >>> ProgressBarBuilder.build(100)
            '█████████████████████████'
        """
        # Calculate filled blocks based on percentage
        filled_blocks = round((percentage / 100) * ProgressBarBuilder.TOTAL_BLOCKS)
        
        # Ensure filled_blocks is within valid range [0, 25]
        filled_blocks = max(0, min(filled_blocks, ProgressBarBuilder.TOTAL_BLOCKS))
        
        # Calculate empty blocks to ensure total is always 25
        empty_blocks = ProgressBarBuilder.TOTAL_BLOCKS - filled_blocks
        
        # Build and return the progress bar string
        return (ProgressBarBuilder.FILLED_BLOCK * filled_blocks + 
                ProgressBarBuilder.EMPTY_BLOCK * empty_blocks)
