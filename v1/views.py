import json
from flask import request, jsonify, abort
import secrets

from ChatGPT.rumormonger import Rumormonger
from Database.Account import Account
from Database.Rumors import Rumors
from config import config


async def validate_key(key):
    if key is None or Rumors.is_key_banned(key):
        abort(403)


async def parse_parameters(messages, temperature):
    messages_obj = json.loads(messages) if messages else None
    return messages_obj, temperature


async def rumor():
    key = request.args.get('key', default=None, type=str)
    data = Rumors.get_data_by_key(key)
    if not data:
        abort(403)
    acc = Account(data['key'], data['tokens'], data['lastip'], data['banned'])
    await validate_key(acc.key)

    if request.remote_addr != acc.ip:
        acc.ip = request.remote_addr

    messages = request.args.get('messages', default=None, type=str)
    temperature = request.args.get('temperature', default=None, type=float)

    messages_obj, temperature = await parse_parameters(messages, temperature)

    if messages_obj is None or temperature is None:
        abort(400)

    resp = await Rumormonger.completion(messages_obj, temperature)

    message = resp[0]
    usage = resp[1]

    acc.tokens += usage

    return jsonify(role=message.role, message=message.content)


async def CreateAccount():
    keyword = request.args.get('secret', default=None, type=str)
    if keyword == config['RUMOR']['secret'] or config['API']['openregistration'] is True:
        secret = secrets.token_hex(12).upper()
        Rumors.insert_data(secret, 0, request.remote_addr, False)
        account = Rumors.get_data_by_key(secret)
        return jsonify(token=account.key, tokens=account.tokens, ip="None", banned=account.banned)
    abort(403)

