# -*- coding:utf-8 -*-

import orm
import asyncio
import anime

async def main(loop):
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='mysql123', database='bilibili')
    
    await anime.getAnime()
    await anime.getGuochuang()
    
    await anime.SetLatestAdditions()
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

    