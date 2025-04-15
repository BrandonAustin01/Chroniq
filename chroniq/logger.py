import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# === Default log directory and file paths ===
DEFAULT_LOG_DIR = Path("data/logs")
SYSTEM_LOG_FILE = DEFAULT_LOG_DIR / "chroniq.log"
ACTIVITY_LOG_FILE = DEFAULT_LOG_DIR / "activity.log"

def setup_logger(name: str, file_path: Path, level=logging.INFO) -> logging.Logger:
    """
    Set up and return a rotating logger.

    Logging rotation size and backup count are loaded from config
    using lazy import to avoid circular dependency.
    """

    # 🧠 Dynamically load config only inside this function (not at the top)
    try:
        # Lazy import to avoid circular import at module level
        from chroniq.config import load_config
        _config = load_config()
        _log_config = _config.get("logging", {})
        rotate_size = _log_config.get("rotate_size", 1_000_000)
        rotate_backups = _log_config.get("rotate_backups", 5)
    except Exception:
        # Fallback if config can't be read (bootstrapping or error)
        rotate_size = 1_000_000
        rotate_backups = 5

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    # Ensure the log directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=file_path,
        mode="a",
        maxBytes=rotate_size,
        backupCount=rotate_backups,
        encoding="utf-8",
        delay=False
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))

    # Console handler (shows warnings and errors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# ✅ Loggers are created after setup_logger is fully defined
system_log = setup_logger("chroniq.system", SYSTEM_LOG_FILE)
activity_log = setup_logger("chroniq.activity", ACTIVITY_LOG_FILE)
