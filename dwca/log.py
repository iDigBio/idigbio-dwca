import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
formatter = logging.Formatter(FORMAT)
logger = logging.getLogger()