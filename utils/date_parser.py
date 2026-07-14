"""
Date Parser Utilities - Centralized date parsing logic
"""

from datetime import datetime, date
from typing import Optional
import logging

logger = logging.getLogger("bot_logger")


def parse_date_flexible(date_str: str, formats: tuple = ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y")) -> Optional[date]:
    """
    Parse tanggal dengan multiple format fallback.
    
    Args:
        date_str: String tanggal yang akan diparse
        formats: Tuple format tanggal yang akan dicoba secara berurutan
        
    Returns:
        date object jika berhasil, None jika gagal
    """
    if not date_str:
        return None
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt).date()
        except (ValueError, TypeError):
            continue
    
    logger.debug(f"Failed to parse date: {date_str} with formats: {formats}")
    return None


def format_date_display(date_obj: date, format_str: str = "%d %B %Y") -> str:
    """
    Format date untuk display.
    
    Args:
        date_obj: Date object yang akan diformat
        format_str: Format string untuk strftime
        
    Returns:
        String tanggal yang diformat
    """
    try:
        return date_obj.strftime(format_str)
    except Exception as e:
        logger.debug(f"Failed to format date {date_obj}: {e}")
        return str(date_obj)
