import logging

def setup_logging(log_file='app.log'):
    """
    Sets up logging configuration.
    """
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())  # Also log to console

def log_error(message):
    """
    Logs an error message.
    """
    logging.error(message)

def log_info(message):
    """
    Logs an informational message.
    """
    logging.info(message)
