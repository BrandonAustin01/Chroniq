import sys

def supports_unicode():
    """
    Check if the terminal supports Unicode emojis.

    This function attempts to encode a known emoji using the current terminal's
    encoding (usually cp1252 on Windows). If it fails, we assume the terminal
    can't render emojis safely.
    """
    try:
        '✅'.encode(sys.stdout.encoding or 'utf-8')
        return True
    except Exception:
        return False

# Determine at runtime if emojis are supported
USE_EMOJIS = supports_unicode()

def emoji(text, fallback=""):
    """
    Safely use emojis if the terminal supports them.

    Args:
        text (str): The emoji character (e.g. '✅')
        fallback (str): A plain text fallback (e.g. '[ok]')

    Returns:
        str: The emoji if supported, otherwise the fallback
    """
    return text if USE_EMOJIS else fallback
