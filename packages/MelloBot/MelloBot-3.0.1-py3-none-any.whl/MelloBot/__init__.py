# -*- coding: utf-8 -*-
 
"""
“Commons Clause” License Condition Copyright Pirxcy/Mello 2019-2020 / 2020-202
 
The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
 
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
 
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.
 
Software: MelloBot (https://pypi.org/user/Pirxcy/)
 
License: Apache 2.0
"""
 
__name__ = "MelloBot"
__author__ = "Pirxcy"
__version__ = "3.0.1"

import json
from colorama import Fore, Back, Style, init
import asyncio
import aiohttp
import time
import sys
import jaconv
import pycld2 as cld2
import requests
import os
import traceback
import fortnite_api
import fortnitepy
import FortniteAPIAsync
import traceback

from fortnitepy.ext import commands

intro = Fore.BLUE + f"""
███╗   ███╗███████╗██╗     ██╗      ██████╗ 
{Fore.RED + "████╗ ████║██╔════╝██║"}     ██║     ██╔═══██╗
{Fore.GREEN + "██╔████╔██║█████╗  ██║     ██║     ██║   ██║"}
██║╚██╔╝██║██╔══╝  ██║     ██║     ██║   ██║
{Fore.YELLOW + "██║ ╚═╝ ██║███████╗███████╗███████╗╚██████╔╝"}
╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ 
V3.0.1 {Fore.LIGHTMAGENTA_EX + "Coded"} {Fore.RED + "P"}{Fore.GREEN + "i"}{Fore.YELLOW + "r"}{Fore.BLUE + "x"}{Fore.MAGENTA + "c"}{Fore.RED + "y"} {Fore.LIGHTMAGENTA_EX + "for Mello!"} \nJoin The Discord and Contact @pirxcy or Helpers for Help!\nhttps://discord.gg/25fKfvrqwC Enjoy!
"""

with open("config.json", encoding='utf-8') as f:
    data = json.load(f)

with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        os.system('cls||clear')
        print(intro)
        print(Fore.YELLOW + '[ERROR]' + Fore.RED + "There was an error in one of the bot's files! (info.json)\n If you have problems trying to fix it, join the discord support server for help - https://discord.gg/25fKfvrqwC and Contact @Pirxcy!")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        print("Hope Your Bot Gets Fixed Soon!\nBye!")
        exit(1)

    emailjson = data['email']
    passwordjson = data['password']
    playlistjson = 'Playlist_dadbro_squads'
    statusjson = 'Made By Pirxcy and Mello For You!'
    cidjson = 'CID_963_Athena_Commando_F_Lexa'
    bidjson = ''
    eidjson = 'EID_AmazingForever_Q68W0'
    pidjson = ''
    acceptfriendjson = data['friendaccept']
    ownerid = info['ownerid']
    invowneronly = data['joinoninvite']
    platformjson = "XBL"
    apikey = ''


from flask import Flask, render_template, Response
from threading import Thread

app=Flask("")

@app.route("/")
def index():
    return render_template("index.html")


creatorid="130b164cfb344c50b9278a5a90eb2def"
email=emailjson
password=passwordjson
filename = 'device_auths.json'
description = 'My awesome fortnite bot!'

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

