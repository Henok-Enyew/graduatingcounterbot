"""Configuration module for Telegram Graduation Countdown Bot.

This module provides centralized environment variable loading and validation.
"""

import os


class Config:
    """Configuration class for managing environment variables."""

    @staticmethod
    def get_bot_token() -> str:
        """Returns TELEGRAM_BOT_TOKEN from environment.
        
        Returns:
            str: The Telegram bot token.
            
        Raises:
            ValueError: If TELEGRAM_BOT_TOKEN is not set or is empty.
        """
        token = os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        return token

    @staticmethod
    def get_group_ids() -> list[str]:
        """Returns parsed list of group IDs from GROUP_IDS environment variable.
        
        Parses comma-separated GROUP_IDS into a list with whitespace trimmed.
        
        Returns:
            list[str]: List of group ID strings.
            
        Raises:
            ValueError: If GROUP_IDS is not set, is empty, or contains no valid IDs.
        """
        group_ids_str = os.environ.get('GROUP_IDS', '').strip()
        if not group_ids_str:
            raise ValueError("GROUP_IDS environment variable is required")
        
        # Parse comma-separated values and trim whitespace from each ID
        group_ids = [gid.strip() for gid in group_ids_str.split(',')]
        
        # Filter out empty strings after trimming
        group_ids = [gid for gid in group_ids if gid]
        
        if not group_ids:
            raise ValueError("GROUP_IDS must contain at least one group ID")
        
        return group_ids

    @staticmethod
    def get_port() -> int:
        """Returns PORT from environment with default 8080.
        
        Returns:
            int: The port number for the keep-alive server.
            
        Raises:
            ValueError: If PORT is set but cannot be parsed as a valid integer.
        """
        port_str = os.environ.get('PORT', '8080').strip()
        try:
            port = int(port_str)
            if port < 1 or port > 65535:
                raise ValueError(f"PORT must be between 1 and 65535, got {port}")
            return port
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError(f"PORT must be a valid integer, got '{port_str}'")
            raise
