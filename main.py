"""Main Entry Point for Telegram Graduation Countdown Bot

This module orchestrates all components: configuration, scheduling,
keep-alive server, and message distribution.
"""

import asyncio
import logging
import signal
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config
from logging_config import setup_logging
from keep_alive_server import KeepAliveServer
from scheduler import DailyScheduler
from message_distributor import MessageDistributor
from countdown_calculator import CountdownCalculator
from progress_bar_builder import ProgressBarBuilder
from message_formatter import MessageFormatter
from image_selector import ImageSelector


# Global variables for cleanup
scheduler = None
application = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command.
    
    Sends the BiT graduation countdown as a photo with caption
    to users who start the bot in direct message.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Generate countdown data
        calculator = CountdownCalculator()
        days = calculator.days_remaining()
        progress_pct = calculator.progress_percentage()
        
        # Generate progress bar
        progress_bar = ProgressBarBuilder.build(progress_pct)
        
        # Format message
        message = MessageFormatter.format_start_command_message(
            days_remaining=days,
            progress_bar=progress_bar,
            progress_percent=progress_pct
        )
        
        # Get random image
        image_selector = ImageSelector()
        image_path = image_selector.get_random_image_path()
        
        # Send photo with caption or text fallback
        if image_path:
            try:
                with open(image_path, 'rb') as photo_file:
                    await update.message.reply_photo(
                        photo=photo_file,
                        caption=message,
                        parse_mode="HTML"
                    )
                logger.info(f"Sent /start photo response to user {update.effective_user.id}")
            except Exception as e:
                logger.warning(f"Failed to send photo, falling back to text: {str(e)}")
                await update.message.reply_text(message, parse_mode="HTML")
        else:
            # No image available, send text only
            await update.message.reply_text(message, parse_mode="HTML")
            logger.info(f"Sent /start text response to user {update.effective_user.id}")
            
    except Exception as e:
        logger.error(f"Error handling /start command: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )


async def send_daily_countdown():
    """Generate and send daily countdown message to all groups.
    
    This function is called by the scheduler at 00:01 AM daily.
    It generates the BiT graduation countdown message and distributes
    it to all configured groups as a photo with caption.
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting daily countdown message generation")
        
        # Load configuration
        bot_token = Config.get_bot_token()
        group_ids = Config.get_group_ids()
        
        # Generate countdown data
        calculator = CountdownCalculator()
        days = calculator.days_remaining()
        progress_pct = calculator.progress_percentage()
        
        # Generate progress bar
        progress_bar = ProgressBarBuilder.build(progress_pct)
        
        # Format message
        message = MessageFormatter.format_countdown_message(
            days_remaining=days,
            progress_bar=progress_bar,
            progress_percent=progress_pct,
            is_graduation_day=calculator.is_graduation_day(),
            is_past_graduation=calculator.is_past_graduation()
        )
        
        # Get random image
        image_selector = ImageSelector()
        image_path = image_selector.get_random_image_path()
        
        # Distribute message to all groups
        distributor = MessageDistributor(bot_token, group_ids)
        results = await distributor.distribute_message(message, image_path)
        
        # Log results
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        logger.info(
            f"Daily message distribution complete: {successful} successful, {failed} failed"
        )
        
    except Exception as e:
        logger.error(f"Error in daily countdown job: {str(e)}", exc_info=True)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully.
    
    Args:
        signum: Signal number
        frame: Current stack frame
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Received signal {signum}, shutting down...")
    
    # Shutdown scheduler
    if scheduler:
        scheduler.shutdown()
    
    # Shutdown application
    if application:
        asyncio.create_task(application.shutdown())
    
    sys.exit(0)


async def main():
    """Main entry point for the bot.
    
    Initializes all components, starts the keep-alive server,
    sets up the Telegram bot with command handlers, and starts
    the scheduler for daily messages.
    """
    global scheduler, application
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Telegram Graduation Countdown Bot")
        
        # Load configuration
        logger.info("Loading configuration...")
        bot_token = Config.get_bot_token()
        group_ids = Config.get_group_ids()
        port = Config.get_port()
        
        logger.info(f"Configuration loaded: {len(group_ids)} groups, port {port}")
        
        # Start keep-alive server
        logger.info("Starting keep-alive server...")
        keep_alive = KeepAliveServer(port)
        keep_alive.start()
        
        # Create Telegram application
        logger.info("Initializing Telegram bot...")
        application = Application.builder().token(bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        
        # Initialize application
        await application.initialize()
        await application.start()
        
        # Start polling for updates (for /start command)
        await application.updater.start_polling()
        
        logger.info("Telegram bot started and listening for commands")
        
        # Start scheduler for daily messages
        logger.info("Starting scheduler...")
        scheduler = DailyScheduler(send_daily_countdown)
        scheduler.start()
        
        logger.info("Bot is fully operational!")
        logger.info("- Keep-alive server running on port " + str(port))
        logger.info("- Telegram bot listening for /start commands")
        logger.info("- Daily messages scheduled for 00:01 AM")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Keep the main thread alive
        while True:
            await asyncio.sleep(1)
            
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())
