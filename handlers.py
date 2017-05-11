#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '


import re, time, json, logging, hashlib, base64, asyncio
from functools import reduce
from aiohttp import web

from coroweb import get, post
from apis import APIValueError, APIResourceNotFoundError

from models import Anime, AnimeItem
from config import configs


def getLatestAddPlay(animeA,animeB):
    if animeA.LatestAddPlay == None:
        animeA.LatestAddPlay=0
    if animeB.LatestAddPlay == None:
        animeB.LatestAddPlay=0
    animeA.LatestAddPlay = animeA.LatestAddPlay + animeB.LatestAddPlay
    return animeA
    

@get('/')
async def index(request):
    animeObj = await Anime.ListAllAnime(orderBy=" order by LatestAddPlay desc")
    countFirst = animeObj[0].LatestAddPlay
    totalCount = reduce(getLatestAddPlay,animeObj)
    countSum = totalCount.LatestAddPlay
    animeObj[0].LatestAddPlay = countFirst
    
    i=0
    animeData=[]
    while i<10:
        animeData.append((animeObj[i].LatestAddPlay/countSum,animeObj[i].title))
        i=i+1
        
    return {
        '__template__': 'index.html',
        'animeObj':animeObj,
        'animeData': animeData
    }
    
@get('/animeItems')
async def animeItems(*,seasonId):
    animeItemsObj = await AnimeItem.ListAnimeItems(seasonId)
    wh = " seasonId='%s'" % seasonId
    animeObj = await Anime.findAll(where = wh)
    return {
        '__template__': 'AnimeItem.html',
        'animeItemObj':animeItemsObj,
        'animeObj':animeObj[0]
    }
    
    
@get('/api/anime')
async def api_get_animes():
    users = await Anime.findAll(where='')
    for u in users:
        u.passwd = '******'
    return dict(users=users)


