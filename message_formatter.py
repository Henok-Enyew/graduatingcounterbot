"""Message Formatter Module

This module provides functionality to format countdown messages for Telegram.
Messages include days remaining, progress bars, and motivational content with
proper formatting and special character escaping.
"""


class MessageFormatter:
    """Formats countdown messages for Telegram with proper markup.
    
    Composes structured messages containing countdown information, progress
    visualization, and motivational content. Handles special cases like
    graduation day and post-graduation scenarios.
    """
    
    @staticmethod
    def format_start_command_message(
        days_remaining: int,
        progress_bar: str,
        progress_percent: float
    ) -> str:
        """Format the all-in-one caption for /start command and daily messages.
        
        Creates the unified caption format for BiT graduation countdown.
        
        Args:
            days_remaining: Number of days until graduation
            progress_bar: Visual progress bar string (25 characters)
            progress_percent: Progress percentage (0-100)
            
        Returns:
            Formatted message string with HTML markup for Telegram
        """
        # Handle special cases
        if days_remaining == 0:
            return (
                "Hey Graduating Ninja! 🥷\n\n"
                f"{progress_bar} 100%\n\n"
                "<b>Day 0: Graduation Day!</b> 🎉\n"
                "Saturday, June 27, 2026"
            )
        
        if days_remaining < 0:
            return (
                "Hey Graduating Ninja! 🥷\n\n"
                f"{progress_bar} 100%\n\n"
                "<b>Graduation Complete!</b> ✨\n"
                "Saturday, June 27, 2026"
            )
        
        # Standard countdown message
        days_text = "day" if days_remaining == 1 else "days"
        
        return (
            "Hey Graduating Ninja! 🥷\n\n"
            f"{progress_bar} {progress_percent:.0f}%\n\n"
            f"Only <b>{days_remaining} {days_text}</b> left until our BiT Graduation!\n"
            "Saturday, June 27, 2026"
        )
    
    @staticmethod
    def format_countdown_message(
        days_remaining: int,
        progress_bar: str,
        progress_percent: float,
        is_graduation_day: bool = False,
        is_past_graduation: bool = False
    ) -> str:
        """Format a complete countdown message with all components.
        
        Uses the unified BiT graduation countdown format.
        This is the same format as the /start command for consistency.
        
        Args:
            days_remaining: Number of days until graduation (can be negative)
            progress_bar: Visual progress bar string (25 characters)
            progress_percent: Progress percentage (0-100)
            is_graduation_day: True if today is graduation day
            is_past_graduation: True if today is after graduation
            
        Returns:
            Formatted message string with HTML markup for Telegram
        """
        # Use the same format as /start command for consistency
        return MessageFormatter.format_start_command_message(
            days_remaining=days_remaining,
            progress_bar=progress_bar,
            progress_percent=progress_percent
        )
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape special HTML characters for Telegram HTML formatting.
        
        Telegram's HTML parser requires escaping of special characters
        to prevent parsing errors.
        
        Args:
            text: Raw text that may contain special characters
            
        Returns:
            Text with HTML special characters escaped
        """
        # Escape HTML special characters
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
        }
        
        result = text
        for char, escaped in replacements.items():
            result = result.replace(char, escaped)
        
        return result
