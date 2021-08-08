import discord
import re
import タイムアウト
import asyncio
import ポーカー
import ガチャ
import dj
import 通話作成部屋
import メンバーキック
from discord.ext import tasks
from datetime import datetime
#import pya3rt
Token = 'ODUxMTQyMDQzNDA4NTMxNTMy.YLz9zA.CnFs0nGIYPNCEQdmbvlbZKzIP98' #botトークン
client = discord.Client(intents = discord.Intents.all())## 接続に必要なオブジェクトを生成
違反者リスト= []
ボットいじる部屋 = 825631578918748201
鯖 = client.get_guild(836208908786729000)
新規チャンネル = []
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('β.py起動したよはげ')
    await client.change_presence(activity=discord.Game("botです"))


class vc:
    def __init__(self, member_id,vc_id,role_id,txt_id):
        self.member_id = member_id
        self.vc_id = vc_id
        self.role_id = role_id
        self.txt_id = txt_id

@client.event
async def on_voice_state_update(member,before,after):
    if member.bot:#botだったら抜ける
        return
    tc = client.get_channel(856211499156242473)
    if before.channel == None and member.guild.id == 855821246745542696:
        if client.user.id in [i.id for i in member.voice.channel.members]:#通話にボットがいるかどうかの判定
            if member.guild.voice_client.is_playing():#もし曲が流れてたら止める
                member.guild.voice_client.stop()
        else:    
            await member.voice.channel.connect()
        member.guild.voice_client.play(discord.FFmpegPCMAudio(r'音楽リスト\学び舎の風景.mp3'))
        #msg = f"**{member.name}さん**が通話に入ってきたよ"
        #await tc.send(embed=discord.Embed(description=msg))
        #await member.guild.voice_client.disconnect()

    通話部屋 = client.get_channel(858724779913117716)
    チャット = client.get_channel(836208908786729003)
    global 新規チャンネル
    guild = member.guild
    if member.voice is not None:#通話作成部屋に入ったら通話チャンネルと新規ロールを作る
        if 通話部屋 == member.voice.channel and before.channel != after.channel:
            仮新規チャンネル = await member.guild.create_voice_channel(name=f"{member.name}のお部屋",user_limit=99,category=member.guild.categories[2],limit=99)
            await member.move_to(仮新規チャンネル)
            role = await guild.create_role(name=f"{member.voice.channel.id}")
            await member.add_roles(role)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel(f'{member.name}の秘密の部屋', overwrites=overwrites,category=member.guild.categories[2])
            新規チャンネル += [vc(member.id,仮新規チャンネル.id,role.id,channel.id)]
            #await チャット.send(f"{member.name}が通話入った")
        for i in 新規チャンネル:
            if i.vc_id == after.channel.id:
                await member.add_roles(guild.get_role(i.role_id))
    if after.channel != before.channel and before.channel is not None: #通話抜けたらロールを外す 
        for i in 新規チャンネル:
            if i.vc_id == before.channel.id:
                await member.remove_roles(guild.get_role(i.role_id))
        #最後の1人が通話を抜けた時
        for channel情報 in 新規チャンネル:
            vc部屋 = guild.get_channel(channel情報.vc_id)
            txt部屋 = guild.get_channel(channel情報.txt_id)
            role_id = guild.get_role(channel情報.role_id)
            if vc部屋 is None:
                continue
            if not vc部屋.members:
                await vc部屋.delete()
                await txt部屋.delete()
                await role_id.delete()
                for i in 新規チャンネル:
                    if i.vc_id == before.channel.id:
                        新規チャンネル.remove(i)
                        return
    
    '''
    if after.channel is not before.channel and before.channel is not None:
        if before.channel.id in [852805916683534377, 852811126961864714]:
            return
        await before.channel.delete()
        #await 通話作成部屋.通話作成(member,before,after,チャット,通話部屋)
        '''
