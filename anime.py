# -*- coding:utf-8 -*-
import urllib.request
import sys
import re, time, json, logging, hashlib, base64, asyncio
from aiohttp import web

from models import ArchiveStat, next_id, Anime, AnimeItem
import orm


regAnimeItems = r'<a\s+?href="(//[\d\w]+\.bilibili\.com/anime/[\d\w]+?)"\s+?data-type="anime"\s+?target="_blank"\s+?title=".+?">'
regAnimeId = r'anime/([\d\w]+)'
regAnimeJson = r'({.+})'
regInt = r'^\d+$'

guochuangUrl = 'http://bangumi.bilibili.com/guochuang/timeline'
animeUrl ='http://bangumi.bilibili.com/anime/timeline'
#新番时间表
#http://bangumi.bilibili.com/guochuang/timeline
#番剧信息  http://bangumi.bilibili.com/jsonp/seasoninfo/5849.ver?callback=seasonListCallback&jsonp=jsonp&_=1492873029892
#节目信息
#http://api.bilibili.com/archive_stat/stat?aid=9044523&type=jsonp
#{"code":0,"data":{"view":746579,"danmaku":13741,"reply":4503,"favorite":649,"coin":14483,"share":732,"now_rank":0,"his_rank":0,"no_reprint":0,"copyright":1},"message":""}
#http://www.bilibili.com/video/av9499794/

async def getGuochuang():
    print("getGuochuang")
    await timeline(guochuangUrl)

async def getAnime():
    print("getAnime")
    await timeline(animeUrl)

async def timeline(timelineUrl):
    html = getHtml(timelineUrl)
    html = html.decode('utf-8')
    animeList = getAnimeList(html)
    for anime in set(animeList):
        url = getAnimeUrl(anime)
        print(url)
        await getAnimeInfo(url)

def getHtml(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read()    
    return html
    
def getAnimeList(html):
    print('getAnimeList')
    reg = regAnimeItems
    animeUrl = re.compile(reg)
    animeList = re.findall(animeUrl,html)
    return animeList    
    
def getAnimeUrl(getAnime):
    print('getAnimeUrl')
    reg = regAnimeId
    animeUrl = re.compile(reg)
    animeList = re.findall(animeUrl,getAnime)
    return 'http://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver?callback=seasonListCallback&jsonp=jsonp' % animeList[0]
    
def getAnimeItemUrl(avId):
    return 'http://api.bilibili.com/archive_stat/stat?aid=%s&type=jsonp' % avId
    
async def getAnimeInfo(url):
    print('getAnimeInfo')
    html = getHtml(url)
    html = html.decode('utf-8')
    reAnimeJson = re.compile(regAnimeJson)
    animeStr = re.findall(reAnimeJson,html)
    animeJson = json.loads(animeStr[0])
    
    if(animeJson['message'] == 'success'):
        uid = next_id()
        result = animeJson['result']
        animeInfo = Anime(id=uid, area=result['area'], bangumiId=result['bangumi_id'],title=result['title'],coins=result['coins'],cover=result['cover'],danmakuCount=result['danmaku_count'],evaluate=result['evaluate'],favorites=result['favorites'],playCount=result['play_count'],seasonId=result['season_id'],shareUrl=result['share_url'],weekday=result['weekday'])
        animeInfo.pubTime=time.mktime(time.strptime(result['pub_time'],"%Y-%m-%d %H:%M:%S"))
        animeInfo.seasonTitle = result['season_title']
        tags=""
        for tag in result['tags']:
            tags = str(tags + ',' + tag['tag_name'])
        animeInfo.tags = tags
        if 'payment' in result:
            animeInfo.price = result['payment']['price']
        episodes = result['episodes']
        for episode in episodes:
            await getAnimeItem(episode,animeInfo.seasonId,animeInfo.seasonTitle)
        
        await animeInfo.save()

    
async def getAnimeItem(episode,seasonId,seasonTitle):
    print('getAnimeItem')
    uid = next_id()
    animeItem = AnimeItem(id=uid,seasonId=seasonId,seasonTitle=seasonTitle,avId=episode['av_id'],cover=episode['cover'],episodeId=episode['episode_id'],title=episode['index_title'],mid=episode['mid'],webplayUrl=episode['webplay_url'])
    animeItem.pubTime=time.mktime(time.strptime(episode['update_time'],"%Y-%m-%d %H:%M:%S.%f"))        
    pattern = re.compile(regInt)
    match = pattern.match(episode['index'])
    if match:
        animeItem.index = episode['index']
    
    url = getAnimeItemUrl(episode['av_id'])
    html = getHtml(url)
    html = html.decode('utf-8')
    animeItemJson = json.loads(html)['data']
        
    animeItem.coins = animeItemJson['coin']
    animeItem.playCount = animeItemJson['view']
    animeItem.danmakuCount = animeItemJson['danmaku']
    animeItem.replyCount = animeItemJson['reply']
    animeItem.favorites = animeItemJson['favorite']
    animeItem.shareCount = animeItemJson['share']
    
    await animeItem.save() 


async def SetLatestAdditions():
    animeObj = await Anime.ListAllAnime()
    animeLastestObj = await Anime.ListYesterdayAnime()
    animeThreedayObj = await Anime.ListThreedayAnime()
    animeWeeddayObj = await Anime.ListWeeddayAnime()
    
    print('SetLatestAdditions')
    for item in animeObj:
        for l in animeLastestObj:
            if l.seasonId == item.seasonId:
                item.LatestAddPlay = item.playCount-l.playCount
                item.LatestAddCoins = item.coins-l.coins
                item.LatestAddDanmaku = item.danmakuCount-l.danmakuCount
        for t in animeThreedayObj:
            if t.seasonId == item.seasonId:
                item.LatestAddPlay3 = item.playCount-t.playCount
                item.LatestAddCoins3 = item.coins-t.coins
                item.LatestAddDanmaku3 = item.danmakuCount-t.danmakuCount

    for item in animeObj:
        item.LatestAddPlay7 = 0
        item.LatestAddCoins7 = 0
        item.LatestAddDanmaku7 = 0
        await item.update()
    
    