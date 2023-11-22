import json
from flask import request, jsonify, abort
import secrets

from ChatGPT.rumormonger import Rumormonger
from Database.Account import Account
from Database.Rumors import Rumors
from config import config
from Utils.log import log_request
from Utils import abort_handler


async def validate_key(key):
    if key is None or Rumors.is_key_banned(key):
        abort(403)


async def parse_parameters(messages):
    messages_obj = None
    try:
        if messages:
            messages_obj = json.loads(messages) if messages else None
    except json.JSONDecodeError:
        abort(400, description="Passed invalid json")
    return messages_obj


async def rumor():
    addr = request.remote_addr
    key = request.args.get('key', default=None, type=str)
    data = Rumors.get_data_by_key(key)

    if not data:
        await abort_handler.handle(403, "Invalid key passed.", addr, None)

    acc = Account(data)
    await validate_key(acc.key)

    if addr != acc.ip:
        acc.ip = addr

    messages = request.args.get('messages', default=None, type=str)
    temperature = request.args.get('temperature', default=None, type=float)

    if temperature and not (0.0 < temperature <= 2.0):
        await abort_handler.handle(400, "Invalid temperature", addr, None)

    messages_obj = await parse_parameters(messages)

    # Where are you going
    if messages_obj is None:
        await abort_handler.handle(400, "Message given is empty", addr, messages_obj)

    await log_request(acc.key, f"Sent request with messageobj {messages_obj}", acc.ip)

    resp = await Rumormonger.completion(messages_obj, temperature)

    message = resp[0]
    usage = resp[1]

    await log_request(acc.key, f"Received response: {message}. Used tokens: {usage}", acc.ip)

    acc.tokens += usage

    return jsonify(role=message.role, message=message.content)


async def CreateAccount():
    keyword = request.args.get('secret', default=None, type=str)
    if keyword == config['RUMOR']['secret'] or config['API']['openregistration'] is True:
        secret = secrets.token_hex(16).upper()
        Rumors.insert_data(secret, 0, request.remote_addr, False)
        data = Rumors.get_data_by_key(secret)
        account = Account(data)
        return jsonify(token=account.key, tokens=account.tokens, ip="None", banned=account.banned)
    await abort_handler.handle(404, "", request.remote_addr, None)

