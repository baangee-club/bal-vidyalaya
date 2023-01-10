import logging
import logging.config
from app import create_app
from app.config import get_settings

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)
logger.info("info")
logger.debug("debug")
logger.error("error")

setting = get_settings()
logger.debug("created settings")

logger.debug("creating app")
app = create_app(setting)
logger.debug("app created")
