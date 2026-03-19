# utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Rotating file — 5MB max, keeps 3 backups
        file_handler = RotatingFileHandler(
            "logs/newsfile.log", maxBytes=5_000_000, backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger