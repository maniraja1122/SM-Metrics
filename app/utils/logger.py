import logging


# Setting Debug Logger for FastAPI
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)