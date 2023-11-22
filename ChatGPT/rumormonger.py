import openai
from config import config


class Rumormonger:

    __key = None
    __base_url = None
    __model = None
    __tokenlimit = None
    __Chat = None

    @staticmethod
    def init():
        Rumormonger.__key = config['OpenAI']['api_key']
        Rumormonger.__base_url = config['OpenAI']['api_endpoint']
        Rumormonger.__model = config['OpenAI']['model']
        Rumormonger.__tokenlimit = config['OpenAI']['tokenlimit']
        Rumormonger.__Chat = openai.AsyncClient(api_key=Rumormonger.__key,
                                                base_url=Rumormonger.__base_url)

    @staticmethod
    async def completion(message, temperature=None):
        args = {'model': Rumormonger.__model, 'messages': message}
        if temperature:
            args['temperature'] = temperature
        reply = await Rumormonger.__Chat.chat.completions.create(**args)
        return [reply.choices[0].message, reply.usage.completion_tokens]
