from app.config import settings
from app.utils.logging import setup_logging
from app.ui.interface import launch_ui

if __name__ == "__main__":
    setup_logging(log_dir=settings.LOG_DIR, log_level=settings.LOG_LEVEL)
    launch_ui(share=settings.SHARE_LINK)
