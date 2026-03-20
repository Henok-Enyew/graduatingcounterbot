"""Message Formatter Module

This module provides functionality to format countdown messages for Telegram.
Messages include days remaining, progress bars, and motivational content with
proper formatting and special character escaping.
"""

from graduation_quotes import GraduationQuotes


class MessageFormatter:
    """Formats countdown messages for Telegram with proper markup.
    
    Composes structured messages containing countdown information, progress
    visualization, and motivational content. Handles special cases like
    graduation day and post-graduation scenarios.
    """
    
    @staticmethod
    def format_group_message(
        days_remaining: int,
        progress_bar: str,
        progress_percent: float
    ) -> str:
        """Format message for GROUP chats with motivational quote.
        
        Creates an energetic group message for BiT Class of 2026.
        
        Args:
            days_remaining: Number of days until graduation
            progress_bar: Visual progress bar string (25 characters)
            progress_percent: Progress percentage (0-100)
            
        Returns:
            Formatted message string with HTML markup and quote for Telegram
        """
        # Get a random graduation quote
        quote = GraduationQuotes.get_random_quote()
        
        # Handle special cases
        if days_remaining == 0:
            return (
                "🎓 <b>Hello GC People!</b> 🎓\n\n"
                f"{progress_bar} 100%\n\n"
                "<b>🎉 TODAY IS THE DAY! 🎉</b>\n"
                "We made it! Graduation Day is here!\n\n"
                "Saturday, June 27, 2026\n\n"
                f"<blockquote>{quote}</blockquote>"
            )
        
        if days_remaining < 0:
            return (
                "🎓 <b>Hello GC People!</b> 🎓\n\n"
                f"{progress_bar} 100%\n\n"
                "<b>✨ We Did It! ✨</b>\n"
                "BiT Class of 2026 - Graduated!\n\n"
                "Saturday, June 27, 2026\n\n"
                f"<blockquote>{quote}</blockquote>"
            )
        
        # Standard countdown message for groups
        days_text = "day" if days_remaining == 1 else "days"
        
        # Creative group messages based on days remaining
        if days_remaining <= 10:
            encouragement = "🔥 Final sprint! We're almost there! Keep pushing!"
        elif days_remaining <= 30:
            encouragement = "💪 The finish line is in sight! Stay strong!"
        elif days_remaining <= 50:
            encouragement = "⚡ Halfway through! Keep the momentum going!"
        else:
            encouragement = "🚀 We're on this journey together! Let's do this!"
        
        return (
            "🎓 <b>Hello GC People!</b> 🎓\n\n"
            f"{progress_bar} {progress_percent:.0f}%\n\n"
            f"{encouragement}\n\n"
            f"Only <b>{days_remaining} {days_text}</b> left until our BiT Graduation!\n"
            "Saturday, June 27, 2026\n\n"
            f"<blockquote>{quote}</blockquote>"
        )
    
    @staticmethod
    def format_start_command_message(
        days_remaining: int,
        progress_bar: str,
        progress_percent: float
    ) -> str:
        """Format message for DIRECT MESSAGE (/start command).
        
        Creates a personal greeting for individual users.
        
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
        
        # Standard countdown message for direct messages
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
        """Format a complete countdown message for GROUP chats.
        
        Uses the group message format with motivational quotes.
        This is for daily automated messages sent to groups.
        
        Args:
            days_remaining: Number of days until graduation (can be negative)
            progress_bar: Visual progress bar string (25 characters)
            progress_percent: Progress percentage (0-100)
            is_graduation_day: True if today is graduation day
            is_past_graduation: True if today is after graduation
            
        Returns:
            Formatted message string with HTML markup for Telegram
        """
        # Use the group message format for daily messages
        return MessageFormatter.format_group_message(
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
