import json
import aiohttp
import asyncio
from .PostUrl import mainurl


class UBPYsearch:
    def __init__(self, token):
        """
        token은 UniqueBots 토큰값
        """
        self.token = token

    async def List(self, page=1):
        token = self.token
        url = mainurl
        headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        data = {"query": "query{bots(page:"f'{int(page)}'",sort: hearts){result{tag, heartCount, discordVerified,guilds,id,status,brief,avatar,prefix,invite,locked,library,description}}}"}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, headers=headers, json=data) as r:
                response = await r.read()
                sid = response.decode('utf-8')
                answer = json.loads(sid)
                if answer["data"]["bots"]["result"] == []:
                    return False
                else:
                    try:
                        res = answer["data"]["bots"]["result"]
                        return res
                    except KeyError:
                        return False


    async def search(self, ID):
        token = self.token
        url = mainurl
        headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        data = {
            "query": "query{bot(id: "f'"{ID}"'"){tag, heartCount, discordVerified,guilds,id,status,brief,avatar,prefix,invite,locked,library,description}}"}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, headers=headers, json=data) as r:
                response = await r.read()
                sid = response.decode('utf-8')
                answer = json.loads(sid)
                if answer["data"]["bot"] == None:
                    return False
                else:
                    try:
                        res = answer["data"]["bot"]
                        return res
                    except KeyError:
                        return False

    async def searchuser(self, ID,page=1):
        token = self.token
        url = mainurl
        headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        data = {
            "query": "query{user(id: "f'"{ID}"'"){bots(page:" f'{int(page)}'"){result{tag, heartCount, discordVerified,guilds,id,status,brief,avatar,prefix,invite,locked,library,description}}}"}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, headers=headers, json=data) as r:
                response = await r.read()
                sid = response.decode('utf-8')
                answer = json.loads(sid)
                try:
                    if answer["data"]["user"]["bots"]["result"] == []:
                        return False
                    else:
                        try:
                            res = answer["data"]["user"]["bots"]["result"]
                            return res
                        except KeyError:
                            return False
                except KeyError:
                    return False