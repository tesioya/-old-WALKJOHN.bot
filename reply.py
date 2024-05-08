# 環境変数、Botトークンを取得
import env

# import area
from googletrans import Translator

import discord
import yt_dlp
import asyncio
#import ffmpeg

# global area
translator = Translator()

song_num = 1
play_now = 0

mixlst = []
title = "title"



# ボイチャ接続コマンド
async def join_vc(ctx):
    bots_vc = ctx.guild.voice_client
    # メッセージ送信者がボイスチャンネルにいない場合
    if ctx.author.voice is None:
        await ctx.channel.send("ボイスチャンネルに入ってからコマンドを入力してください")
    # 送信者がボイチャIN中かつ、ボット自身が接続中でない場合のみ接続処理
    else:
        if bots_vc is None:
            await ctx.author.voice.channel.connect()
        else:
            pass


# ボイチャ退出コマンド
async def leave_vc(ctx):
    # 現在VCに入っているか確認する
    bots_vc = ctx.guild.voice_client
    if bots_vc is None:  # VCに入っていない場合
        await ctx.channel.send("botはボイスチャンネル内にいません")
    # VCに入っている場合は処理を継続して退出する
    await bots_vc.disconnect()

# スキップコマンド
async def skip(ctx):
    bots_vc = ctx.guild.voice_client
    if bots_vc and bots_vc.is_playing():
        bots_vc.stop()
        play_now += 1
        await asyncio.sleep(1)
        await play_loop
    else:
        await ctx.channel.send("スキップする曲がありません")

# 再生中の曲のURL表示コマンド
async def now_info(ctx):
    global mixlst
    global play_now
    try:
        await ctx.channel.send(mixlst[play_now][2])
    except:
        await ctx.channel.send("URL情報の取得に失敗しました")

# プレイリスト全体の表示    
async def lst_info(ctx):
    global mixlst
    global play_now
    try:
        len_lst = int(len(mixlst))-int(play_now)
        for i in range( 1 , len_lst+1 ):
            await ctx.channel.send(str(i) + ":" + mixlst[ i + play_now - 1][1])
    except:
        print("プレイリストの表示に失敗しました")



# youtube再生コマンド
async def play_loop(message):
    global mixlst
    global play_now

    bots_vc = message.guild.voice_client
    while True:
        if play_now >= len(mixlst):
            # await message.channel.send("プレイリストを全て再生しました")
            break
        # mp3のパスを指定して再生
        mp3 = mixlst[play_now][0] + ".mp3"
        song = discord.FFmpegPCMAudio(mp3) 
        
        bots_vc.play(song, after=lambda e: asyncio.create_task(play_next(message)))# by GPT

        play_now += 1

        await asyncio.sleep(1)
        
# 再生が終わったら次の曲に移行する
async def play_next(message):
    global mixlst
    global play_now

    play_now += 1
    if play_now < len(mixlst):
        await play_loop(message)    



# プレイリストに曲を追加するコマンド
async def add_playlist(message):
    global mixlst
    global song_num
    global title
    bots_vc = message.guild.voice_client
    
    if message.author.voice is None:
        await message.channel.send("ボイスチャンネルに入ってからコマンドを入力してください")
    else:
        await join_vc(message)
        # 先頭のqを除いたURL抽出、生成mp3パスを指定、保存作業
        yt_url = message.content[1:]
        output_path = "save_mp3/" + str(song_num)
        ffmpeg_path = env.ffmpeg_path # local test

        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_path,
                "ffmpeg_location": ffmpeg_path,  # local test
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])

            res = ydl.extract_info(yt_url)
            title = res["title"]

            mixlst.append([output_path, title, yt_url])
            song_num += 1
            
        # YoutubeライブのURLとか１時間越えとか、そもそも何かが間違ってると失敗する
        except:
            await message.channel.send("URL[" + yt_url + "]の読み込みに失敗しました")

        #現在音楽を再生中でないなら再生する、再生中であればパス
        if bots_vc and bots_vc.is_playing():
            pass
        else:
            await play_loop(message)



# ! から始まる言葉を日本語に翻訳して返す
async def translate(message):
    comment = message.channel.send

    # 先頭の!を除いた文字を取得
    to_translate = message.content[1:]

    # 例外処理のため
    try:
    # メッセージの言語を判別
        lang = translator.detect(to_translate).lang

    # 日本語の場合は英語に翻訳
        if lang == "ja":
            translated = translator.translate(to_translate, src=lang, dest="en").text
            await comment(str(translated))

        # 日本語以外の言語の場合は、日本語に翻訳
        else:
            translated = translator.translate(to_translate, src=lang, dest="ja").text
            await comment(str(translated))

    # 翻訳ミス(だいたいlang判定でミスる)の場合に出力
    except:
        await comment("その言葉は翻訳できません")


# # から始まる特定の言葉に対する挨拶リスト ここは思い出ゾーンです
async def greeting(message):

    if message.content.startswith("#おは"):
        await message.channel.send("おはようございますワン")

    elif message.content.startswith("#cat"):
        await message.channel.send("ぼくはねこじゃないワン")

    elif message.content.startswith("#dog"):
        await message.channel.send("犬といえばジョンだワン")

    else:
        await message.channel.send("そんな言葉は習ってないワンよ")