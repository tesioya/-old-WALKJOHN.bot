import os

# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv

# 環境変数を参照
load_dotenv()

BOT_TOKEN: str = os.getenv(
    "BOT_TOKEN",
    "ボットトークンは機密情報なので載せられないよ",
)

ffmpeg_path = r"ffmpeg.exeのローカルアドレス"