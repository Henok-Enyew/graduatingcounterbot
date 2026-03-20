"""Scheduler Module

This module handles daily scheduling of countdown messages using APScheduler.
"""

import logging
import asyncio
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class DailyScheduler:
    """Schedules and executes daily countdown message jobs.
    
    Uses AsyncIOScheduler to trigger message generation and distribution
    at a specified time each day (00:01 AM by default).
    """
    
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
        
        Sets up a daily job to run at 00:01 AM system time and starts
        the scheduler. The scheduler runs in non-blocking mode.
        """
        try:
            # Configure daily job at 00:01 AM
            self.scheduler.add_job(
                self.execute_daily_job,
                trigger=CronTrigger(hour=0, minute=1),
                id='daily_countdown_message',
                name='Daily Countdown Message',
                replace_existing=True
            )
            
            # Start the scheduler
            self.scheduler.start()
            
            self.logger.info("Scheduler started - daily messages will be sent at 00:01 AM")
            
        except Exception as e:
            self.logger.error(f"Failed to start scheduler: {str(e)}")
            raise
    
    async def execute_daily_job(self):
        """Execute the daily job function.
        
        This method is called by the scheduler at the configured time.
        It wraps the job function with error handling to ensure the
        scheduler continues running even if a job fails.
        """
        try:
            self.logger.info("Executing daily countdown message job")
            await self.job_function()
            self.logger.info("Daily countdown message job completed successfully")
            
        except Exception as e:
            self.logger.error(
                f"Error executing daily job: {str(e)}",
                exc_info=True
            )
            # Don't re-raise - let scheduler continue for next day
    
    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        try:
            self.scheduler.shutdown(wait=False)
            self.logger.info("Scheduler shut down")
        except Exception as e:
            self.logger.error(f"Error shutting down scheduler: {str(e)}")
