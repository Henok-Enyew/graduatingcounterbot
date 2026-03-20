"""Message Distributor Module

This module handles sending countdown messages to multiple Telegram groups
with fault isolation and comprehensive logging.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional

from telegram import Bot
from telegram.error import TelegramError


class MessageDistributor:
    """Distributes messages to multiple Telegram groups with error isolation.
    
    This class manages message delivery to multiple Telegram groups independently,
    ensuring that a failure in one group doesn't prevent delivery to others.
    All delivery attempts are logged with timestamps and status information.
    """
    
    def __init__(self, bot_token: str, group_ids: list[str]):
        """Initialize the MessageDistributor.
        
        Args:
            bot_token: Telegram bot authentication token
            group_ids: List of Telegram group chat IDs to send messages to
        """
        self.bot = Bot(token=bot_token)
        self.group_ids = group_ids
        self.logger = logging.getLogger(__name__)
    
    async def distribute_message(
        self, 
        message: str, 
        image_path: Optional[str] = None
    ) -> Dict[str, bool]:
        """Send message to all configured groups.
        
        Iterates through all group IDs and attempts to send the message to each.
        If image_path is provided, sends as photo with caption. Otherwise sends
        as text message. Failures in individual groups are logged but don't 
        prevent delivery to other groups.
        
        Args:
            message: The formatted message text to send (or caption if image provided)
            image_path: Optional path to image file to send with message as caption
            
        Returns:
            Dictionary mapping group_id to success status (True/False)
        """
        results = {}
        
        try:
            # Use asyncio.wait_for to enforce 60-second timeout
            results = await asyncio.wait_for(
                self._send_to_all_groups(message, image_path),
                timeout=60.0
            )
        except asyncio.TimeoutError:
            self.logger.error(
                "Message distribution timed out after 60 seconds",
                extra={"timestamp": datetime.now().isoformat()}
            )
            # Mark any groups that weren't processed as failed
            for group_id in self.group_ids:
                if group_id not in results:
                    results[group_id] = False
        
        return results
    
    async def _send_to_all_groups(
        self, 
        message: str, 
        image_path: Optional[str] = None
    ) -> Dict[str, bool]:
        """Internal method to send message to all groups.
        
        Args:
            message: The formatted message text to send (or caption)
            image_path: Optional path to image file
            
        Returns:
            Dictionary mapping group_id to success status
        """
        results = {}
        
        for group_id in self.group_ids:
            success = await self._send_to_group(group_id, message, image_path)
            results[group_id] = success
        
        return results
    
    async def _send_to_group(
        self, 
        group_id: str, 
        message: str, 
        image_path: Optional[str] = None
    ) -> bool:
        """Send message to a single group with error handling.
        
        Attempts to send as photo with caption if image_path is provided.
        Falls back to text-only message if image fails to load or send.
        
        Args:
            group_id: Telegram group chat ID
            message: The formatted message text (or caption if image provided)
            image_path: Optional path to image file
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        timestamp = datetime.now().isoformat()
        
        try:
            # Try to send as photo with caption if image path provided
            if image_path:
                try:
                    with open(image_path, 'rb') as photo_file:
                        await self.bot.send_photo(
                            chat_id=group_id,
                            photo=photo_file,
                            caption=message,
                            parse_mode="HTML"
                        )
                    
                    self.logger.info(
                        f"Successfully sent photo message to group {group_id}",
                        extra={
                            "group_id": group_id,
                            "timestamp": timestamp,
                            "status": "success",
                            "message_type": "photo"
                        }
                    )
                    return True
                    
                except (FileNotFoundError, IOError) as e:
                    # Image failed to load, fall back to text message
                    self.logger.warning(
                        f"Failed to load image {image_path}, falling back to text message: {str(e)}",
                        extra={
                            "group_id": group_id,
                            "image_path": image_path,
                            "error": str(e)
                        }
                    )
                    # Continue to send as text message below
            
            # Send as text message (either no image provided or image failed)
            await self.bot.send_message(
                chat_id=group_id,
                text=message,
                parse_mode="HTML"
            )
            
            self.logger.info(
                f"Successfully sent text message to group {group_id}",
                extra={
                    "group_id": group_id,
                    "timestamp": timestamp,
                    "status": "success",
                    "message_type": "text"
                }
            )
            return True
            
        except TelegramError as e:
            self.logger.error(
                f"Failed to send message to group {group_id}: {str(e)}",
                extra={
                    "group_id": group_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "timestamp": timestamp,
                    "status": "failed"
                }
            )
            return False
            
        except Exception as e:
            self.logger.error(
                f"Unexpected error sending to group {group_id}: {str(e)}",
                extra={
                    "group_id": group_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "timestamp": timestamp,
                    "status": "failed"
                }
            )
            return False
