import os
import datetime
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# タイムゾーンを日本（JST）に設定
JST = datetime.timezone(datetime.timedelta(hours=9))

intents = discord.Intents.default()
intents.message_content = True  # メッセージの読み取り権限
intents.voice_states = True     # ボイチャの入退室検知権限
bot = commands.Bot(command_prefix="!", intents=intents)

# ==================== 【重要】チャンネルIDの設定 ====================
# 💡 お祝いメッセージや、ボイチャ通知を流したいテキストチャンネルのIDに書き換えてください。
BIRTHDAY_CHANNEL_ID = https://discord.com/channels/1550919186170126496/1550919690099097772  # 誕生日お祝いを流すチャンネル
VC_NOTIFY_CHANNEL_ID = https://discord.com/channels/1550919186170126496/1550922301539618846 # ボイチャ通知を流すチャンネル
====================================================================
# 誕生日リスト（月日: メッセージ）
BIRTHDAYS = {
    "10/27": "なつめさん、誕生日おめでとうございます",
    "06/03": "くれはさん、誕生日おめでとうございます",
    "06/10": "ちゃこさん、誕生日おめでとうございます",
    "08/27": "タクトさん、誕生日おめでとうございます",
    "05/29": "トバリさん、誕生日おめでとうございます"
}

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")
    # 定期チェックタスクを開始
    if not check_birthday.is_running():
        check_birthday.start()
      
# ----------------------------------------------------------------
# 機能1: 毎日0:00に誕生日メッセージを自動送信するタスク
# ----------------------------------------------------------------
@tasks.loop(minutes=1)  # 1分ごとに現在時刻をチェック
async def check_birthday():
    now = datetime.datetime.now(JST)

# 夜中の「0時00分」になった瞬間に実行
    if now.hour == 0 and now.minute == 0:
        # 今日の日付を「MM/DD」の形式にする（例: 10/27）
        today_str = now.strftime("%m/%d")

# 誕生日リストに今日の日付があるかチェック
        if today_str in BIRTHDAYS:
            channel = bot.get_channel(BIRTHDAY_CHANNEL_ID)
            if channel:
                message = BIRTHDAYS[today_str]
                await channel.send(message)
                print(f"【0:00通知】誕生日祝いを送信しました: {today_str}")

# ----------------------------------------------------------------
# 機能2: 誰かがボイスチャット（VC）に参加したら通知するイベント
# ----------------------------------------------------------------
@bot.event
async def on_voice_state_update(member, before, after):
    # Bot自身の動きは無視
    if member.bot:
        return

    # before.channel が None で、after.channel が None ではない場合 ＝ 「VCに参加した」
    if before.channel is None and after.channel is not None:
        channel = bot.get_channel(VC_NOTIFY_CHANNEL_ID)
        if channel:
            # 参加した人の名前（ニックネームがあればそれを優先、なければユーザー名）
            display_name = member.display_name
            await channel.send(f"【VC通知】{display_name} さんがボイスチャットに参加しました。")
            print(f"ボイチャ参加通知を送信: {display_name}")

# --- UptimeRobot用のWebサーバー設定（Renderが寝るのを防ぐ用） ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is perfectly running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 起動
keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
