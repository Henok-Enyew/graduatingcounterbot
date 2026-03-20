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
        motivational_message: str
    ) -> str:
        """Format a personalized message for the /start command.
        
        Creates a friendly greeting message for users who start the bot
        in a direct message.
        
        Args:
            days_remaining: Number of days until graduation
            progress_bar: Visual progress bar string
            motivational_message: Motivational quote or message
            
        Returns:
            Formatted message string with HTML markup for Telegram
        """
        escaped_message = MessageFormatter._escape_html(motivational_message)
        
        message_parts = [
            "Hey Graduating Ninja! 🥷",
            "",
            f"How are you doing? You have <b>{days_remaining} days</b> left until graduation!",
            "",
            "<b>Progress:</b>",
            progress_bar,
            "",
            f"💡 <i>{escaped_message}</i>"
        ]
        
        return "\n".join(message_parts)
    
    @staticmethod
    def format_countdown_message(
        days_remaining: int,
        progress_bar: str,
        motivational_message: str,
        is_graduation_day: bool = False,
        is_past_graduation: bool = False
    ) -> str:
        """Format a complete countdown message with all components.
        
        Creates a structured message with emoji headers, days remaining count,
        progress bar visualization, and motivational content. Handles special
        cases for graduation day and post-graduation scenarios.
        
        Args:
            days_remaining: Number of days until graduation (0 or positive)
            progress_bar: Visual progress bar string (emoji blocks)
            motivational_message: Motivational quote or message
            is_graduation_day: True if today is graduation day
            is_past_graduation: True if today is after graduation
            
        Returns:
            Formatted message string with HTML markup for Telegram
            
        Example:
            >>> MessageFormatter.format_countdown_message(
            ...     days_remaining=100,
            ...     progress_bar="🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜",
            ...     motivational_message="Keep coding!",
            ...     is_graduation_day=False,
            ...     is_past_graduation=False
            ... )
            '🎓 <b>Graduation Countdown</b> 🎓\\n\\n📅 <b>Days Remaining:</b> 100 days\\n\\n<b>Progress:</b>\\n🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜\\n\\n💡 <i>Keep coding!</i>'
        """
        # Handle special case: graduation day
        if is_graduation_day:
            return MessageFormatter._format_graduation_day_message(
                progress_bar, motivational_message
            )
        
        # Handle special case: past graduation
        if is_past_graduation:
            return MessageFormatter._format_post_graduation_message(
                progress_bar, motivational_message
            )
        
        # Format standard countdown message
        return MessageFormatter._format_standard_message(
            days_remaining, progress_bar, motivational_message
        )
    
    @staticmethod
    def _format_standard_message(
        days_remaining: int,
        progress_bar: str,
        motivational_message: str
    ) -> str:
        """Format a standard countdown message.
        
        Args:
            days_remaining: Number of days until graduation
            progress_bar: Visual progress bar string
            motivational_message: Motivational quote or message
            
        Returns:
            Formatted message string with HTML markup
        """
        # Escape special HTML characters in motivational message
        escaped_message = MessageFormatter._escape_html(motivational_message)
        
        # Build message with HTML formatting
        message_parts = [
            "🎓 <b>Graduation Countdown</b> 🎓",
            "",
            f"📅 <b>Days Remaining:</b> {days_remaining} days",
            "",
            "<b>Progress:</b>",
            progress_bar,
            "",
            f"💡 <i>{escaped_message}</i>"
        ]
        
        return "\n".join(message_parts)
    
    @staticmethod
    def _format_graduation_day_message(
        progress_bar: str,
        motivational_message: str
    ) -> str:
        """Format a special message for graduation day.
        
        Args:
            progress_bar: Visual progress bar string (should be 100% filled)
            motivational_message: Motivational quote or message
            
        Returns:
            Formatted graduation day message with HTML markup
        """
        escaped_message = MessageFormatter._escape_html(motivational_message)
        
        message_parts = [
            "🎓 <b>Graduation Day!</b> 🎓",
            "",
            "🎉 <b>Congratulations!</b> Today is the day! 🎉",
            "",
            "<b>Progress:</b>",
            progress_bar,
            "",
            f"💡 <i>{escaped_message}</i>"
        ]
        
        return "\n".join(message_parts)
    
    @staticmethod
    def _format_post_graduation_message(
        progress_bar: str,
        motivational_message: str
    ) -> str:
        """Format a special message for after graduation.
        
        Args:
            progress_bar: Visual progress bar string (should be 100% filled)
            motivational_message: Motivational quote or message
            
        Returns:
            Formatted post-graduation message with HTML markup
        """
        escaped_message = MessageFormatter._escape_html(motivational_message)
        
        message_parts = [
            "🎓 <b>Post-Graduation</b> 🎓",
            "",
            "✨ <b>Journey Complete!</b> ✨",
            "",
            "<b>Progress:</b>",
            progress_bar,
            "",
            f"💡 <i>{escaped_message}</i>"
        ]
        
        return "\n".join(message_parts)
    
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
