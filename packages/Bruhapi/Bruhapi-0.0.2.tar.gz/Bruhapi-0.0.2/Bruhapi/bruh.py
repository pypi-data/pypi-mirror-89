import aiohttp
import random
import string
from .exceptions import *


def random_char(y):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(y))
idk = random_char(20) 
class Bruh(object):
  
    
    async def sponge(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bruhapi.xyz/sponge/{idk}') as r:
                data = await r.json()
                sponges = data['res']
                error = errors.get(r.status)
                if error:
                    raise error
        return sponges
    
    async def chatbot(self, *, text):
        async with aiohttp.ClientSession() as session:
            if text is None:
                raise NoargsError('"Text" is an required arg')
            async with session.get(f'https://bruhapi.xyz/cb/{text}') as r:
                data = await r.json()
                chats = data['res']
                error = errors.get(r.status)
                if error:
                    raise error
        return chats

    async def joke(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bruhapi.xyz/joke') as r:
                data = await r.json()
                jokes = data['res']
                error = errors.get(r.status)
                if error:
                    raise error
        return jokes

    async def word(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bruhapi.xyz/word') as r:
                data = await r.json()
                word = data['res']
                error = errors.get(r.status)
                if error:
                    raise error
        return word

    async def topic(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bruhapi.xyz/topic') as r:
                data = await r.json()
                topic = data['res']
                error = errors.get(r.status)
                if error:
                    raise error
        return topic

    async def fact(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bruhapi.xyz/fact') as r:
                data = await r.json()
                fact = data['res']
                error = errors.get(r.status)
                if error:
                    raise error
        return fact

        

        
       
