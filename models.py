#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
http://api.bilibili.com/archive_stat/stat?aid=9958912&type=jsonp
'''

__author__ = 'fangwei.lee'

import time, uuid
import asyncio,aiomysql

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField, select

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)
    
    
class ArchiveStat(Model):
    __table__ = 'ArchiveStat'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')
    view = IntegerField()
    danmaku = IntegerField()
    reply = IntegerField()
    favorite = IntegerField()
    created_at = IntegerField()
    
class Anime(Model):
    __table__ = 'Anime'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')
    area = StringField(column_type='varchar(50)')
    bangumiId = StringField(column_type='varchar(50)')
    title = StringField(column_type='varchar(100)')
    coins = IntegerField()
    cover = StringField(column_type='varchar(200)')
    danmakuCount = IntegerField()
    newestEpIndex = IntegerField()
    evaluate = StringField(column_type='varchar(500)')
    favorites = IntegerField()
    price = FloatField()
    playCount = IntegerField()
    pubTime = FloatField(default=time.time)
    seasonId = StringField(column_type='varchar(50)')
    seasonTitle = StringField(column_type='varchar(100)')
    shareUrl = StringField(column_type='varchar(200)')
    tags = StringField(column_type='varchar(200)')
    weekday = IntegerField()
    created_at = FloatField(default=time.time)
    LatestAddPlay = IntegerField()
    LatestAddCoins = IntegerField()
    LatestAddDanmaku = IntegerField()
    LatestAddPlay3 = IntegerField()
    LatestAddCoins3 = IntegerField()
    LatestAddDanmaku3 = IntegerField()
    LatestAddPlay7 = IntegerField()
    LatestAddCoins7 = IntegerField()
    LatestAddDanmaku7 = IntegerField()
    
    
    @classmethod
    @asyncio.coroutine
    def ListAllAnime(cls,orderBy=None):
        sql = "select a.* from anime a inner join (select seasonId,max(created_at) 'maxgdtime' from anime group by seasonId) b on a.seasonId=b.seasonId and a.created_at=b.maxgdtime "
        if orderBy != None:
            sql= sql+orderBy
        rs = yield from select(sql,[])
        return [cls(**r) for r in rs]
        
        
    @classmethod
    @asyncio.coroutine
    def ListYesterdayAnime(cls):
        cur_time = time.time()
        today_time = cur_time-cur_time%86400
        yesterday_time = today_time-86400
        
        sql = "select a.* from anime a inner join (select seasonId,max(created_at) 'maxgdtime' from anime where created_at>%s and created_at<%s group by seasonId) b on a.seasonId=b.seasonId and a.created_at=b.maxgdtime order by playCount desc" % (yesterday_time,today_time)
        rs = yield from select(sql,[])
        return [cls(**r) for r in rs]
        
    @classmethod
    @asyncio.coroutine
    def ListThreedayAnime(cls):
        cur_time = time.time()
        today_time = cur_time-cur_time%86400-86400*2
        threeday_time = today_time-86400
        
        sql = "select a.* from anime a inner join (select seasonId,max(created_at) 'maxgdtime' from anime where created_at>%s and created_at<%s group by seasonId) b on a.seasonId=b.seasonId and a.created_at=b.maxgdtime order by playCount desc" % (threeday_time,today_time)
        rs = yield from select(sql,[])
        return [cls(**r) for r in rs]
        
    @classmethod
    @asyncio.coroutine
    def ListWeeddayAnime(cls):
        cur_time = time.time()
        today_time = cur_time-cur_time%86400-86400*6
        weedday_time = today_time-86400
        
        sql = "select a.* from anime a inner join (select seasonId,max(created_at) 'maxgdtime' from anime where created_at>%s and created_at<%s group by seasonId) b on a.seasonId=b.seasonId and a.created_at=b.maxgdtime order by playCount desc" % (weedday_time,today_time)
        rs = yield from select(sql,[])
        return [cls(**r) for r in rs]
    
    
class AnimeItem(Model):
    __table__ = 'AnimeItem'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')
    seasonId = StringField(column_type='varchar(50)')
    seasonTitle = StringField(column_type='varchar(100)')
    avId = StringField(column_type='varchar(50)')
    cover = StringField(column_type='varchar(200)')
    episodeId = StringField(column_type='varchar(50)')
    index = IntegerField()
    title = StringField(column_type='varchar(100)')    
    mid = StringField(column_type='varchar(200)')
    pubTime = FloatField(default=time.time)
    webplayUrl = StringField(column_type='varchar(200)')
    coins = IntegerField()
    playCount = IntegerField()    
    danmakuCount = IntegerField()
    replyCount = IntegerField()
    favorites = IntegerField()
    shareCount = IntegerField()
    created_at = FloatField(default=time.time)
    
    @classmethod
    @asyncio.coroutine
    def ListAnimeItems(cls,seasonId):
        sql = "select a.* from animeitem a inner join (select episodeId,max(created_at) 'maxgdtime' from animeitem where seasonid=%s group by episodeId ) b on a.episodeId=b.episodeId and a.created_at=b.maxgdtime order by pubTime" % seasonId
        rs = yield from select(sql,[])
        return [cls(**r) for r in rs]
    