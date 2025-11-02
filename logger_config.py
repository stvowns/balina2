#!/usr/bin/env python3
"""
Centralized logging configuration for the crypto wallet tracker
"""

import logging
import sys
from datetime import datetime
from typing import Optional

# ANSI color codes for console output
class LogColors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""

    COLORS = {
        'DEBUG': LogColors.CYAN,
        'INFO': LogColors.GREEN,
        'WARNING': LogColors.YELLOW,
        'ERROR': LogColors.RED,
        'CRITICAL': LogColors.RED + LogColors.BOLD,
    }

    def format(self, record):
        # Store original levelname
        original_levelname = record.levelname

        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{LogColors.RESET}"

        # Format the message
        formatted = super().format(record)

        # Restore original levelname for other handlers
        record.levelname = original_levelname

        return formatted

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> None:
    """Setup logging configuration for the application"""

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatters
    console_formatter = ColoredFormatter(
        fmt='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )

    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

# Convenience functions for different log levels
def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name or __name__)

# Quick setup function
def init_logger(level: str = "INFO", log_file: str = "wallet_tracker.log"):
    """Initialize logging with default settings"""
    setup_logging(
        level=level,
        log_file=log_file,
        console_output=True
    )

# Emoji shortcuts for common operations
def log_emoji(message: str, emoji: str = "📊", level: str = "info"):
    """Log message with emoji prefix"""
    logger = get_logger()
    log_func = getattr(logger, level.lower())
    log_func(f"{emoji} {message}")

# Specialized logging functions
def log_wallet_action(action: str, wallet_name: str, details: str = ""):
    """Log wallet-related actions"""
    logger = get_logger()
    message = f"🔍 {wallet_name}: {action}"
    if details:
        message += f" | {details}"
    logger.info(message)

def log_notification(channel: str, status: str, details: str = ""):
    """Log notification actions"""
    logger = get_logger()
    message = f"📱 {channel} notification {status}"
    if details:
        message += f" | {details}"
    logger.info(message)

def log_api_call(api_name: str, status: str, response_time: float = None):
    """Log API calls"""
    logger = get_logger()
    message = f"🌐 {api_name} API {status}"
    if response_time:
        message += f" ({response_time:.2f}s)"
    logger.info(message)

def log_error(operation: str, error: Exception, context: str = ""):
    """Log errors with context"""
    logger = get_logger()
    message = f"❌ Error in {operation}: {str(error)}"
    if context:
        message += f" | Context: {context}"
    logger.error(message)

def log_startup(wallet_count: int, interval: int):
    """Log application startup"""
    logger = get_logger()
    logger.info(f"🚀 Starting multi-wallet tracker for {wallet_count} wallet(s)")
    logger.info(f"⏰ Check interval: {interval} seconds")

def log_wallet_summary(wallet_name: str, address: str, status: str):
    """Log wallet summary information"""
    logger = get_logger()
    status_emoji = "✅" if status == "active" else "❌"
    logger.info(f"  {status_emoji} {wallet_name} ({address[:10]}...{address[-6:]})")