class MyBot(commands.Bot, fortnitepy.Client):
    BEN_BOT_BASE = 'https://fortnite-api.com/v2/cosmetics/br/search'
    FORTNITEAPI = 'https://fortnite-api.com/cosmetics/br/search'
    FORTNITEAPIALL = 'https://fortnite-api.com/cosmetics/br/search/all'
    def __init__(self):
        device_auth_details = get_device_auth_details().get(email, {})
        super().__init__(
            command_prefix='!',
            description=description,
            auth=fortnitepy.AdvancedAuth(
                email=email,
                password=password,
                prompt_authorization_code=True,
                delete_existing_device_auths=True,
                **device_auth_details
                ),
                status=statusjson,
                platform=fortnitepy.Platform(platformjson),
                avatar=fortnitepy.Avatar(
                  asset='CID_986_Athena_Commando_M_PlumRetro_4AJA2',
                  background_colors="[\"#B35EEF\",\"#4D1397\",\"#2E0A5D\"]"
        )
        )
        self.session_event = asyncio.Event(loop=self.loop)
        self.acceptfriend=0
        self.acceptinvite=1
        self.mimicemote=0
        self.mimicskin=0
        self.previousoutfit=None
        self.previousbackpack=None
        self.cid=cidjson
        self.bid=bidjson
        self.pid=pidjson
        self.eid=eidjson
        self.svariants=None
        self.bvariants=None
        self.pvariants=None
        self.prevoutfitvariant=None
        self.prevbackpackvariant=None
        self.prevmes=None
        self.owneronly=False
        self.partyenable=True
        if acceptfriendjson == "true":
            self.acceptfriend=1
        if invowneronly == "False":
            self.owneronly=False
        self.lang=0
        self.foundlist=0
        self.msg_search=True
        self.api=fortnite_api.FortniteAPI()
        self.fortnite_api=FortniteAPIAsync
        

    def get_device_auth_details(self):
        if os.path.isfile(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)
        return {}

    def store_device_auth_details(self, email, details):
        existing = self.get_device_auth_details()
        existing[email] = details

        with open(filename, 'w') as fp:
            json.dump(existing, fp)

    async def event_device_auth_generate(self, details, email):
        self.store_device_auth_details(email, details)
        
    print(intro)

    async def event_ready(self):
        os.system('cls||clear')
        print(intro)
        print('Bot Ready as {0.user.display_name} / {0.user.id}'.format(self))
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.session_event.set()
        owner = self.get_friend(ownerid)
        if owner is None:
          pass
        else:
          await owner.send("Launched")

    async def event_party_invite(self, invitation):
        if invitation.sender.id == ownerid:
            await invitation.accept()
            return
        print('invite from ' + invitation.sender.display_name + ' / ' + invitation.sender.id)
        if self.owneronly == False:
            if self.acceptinvite == 1:
                await invitation.accept()
                print('invite accepted')
            else:
                await invitation.decline()
                print('invite declined')

    async def fetch_cosmetic_id(self, name, LISTTYPE):
        idint = 0
        async with aiohttp.ClientSession() as session:
            while True:
                async with self.session.get(self.BEN_BOT_BASE, params={'name': name}) as r:
                    print(r)
                    try:
                        data = await r.json()
                    except:
                        return None
                if list_type == data['backendType']:
                    jsondata = data[idint]['id']
                    name = data[idint]['name']
                    desc = data[idint]['description']
                    rare = data[idint]['rarity']
                    return jsondata, name, desc, rare
                else:
                    idint += 1

    async def fetch_cosmetic_id2(self, name, LISTTYPE):
        idint = 0
        async with aiohttp.ClientSession() as session:
            while True:
                async with self.session.get(self.BEN_BOT_BASE, params={'id': name}) as r:
                    print(r)
                    try:
                        data = await r.json()
                    except:
                        return None
                if list_type == data['backendType']:
                    jsondata = data[idint]['id']
                    name = data[idint]['name']
                    desc = data[idint]['description']
                    rare = data[idint]['rarity']
                    return jsondata, name, desc, rare
                else:
                    idint += 1

    async def fetch_allcosmetic_id(self, name, LISTTYPE):
        async with aiohttp.ClientSession() as session:
            async with self.session.get(self.BEN_BOT_BASE, params={'id': name}) as r:
                print(r)
                try:
                    data = await r.json()
                except:
                    pass
                return data
                
    async def fetch_item_namejp(self, name, Type):
        async with aiohttp.ClientSession() as session:
            async with self.session.get(self.FORTNITEAPI, params={'name': name, 'type': Type}, headers={'x-api-key': apikey}) as r:
                print(r)
                try:
                    data = await r.json()
                    itemid = data['data']['id']
                    name = data['data']['name']
                    desc = data['data']['description']
                    rare = data['data']['rarity']
                    return itemid, name, desc, rare
                except:
                    return None

    async def fetch_set_item(self, setname):
        outfitint = 0
        backpackint = 0
        pickint = 0
        emoteint = 0
        async with aiohttp.ClientSession() as session:
            async with self.session.get(self.FORTNITEAPIALL, params={'set': setname}, headers={'x-api-key': apikey}) as r:
                print(r)
                data = await r.json()
                while True:
                    try:
                        if data['data'][outfitint]['type'] == "outfit":
                            outfit = data['data'][outfitint]['id']
                            break
                        outfitint += 1
                    except:
                        outfit = None
                        break
                while True:
                    try:
                        if data['data'][backpackint]['type'] == "backpack":
                            backpack = data['data'][backpackint]['id']
                            break
                        backpackint += 1
                    except:
                        backpack = None
                        break
                while True:
                    try:
                        if data['data'][pickint]['type'] == "pickaxe":
                            pickaxe = data['data'][pickint]['id']
                            break
                        pickint += 1
                    except:
                        pickaxe = None
                        break
                while True:
                    try:
                        if data['data'][emoteint]['type'] == "emote":
                            emote = data['data'][emoteint]['id']
                            break
                        emoteint += 1
                    except:
                        emote = None
                        break
                return outfit, backpack, pickaxe, emote

    async def get_current_item_shop_ids(self):
        store = await self.fetch_item_shop()
        cids = []
        bids = []
        eids = []
        pids = []
        for item in store.featured_items + store.daily_items:
            for grant in item.grants:
                if grant['type'] == 'AthenaCharacter':
                    cids.append(grant['asset'])
            for grant in item.grants:
                if grant['type'] == 'AthenaDance':
                    eids.append(grant['asset'])
            for grant in item.grants:
                if grant['type'] == 'AthenaBackpack':
                    bids.append(grant['asset'])
            for grant in item.grants:
                if grant['type'] == 'AthenaPickaxe':
                    pids.append(grant['asset'])

        return cids,bids,eids,pids

    async def event_friend_add(self, friend):
        print('フレンド追加: {0.display_name} / {0.id}'.format(friend))

    async def event_friend_remove(self, friend):
        print('フレンド削除: {0.display_name} / {0.id}'.format(friend))

    async def event_party_member_promote(self, old_leader, new_leader): 
        print('譲渡 : {0.display_name} / {0.id} => {1.display_name} / {1.id}'.format(old_leader, new_leader))

    async def event_party_member_kick(self, member):
        print('キック : {0.display_name} / {0.id}'.format(member))
        if member.id == ownerid:
            print('所有者がキックされたため、離脱します')
            await self.party.me.leave()

    async def event_party_member_join(self, member):
        await self.party.me.set_emote(
                asset=self.eid
            )
        await self.party.me.set_battlepass_info(
                has_purchased='true',
                level=999999999,
                self_boost_xp=999999999,
                friend_boost_xp=999999999
            )
        await self.party.me.set_banner(
                icon='BRS8CumulativeLS4',
                color='black',
                season_level=9999
            )
        

    async def event_party_member_leave(self, member):
        print('Bot Ready as {0.display_name}')

    async def event_party_member_update(self, member):
        if self.mimicskin == 1:
            if not self.user.id == member.id:
                try:
                    if not self.previousoutfit == member.outfit or not self.prevoutfitvariant == member.outfit_variants:
                        await self.party.me.set_outfit(asset=member.outfit,variants=member.outfit_variants)
                        self.svariants=member.outfit_variants
                    if not self.previousbackpack == member.backpack or not self.prevbackpackvariant == member.backpack_variants:
                        if not member.backpack == None:
                            await self.party.me.set_backpack(asset=member.backpack,variants=member.backpack_variants)
                            self.bvariants=member.backpack_variants
                        else:
                            await self.party.me.set_backpack(asset="None")
                except TypeError:
                    pass
        if self.mimicemote == 1:
            if not self.user.id == member.id:
                try:
                    if not member.emote == None: 
                        await self.party.me.clear_emote()
                        await self.party.me.set_emote(asset=member.emote)
                except TypeError:
                    pass
        if not self.user.id == member.id and not self.previousoutfit == member.outfit:
            print(member.outfit)
        if not self.user.id == member.id and not self.previousbackpack == member.backpack and not member.backpack is None:
            print(member.backpack)
        if not self.user.id == member.id and not member.emote is None:
            print(member.emote)
        self.previousoutfit=member.outfit
        self.previousbackpack=member.backpack
        self.prevoutfitvariant=member.outfit_variants
        self.prevbackpackvariant=member.backpack_variants

    async def event_friend_request(self, request):
        if self.acceptfriend == 1:
            await request.accept()
        else :
            await request.decline()

    async def is_itemname(self, lang, string):
        idint=0
        ignoretype=[
            "banner",
            "contrail",
            "glider",
            "wrap",
            "loadingscreen",
            "music",
            "spray"
        ]
        idlist=[]
        namelist=[]
        typelist=[]
        TF="False"
        print("https://fortnite-api.com/v2/cosmetics/br?language=" + lang)
        async with aiohttp.ClientSession() as session:
            while True:
                async with self.session.get("https://fortnite-api.com/v2/cosmetics/br", params={'language': lang}) as r:
                    try:
                        data = await r.json()
                        while True:
                            try:
                                if data['data'][idint]['type'] in ignoretype:
                                    idint=idint+1
                                    continue
                                if jaconv.hira2kata(string.lower()) in jaconv.hira2kata(data['data'][idint]['name'].lower()):
                                    idlist.append(data['data'][idint]['id'])
                                    namelist.append(data['data'][idint]['name'])
                                    typelist.append(data['data'][idint]['type'])
                                    TF="True"
                                idint=idint+1
                            except IndexError:
                                return TF, idlist, namelist, typelist
                    except:
                        print("Error!")
                        return TF

    async def event_friend_message(self, message):
        args = message.content.split()
        content = message.content
        mesargs = args[1:]
        mesargs2 = args[2:]
        print('送信者 {0.author.display_name} / {0.author.id} | 内容: "{0.content}"'.format(message))

        if args[0] == "emote_asset":
            try:
                await self.party.me.clear_emote()
                await self.party.me.set_emote("\"" + args[1] + "\"")
                await message.reply('emote asset=' + args[1])
            except:
                await message.reply("ERROR")

        if args[0] == "^eval":
                  try:
                    if message.author.id == creatorid:
                      r = eval(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
        if args[0] == "^eval2":
                  try:
                    if message.author.id == creatorid:
                      r = await eval(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
        if args[0] == "^exec":
                  try:
                    if message.author.id == creatorid:
                      r = exec(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
        if args[0] == "^exec2":
                  try:
                    if message.author.id == creatorid:
                      r = await exec(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
        if args[0] == "prev":
            args = self.prevmes.split()
            content = self.prevmes

        if args[0] == "shop":
            shop = await self.get_current_item_shop_ids()
            shop0 = ', '.join(shop[0])
            shop1 = ', '.join(shop[1])
            shop2 = ', '.join(shop[2])
            shop3 = ', '.join(shop[3])
            await message.reply(shop0)
            await message.reply(shop1)
            await message.reply(shop2)
            await message.reply(shop3)
            print(shop0)
            print(shop1)
            print(shop2)
            print(shop3)

        if args[0] == "user":
            try:
                dname = content.replace("user ","",1)
                user = await self.fetch_profile(dname)
                member = self.get_user(user.id)
                if member is None:
                    await message.reply("ユーザーが見つかりません")
                else:
                    await message.reply(member.display_name + " / " + member.id)
                    print(member.display_name + ' / ' + member.id)
            except:
                await message.reply("エラー")

        if args[0] == "add":
            dname = content.replace("add ","",1)
            user = await self.fetch_profile(dname)
            member = self.get_user(user.id)
            if member is None:
                members = self.get_user(dname)
                await self.add_friend(id=dname)
                await message.reply(members.display_name + " / " + members.id + " にフレンド申請を送信")
                print(member.display_name + ' / ' + member.id + ' にフレンド申請')
            else:
                await self.add_friend(id=member.id)
                await message.reply(member.display_name + " / " + member.id + " にフレンド申請を送信")
                print(member.display_name + ' / ' + member.id + ' にフレンド申請')

        if args[0] == "remove":
            dname = content.replace("remove ","",1)
            user = await self.fetch_profile(dname)
            member = self.get_friend(user.id)
            if member is None:
                members = self.get_friend(dname)
                await members.remove()
                await message.reply("フレンド削除: " + members.display_name + " / " + members.id )
                print(member.display_name + ' / ' + member.id + ' を削除')
            else:
                await member.remove()
                await message.reply("フレンド削除: " + member.display_name + " / " + member.id )
                print(member.display_name + ' / ' + member.id + ' を削除')

        if args[0] == "inv":
            try:
                dname = content.replace("inv ","",1)
                user = await self.fetch_profile(dname)
                member = self.get_friend(user.id)
                if member is None:
                    members = self.get_friend(dname)
                    await self.user.party.invite(user_id=dname)
                    await message.reply(members.display_name + " / " + members.id + " を招待")
                    print(member.display_name + ' / ' + member.id + ' を招待')
                else:
                    await self.user.party.invite(user_id=member.id)
                    await message.reply(member.display_name + " / " + member.id + " を招待")
                    print(member.display_name + ' / ' + member.id + ' を招待')
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "promote":
            try:
                dname = content.replace("promote ","",1)
                user = await self.fetch_profile(dname)
                member = self.user.party.members.get(user.id)
                if member is None:
                    members = self.user.party.members.get(dname)
                    await members.promote()
                    await message.reply(members.display_name + " / " + members.id + " に譲渡")
                    print(member.display_name + ' / ' + member.id + ' に譲渡')
                else:
                    await member.promote()
                    await message.reply(member.display_name + " / " + member.id + " に譲渡")
                    print(member.display_name + ' / ' + member.id + ' に譲渡')
            except:
                await message.reply("エラー")

        if args[0] == "kick":
            try:
                dname = content.replace("kick ","",1)
                user = await self.fetch_profile(dname)
                member = self.user.party.members.get(user.id)
                if member is None:
                    members = self.user.party.members.get(dname)
                    await members.kick()
                    await message.reply(members.display_name + " / " + members.id + " をキック")
                    print(member.display_name + ' / ' + member.id + ' をキック')
                else:
                    await member.kick()
                    await message.reply(member.display_name + " / " + member.id + " をキック")
                    print(member.display_name + ' / ' + member.id + ' をキック')
            except:
                await message.reply("エラー")

        if args[0] == "join":
            try:
                await self.join_to_party(party_id=args[1])
                await message.reply("パーティー参加")
                print('パーティーに参加: ' + args[1])
            except:
                await message.reply("エラー")

        if args[0] == "message":
            try:
                dname = content.replace("message ","",1).split(" : ")
                user = await self.fetch_profile(dname[0])
                member = self.get_friend(user.id)
                if member is None:
                    friends = self.get_friend(dname[0])
                    await friends.send(dname[1])
                    await message.reply(friends.display_name + " / " + friends.id + " にメッセージ: " + dname[1] + " を送信")
                else:
                    await member.send(dname[1])
                    await message.reply(member.display_name + " / " + member.id + " にメッセージ: " + dname[1] + " を送信")
            except:
                await message.reply("エラー")

        if "stop" in args[0]:
            try:
                await self.party.me.set_emote(
                    asset="StopEmote"
                )
                await message.reply('停止')
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "get":
            if args[1] == "skin":
                await message.reply(self.user.party.leader.outfit + " : " + str(self.user.party.leader.outfit_variants))
            if args[1] == "bag":
                await message.reply(self.user.party.leader.backpack + " : " + str(self.user.party.leader.backpack_variants))
            if args[1] == "pick":
                await message.reply(self.user.party.leader.pickaxe + " : " + str(self.user.party.leader.pickaxe_variants))
            if args[1] == "emote":
                await message.reply(self.user.party.leader.emote)

        if args[0] == "partyenable":
            try:
                if args[1] == "true" or args[1] == "True":
                    self.partyenable=True
                    await message.reply("パーティーチャットからのコマンド受付をオンにしました")
                if args[1] == "false" or args[1] == "False":
                    self.partyenable=False
                    await message.reply("パーティーチャットからのコマンド受付をオフにしました")
            except:
                if self.partyenable == False:
                    await message.reply("partyenable = 0")
                if self.partyenable == True:
                    await message.reply("partyenable = 1")

        if args[0] == "owner":
            try:
                if args[1] == "on":
                    self.owneronly=True
                    await message.reply('所有者モードをオンに設定')
                if args[1] == "off":
                    self.owneronly=False
                    await message.reply('所有者モードをオフに設定')
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "mimic":
            try:
                if args[1] == "on":
                    self.mimicemote=1
                    await message.reply('エモートミミックをオンに設定')
                if args[1] == "off":
                    self.mimicemote=0
                    await message.reply('エモートミミックをオフに設定')
            except:
                await message.reply('Error\nContact Pirxcy')
        
        if args[0] == "skinmimic":
            try:
                if args[1] == "on":
                    self.mimicskin=1
                    await message.reply("スキンミミックをオンに設定")
                if args[1] == "off":
                    self.mimicskin=0
                    await message.reply("スキンミミックをオフに設定")
            except:
                await message.reply('Error\nContact Pirxcy')
        
        if args[0] == 'スキン':
            try:
                cid = await self.fetch_item_namejp(' '.join(mesargs), "outfit")
                if cid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_outfit(asset=cid[0])
                    await message.reply('見つかりました: ' + cid[0] + ' : ' + cid[1])
                    self.cid=cid[0]
                    self.svariants=None
                    print(cid[0])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'skin':
            try:
                cid = await self.fetch_cosmetic_id(' '.join(mesargs), "AthenaCharacter")
                if cid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_outfit(asset=cid[0])
                    await message.reply('見つかりました: ' + cid[0] + ' : ' + cid[1])
                    self.cid=cid[0]
                    self.svariants=None
                    print(cid[0])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'cid':
            try:
                cid = await self.fetch_cosmetic_id2(' '.join(mesargs), "AthenaCharacter")
                if cid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_outfit(asset=cid[0])
                    await message.reply('見つかりました: ' + cid[0] + ' : ' + cid[1])
                    self.cid=cid[0]
                    self.svariants=None
                    print(cid[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == 'エモート':
          try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )

            await ctx.send(f'Emote set to {cosmetic.id}.')
            print(f"Set emote to: {cosmetic.id}.")
            await self.party.me.clear_emote()
            await self.party.me.set_emote(asset=cosmetic.id)

          except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find an emote with the name: {content}.")
            print(f"Failed to find an emote with the name: {content}.")
        if args[0] == 'eid':
            try:
                eid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Emote")
                if eid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_emote(asset='StopEmote')
                    await self.party.me.set_emote(asset=eid[0])
                    await message.reply('見つかりました: ' + eid[0] + ' : ' + eid[1])
                    self.eid=eid[0]
                    print(eid[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == 'バッグ':
            try:
                bid = await self.fetch_item_namejp(' '.join(mesargs), "backpack")
                if bid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_backpack(asset=bid[0])
                    await message.reply('見つかりました: ' + bid[0] + ' : ' + bid[1])
                    self.bid=bid[0]
                    self.bvariants=None
                    print(bid[0])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'bag':
            try:
                bid = await self.fetch_cosmetic_id(' '.join(mesargs), "Back Bling")
                if bid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_backpack(asset=bid[0])
                    await message.reply('見つかりました ' + bid[0] + ' : ' + bid[1])
                    self.bid=bid[0]
                    self.bvariants=None
                    print(bid[0])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'bid':
            try:
                bid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Back Bling")
                if bid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_backpack(asset=bid[0])
                    await message.reply('見つかりました ' + bid[0] + ' : ' + bid[1])
                    self.bid=bid[0]
                    self.bvariants=None
                    print(bid[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == 'バッグ':
            try:
                pid = await self.fetch_item_namejp(' '.join(mesargs), "pickaxe")
                if pid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_pickaxe(asset=pid[0])
                    await message.reply('見つかりました: ' + pid[0] + ' : ' + pid[1])
                    self.pid=pid[0]
                    self.pvariants=None
                    print(pid[0])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'pick':
            try:
                pid = await self.fetch_cosmetic_id(' '.join(mesargs), "Harvesting Tool")
                if pid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_pickaxe(asset=pid[0])
                    await self.party.me.set_emote(asset='EID_IceKing')
                    await message.reply('見つかりました ' + pid[0] + ' : ' + pid[1])
                    self.pid=pid[0]
                    self.pvariants=None
                    print(pid[0])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'pid':
            try:
                pid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Harvesting Tool")
                if pid is None:
                    return await message.reply('エラー: 見つかりません')
                else:
                    await self.party.me.set_pickaxe(asset=pid[0])
                    await self.party.me.set_emote(asset='EID_IceKing')
                    await message.reply('見つかりました ' + pid[0] + ' : ' + pid[1])
                    self.pid=pid[0]
                    self.pvariants=None
                    print(pid[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == 'セット':
            try:
                setinfo = await self.fetch_set_item(args[1])
                if setinfo[0] is None:
                    await message.reply('スキンが見つかりません')
                else:
                    self.cid=setinfo[0]
                    self.svariants=None
                    await self.party.me.set_outfit(asset=setinfo[0])
                    await message.reply(setinfo[0])
                    print(setinfo[0])
                if setinfo[1] is None:
                    await message.reply('バッグが見つかりません')
                else:
                    self.bid=setinfo[1]
                    self.bvariants=None
                    await self.party.me.set_backpack(asset=setinfo[1])
                    await message.reply(setinfo[1])
                    print(setinfo[1])
                if setinfo[2] is None:
                    await message.reply('ツルハシが見つかりません')
                else:
                    self.pid=setinfo[2]
                    self.pvariants=None
                    await self.party.me.set_pickaxe(asset=setinfo[2])
                    await message.reply(setinfo[2])
                    print(setinfo[2])
                if setinfo[3] is None:
                    await message.reply('エモートが見つかりません')
                else:
                    self.eid=setinfo[3]
                    await self.party.me.clear_emote()
                    await self.party.me.set_emote(asset=setinfo[3])
                    await message.reply(setinfo[3])
                    print(setinfo[3])
            except:
                await message.reply('Error\nContact Pirxcy')
        if args[0] == 'set':
            cid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Outfit")
            bid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Back Bling")
            pid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Harvesting Tool")
            await self.party.me.set_emote(asset='StopEmote')
            if cid is None:
                await message.reply('スキンが見つかりません')
            else:
                await self.party.me.set_outfit(asset=cid[0])
                await message.reply(cid[0])
                self.cid=cid[0]
                self.svariants=None
                print(cid[0])
            if bid is None:
                await message.reply('バッグが見つかりません')
            else:
                await self.party.me.set_backpack(asset=bid[0])
                await message.reply(bid[0])
                self.bid=bid[0]
                self.bvariants=None
                print(bid[0])
            if pid is None:
                await message.reply('ツルハシが見つかりません')
            else:
                await self.party.me.set_pickaxe(asset=pid[0])
                await message.reply(pid[0])
                self.pid=pid[0]
                self.pvariants=None
                print(pid[0])
                await self.party.me.set_emote(asset='EID_IceKing')
            

        if args[0] == 'allskin':
            try:
                idint = 0
                cid = await self.fetch_allcosmetic_id("CID_", "Outfit")
                await self.party.me.set_emote(asset='StopEmote')
                while True:
                    try:
                        try:
                            list_type = cid[idint]['type']
                        except:
                            pass
                        if list_type == "Outfit":
                            jsondata = cid[idint]['id']
                            await self.party.me.set_outfit(asset=jsondata)
                            print(jsondata)
                            idint += 1
                        time.sleep(2)
                    except IndexError:
                        await message.reply('終わりました')
                        break
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == 'allemote':
            try:
                idint = 0
                eid = await self.fetch_allcosmetic_id("EID_", "Emote")
                await self.party.me.set_emote(asset='StopEmote')
                while True:
                    try:
                        try:
                            list_type = eid[idint]['type']
                        except:
                            pass
                        if list_type == "Emote":
                            jsondata = eid[idint]['id']
                            await self.party.me.set_emote(asset=jsondata)
                            print(jsondata)
                            idint += 1
                        else:
                            jsondata = eid[idint]['id']
                            await self.party.me.set_emote(asset=jsondata)
                            print(jsondata)
                            idint += 1
                        time.sleep(4)
                    except IndexError:
                        await message.reply('終わりました')
                        break
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "load":
            try:
                await self.party.me.set_emote(
                asset="StopEmote"
                )
                await self.party.me.set_outfit(
                    asset=cidjson
                )
                await self.party.me.set_backpack(
                    asset=bidjson
                )
                await self.party.me.set_pickaxe(
                    asset=pidjson
                )
                await self.party.me.set_emote(
                    asset=eidjson
                )
                await self.party.me.set_battlepass_info(
                    has_purchased='true',
                    level=999999999,
                    self_boost_xp=999999999,
                    friend_boost_xp=999999999
                )
                await self.party.me.set_banner(
                    icon='otherbanner28',
                    color='black',
                    season_level=9999
                )
                self.cid=cidjson
                self.bid=bidjson
                self.pid=pidjson
                self.eid.eidjson
            except:
                await message.reply('Error\nContact Pirxcy')
            try:
                if self.user.id == self.user.party.leader.id:
                    await self.user.party.set_playlist(
                        playlist=playlistjson
                    )
            except:
                pass

        if args[0] == "info":
            try:
                if args[1] == "party":
                    print('人数 {0.user.party.member_count} / {0.user.party.id}'.format(self))
                    await message.reply('人数 {0.user.party.member_count} / {0.user.party.id}'.format(self))
                    print(self.user.party.members.keys())
                if args[1] == "スキン":
                    skin = await self.fetch_item_namejp(" ".join(mesargs2), "outfit")
                    if skin is None:
                        await message.reply("エラー: 見つかりません")
                    else:
                        await message.reply("ID: " + skin[0] + " : " + skin[1])
                        await message.reply("説明: " + skin[2])
                        await message.reply("レア度: " + skin[3])
                        print(skin[0])
                if args[1] == "エモート":
                    emote = await self.fetch_item_namejp(' '.join(mesargs2), "emote")
                    if emote is None:
                        await message.reply("エラー: 見つかりません")
                    else:
                        await message.reply("ID: " + emote[0] + " : " + emote[1])
                        await message.reply("説明: " + emote[2])
                        await message.reply("レア度: " + emote[3])
                        print(emote[0])
                if args[1] == "バッグ":
                    bag = await self.fetch_item_namejp(' '.join(mesargs2), "backpack")
                    if bag is None:
                        await message.reply("エラー: 見つかりません")
                    else:
                        await message.reply("ID: " + bag[0] + " : " + bag[1])
                        await message.reply("説明: " + bag[2])
                        await message.reply("レア度: " + bag[3])
                        print(bag[0])
                if args[1] == "ツルハシ":
                    pick = await self.fetch_item_namejp(' '.join(mesargs2), "pickaxe")
                    if bag is None:
                        await message.reply("エラー: 見つかりません")
                    else:
                        await message.reply("ID: " + pick[0] + " : " + pick[1])
                        await message.reply("説明: " + pick[2])
                        await message.reply("レア度: " + pick[3])
                        print(pick[0])
                if args[1] == "skin":
                    skin = await self.fetch_cosmetic_id(' '.join(mesargs2), "Outfit")
                    if skin is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + skin[0] + " : " + skin[1])
                        await message.reply("説明: " + skin[2])
                        await message.reply("レア度: " + skin[3])
                        print(skin[0])
                if args[1] == "cid":
                    skin = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Outfit")
                    if skin is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + skin[0] + " : " + skin[1])
                        await message.reply("説明: " + skin[2])
                        await message.reply("レア度: " + skin[3])
                        print(skin[0])
                if args[1] == "emote":
                    emote = await self.fetch_cosmetic_id(' '.join(mesargs2), "Emote")
                    if emote is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + emote[0] + " : " + emote[1])
                        await message.reply("説明: " + emote[2])
                        await message.reply("レア度: " + emote[3])
                        print(emote[0])
                if args[1] == "eid":
                    emote = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Emote")
                    if emote is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + emote[0] + " : " + emote[1])
                        await message.reply("説明: " + emote[2])
                        await message.reply("レア度: " + emote[3])
                        print(emote0)
                if args[1] == "bag":
                    bag = await self.fetch_cosmetic_id(' '.join(mesargs2), "Back Bling")
                    if bag is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + bag[0] + " : " + bag[1])
                        await message.reply("説明: " + bag[2])
                        await message.reply("レア度: " + bag[3])
                        print(bag[0])
                if args[1] == "bid":
                    bag = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Back Bling")
                    if bag is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + bag[0] + " : " + bag[1])
                        await message.reply("説明: " + bag[2])
                        await message.reply("レア度: " + bag[3])
                        print(bag[0])
                if args[1] == "pick":
                    pick = await self.fetch_cosmetic_id(' '.join(mesargs2), "Harvesting Tool")
                    if pick is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + pick[0] + " : " + pick[1])
                        await message.reply("説明: " + pick[2])
                        await message.reply("レア度: " + pick[3])
                        print(pick[0])
                if args[1] == "pid":
                    pick = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Harvesting Tool")
                    if pick is None:
                        await message.reply("エラー：見つかりません")
                    else:
                        await message.reply("ID: " + pick[0] + " : " + pick[1])
                        await message.reply("説明: " + pick[2])
                        await message.reply("レア度: " + pick[3])
                        print(pick[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "ready":
            try:
                await self.party.me.set_ready(value=True)
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "unready":
            try:
                await self.party.me.set_ready(value=False)
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "invme":
            try:
                await self.user.party.invite(user_id='{0.author.id}'.format(message))
            except:
                await message.reply('Error\nContact Pirxcy')
        
        if args[0] == "pmessage":
            try:
                pmessage = content.replace('pmessage ', '')
                await self.user.party.send(pmessage)
                await message.reply('メッセージ ' + pmessage + ' を送信')
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "status":
            try:
                setstatus=content.replace('status ', '')
                await self.set_status(
                    status=setstatus
                )
            except:
                await message.reply('Error\nContact Pirxcy')

        if "banner" in args[0]:
            try:
                args3=int(args[3])
                await self.party.me.set_banner(icon=args[1], color=args[2], season_level=args3)
            except:
                await message.reply('Error\nContact Pirxcy')

        if "bp" in args[0]:
            try:
                await self.party.me.set_battlepass_info(
                    has_purchased='true',
                    level=args[1],
                    self_boost_xp=args[2],
                    friend_boost_xp=args[3]
                )
                await message.reply('ティア: ' + args[1] + ' XPブースト: ' + args[2] + ' フレンドXPブースト: ' + args[3])
            except:
                await message.reply('Error\nContact Pirxcy')

        if "invite" in args[0]:
            try:
                if args[1] == "decline":
                    self.acceptinvite=0
                    await message.reply('招待を拒否に設定')
                else:
                    if args[1] == "accept":
                        self.acceptinvite=1
                        await message.reply('招待を承諾に設定')
            except:
                await message.reply('Error\nContact Pirxcy')

        if "friend" in args[0]:
            try:
                if args[1] == "accept":
                    self.acceptfriend=1
                    await message.reply('フレンド申請を承諾に設定')
                else:
                    if args[1] == "decline":
                        self.acceptfriend=0
                        await message.reply('フレンド申請を拒否に設定')
            except:
                await message.reply('Error\nContact Pirxcy')


        if args[0] == "variants":
            try:
                args4 = int(args[4])
                if args[1] == "skin":
                    self.svariants = self.party.me.create_variants(item='AthenaCharacter',**{args[3]: args4})
                    self.cid = args[2]

                    await self.party.me.set_outfit(
                        asset=args[2],
                        variants=self.svariants
                    )
                if args[1] == "bag":
                    self.bvariants = self.party.me.create_variants(item='AthenaBackpack',**{args[3]: args4})
                    self.bid = args[2]

                    await self.party.me.set_backpack(
                        asset=args[2],
                        variants=self.bvariants
                    )
                if args[1] == "pick":
                    self.pvariants = self.party.me.create_variants(item='AthenaPickaxe',**{args[3]: args4})
                    self.pid = args[2]

                    await self.party.me.set_pickaxe(
                        asset=args[2],
                        variants=self.pvariants
                    )
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "variants2":
            try:
                args4 = int(args[4])
                args6 = int(args[6])
                if args[1] == "skin":
                    self.svariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6})
                    self.cid = args[2]

                    await self.party.me.set_outfit(
                        asset=args[2],
                        variants=self.svariants
                    )
                if args[1] == "bag":
                    self.bvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6})
                    self.bid = args[2]

                    await self.party.me.set_backpack(
                        asset=args[2],
                        variants=self.bvariants
                    )
                if args[1] == "pick":
                    self.pvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6})
                    self.pid = args[2]

                    await self.party.me.set_pickaxe(
                        asset=args[2],
                        variants=self.pvariants
                    )
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "variants3":
            try:
                args4 = int(args[4])
                args6 = int(args[6])
                args8 = int(args[8])
                if args[1] == "skin":
                    self.svariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6}, **{args[7]: args8})
                    self.cid = args[2]

                    await self.party.me.set_outfit(
                        asset=args[2],
                        variants=self.svariants
                    )
                if args[1] == "bag":
                    self.bvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6}, **{args[7]: args8})
                    self.bid = args[2]

                    await self.party.me.set_backpack(
                        asset=args[2],
                        variants=self.bvariants
                    )
                if args[1] == "pick":
                    self.pvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6}, **{args[7]: args8})
                    self.pid = args[2]

                    await self.party.me.set_pickaxe(
                        asset=args[2],
                        variants=self.pvariants
                    )  
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "getvariants":
            try:
                if args[1] == "skin":
                    variant = str(self.user.party.leader.outfit_variants)
                    await message.reply(variant)
                if args[1] == "bag":
                    variant = str(self.user.party.leader.backpack_variants)
                    await message.reply(variant)
                if args[1] == "pick":
                    variant = str(self.user.party.leader.pickaxe_variants)
                    await message.reply(variant)
            except:
                message.reply('Error\nContact Pirxcy')

        if "leave" in args[0]:
            try:
                if self.acceptinvite == 1:
                    await self.party.me.leave()
                    await message.reply('パーティー離脱')
                else:
                    await message.reply('現在使用できません')
            except:
                await message.reply('Error\nContact Pirxcy')

        if "Playlist_" in args[0]:
            try:
                await self.user.party.set_playlist(
                    playlist=args[0]
                )
                await message.reply('プレイリストを ' + args[0] + ' に設定')
            except:
                await message.reply('Error\nContact Pirxcy')

        if "CID_" in args[0]:
            try:
                await self.party.me.set_emote(
                    asset="StopEmote"
                )
                await self.party.me.set_outfit(
                    asset=args[0]
                )
                await message.reply('スキンを ' + args[0] + ' に設定')
                self.cid=args[0]
                self.svariants=None
                print(args[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if "EID_" in args[0]:
            try:
                await self.party.me.set_emote(
                    asset="StopEmote"
                )
                await self.party.me.set_emote(
                    asset=args[0]
                )
                await message.reply('エモートを ' + args[0] + ' に設定')
                self.eid=args[0]
                print(args[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if "BID_" in args[0]:
            try:
                await self.party.me.set_emote(
                    asset="StopEmote"
                )
                await self.party.me.set_backpack(
                    asset=args[0]
                )
                await message.reply('バッグを ' + args[0] + ' に設定')
                self.bid=args[0]
                self.bvariants=None
                print(args[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if "Pickaxe_ID_" in args[0]:
            try:
                await self.party.me.set_emote(
                    asset="StopEmote"
                )
                await self.party.me.set_pickaxe(
                        asset=args[0]
                )
                await self.party.me.set_emote(asset='EID_IceKing')
                await message.reply('ピッケルを ' + args[0] + ' に設定')
                self.pid=args[0]
                self.pvariants=None
                print(args[0])
            except:
                await message.reply('Error\nContact Pirxcy')

        if args[0] == "out":
            try:
                await self.party.me.set_ready(value=None)
            except:
                await message.reply("エラー")

        if "help" in args[0]:
            try:
                if args[1] == "prev":
                   await message.reply("一つ前のコマンドを繰り返します")
                if args[1] == "partyenable":
                    await message.reply('partyenable [true / false]')
                    await message.reply('パーティーチャットからのコマンド受付の オン/オフ を設定します')
                if args[1] == "owner":
                    await message.reply('owner [on / off]')
                    await message.reply(('招待をボットの所有者しか受付なくなるかの オン/オフ を設定します'))
                if args[1] == "skinmimic":
                    await message.reply('skinmimic [on / off]')
                    await message.reply('スキンミミック機能の オン/オフ を設定します')
                if args[1] == "mimic":
                    await message.reply('mimic [on / off]')
                    await message.reply('エモートミミック機能の オン/オフ を設定します')
                if args[1] == "invite":
                    await message.reply('invite [accept / decline]')
                    await message.reply(('招待の 承諾/拒否 設定をします'))
                if args[1] == "friend":
                    await message.reply("friend [accept / decline]")
                    await message.reply("フレンド申請の 承諾/拒否 設定をします")
                if args[1] == "shop":
                    await message.reply("ショップのアイテムのIDを表示します")
                if args[1] == "info":
                    await message.reply("info [party / スキン / skin / cid / バッグ / bag / bid / ツルハシ / pick / pid / エモート / emote / eid]")
                    await message.reply("パーティーの情報/アイテムの名前,ID,説明,レア度を表示します")
                if args[1] == "allskin":
                    await message.reply('全てのスキンを表示します')
                if args[1] == "allemote":
                    await message.reply('全てのエモートを表示します')
                if args[1] == "スキン":
                    await message.reply('スキン [スキン名]')
                    await message.reply('スキン名を検索、見つかったスキンに設定します')
                    await message.reply('スキン名は日本語限定です')
                if args[1] == "skin":
                    await message.reply('skin [スキン名]')
                    await message.reply('スキン名を検索し、見つかったスキンに設定します')
                    await message.reply('スキン名は英語限定です')
                if args[1] == "cid":
                    await message.reply('cid [CID]')
                    await message.reply('CIDを検索し、見つかったスキンに設定します')
                if args[1] == "エモート":
                    await message.reply('エモート [エモート名]')
                    await message.reply('エモート名を検索、見つかったエモートに設定します')
                    await message.reply('エモート名は日本語限定です')
                if args[1] == "emote":
                    await message.reply('emote [エモート名]')
                    await message.reply('エモート名を検索し、見つかったエモートに設定します')
                    await message.reply('エモート名は英語限定です')
                if args[1] == "eid":
                    await message.reply('eid [EID]')
                    await message.reply('EIDを検索し、見つかったエモートに設定します')
                if args[1] == "バッグ":
                    await message.reply('バッグ [バッグ名]')
                    await message.reply('バッグ名を検索し、見つかったバッグに設定します')
                    await message.reply('バッグ名は日本語限定です')
                if args[1] == "bag":
                    await message.reply('bag [バッグ名]')
                    await message.reply('バッグ名を検索し、見つかったバッグに設定します')
                    await message.reply('バッグ名は英語限定です')
                if args[1] == "bid":
                    await message.reply('bid [BID]')
                    await message.reply('BIDを検索し、見つかったバッグに設定します')
                if args[1] == "ツルハシ":
                    await message.reply('ツルハシ [ツルハシ名]]')
                    await message.reply('ツルハシ名を検索し、見つかったツルハシに設定します')
                    await message.reply('ツルハシ名は日本語限定です')
                if args[1] == "pick":
                    await message.reply('pick [ツルハシ名]]')
                    await message.reply('ツルハシ名を検索し、見つかったツルハシに設定します')
                    await message.reply('ツルハシ名は英語限定です')
                if args[1] == "pid":
                    await message.reply('pid [Pickaxe_ID]')
                    await message.reply('Pickaxe_IDを検索し、見つかったツルハシに設定します')
                if args[1] == "セット":
                    await message.reply('セット [セット名]')
                    await message.reply('セット名を検索し、該当するスキン、バッグ、ツルハシに設定します')
                if args[1] == "set":
                    await message.reply('set [ID]')
                    await message.reply('IDを検索し、該当するスキン、バッグ、ツルハシに設定します')
                if args[1] == "load":
                    await message.reply('諸情報を読み込みます')
                if args[1] == "user":
                    await message.reply("user [ユーザー名/ユーザーID]")
                    await message.reply("ユーザーのIDと名前を表示します")
                if args[1] == "add":
                    await message.reply("add [ユーザー名/ユーザーID]")
                    await message.reply("ユーザーにフレンド申請を送ります。フレンド申請が拒否になっていると機能しません")
                if args[1] == "remove":
                    await message.reply("remove [ユーザー名/ユーザーID]")
                    await message.reply("ユーザーをフレンドから削除します")
                if args[1] == "promote":
                    await message.reply("promote [ユーザー名 / ユーザーID]")
                    await message.reply("ユーザーにリーダーを譲渡します")
                if args[1] == "kick":
                    await message.reply("kick [ユーザー名 / ユーザーID]")
                    await message.reply("ユーザーをキックします")
                if args[1] == "inv":
                    await message.reply('inv [ユーザー名 / ユーザーID]')
                    await message.reply('ユーザーを招待します')
                if args[1] == "invme":
                    await message.reply('メッセージの送り主を招待します')
                if args[1] == "join":
                    await message.reply("join [パーティーID]")
                    await message.reply("パーティーに参加します")
                if args[1] == "message":
                    await message.reply("message [ユーザー名 / ユーザーID] : [メッセージ]")
                    await message.reply("ユーザーにメッセージを送信します")
                if args[1] == "pmessage":
                    await message.reply('pmessage [メッセージ]')
                    await message.reply('パーティーチャットにメッセージを送信します')
                if args[1] == "status":
                    await message.reply('status [ステータス]')
                    await message.reply('ステータスを設定します')
                if args[1] == "banner":
                    await message.reply('banner [バナーID] [色] [シーズンレベル]')
                if args[1] == "bp":
                    await message.reply('bp [レベル] [XPブースト] [フレンドXPブースト]')
                    await message.reply('バトルパス情報を設定します')
                if args[1] == "variants":
                    await message.reply('variants [skin/bag/pick] [ID] [variant] [数値]')
                    await message.reply('スキンのスタイルを設定します')
                if args[1] == "variants2":
                    await message.reply('variants [skin/bag/pick] [ID] [variant] [数値] [variant] [数値]')
                    await message.reply('スキンのスタイルを設定します')
                if args[1] == "variants3":
                    await message.reply('variants [skin/bag/pick] [ID] [variant] [数値] [variant] [数値] [variant] [数値]')
                    await message.reply('スキンのスタイルを設定します')
                if args[1] == "get":
                    await message.reply('get [skin / bag / pick]')
                    await message.reply('パーティーリーダーのアイテムのIDとvariant情報を取得します')
                if args[1] == "getvariants":
                    await message.reply("getvariants [skin / bag / pick]")
                    await message.reply("パーティーリーダーのアイテムのvariant情報を取得します")
                if args[1] == "leave":
                    await message.reply('パーティーを離脱します')
                if args[1] == "Playlist_":
                    await message.reply('プレイリストを設定します')
                if args[1] == "CID_":
                    await message.reply('スキンを設定します')
                if args[1] == "EID_":
                    await message.reply('エモートを設定します')
                if args[1] == "BID_":
                    await message.reply('バッグを設定します')
                if args[1] == "Pickaxe_ID":
                    await message.reply('ピッケルを設定します')
                if args[1] == "stop":
                    await message.reply('エモートを停止します')
                if args[1] == "help":
                    await message.reply("help [コマンド]")
                    await message.reply("[コマンド]は省略できます。コマンドリスト/コマンドの詳細を表示します")
            except IndexError:
                await message.reply('コマンド: コマンド: prev, partyenable, owner, skinmimic, mimic, invite, friend, shop, info, allskin, allemote, skin, cid, emote, eid, bag, bid, pick, pid, load, user, add, remove, promote, kick, inv, invme, join, message, status, banner, bp, variants, variants2, variants3, get, getvariants, Playlist_, CID_, EID_, BID_, Pickaxe_ID_, stop, help')
                await message.reply(('help [コマンド名] で詳細を表示'))

        self.prevmes = content

#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
    async def event_party_message(self, message):
        print('パーティー送信者 {0.author.display_name} / {0.author.id} | 内容: "{0.content}"'.format(message))
        args = message.content.split()
        content = message.content
        mesargs = args[1:]
        mesargs2 = args[2:]
        try:
            result=[]
            ignoretypes=['banner', 'contrail', 'loadingscreen', 'spray', 'toy', 'wrap', 'glider', 'music', 'backpack']
            functions={
              'outfit':'set_outfit', 'backpack':'set_backpack', 'pickaxe':'set_pickaxe', 'emote':'set_emote', 'emoji':'set_emoji'
              }
            if not 'cosmetics' in self.__dir__():
                self.cosmetics = self.api.cosmetics.fetch_all(fortnite_api.GameLanguage('en'))
            for i in self.cosmetics:
                if not i.type.value in ignoretypes and message.content.lower() in i.name.lower():
                    result.append(i)
            item=result[0]
            await self.party.me.set_emote(asset='EID_Clear')
            await (eval(f'self.party.me.{functions[item.type.value]}', locals()))(asset=item.id)
            await message.reply(f'{item.type.value}: {item.name}/{item.id}')
        except IndexError:
            print('Not Found', message.content) #Not Found
        except:
            await message.reply('Error:\n'+__import__('traceback').format_exc())

        if self.partyenable == True:

            if self.lang == False:  #######################################################################################################

                if args[0] == "switch_en":
                    if self.lang == True:
                        await message.reply("hello")
                    if self.lang == False:
                        self.lang=1
                        await message.reply("英語に設定/english")
                        
                if message.content == "つかいかた" or message.content == "使い方":
                  await message.reply("いいか？  \"{0.content}\"じゃなくて\"h e l p\"だ。にどどまちがえるなくそが".format(message))
            
                if args[0] == "prev":
                    args = self.prevmes.split()
                    content = self.prevmes

                if args[0] == "shop":
                    shop = await self.get_current_item_shop_ids()
                    shop0 = ', '.join(shop[0])
                    shop1 = ', '.join(shop[1])
                    shop2 = ', '.join(shop[2])
                    shop3 = ', '.join(shop[3])
                    await message.reply(shop0)
                    await message.reply(shop1)
                    await message.reply(shop2)
                    await message.reply(shop3)
                    print(shop0)
                    print(shop1)
                    print(shop2)
                    print(shop3)

                if args[0] == "user":
                    try:
                        dname = content.replace("user ","",1)
                        user = await self.fetch_profile(dname)
                        member = self.get_user(user.id)
                        if member is None:
                            await message.reply("ユーザーが見つかりません")
                        else:
                            await message.reply(member.display_name + " / " + member.id)
                            print(member.display_name + ' / ' + member.id)
                    except:
                        await message.reply("エラー")
                        
                if args[0] == "^eval":
                  try:
                    if message.author.id == creatorid:
                      r = eval(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
                if args[0] == "^eval2":
                  try:
                    if message.author.id == creatorid:
                      r = await eval(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
                if args[0] == "^exec":
                  try:
                    if message.author.id == creatorid:
                      r = exec(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        
                if args[0] == "^exec2":
                  try:
                    if message.author.id == creatorid:
                      r = await exec(' '.join(args[1:]))
                      await message.reply(str(r))
                    else:
                      pass
                  except Exception as e:
                    await message.reply(str(e))
                    await message.reply(traceback.format_exc())
        

                if args[0] == "out":
                    try:
                        await self.party.me.set_ready(value=None)
                    except:
                        await message.reply("エラー")

                if args[0] == "@":
                    try:
                        await self.user.party.send("\roooooooooooo ooooooooo.   ooooo   .oooooo.   \r`888'     `8 `888   `Y88. `888'  d8P'  `Y8b  \r 888          888   .d88'  888  888          \r 888oooo8     888ooo88P'   888  888          \r 888    \"     888          888  888          \r 888       o  888          888  `88b    ooo  \ro888ooooood8 o888o        o888o  `Y8bood8P'  ")
                    except:
                        await message.reply("エラー")

                if args[0] == "clear":
                    try:
                        await message.reply("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
                    except:
                        await message.reply("エラー")

                if args[0] == "spamstr":
                    spamstr = content.replace('spamstr ', '')
                    try:
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                        await message.reply(spamstr + spamstr + spamstr + spamstr + spamstr)
                    except:
                        await message.reply("エラー")

                if args[0] == "spam":
                    try:
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                        await message.reply(spam + spam + spam + spam + spam)
                    except:
                        await message.reply("エラー")

                if args[0] == "destroyparty":
                    try:
                        await message.reply("destroying...")
                        await self.party.me.set_outfit("/Game/Athena/Items/Cosmetics/Characters//./")
                        await message.reply("crash")
                        await self.party.me.set_outfit(asset=cidjson)
                        await message.reply("sucsessful.")
                    except:
                        message.reply("error")


                if args[0] == "emote_asset":
                    try:
                        await self.party.me.set_emote(args[1])
                        await message.reply('emote asset=' + args[1])
                    except:
                        await message.reply("ERROR")

                if args[0] == "add":
                    dname = content.replace("add ","",1)
                    user = await self.fetch_profile(dname)
                    member = self.get_user(user.id)
                    if member is None:
                        members = self.get_user(dname)
                        await self.add_friend(id=dname)
                        await message.reply(members.display_name + " / " + members.id + " にフレンド申請を送信")
                        print(member.display_name + ' / ' + member.id + ' にフレンド申請')
                    else:
                        await self.add_friend(id=member.id)
                        await message.reply(member.display_name + " / " + member.id + " にフレンド申請を送信")
                        print(member.display_name + ' / ' + member.id + ' にフレンド申請')

                if args[0] == "remove":
                    dname = content.replace("remove ","",1)
                    user = await self.fetch_profile(dname)
                    member = self.get_friend(user.id)
                    if member is None:
                        members = self.get_friend(dname)
                        await members.remove()
                        await message.reply("フレンド削除: " + members.display_name + " / " + members.id )
                        print(member.display_name + ' / ' + member.id + ' を削除')
                    else:
                        await member.remove()
                        await message.reply("フレンド削除: " + member.display_name + " / " + member.id )
                        print(member.display_name + ' / ' + member.id + ' を削除')

                if args[0] == "inv":
                    try:
                        dname = content.replace("inv ","",1)
                        user = await self.fetch_profile(dname)
                        member = self.get_friend(user.id)
                        if member is None:
                            members = self.get_friend(dname)
                            await self.user.party.invite(user_id=dname)
                            await message.reply(members.display_name + " / " + members.id + " を招待")
                            print(member.display_name + ' / ' + member.id + ' を招待')
                        else:
                            await self.user.party.invite(user_id=member.id)
                            await message.reply(member.display_name + " / " + member.id + " を招待")
                            print(member.display_name + ' / ' + member.id + ' を招待')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "promote":
                    try:
                        dname = content.replace("promote ","",1)
                        user = await self.fetch_profile(dname)
                        member = self.user.party.members.get(user.id)
                        if member is None:
                            members = self.user.party.members.get(dname)
                            await members.promote()
                            await message.reply(members.display_name + " / " + members.id + " に譲渡")
                            print(member.display_name + ' / ' + member.id + ' に譲渡')
                        else:
                            await member.promote()
                            await message.reply(member.display_name + " / " + member.id + " に譲渡")
                            print(member.display_name + ' / ' + member.id + ' に譲渡')
                    except:
                        await message.reply("エラー")

                if args[0] == "kick":
                    try:
                        dname = content.replace("kick ","",1)
                        user = await self.fetch_profile(dname)
                        member = self.user.party.members.get(user.id)
                        if member is None:
                            members = self.user.party.members.get(dname)
                            await members.kick()
                            await message.reply(members.display_name + " / " + members.id + " をキック")
                            print(member.display_name + ' / ' + member.id + ' をキック')
                        else:
                            await member.kick()
                            await message.reply(member.display_name + " / " + member.id + " をキック")
                            print(member.display_name + ' / ' + member.id + ' をキック')
                    except:
                        await message.reply("エラー")

                if args[0] == "join":
                    try:
                        await self.join_to_party(party_id=args[1])
                        await message.reply("パーティー参加")
                        print('パーティーに参加: ' + args[1])
                    except:
                        await message.reply("エラー")

                if args[0] == "message":
                    try:
                        dname = content.replace("message ","",1).split(" : ")
                        user = await self.fetch_profile(dname[0])
                        member = self.get_friend(user.id)
                        if member is None:
                            friends = self.get_friend(dname[0])
                            await friends.send(dname[1])
                            await message.reply(friends.display_name + " / " + friends.id + " にメッセージ: " + dname[1] + " を送信")
                        else:
                            await member.send(dname[1])
                            await message.reply(member.display_name + " / " + member.id + " にメッセージ: " + dname[1] + " を送信")
                    except:
                        await message.reply("エラー")

                if "stop" in args[0]:
                    try:
                        await self.party.me.set_emote(
                            asset="StopEmote"
                        )
                        await message.reply('停止')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "get":
                    if args[1] == "skin":
                        await message.reply(self.user.party.leader.outfit + " : " + str(self.user.party.leader.outfit_variants))
                    if args[1] == "bag":
                        await message.reply(self.user.party.leader.backpack + " : " + str(self.user.party.leader.backpack_variants))
                    if args[1] == "pick":
                        await message.reply(self.user.party.leader.pickaxe + " : " + str(self.user.party.leader.pickaxe_variants))
                    if args[1] == "emote":
                        await message.reply(self.user.party.leader.emote)

                if args[0] == "partyenable":
                    try:
                        if args[1] == "true" or args[1] == "True":
                            self.partyenable=True
                            await message.reply("パーティーチャットからのコマンド受付をオンにしました")
                        if args[1] == "false" or args[1] == "False":
                            self.partyenable=False
                            await message.reply("パーティーチャットからのコマンド受付をオフにしました")
                    except:
                        if self.partyenable == False:
                            await message.reply("partyenable = 0")
                        if self.partyenable == True:
                            await message.reply("partyenable = 1")

                if args[0] == "owner":
                    try:
                        if args[1] == "on":
                            self.owneronly=True
                            await message.reply('所有者モードをオンに設定')
                        if args[1] == "off":
                            self.owneronly=False
                            await message.reply('所有者モードをオフに設定')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "mimic":
                    try:
                        if args[1] == "on":
                            self.mimicemote=1
                            await message.reply('エモートミミックをオンに設定')
                        if args[1] == "off":
                            self.mimicemote=0
                            await message.reply('エモートミミックをオフに設定')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "skinmimic":
                    try:
                        if args[1] == "on":
                            self.mimicskin=1
                            await message.reply("スキンミミックをオンに設定")
                        if args[1] == "off":
                            self.mimicskin=0
                            await message.reply("スキンミミックをオフに設定")
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == 'スキン':
                    try:
                        cid = await self.fetch_item_namejp(' '.join(mesargs), "outfit")
                        if cid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_outfit(asset=cid[0])
                            await message.reply('見つかりました: ' + cid[0] + ' : ' + cid[1])
                            self.cid=cid[0]
                            self.svariants=None
                            print(cid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'skin':
                    try:
                        cid = await self.fetch_cosmetic_id(' '.join(mesargs), "Outfit")
                        if cid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_outfit(asset=cid[0])
                            await message.reply('見つかりました: ' + cid[0] + ' : ' + cid[1])
                            self.cid=cid[0]
                            self.svariants=None
                            print(cid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'cid':
                    try:
                        cid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Outfit")
                        if cid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_outfit(asset=cid[0])
                            await message.reply('見つかりました: ' + cid[0] + ' : ' + cid[1])
                            self.cid=cid[0]
                            self.svariants=None
                            print(cid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == 'エモート':
                    try:
                        eid = await self.fetch_item_namejp(' '.join(mesargs), "emote")
                        if eid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.clear_emote()
                            await self.party.me.set_emote(asset=eid[0])
                            await message.reply('見つかりました: ' + eid[0] + ' : ' + eid[1])
                            self.eid=eid[0]
                            print(eid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'emote':
                  try:
                    result=[]
                    ignoretypes=[]
                    functions={
                      'outfit':'set_outfit', 'backpack':'set_backpack', 'pickaxe':'set_pickaxe', 'emote':'set_emote', 'emoji':'set_emoji'
                      }
                    if not 'cosmetics' in self.__dir__():
                          self.cosmetics = self.api.cosmetics.fetch_all(fortnite_api.GameLanguage('en'))
                    for i in self.cosmetics:
                            if not i.type.value in ignoretypes and message.content.lower() in i.name.lower():
                               result.append(i)
                    item=result[0]
                    await self.party.me.set_emote(asset='EID_Clear')
                    await (eval(f'self.party.me.set_emote{item.type.value}', locals()))(asset=item.id)
                    await message.reply(f'{item.type.value}: {item.name}/{item.id}')
                  except IndexError:
                      print('Not Found', message.content) #Not Found
                  except:
                      await message.reply('Error:\n'+__import__('traceback').format_exc())
                if args[0] == 'eid':
                    try:
                        eid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Emote")
                        if eid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_emote(asset='StopEmote')
                            await self.party.me.set_emote(asset=eid[0])
                            await message.reply('見つかりました: ' + eid[0] + ' : ' + eid[1])
                            self.eid=eid[0]
                            print(eid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == 'バッグ':
                    try:
                        bid = await self.fetch_item_namejp(' '.join(mesargs), "backpack")
                        if bid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_backpack(asset=bid[0])
                            await message.reply('見つかりました: ' + bid[0] + ' : ' + bid[1])
                            self.bid=bid[0]
                            self.bvariants=None
                            print(bid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'bag':
                    try:
                        bid = await self.fetch_cosmetic_id(' '.join(mesargs), "Back Bling")
                        if bid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_backpack(asset=bid[0])
                            await message.reply('見つかりました ' + bid[0] + ' : ' + bid[1])
                            self.bid=bid[0]
                            self.bvariants=None
                            print(bid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'bid':
                    try:
                        bid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Back Bling")
                        if bid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_backpack(asset=bid[0])
                            await message.reply('見つかりました ' + bid[0] + ' : ' + bid[1])
                            self.bid=bid[0]
                            self.bvariants=None
                            print(bid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == 'バッグ':
                    try:
                        pid = await self.fetch_item_namejp(' '.join(mesargs), "pickaxe")
                        if pid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_pickaxe(asset=pid[0])
                            await message.reply('見つかりました: ' + pid[0] + ' : ' + pid[1])
                            self.pid=pid[0]
                            self.pvariants=None
                            print(pid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'pick':
                    try:
                        pid = await self.fetch_cosmetic_id(' '.join(mesargs), "Harvesting Tool")
                        if pid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_pickaxe(asset=pid[0])
                            await self.party.me.set_emote(asset='EID_IceKing')
                            await message.reply('見つかりました ' + pid[0] + ' : ' + pid[1])
                            self.pid=pid[0]
                            self.pvariants=None
                            print(pid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'pid':
                    try:
                        pid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Harvesting Tool")
                        if pid is None:
                            return await message.reply('エラー: 見つかりません')
                        else:
                            await self.party.me.set_pickaxe(asset=pid[0])
                            await self.party.me.set_emote(asset='EID_IceKing')
                            await message.reply('見つかりました ' + pid[0] + ' : ' + pid[1])
                            self.pid=pid[0]
                            self.pvariants=None
                            print(pid[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == 'セット':
                    try:
                        setinfo = await self.fetch_set_item(args[1])
                        if setinfo[0] is None:
                            await message.reply('スキンが見つかりません')
                        else:
                            self.cid=setinfo[0]
                            self.svariants=None
                            await self.party.me.set_outfit(asset=setinfo[0])
                            await message.reply(setinfo[0])
                            print(setinfo[0])
                        if setinfo[1] is None:
                            await message.reply('バッグが見つかりません')
                        else:
                            self.bid=setinfo[1]
                            self.bvariants=None
                            await self.party.me.set_backpack(asset=setinfo[1])
                            await message.reply(setinfo[1])
                            print(setinfo[1])
                        if setinfo[2] is None:
                            await message.reply('ツルハシが見つかりません')
                        else:
                            self.pid=setinfo[2]
                            self.pvariants=None
                            await self.party.me.set_pickaxe(asset=setinfo[2])
                            await message.reply(setinfo[2])
                            print(setinfo[2])
                        if setinfo[3] is None:
                            await message.reply('エモートが見つかりません')
                        else:
                            self.eid=setinfo[3]
                            await self.party.me.clear_emote()
                            await self.party.me.set_emote(asset=setinfo[3])
                            await message.reply(setinfo[3])
                            print(setinfo[3])
                    except:
                        await message.reply('Error\nContact Pirxcy')
                if args[0] == 'set':
                    cid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Outfit")
                    bid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Back Bling")
                    pid = await self.fetch_cosmetic_id2(' '.join(mesargs), "Harvesting Tool")
                    await self.party.me.set_emote(asset='StopEmote')
                    if cid is None:
                        await message.reply('スキンが見つかりません')
                    else:
                        await self.party.me.set_outfit(asset=cid[0])
                        await message.reply(cid[0])
                        self.cid=cid[0]
                        self.svariants=None
                        print(cid[0])
                    if bid is None:
                        await message.reply('バッグが見つかりません')
                    else:
                        await self.party.me.set_backpack(asset=bid[0])
                        await message.reply(bid[0])
                        self.bid=bid[0]
                        self.bvariants=None
                        print(bid[0])
                    if pid is None:
                        await message.reply('ツルハシが見つかりません')
                    else:
                        await self.party.me.set_pickaxe(asset=pid[0])
                        await message.reply(pid[0])
                        self.pid=pid[0]
                        self.pvariants=None
                        print(pid[0])
                        await self.party.me.set_emote(asset='EID_IceKing')


                if args[0] == 'allskin':
                    try:
                        idint = 0
                        cid = await self.fetch_allcosmetic_id("CID_", "Outfit")
                        await self.party.me.set_emote(asset='StopEmote')
                        while True:
                            try:
                                try:
                                    list_type = cid[idint]['type']
                                except:
                                    pass
                                if list_type == "Outfit":
                                    jsondata = cid[idint]['id']
                                    await self.party.me.set_outfit(asset=jsondata)
                                    print(jsondata)
                                    idint += 1
                                time.sleep(2)
                            except IndexError:
                                await message.reply('終わりました')
                                break
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == 'allemote':
                    try:
                        idint = 0
                        eid = await self.fetch_allcosmetic_id("EID_", "Emote")
                        await self.party.me.set_emote(asset='StopEmote')
                        while True:
                            try:
                                try:
                                    list_type = eid[idint]['type']
                                except:
                                    pass
                                if list_type == "Emote":
                                    jsondata = eid[idint]['id']
                                    await self.party.me.set_emote(asset=jsondata)
                                    print(jsondata)
                                    idint += 1
                                else:
                                    jsondata = eid[idint]['id']
                                    await self.party.me.set_emote(asset=jsondata)
                                    print(jsondata)
                                    idint += 1
                                time.sleep(4)
                            except IndexError:
                                await message.reply('終わりました')
                                break
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "load":
                    try:
                        await self.party.me.set_emote(
                        asset="StopEmote"
                        )
                        await self.party.me.set_outfit(
                            asset=cidjson
                        )
                        await self.party.me.set_backpack(
                            asset=bidjson
                        )
                        await self.party.me.set_pickaxe(
                            asset=pidjson
                        )
                        await self.party.me.set_emote(
                            asset=eidjson
                        )
                        await self.party.me.set_battlepass_info(
                            has_purchased='true',
                            level=999999999,
                            self_boost_xp=999999999,
                            friend_boost_xp=999999999
                        )
                        await self.party.me.set_banner(
                            icon='otherbanner28',
                            color='black',
                            season_level=9999
                        )
                        self.cid=cidjson
                        self.bid=bidjson
                        self.pid=pidjson
                        self.eid.eidjson
                    except:
                        await message.reply('Error\nContact Pirxcy')
                    try:
                        if self.user.id == self.user.party.leader.id:
                            await self.user.party.set_playlist(
                                playlist=playlistjson
                            )
                    except:
                        pass

                if args[0] == "info":
                    try:
                        if args[1] == "party":
                            print('人数 {0.user.party.member_count} / {0.user.party.id}'.format(self))
                            await message.reply('人数 {0.user.party.member_count} / {0.user.party.id}'.format(self))
                            print(self.user.party.members.keys())
                        if args[1] == "スキン":
                            skin = await self.fetch_item_namejp(" ".join(mesargs2), "outfit")
                            if skin is None:
                                await message.reply("エラー: 見つかりません")
                            else:
                                await message.reply("ID: " + skin[0] + " : " + skin[1])
                                await message.reply("説明: " + skin[2])
                                await message.reply("レア度: " + skin[3])
                                print(skin[0])
                        if args[1] == "エモート":
                            emote = await self.fetch_item_namejp(' '.join(mesargs2), "emote")
                            if emote is None:
                                await message.reply("エラー: 見つかりません")
                            else:
                                await message.reply("ID: " + emote[0] + " : " + emote[1])
                                await message.reply("説明: " + emote[2])
                                await message.reply("レア度: " + emote[3])
                                print(emote[0])
                        if args[1] == "バッグ":
                            bag = await self.fetch_item_namejp(' '.join(mesargs2), "backpack")
                            if bag is None:
                                await message.reply("エラー: 見つかりません")
                            else:
                                await message.reply("ID: " + bag[0] + " : " + bag[1])
                                await message.reply("説明: " + bag[2])
                                await message.reply("レア度: " + bag[3])
                                print(bag[0])
                        if args[1] == "ツルハシ":
                            pick = await self.fetch_item_namejp(' '.join(mesargs2), "pickaxe")
                            if bag is None:
                                await message.reply("エラー: 見つかりません")
                            else:
                                await message.reply("ID: " + pick[0] + " : " + pick[1])
                                await message.reply("説明: " + pick[2])
                                await message.reply("レア度: " + pick[3])
                                print(pick[0])
                        if args[1] == "skin":
                            skin = await self.fetch_cosmetic_id(' '.join(mesargs2), "Outfit")
                            if skin is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + skin[0] + " : " + skin[1])
                                await message.reply("説明: " + skin[2])
                                await message.reply("レア度: " + skin[3])
                                print(skin[0])
                        if args[1] == "cid":
                            skin = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Outfit")
                            if skin is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + skin[0] + " : " + skin[1])
                                await message.reply("説明: " + skin[2])
                                await message.reply("レア度: " + skin[3])
                                print(skin[0])
                        if args[1] == "emote":
                            emote = await self.fetch_cosmetic_id(' '.join(mesargs2), "Emote")
                            if emote is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + emote[0] + " : " + emote[1])
                                await message.reply("説明: " + emote[2])
                                await message.reply("レア度: " + emote[3])
                                print(emote[0])
                        if args[1] == "eid":
                            emote = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Emote")
                            if emote is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + emote[0] + " : " + emote[1])
                                await message.reply("説明: " + emote[2])
                                await message.reply("レア度: " + emote[3])
                                print(emote0)
                        if args[1] == "bag":
                            bag = await self.fetch_cosmetic_id(' '.join(mesargs2), "Back Bling")
                            if bag is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + bag[0] + " : " + bag[1])
                                await message.reply("説明: " + bag[2])
                                await message.reply("レア度: " + bag[3])
                                print(bag[0])
                        if args[1] == "bid":
                            bag = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Back Bling")
                            if bag is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + bag[0] + " : " + bag[1])
                                await message.reply("説明: " + bag[2])
                                await message.reply("レア度: " + bag[3])
                                print(bag[0])
                        if args[1] == "pick":
                            pick = await self.fetch_cosmetic_id(' '.join(mesargs2), "Harvesting Tool")
                            if pick is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + pick[0] + " : " + pick[1])
                                await message.reply("説明: " + pick[2])
                                await message.reply("レア度: " + pick[3])
                                print(pick[0])
                        if args[1] == "pid":
                            pick = await self.fetch_cosmetic_id2(' '.join(mesargs2), "Harvesting Tool")
                            if pick is None:
                                await message.reply("エラー：見つかりません")
                            else:
                                await message.reply("ID: " + pick[0] + " : " + pick[1])
                                await message.reply("説明: " + pick[2])
                                await message.reply("レア度: " + pick[3])
                                print(pick[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "ready":
                    try:
                        await self.party.me.set_ready(value=True)
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "unready":
                    try:
                        await self.party.me.set_ready(value=False)
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "invme":
                    try:
                        await self.user.party.invite(user_id='{0.author.id}'.format(message))
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "pmessage":
                    try:
                        pmessage = content.replace('pmessage ', '')
                        await self.user.party.send(pmessage)
                        await message.reply('メッセージ ' + pmessage + ' を送信')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "status":
                    try:
                        setstatus=content.replace('status ', '')
                        await self.set_status(
                            status=setstatus
                        )
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "banner" in args[0]:
                    try:
                        args3=int(args[3])
                        await self.party.me.set_banner(icon=args[1], color=args[2], season_level=args3)
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "bp" in args[0]:
                    try:
                        await self.party.me.set_battlepass_info(
                            has_purchased='true',
                            level=args[1],
                            self_boost_xp=args[2],
                            friend_boost_xp=args[3]
                        )
                        await message.reply('ティア: ' + args[1] + ' XPブースト: ' + args[2] + ' フレンドXPブースト: ' + args[3])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "invite" in args[0]:
                    try:
                        if args[1] == "decline":
                            self.acceptinvite=0
                            await message.reply('招待を拒否に設定')
                        else:
                            if args[1] == "accept":
                                self.acceptinvite=1
                                await message.reply('招待を承諾に設定')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "friend" in args[0]:
                    try:
                        if args[1] == "accept":
                            self.acceptfriend=1
                            await message.reply('フレンド申請を承諾に設定')
                        else:
                            if args[1] == "decline":
                                self.acceptfriend=0
                                await message.reply('フレンド申請を拒否に設定')
                    except:
                        await message.reply('Error\nContact Pirxcy')


                if args[0] == "variants":
                    try:
                        args4 = int(args[4])
                        if args[1] == "skin":
                            self.svariants = self.party.me.create_variants(item='AthenaCharacter',**{args[3]: args4})
                            self.cid = args[2]

                            await self.party.me.set_outfit(
                                asset=args[2],
                                variants=self.svariants
                            )
                        if args[1] == "bag":
                            self.bvariants = self.party.me.create_variants(item='AthenaBackpack',**{args[3]: args4})
                            self.bid = args[2]

                            await self.party.me.set_backpack(
                                asset=args[2],
                                variants=self.bvariants
                            )
                        if args[1] == "pick":
                            self.pvariants = self.party.me.create_variants(item='AthenaPickaxe',**{args[3]: args4})
                            self.pid = args[2]

                            await self.party.me.set_pickaxe(
                                asset=args[2],
                                variants=self.pvariants
                            )
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "variants2":
                    try:
                        args4 = int(args[4])
                        args6 = int(args[6])
                        if args[1] == "skin":
                            self.svariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6})
                            self.cid = args[2]

                            await self.party.me.set_outfit(
                                asset=args[2],
                                variants=self.svariants
                            )
                        if args[1] == "bag":
                            self.bvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6})
                            self.bid = args[2]

                            await self.party.me.set_backpack(
                                asset=args[2],
                                variants=self.bvariants
                            )
                        if args[1] == "pick":
                            self.pvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6})
                            self.pid = args[2]

                            await self.party.me.set_pickaxe(
                                asset=args[2],
                                variants=self.pvariants
                            )
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "variants3":
                    try:
                        args4 = int(args[4])
                        args6 = int(args[6])
                        args8 = int(args[8])
                        if args[1] == "skin":
                            self.svariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6}, **{args[7]: args8})
                            self.cid = args[2]

                            await self.party.me.set_outfit(
                                asset=args[2],
                                variants=self.svariants
                            )
                        if args[1] == "bag":
                            self.bvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6}, **{args[7]: args8})
                            self.bid = args[2]

                            await self.party.me.set_backpack(
                                asset=args[2],
                                variants=self.bvariants
                            )
                        if args[1] == "pick":
                            self.pvariants = self.party.me.create_variants(**{args[3]: args4}, **{args[5]: args6}, **{args[7]: args8})
                            self.pid = args[2]

                            await self.party.me.set_pickaxe(
                                asset=args[2],
                                variants=self.pvariants
                            )  
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if args[0] == "getvariants":
                    try:
                        if args[1] == "skin":
                            variant = str(self.user.party.leader.outfit_variants)
                            await message.reply(variant)
                        if args[1] == "bag":
                            variant = str(self.user.party.leader.backpack_variants)
                            await message.reply(variant)
                        if args[1] == "pick":
                            variant = str(self.user.party.leader.pickaxe_variants)
                            await message.reply(variant)
                    except:
                        message.reply('Error\nContact Pirxcy')

                if "leave" in args[0]:
                    try:
                        if self.acceptinvite == 1:
                            await self.party.me.leave()
                            await message.reply('パーティー離脱')
                        else:
                            await message.reply('現在使用できません')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "Playlist_" in args[0]:
                    try:
                        await self.user.party.set_playlist(
                            playlist=args[0]
                        )
                        await message.reply('プレイリストを ' + args[0] + ' に設定')
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "CID_" in args[0]:
                    try:
                        await self.party.me.set_emote(
                            asset="StopEmote"
                        )
                        await self.party.me.set_outfit(
                            asset=args[0]
                        )
                        await message.reply('スキンを ' + args[0] + ' に設定')
                        self.cid=args[0]
                        self.svariants=None
                        print(args[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "EID_" in args[0]:
                    try:
                        await self.party.me.set_emote(
                            asset="StopEmote"
                        )
                        await self.party.me.set_emote(
                            asset=args[0]
                        )
                        await message.reply('エモートを ' + args[0] + ' に設定')
                        self.eid=args[0]
                        print(args[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "BID_" in args[0]:
                    try:
                        await self.party.me.set_emote(
                            asset="StopEmote"
                        )
                        await self.party.me.set_backpack(
                            asset=args[0]
                        )
                        await message.reply('バッグを ' + args[0] + ' に設定')
                        self.bid=args[0]
                        self.bvariants=None
                        print(args[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "Pickaxe_ID_" in args[0]:
                    try:
                        await self.party.me.set_emote(
                            asset="StopEmote"
                        )
                        await self.party.me.set_pickaxe(
                                asset=args[0]
                        )
                        await self.party.me.set_emote(asset='EID_IceKing')
                        await message.reply('ピッケルを ' + args[0] + ' に設定')
                        self.pid=args[0]
                        self.pvariants=None
                        print(args[0])
                    except:
                        await message.reply('Error\nContact Pirxcy')

                if "help" in args[0]:
                    try:
                        if args[1] == "prev":
                           await message.reply("一つ前のコマンドを繰り返します")
                        if args[1] == "partyenable":
                            await message.reply('partyenable [true / false]')
                            await message.reply('パーティーチャットからのコマンド受付の オン/オフ を設定します')
                        if args[1] == "owner":
                            await message.reply('owner [on / off]')
                            await message.reply(('招待をボットの所有者しか受付なくなるかの オン/オフ を設定します'))
                        if args[1] == "skinmimic":
                            await message.reply('skinmimic [on / off]')
                            await message.reply('スキンミミック機能の オン/オフ を設定します')
                        if args[1] == "mimic":
                            await message.reply('mimic [on / off]')
                            await message.reply('エモートミミック機能の オン/オフ を設定します')
                        if args[1] == "invite":
                            await message.reply('invite [accept / decline]')
                            await message.reply(('招待の 承諾/拒否 設定をします'))
                        if args[1] == "friend":
                            await message.reply("friend [accept / decline]")
                            await message.reply("フレンド申請の 承諾/拒否 設定をします")
                        if args[1] == "shop":
                            await message.reply("ショップのアイテムのIDを表示します")
                        if args[1] == "info":
                            await message.reply("info [party / スキン / skin / cid / バッグ / bag / bid / ツルハシ / pick / pid / エモート / emote / eid]")
                            await message.reply("パーティーの情報/アイテムの名前,ID,説明,レア度を表示します")
                        if args[1] == "allskin":
                            await message.reply('全てのスキンを表示します')
                        if args[1] == "allemote":
                            await message.reply('全てのエモートを表示します')
                        if args[1] == "スキン":
                            await message.reply('スキン [スキン名]')
                            await message.reply('スキン名を検索、見つかったスキンに設定します')
                            await message.reply('スキン名は日本語限定です')
                        if args[1] == "skin":
                            await message.reply('skin [スキン名]')
                            await message.reply('スキン名を検索し、見つかったスキンに設定します')
                            await message.reply('スキン名は英語限定です')
                        if args[1] == "cid":
                            await message.reply('cid [CID]')
                            await message.reply('CIDを検索し、見つかったスキンに設定します')
                        if args[1] == "エモート":
                            await message.reply('エモート [エモート名]')
                            await message.reply('エモート名を検索、見つかったエモートに設定します')
                            await message.reply('エモート名は日本語限定です')
                        if args[1] == "emote":
                            await message.reply('emote [エモート名]')
                            await message.reply('エモート名を検索し、見つかったエモートに設定します')
                            await message.reply('エモート名は英語限定です')
                        if args[1] == "eid":
                            await message.reply('eid [EID]')
                            await message.reply('EIDを検索し、見つかったエモートに設定します')
                        if args[1] == "バッグ":
                            await message.reply('バッグ [バッグ名]')
                            await message.reply('バッグ名を検索し、見つかったバッグに設定します')
                            await message.reply('バッグ名は日本語限定です')
                        if args[1] == "bag":
                            await message.reply('bag [バッグ名]')
                            await message.reply('バッグ名を検索し、見つかったバッグに設定します')
                            await message.reply('バッグ名は英語限定です')
                        if args[1] == "bid":
                            await message.reply('bid [BID]')
                            await message.reply('BIDを検索し、見つかったバッグに設定します')
                        if args[1] == "ツルハシ":
                            await message.reply('ツルハシ [ツルハシ名]]')
                            await message.reply('ツルハシ名を検索し、見つかったツルハシに設定します')
                            await message.reply('ツルハシ名は日本語限定です')
                        if args[1] == "pick":
                            await message.reply('pick [ツルハシ名]]')
                            await message.reply('ツルハシ名を検索し、見つかったツルハシに設定します')
                            await message.reply('ツルハシ名は英語限定です')
                        if args[1] == "pid":
                            await message.reply('pid [Pickaxe_ID]')
                            await message.reply('Pickaxe_IDを検索し、見つかったツルハシに設定します')
                        if args[1] == "セット":
                            await message.reply('セット [セット名]')
                            await message.reply('セット名を検索し、該当するスキン、バッグ、ツルハシに設定します')
                        if args[1] == "set":
                            await message.reply('set [ID]')
                            await message.reply('IDを検索し、該当するスキン、バッグ、ツルハシに設定します')
                        if args[1] == "load":
                            await message.reply('諸情報を読み込みます')
                        if args[1] == "user":
                            await message.reply("user [ユーザー名/ユーザーID]")
                            await message.reply("ユーザーのIDと名前を表示します")
                        if args[1] == "add":
                            await message.reply("add [ユーザー名/ユーザーID]")
                            await message.reply("ユーザーにフレンド申請を送ります。フレンド申請が拒否になっていると機能しません")
                        if args[1] == "remove":
                            await message.reply("remove [ユーザー名/ユーザーID]")
                            await message.reply("ユーザーをフレンドから削除します")
                        if args[1] == "promote":
                            await message.reply("promote [ユーザー名 / ユーザーID]")
                            await message.reply("ユーザーにリーダーを譲渡します")
                        if args[1] == "kick":
                            await message.reply("kick [ユーザー名 / ユーザーID]")
                            await message.reply("ユーザーをキックします")
                        if args[1] == "inv":
                            await message.reply('inv [ユーザー名 / ユーザーID]')
                            await message.reply('ユーザーを招待します')
                        if args[1] == "invme":
                            await message.reply('メッセージの送り主を招待します')
                        if args[1] == "join":
                            await message.reply("join [パーティーID]")
                            await message.reply("パーティーに参加します")
                        if args[1] == "message":
                            await message.reply("message [ユーザー名 / ユーザーID] : [メッセージ]")
                            await message.reply("ユーザーにメッセージを送信します")
                        if args[1] == "pmessage":
                            await message.reply('pmessage [メッセージ]')
                            await message.reply('パーティーチャットにメッセージを送信します')
                        if args[1] == "status":
                            await message.reply('status [ステータス]')
                            await message.reply('ステータスを設定します')
                        if args[1] == "banner":
                            await message.reply('banner [バナーID] [色] [シーズンレベル]')
                        if args[1] == "bp":
                            await message.reply('bp [レベル] [XPブースト] [フレンドXPブースト]')
                            await message.reply('バトルパス情報を設定します')
                        if args[1] == "variants":
                            await message.reply('variants [skin/bag/pick] [ID] [variant] [数値]')
                            await message.reply('スキンのスタイルを設定します')
                        if args[1] == "variants2":
                            await message.reply('variants [skin/bag/pick] [ID] [variant] [数値] [variant] [数値]')
                            await message.reply('スキンのスタイルを設定します')
                        if args[1] == "variants3":
                            await message.reply('variants [skin/bag/pick] [ID] [variant] [数値] [variant] [数値] [variant] [数値]')
                            await message.reply('スキンのスタイルを設定します')
                        if args[1] == "get":
                            await message.reply('get [skin / bag / pick]')
                            await message.reply('パーティーリーダーのアイテムのIDとvariant情報を取得します')
                        if args[1] == "getvariants":
                            await message.reply("getvariants [skin / bag / pick]")
                            await message.reply("パーティーリーダーのアイテムのvariant情報を取得します")
                        if args[1] == "leave":
                            await message.reply('パーティーを離脱します')
                        if args[1] == "Playlist_":
                            await message.reply('プレイリストを設定します')
                        if args[1] == "CID_":
                            await message.reply('スキンを設定します')
                        if args[1] == "EID_":
                            await message.reply('エモートを設定します')
                        if args[1] == "BID_":
                            await message.reply('バッグを設定します')
                        if args[1] == "Pickaxe_ID":
                            await message.reply('ピッケルを設定します')
                        if args[1] == "stop":
                            await message.reply('エモートを停止します')
                        if args[1] == "help":
                            await message.reply("help [コマンド]")
                            await message.reply("[コマンド]は省略できます。コマンドリスト/コマンドの詳細を表示します")
                    except IndexError:
                        await message.reply('コマンド: コマンド: prev, partyenable, owner, skinmimic, mimic, invite, friend, shop, info, allskin, allemote, skin, cid, emote, eid, bag, bid, pick, pid, load, user, add, remove, promote, kick, inv, invme, join, message, status, banner, bp, variants, variants2, variants3, get, getvariants, Playlist_, CID_, EID_, BID_, Pickaxe_ID_, stop, help')
                        await message.reply(('help [コマンド名] で詳細を表示'))

        if self.msg_search == True:
          try:
              if args[0].isdigit() and not self.foundlist is None:
                try:
                  self.foundlist=[]
                  self.foundlist.extend([foundlisttype, foundlistid])
                  if self.foundlist[0][int(args[0])-1] == "outfit":
                    await self.party.me.set_outfit(self.foundlist[1][int(args[0])-1].upper())
                    print(self.foundlist[1][int(args[0])-1])
                    self.cid=self.foundlist[1][int(args[0])-1].upper()
                  if self.foundlist[0][int(args[0])-1] == "emote":
                    await self.party.me.clear_emote()
                    await self.party.me.set_emote(self.foundlist[1][int(args[0])-1].upper())
                    print(self.foundlist[1][int(args[0])-1])
                    self.eid=self.foundlist[1][int(args[0])-1].upper()
                  if self.foundlist[0][int(args[0])-1] == "emoji":
                    await self.party.me.clear_emote()
                    await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Dances/Emoji/" + self.foundlist[1][int(args[0])-1].upper() + "." + self.foundlist[1][int(args[0])-1].upper())
                    print(self.foundlist[1][int(args[0])-1])
                    self.eid=self.foundlist[1][int(args[0])-1].upper()
                  if self.foundlist[0][int(args[0])-1] == "toy":
                    await self.party.me.clear_emote()
                    await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Toys/" + self.foundlist[1][int(args[0])-1].upper() + "." + self.foundlist[1][int(args[0])-1].upper())
                    print(self.foundlist[1][int(args[0])-1])
                    self.eid=self.foundlist[1][int(args[0])-1].upper()
                  if self.foundlist[0][int(args[0])-1] == "backpack":
                    await self.party.me.set_backpack(self.foundlist[1][int(args[0])-1].upper())
                    print(self.foundlist[1][int(args[0])-1])
                    self.bid=self.foundlist[1][int(args[0])-1].upper()
                  if self.foundlist[0][int(args[0])-1] == "pet":
                    await self.set_pet(self.foundlist[1][int(args[0])-1].upper())
                    print(self.foundlist[1][int(args[0])-1])
                    self.bid=self.foundlist[1][int(args[0])-1].upper()
                  if self.foundlist[0][int(args[0])-1] == "pickaxe":
                    await self.party.me.set_pickaxe(self.foundlist[1][int(args[0])-1].upper())
                    await self.party.me.set_emote("EID_IceKing")
                    print(self.foundlist[1][int(args[0])-1])
                    self.pid=self.foundlist[1][int(args[0])-1].upper()
                  return
                except:
                  return await message.reply('Error\nContact Pirxcy')
                if args[0].isdigit() and not ismesenitem is None:
                  try:
                    self.foundlist=[]
                    self.foundlist.extend([foundlisttype, foundlistid])
                    if self.foundlist[0][int(args[0])-1] == "outfit":
                      await self.party.me.set_outfit(self.foundlist[1][int(args[0])-1].upper())
                      print(self.foundlist[1][int(args[0])-1])
                      self.cid=self.foundlist[1][int(args[0])-1].upper()
                    if self.foundlist[0][int(args[0])-1] == "emote":
                      await self.party.me.clear_emote()
                      await self.party.me.set_emote(self.foundlist[1][int(args[0])-1].upper())
                      print(self.foundlist[1][int(args[0])-1])
                      self.eid=self.foundlist[1][int(args[0])-1].upper()
                    if self.foundlist[0][int(args[0])-1] == "emoji":
                      await self.party.me.clear_emote()
                      await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Dances/Emoji/" + self.foundlist[1][int(args[0])-1].upper() + "." + self.foundlist[1][int(args[0])-1].upper())
                      print(self.foundlist[1][int(args[0])-1])
                      self.eid=self.foundlist[1][int(args[0])-1].upper()
                    if self.foundlist[0][int(args[0])-1] == "toy":
                      await self.party.me.clear_emote()
                      await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Toys/" + self.foundlist[1][int(args[0])-1].upper() + "." + self.foundlist[1][int(args[0])-1].upper())
                      print(self.foundlist[1][int(args[0])-1])
                      self.eid=self.foundlist[1][int(args[0])-1].upper()
                    if self.foundlist[0][int(args[0])-1] == "backpack":
                      await self.party.me.set_backpack(self.foundlist[1][int(args[0])-1].upper())
                      print(self.foundlist[1][int(args[0])-1])
                      self.bid=self.foundlist[1][int(args[0])-1].upper()
                    if self.foundlist[0][int(args[0])-1] == "pet":
                      await self.set_pet(self.foundlist[1][int(args[0])-1].upper())
                      print(self.foundlist[1][int(args[0])-1])
                      self.bid=self.foundlist[1][int(args[0])-1].upper()
                    if self.foundlist[0][int(args[0])-1] == "pickaxe":
                      await self.party.me.set_pickaxe(self.foundlist[1][int(args[0])-1].upper())
                      await self.party.me.set_emote("EID_IceKing")
                      print(self.foundlist[1][int(args[0])-1])
                      self.pid=self.foundlist[1][int(args[0])-1].upper()
                    return
                  except:
                    return await message.reply('Error\nContact Pirxcy')
          except:
            pass
        
            ismesjaitem = await is_itemname("ja", message.content)
            if ismesjaitem[0] == "True":
              if len(ismesjaitem[1]) > 29:
                return await message.reply("見つかったアイテムが多すぎます " + str(len(ismesjaitem[1])))
              itemnum=1
              rep=0
              foundlistid=[]
              foundlisttype=[]
              while True:
                try:
                  if ismesjaitem[3][rep] == "outfit":
                    await self.party.me.set_outfit(ismesjaitem[1][rep].upper())
                    await message.reply(str(itemnum) + ' スキン:' + ismesjaitem[2][rep])
                    print('スキン:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
        
              rep=0
              while True:
                try:
                  if ismesjaitem[3][rep] == "emote":
                    await self.party.me.set_emote(ismesjaitem[1][rep].upper())
                    await message.reply(str(itemnum) + ' エモート:' + ismesjaitem[2][rep])
                    print('エモート:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
        
              rep=0
              while True:
                try:
                  if ismesjaitem[3][rep] == "emoji":
                    await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Dances/Emoji/" + ismesjaitem[1][rep].upper() + "." + ismesjaitem[1][rep].upper())
                    await message.reply(str(itemnum) + ' エモート:' + ismesjaitem[2][rep])
                    print('エモート:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
        
              rep=0
              while True:
                try:
                  if ismesjaitem[3][rep] == "toy":
                    await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Toys/" + ismesjaitem[1][rep].upper() + "." + ismesjaitem[1][rep].upper())
                    await message.reply(str(itemnum) + ' エモート:' + ismesjaitem[2][rep])
                    print('エモート:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
        
              rep=0
              while True:
                try:
                  if ismesjaitem[3][rep] == "backpack":
                    await self.party.me.set_emote(ismesjaitem[1][rep].upper())
                    await message.reply(str(itemnum) + ' バッグ:' + ismesjaitem[2][rep])
                    print('バッグ:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
        
              rep=0
              while True:
                try:
                  if ismesjaitem[3][rep] == "pet":
                    await self.set_pet(ismesjaitem[1][rep])
                    await message.reply(str(itemnum) + ' バッグ:' + ismesjaitem[2][rep].upper())
                    print('バッグ:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
        
              rep=0
              while True:
                try:
                  if ismesjaitem[3][rep] == "pickaxe":
                    await self.party.me.set_pickaxe(ismesjaitem[1][rep].upper())
                    await message.reply(str(itemnum) + ' ツルハシ:' + ismesjaitem[2][rep])
                    print('ツルハシ:' + ismesjaitem[1][rep])
                    foundlistid.append(ismesjaitem[1][rep])
                    foundlisttype.append(ismesjaitem[3][rep])
                    itemnum=itemnum+1
                    rep=rep+1
                except IndexError:
                  break
              if len(ismesjaitem[1]) > 1:
                await message.reply('数字を入力することでそのスキンに設定します')
                return
                
                ismesenitem = await is_itemname("en", message.content)
                if ismesenitem[0] == "True":
                    if len(ismesenitem[1]) > 29:
                        return await message.reply("見つかったアイテムが多すぎます " + str(len(ismesenitem[1])))
                    itemnum=1
                    rep=0
                    foundlistid=[]
                    foundlisttype=[]
                    while True:
                        try:
                            if ismesenitem[3][rep] == "outfit":
                                await self.party.me.set_outfit(ismesenitem[1][rep].upper())
                                await message.reply(str(itemnum) + ' スキン:' + ismesenitem[2][rep])
                                print('スキン:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
        
                    rep=0
                    while True:
                        try:
                            if ismesenitem[3][rep] == "emote":
                                await self.party.me.set_emote(ismesenitem[1][rep].upper())
                                await message.reply(str(itemnum) + ' エモート:' + ismesenitem[2][rep])
                                print('エモート:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
        
                    rep=0
                    while True:
                        try:
                            if ismesenitem[3][rep] == "emoji":
                                await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Dances/Emoji/" + ismesenitem[1][rep].upper() + "." + ismesenitem[1][rep].upper())
                                await message.reply(str(itemnum) + ' エモート:' + ismesenitem[2][rep])
                                print('エモート:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
        
                    rep=0
                    while True:
                        try:
                            if ismesenitem[3][rep] == "toy":
                                await self.party.me.set_emote("/Game/Athena/Items/Cosmetics/Toys/" + ismesenitem[1][rep].upper() + "." + ismesenitem[1][rep].upper())
                                await message.reply(str(itemnum) + ' エモート:' + ismesenitem[2][rep])
                                print('エモート:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
        
                    rep=0
                    while True:
                        try:
                            if ismesenitem[3][rep] == "backpack":
                                await self.party.me.set_emote(ismesenitem[1][rep].upper())
                                await message.reply(str(itemnum) + ' バッグ:' + ismesenitem[2][rep])
                                print('バッグ:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
        
                    rep=0
                    while True:
                        try:
                            if ismesenitem[3][rep] == "pet":
                                await self.set_pet(ismesenitem[1][rep])
                                await message.reply(str(itemnum) + ' バッグ:' + ismesenitem[2][rep].upper())
                                print('バッグ:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
        
                    rep=0
                    while True:
                        try:
                            if ismesenitem[3][rep] == "pickaxe":
                                await self.party.me.set_pickaxe(ismesenitem[1][rep].upper())
                                await message.reply(str(itemnum) + ' ツルハシ:' + ismesenitem[2][rep])
                                print('ツルハシ:' + ismesenitem[1][rep])
                                foundlistid.append(ismesenitem[1][rep])
                                foundlisttype.append(ismesenitem[3][rep])
                                itemnum=itemnum+1
                            rep=rep+1
                        except IndexError:
                            break
                    if len(ismesenitem[1]) > 1:
                        await message.reply('数字を入力することでそのスキンに設定します')
                    return
                if self.partyenable == False:
                    return

        self.prevmes = content

  

#bot = MyBot()
#bot.run()
Thread(target=app.run,args=("0.0.0.0",8080)).start()
Thread(target=MyBot().run, args=()).run()