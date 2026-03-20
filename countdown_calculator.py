"""Countdown Calculator module for Telegram Graduation Countdown Bot.

This module provides temporal metrics calculation for countdown messages.
Uses 100-day sprint countdown with Africa/Addis_Ababa timezone.
"""

from datetime import date, datetime, timedelta
import pytz


class CountdownCalculator:
    """Calculator for countdown metrics and graduation date tracking.
    
    Uses 100-day sprint countdown starting from 100 days before graduation.
    All date calculations use Africa/Addis_Ababa timezone.
    """
    
    GRADUATION_DATE = date(2026, 6, 27)
    SPRINT_DAYS = 100
    TIMEZONE = pytz.timezone('Africa/Addis_Ababa')
    
    # Calculate sprint start date (100 days before graduation)
    START_DATE = GRADUATION_DATE - timedelta(days=SPRINT_DAYS)
    
    @staticmethod
    def days_remaining() -> int:
        """Returns days from today to graduation date for 100-day sprint.
        
        Calculates days remaining in the 100-day sprint countdown.
        Uses Africa/Addis_Ababa timezone for accurate date calculation.
        Returns 0 on graduation day, negative if past graduation.
        
        Returns:
            int: Number of days remaining (can be negative if past graduation).
        """
        # Get current date in Africa/Addis_Ababa timezone
        now = datetime.now(CountdownCalculator.TIMEZONE)
        today = now.date()
        
        delta = CountdownCalculator.GRADUATION_DATE - today
        return delta.days
    
    @staticmethod
    def progress_percentage() -> float:
        """Returns percentage of 100-day sprint completed (0-100).
        
        Calculates progress based on 100-day sprint countdown.
        - If more than 100 days remain: 0%
        - If 0 days remain (graduation day): 100%
        - If past graduation: 100%
        
        Formula: progress = (100 - days_left) for the 100-day sprint
        
        Returns:
            float: Progress percentage clamped to 0-100 range.
        """
        days_left = CountdownCalculator.days_remaining()
        
        # If more than 100 days until graduation, show 0%
        if days_left > CountdownCalculator.SPRINT_DAYS:
            return 0.0
        
        # If past graduation, show 100%
        if days_left < 0:
            return 100.0
        
        # Calculate progress: (100 - days_left) gives us progress out of 100
        progress = CountdownCalculator.SPRINT_DAYS - days_left
        percentage = (progress / CountdownCalculator.SPRINT_DAYS) * 100
        
        return max(0.0, min(100.0, percentage))
    
    @staticmethod
    def is_graduation_day() -> bool:
        """Returns True if today is graduation date.
        
        Uses Africa/Addis_Ababa timezone for accurate date check.
        
        Returns:
            bool: True if current date equals graduation date, False otherwise.
        """
        now = datetime.now(CountdownCalculator.TIMEZONE)
        today = now.date()
        return today == CountdownCalculator.GRADUATION_DATE
    
    @staticmethod
    def is_past_graduation() -> bool:
        """Returns True if today is after graduation date.
        
        Uses Africa/Addis_Ababa timezone for accurate date check.
        
        Returns:
            bool: True if current date is after graduation date, False otherwise.
        """
        now = datetime.now(CountdownCalculator.TIMEZONE)
        today = now.date()
        return today > CountdownCalculator.GRADUATION_DATE
