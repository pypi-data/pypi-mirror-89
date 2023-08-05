import json
import aiohttp
import asyncio
from .PostUrl import mainurl
"""
이 소스는 SaidBySolo님의 KoreanBots비공식 sdk레포의 일부를 사용해 제작되었습니다.
URL: https://github.com/SaidBySolo/DBKR-API-Python
"""

class UBPYvote:
    def __init__(self,ctx, token, bot_id):
        """
        token은 UniqueBots 토큰값을,
        bot_id는 구동할 봇의 아이디(18자리)
        """
        self.ctx = ctx
        self.token = token
        self.id = bot_id

    async def vote(self, ctx,token, id):
        vot = await self.Check_vote(ctx, token,id)
        if vot == 200:
            return True
        elif vot == 400:
            return False
        elif vot == 404:
            return 0




    @staticmethod
    async def Check_vote(ctx, token, ID):
        URL = mainurl
        headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        data = {"query": 'query{bot(id:' f'"{ID}"''){''heartClicked(user:' f'"{ctx.author.id}"'')}}'}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(URL, headers=headers, json=data) as r:
                response = await r.read()
                sid = response.decode('utf-8')
                answer = json.loads(sid)
                try:
                    if answer["data"]["bot"]["heartClicked"] == True:
                        return 200
                    elif answer["data"]["bot"]["heartClicked"] == False:
                        return 400
                    else:
                        return 400
                except KeyError:
                    return 404
    
