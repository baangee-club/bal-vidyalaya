import logging
import logging.config
from app import create_app
from app.config import get_settings

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger("app")
logger.debug("created settings")

setting = get_settings()
print(f"setting log level to {setting.log_level.upper()}")
logger.setLevel(setting.log_level.upper())

logger.info("info")
logger.debug("debug")
logger.error("error")

logger.debug("creating app")
app = create_app(setting)
logger.debug("app created")
