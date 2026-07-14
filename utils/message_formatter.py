"""
Message Formatter Utilities - Centralized message formatting logic
"""

import logging
from core.master_data import format_rupiah

logger = logging.getLogger("bot_logger")


def format_money_field(label: str, value: float, is_bold: bool = True) -> str:
    """
    Format field uang dengan emoji dan formatting konsisten.
    
    Args:
        label: Label untuk field (misal: "💸 Uang Masuk:")
        value: Nilai uang yang akan diformat
        is_bold: Jika True, gunakan bold tag, jika False gunakan code tag
        
    Returns:
        String yang diformat
    """
    try:
        formatted_value = format_rupiah(value)
        if is_bold:
            return f"{label} <b>{formatted_value}</b>"
        return f"{label} <code>{formatted_value}</code>"
    except Exception as e:
        logger.debug(f"Failed to format money field: {e}")
        return f"{label} {value}"


def format_status_line(status: str, nominal: float = 0, tagihan: float = 0) -> str:
    """
    Format baris status pembayaran.
    
    Args:
        status: Status pembayaran (LUNAS, DICICIL, HUTANG)
        nominal: Nominal yang sudah dibayar
        tagihan: Sisa tagihan
        
    Returns:
        String status yang diformat
    """
    lines = []
    
    try:
        if status == "DICICIL":
            lines.append(f"💸 Uang Masuk: <code>{format_rupiah(nominal)}</code>")
            lines.append(f"⚠️ Sisa Tagihan: <code>{format_rupiah(tagihan)}</code>")
        elif status == "HUTANG":
            lines.append(f"💸 Uang Masuk: <code>{format_rupiah(0)}</code>")
            lines.append(f"⚠️ Sisa Tagihan: <code>{format_rupiah(tagihan)}</code>")
        else:  # LUNAS
            lines.append(f"💸 Uang Masuk: <code>{format_rupiah(nominal)}</code>")
    except Exception as e:
        logger.debug(f"Failed to format status line: {e}")
        lines.append(f"Status: {status}")
    
    return "\n".join(lines)


def format_correction_line(old_value: float, new_value: float) -> str:
    """
    Format baris koreksi harga.
    
    Args:
        old_value: Nilai lama
        new_value: Nilai baru
        
    Returns:
        String koreksi yang diformat
    """
    try:
        return f"2️⃣ <b>KOREKSI</b> ➡️ Jadi <code>{format_rupiah(new_value)}</code> (Menimpa)\n"
    except Exception as e:
        logger.debug(f"Failed to format correction line: {e}")
        return f"2️⃣ KOREKSI ➡️ Jadi {new_value} (Menimpa)\n"
