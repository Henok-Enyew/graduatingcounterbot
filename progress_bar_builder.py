"""Progress Bar Builder Module

This module provides functionality to generate visual progress bars using emoji blocks.
The progress bar represents completion percentage with filled and empty blocks.
"""


class ProgressBarBuilder:
    """Builds visual progress bars using emoji blocks.
    
    The progress bar consists of exactly 10 blocks total, with filled blocks
    representing completed progress and empty blocks representing remaining progress.
    """
    
    FILLED_BLOCK = "🟦"
    EMPTY_BLOCK = "⬜"
    TOTAL_BLOCKS = 10
    
    @staticmethod
    def build(percentage: float) -> str:
        """Generate a 10-block progress bar based on percentage.
        
        Args:
            percentage: Progress percentage (0-100)
            
        Returns:
            A string containing exactly 10 emoji blocks representing the progress
            
        Example:
            >>> ProgressBarBuilder.build(0)
            '⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜'
            >>> ProgressBarBuilder.build(50)
            '🟦🟦🟦🟦🟦⬜⬜⬜⬜⬜'
            >>> ProgressBarBuilder.build(100)
            '🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦'
        """
        # Calculate filled blocks by rounding percentage to nearest 10%
        filled_blocks = round(percentage / 10)
        
        # Ensure filled_blocks is within valid range [0, 10]
        filled_blocks = max(0, min(filled_blocks, ProgressBarBuilder.TOTAL_BLOCKS))
        
        # Calculate empty blocks to ensure total is always 10
        empty_blocks = ProgressBarBuilder.TOTAL_BLOCKS - filled_blocks
        
        # Build and return the progress bar string
        return (ProgressBarBuilder.FILLED_BLOCK * filled_blocks + 
                ProgressBarBuilder.EMPTY_BLOCK * empty_blocks)
