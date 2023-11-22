import logging


async def log_request(token, message, ip, file='rumor.log'):
    """
    Logs requests. What did you expect?
    :param token: Token passed
    :param message: Log message
    :param ip: IP causing the log
    :param file: Which file is logged to - defaults to rumor.log
    """
    logger = logging.getLogger('log_request')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        fh = logging.FileHandler(file)
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)

        logger.addHandler(fh)

    # Assume if token is passed - it's a valid request
    if token:
        short_token = token[:8]
        formatted_message = f"{ip}/{short_token}: {message}"
    else:
        formatted_message = f"{ip}: {message}"

    logger.info(formatted_message)
