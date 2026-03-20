"""Test Scheduler - Sends messages every 5 minutes for testing

USAGE:
1. Replace scheduler.py with this file temporarily
2. Deploy to Render
3. Bot will send messages every 5 minutes
4. Revert back to scheduler.py when done testing
"""

import logging
import asyncio
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


class DailyScheduler:
    """TEST VERSION: Schedules messages every 5 minutes for testing."""
    
    def __init__(self, job_function: Callable):
        """Initialize the DailyScheduler.
        
        Args:
            job_function: Async function to call when the scheduled time arrives
        """
        self.job_function = job_function
        self.scheduler = AsyncIOScheduler()
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Configure and start the scheduler.
        
        TEST MODE: Runs every 5 minutes instead of daily at 00:01 AM.
        """
        try:
            # Configure job to run every 5 minutes (FOR TESTING)
            self.scheduler.add_job(
                self.execute_daily_job,
                trigger=IntervalTrigger(minutes=5),
                id='test_countdown_message',
                name='Test Countdown Message (Every 5 min)',
                replace_existing=True
            )
            
            # Start the scheduler
            self.scheduler.start()
            
            self.logger.warning("⚠️ TEST MODE: Scheduler started - messages every 5 minutes!")
            
        except Exception as e:
            self.logger.error(f"Failed to start scheduler: {str(e)}")
            raise
    
    async def execute_daily_job(self):
        """Execute the daily job function.
        
        This method is called by the scheduler every 5 minutes in test mode.
        """
        try:
            self.logger.info("Executing test countdown message job (5-min interval)")
            await self.job_function()
            self.logger.info("Test countdown message job completed successfully")
            
        except Exception as e:
            self.logger.error(
                f"Error executing test job: {str(e)}",
                exc_info=True
            )
    
    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        try:
            self.scheduler.shutdown(wait=False)
            self.logger.info("Scheduler shut down")
        except Exception as e:
            self.logger.error(f"Error shutting down scheduler: {str(e)}")