'''
@client.event
async def on_typing(channel,user,when):
    await channel.send(f"{user.name}がなんか文字を打ってるぞｗｗｗｗｗ{when}{channel}")
    
@client.event
async def on_message_delete(message):
    if message.author.bot:
        return
    await message.channel.send(f"**{message.author.name}**さん、あなた今メッセージ削除しましたよね？あれれ？{message.content}って言いましたよね？")
 

@client.event
async def on_member_update(before,after):
    いじる部屋 = client.get_channel(850349987954425927)
    if before.status != after.status:
        await いじる部屋.send(f"**{after.name}**が**{before.status}**状態から**{after.status}**状態に変更したね👀")

'''
@client.event
async def on_message(message):
    if message.author.bot:
        #botだったら抜ける
        return

    if re.search("死にたい",message.content):
        await message.reply("こころの健康相談統一ダイヤル\n時間: 都道府県によって異なります\n**0570-064-556**")
    
    if message.content == "dj": #djロールを作る
        await dj.dj_on(message)
            
    if message.content == "djdel": #djロールを作る
        await dj.dj_off(message)
        """
    if message.content == "abv": #メンバーキック
        if not message.author.guild_permissions.administrator:
            message.channel.send("管理者じゃありませんねはげ")
            return
        guild = message.guild

        for member in guild.members:
            if member.guild_permissions.administrator:
                continue
            if not member.bot:
                await member.kick(reason=None)
                await message.channel.send(member)
    if re.match("tesuto",message.content):#ed曲流す
        if message.author.voice is None:
            await message.reply("通話入ってないから音楽かけれません")
            return
        if client.user.id in [i.id for i in message.author.voice.channel.members]:#通話にボットがいるかどうかの判定
                if message.guild.voice_client.is_playing():#もし曲が流れてたら止める
                    message.guild.voice_client.stop()
        else:    
            await message.author.voice.channel.connect()
        await message.channel.send("サーバー削除まで、")
        for a in range(5,0,-1):
            await asyncio.sleep(1)
            await message.channel.send(a)
        await asyncio.sleep(1)
        await message.channel.send("ばいばーい")
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(r"音楽集/ed.mp3"), volume=0.05)
        message.guild.voice_client.play(source)
        await asyncio.sleep(10)
        guild = message.guild
        for member in guild.members:
            if member.guild_permissions.administrator:
                continue
            if not member.bot:
                await member.kick(reason=None)
                await message.channel.send(member)
        return
        """
    if re.search("死ね|[はハﾊ][げゲｹﾞ]|表示", message.content):#タイムアウト.py
            global 違反者リスト
            リスト判定 = False
            t = None

            if re.search("死ね|[はハﾊ][げゲｹﾞ]", message.content): 
                for i in 違反者リスト:
                    if message.author.id == i.userid:
                        i.違反回数 += 1
                        リスト判定 = True
                        t = i
                if not リスト判定:
                    t = タイムアウト.タイムアウト(message.author.id, 1)
                    違反者リスト += [t]
                await t.タイムアウト(message)
                return
            if re.search("表示", message.content):
                await タイムアウト.タイムアウト.表示(message,違反者リスト,client)
                return
    if message.content == "てすと":
        user = client.get_user(707486020928798782)
        for a in range(101):
            await message.channel.send("はげ")
        #await message.reply(embed=discord.Embed(description=user.name))
    if re.search("ポーカー", message.content):
            await ポーカー.ポーカー起動(message)

    if message.content == "ガチャ":
        await ガチャ.ガチャ(message,client)
    
    if message.content == '消す':
        
        while True:
            if message.author.guild_permissions.administrator:
                channela = client.get_channel(message.channel.id)
                await channela.purge(limit=None)
                await message.channel.send("終わりました")
                await message.delete(delay=30)
                return

            else:
                await message.reply("あなた管理者じゃないのでメッセージ消せません")
                break

        if message.author.bot:
            return
'''
@tasks.loop(seconds=1)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M:%S')
    channel = client.get_channel(654290509505888269)#本番(654290509505888269)
    vchannel = client.get_channel(810401198238334986)#本番(810401198238334986)
    if now == '23:00:00':
        await channel.send(embed=discord.Embed(description="サーバー削除まで残り1時間となりました"))
    if now == '23:30:00':
        await channel.send(embed=discord.Embed(description="サーバー削除まで残り30分となりました")) 
    if now == '23:59:00':
        await channel.send(embed=discord.Embed(description="サーバー削除まで残り1分となりました"))
    if now == '23:59:50': 
        await vchannel.connect()
        await channel.send(embed=discord.Embed(description="サーバー削除まで、"))
        for a in range(15,0,-1):
            await asyncio.sleep(1)
            await channel.send(a)
        await asyncio.sleep(1)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(r"音楽集/ed.mp3"), volume=0.05)
        channel.guild.voice_client.play(source)
        await channel.send(embed=discord.Embed(title="すべての機能を停止いたします。\n俺のサーバーをご愛顧いただき、誠にありがとうございました。"))
        await asyncio.sleep(63)
        guild = channel.guild
        for member in guild.members:
            if member.guild_permissions.administrator:
                continue
            if not member.bot:
                await member.kick(reason=None)
                #await channel.send(f"{member}を消しました")
        return

#ループ処理実行
loop.start()

# Botの起動とDiscordサーバーへの接続
#('%H:%M')
'''
# Botの起動とDiscordサーバーへの接続
client.run(Token)
