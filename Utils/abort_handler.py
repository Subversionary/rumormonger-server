from flask import abort
from Utils.log import log_request
import json


async def handle(code: int, message: str, ip: str, data: json):
    """
    Doesn't really handle, does really abort.
    Exists to log messages to a separate file before aborting
    :param code: error code
    :param message: message to log, this is user facing
    :param ip: IP of the person causing the error
    :param data: misc data, this is server facing
    """
    formatted_message = f"{code}: {message}"
    if data:
        formatted_message += f" Data: {data}"
    await log_request(None, formatted_message, ip, "rumor.err.log")
    abort(code, description=message)
