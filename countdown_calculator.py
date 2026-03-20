"""Countdown Calculator module for Telegram Graduation Countdown Bot.

This module provides temporal metrics calculation for countdown messages.
"""

from datetime import date, datetime


class CountdownCalculator:
    """Calculator for countdown metrics and graduation date tracking."""
    
    START_DATE = date(2021, 10, 1)
    GRADUATION_DATE = date(2026, 6, 27)
    
    @staticmethod
    def days_remaining() -> int:
        """Returns days from today to graduation date, minimum 0.
        
        Calculates the number of days between the current date and the
        graduation date. Returns 0 if the current date is on or after
        the graduation date.
        
        Returns:
            int: Number of days remaining until graduation (minimum 0).
        """
        today = date.today()
        delta = CountdownCalculator.GRADUATION_DATE - today
        return max(0, delta.days)
    
    @staticmethod
    def progress_percentage() -> float:
        """Returns percentage of time elapsed from start to graduation (0-100).
        
        Calculates the progress percentage based on the elapsed time from
        the start date to the current date, relative to the total time
        from start date to graduation date. The result is clamped to the
        range [0, 100].
        
        Returns:
            float: Progress percentage clamped to 0-100 range.
        """
        today = date.today()
        total_days = (CountdownCalculator.GRADUATION_DATE - CountdownCalculator.START_DATE).days
        elapsed_days = (today - CountdownCalculator.START_DATE).days
        
        if elapsed_days <= 0:
            return 0.0
        if elapsed_days >= total_days:
            return 100.0
        
        percentage = (elapsed_days / total_days) * 100
        return max(0.0, min(100.0, percentage))
    
    @staticmethod
    def is_graduation_day() -> bool:
        """Returns True if today is graduation date.
        
        Returns:
            bool: True if current date equals graduation date, False otherwise.
        """
        return date.today() == CountdownCalculator.GRADUATION_DATE
    
    @staticmethod
    def is_past_graduation() -> bool:
        """Returns True if today is after graduation date.
        
        Returns:
            bool: True if current date is after graduation date, False otherwise.
        """
        return date.today() > CountdownCalculator.GRADUATION_DATE
