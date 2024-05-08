import discord
from discord.ext import commands

# 環境変数、Botトークンを取得
import env

# 返答プログラム及び必要なライブラリ
import reply

# インテント確認
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Botログイン完了時にターミナルにログイン報告を出力
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(description="ボイスチャンネルに参加")
async def join(ctx):
    await reply.join_vc(ctx)


@bot.slash_command(description="ボイスチャンネルから退出")
async def leave(ctx):
    await reply.leave_vc(ctx)


@bot.slash_command(description="再生中の曲をスキップ")
async def skip(ctx):
    await reply.skip(ctx)


@bot.slash_command(description="再生中の曲のURLを表示")
async def now(ctx):
    await reply.now_info(ctx)


@bot.slash_command(description="プレイリスト表示")
async def list(ctx):
    await reply.lst_info(ctx)



@bot.event
async def on_message(message):
    if message.content.startswith("q"):
        await reply.add_playlist(message)

    elif message.content.startswith("!"):
        await reply.translate(message)

    elif message.content.startswith("#"):
        await reply.greeting(message)



bot.run(env.BOT_TOKEN)
