-- schema.sql

drop database if exists bilibili;

create database bilibili;

use bilibili;

grant select, insert, update, delete on bilibili.* to 'www-data'@'localhost' identified by 'www-data';

create table ArchiveStat (
    `id` varchar(50) not null,
    `view` bigint not null,
    `danmaku` bigint not null,
    `reply` bigint not null,
    `favorite` bigint not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table Anime (
    `id` varchar(50) not null,
    `area` varchar(50),
    `bangumiId` varchar(50),
    `title` varchar(100),
    `coins` bigint,
    `cover` varchar(200),
    `danmakuCount` bigint,
    `newestEpIndex` bigint,
    `evaluate` varchar(500),
    `favorites` bigint,
    `price` real,
    `playCount` bigint,
    `pubTime` real,
    `seasonId` varchar(50),
    `seasonTitle` varchar(100),
    `shareUrl` varchar(200),
    `tags` varchar(200),
    `weekday` bigint,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table AnimeItem (
    `id` varchar(50) not null,
    `seasonId` varchar(50),
    `seasonTitle` varchar(100),
    `avId` varchar(50),
    `cover` varchar(200),
    `episodeId` varchar(50),
    `Index` bigint,
    `title` varchar(100),
    `mid` varchar(100),
    `pubTime` real, 
    `webplayUrl` varchar(200),
    `coins` bigint,
    `playCount` bigint,
    `danmakuCount` bigint,
    `replyCount` bigint,
    `favorites` bigint, 
    `shareCount` bigint,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;


 alter table anime add column LatestAddPlay bigint;
 
 alter table anime add column LatestAddCoins bigint;
  
 alter table anime add column LatestAddDanmaku bigint;
 
 
 alter table anime add column LatestAddPlay3 bigint;
 
 alter table anime add column LatestAddCoins3 bigint;
  
 alter table anime add column LatestAddDanmaku3 bigint;
 
 
 alter table anime add column LatestAddPlay7 bigint;
 
 alter table anime add column LatestAddCoins7 bigint;
  
 alter table anime add column LatestAddDanmaku7 bigint;
