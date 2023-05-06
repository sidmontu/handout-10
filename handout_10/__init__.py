#!/usr/bin/env python3
"""
Package __init__.py
"""
__version__ = "0.1.0"

from loguru import logger

# Configure logger
logger.remove()  # remove any existing defaults

# Set level colours
# logger.level("TRACE", color="<yellow>") # unused
# logger.level("ERROR", color="<WHITE><yellow>") # unused
logger.level("DEBUG", color="<LIGHT-CYAN><blue>")
logger.level("INFO", color="<green>")
logger.level("SUCCESS", color="<GREEN><black>")
logger.level("WARNING", color="<MAGENTA><white>")
logger.level("ERROR", color="<RED><white>")
logger.level("CRITICAL", color="<RED><yellow>")
