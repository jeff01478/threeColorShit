import discord
from discord.ext import commands
import json
import pytz
import asyncio
from datetime import datetime, timedelta
from pypinyin import pinyin, Style

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix= "/", intents=intents)
channels = 954950144686710837
threeColorTemp = "good"

# 將 UTC 時間轉換為台灣時間
def utc_to_taiwan(utc_dt):
    taiwan_offset = timedelta(hours=8)  # 台灣時區 UTC+8
    taiwan_dt = utc_dt + taiwan_offset
    return taiwan_dt

#將文字轉換為注音
def get_zhuyin(text):
    zhuyin_list = pinyin(text, style=Style.BOPOMOFO)
    zhuyin = ''.join([p[0] for p in zhuyin_list])
    return zhuyin

def add_violation_point(member):
    point = 1
    with open("violation_points.json", "r", encoding="utf8") as f:
        member_points = json.load(f)
        f.close()
    if not(member in member_points):
        member_points[member] = 1
    else:
        member_points[member] += 1
        point = member_points[member]
        if point >= 3:
            member_points[member] = 0
    with open("violation_points.json", "w", encoding="utf8") as f:
        json.dump(member_points, f)
        f.close()
    return point

@bot.event
async def on_ready():
    print(">> Bot is online <<")
    user_id = bot.get_user(1209387395016040448)
    print(user_id)
    channel = bot.get_channel(channels)
    await channel.send("三色豆警察成功啟動")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        if "/" in message.content[0]:
            await bot.process_commands(message)
            return
    except:
        print("")
    #await message.author.edit(send_messages=False)
    channel = bot.get_channel(message.channel.id)
    #await message.channel.set_permissions(message.author, send_messages=False)
    msg = message.content
    msg = get_zhuyin(msg)
    msg = msg.replace(" ","").replace("ㄕ","ㄙ").replace("ㄔ","ㄙ").replace("ㄘ","ㄙ").replace("🟩","🟢").replace("🟧","🟠").replace("🟨","🟡").replace("🥕", "🟠").replace("🫛", "🟢").replace("🌽", "🟡").replace("🔶", "🟠")
    # if str(message.author.id) == "609563252443316258":
    #     await message.add_reaction("<:threeColorShit:1209517222834217010>")
    if "ㄙㄢㄙㄜˋㄉㄡˋ" in msg or "ㄙㄢㄐㄧㄉㄡˋ" in msg:
        print("三色豆警告")
        pic = discord.File('pic/三色豆廚餘.png')
        await message.add_reaction("<:threeColorShit:1209517222834217010>")
        await channel.send(f"{message.author.mention}三色豆就該待在廚餘桶")
        await channel.send(file= pic)
    global threeColorTemp
    threeColorSet = {'🟢', '🟡', '🟠'}
    point = 0
    member = message.author.mention
    if threeColorSet.intersection(msg) == threeColorSet:
        await message.add_reaction("<:threeColorShit:1209517222834217010>")
        await channel.send(f"{message.author.mention}記違規1點")
        point = add_violation_point(member)
    elif "🟢" in msg or "🟡" in msg or "🟠" in msg:
        threeColorTemp += msg
        if threeColorSet.intersection(threeColorTemp) == threeColorSet:
            await message.add_reaction("<:threeColorShit:1209517222834217010>")
            await channel.send(f"{message.author.mention}記違規1點")
            point = add_violation_point(member)
            threeColorTemp = ""
    else:
        threeColorTemp = ""

    if point >= 3:
        await channel.send(f"臭雞雞成員{member}累積違規點10點，送入600監獄")
        await message.channel.set_permissions(message.author, send_messages=False)
        await asyncio.sleep(600)
        await message.channel.set_permissions(message.author, send_messages=True)
    if "🥟" in msg:
        await message.add_reaction("🥟")
    
# @bot.event
# async def on_reaction_add(reaction, user):
#     print(reaction)
#     print(user)

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = guild.system_channel
    await channel.send(f"Hi! {member.mention} 希望你不會喜歡三色豆")

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = guild.system_channel
    await channel.send(f"{member.mention} 你這個臭雞雞")

@bot.event
async def on_message_edit(bf, af):
    bf_content = bf.content
    af_content = af.content
    bf_time = utc_to_taiwan(bf.created_at).strftime("%Y-%m-%d %H:%M:%S")
    af_time = utc_to_taiwan(af.edited_at).strftime("%Y-%m-%d %H:%M:%S")
    member = af.author.mention

    channel = bot.get_channel(af.channel.id)
    await channel.send(f"此訊息已被編輯\n編輯者: {member}\n編輯前: {bf_content} {bf_time}\n編輯後: {af_content} {af_time}")
    
    print(f"{member}: {bf_content} {bf_time} -> {af_content} {af_time}")

@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    del_msg = message.content
    del_time = utc_to_taiwan(datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")
    member = message.author.mention

    channel = bot.get_channel(message.channel.id)
    await channel.send(f"此訊息已被刪除\n原訊息者: {member}\n刪除訊息: {del_msg} {del_time}")
    
    print(f"此訊息已被刪除\n刪除者: {member}\n刪除訊息: {del_msg} {del_time}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"{round(bot.latency*1000)} ms")

@bot.command()
async def 三色豆風險(ctx):
    risk = open('三色豆廢文/三色豆風險.txt', 'r', encoding='utf8')
    await ctx.send(risk.read())
    risk.close()

@bot.command()
async def 違規點數(ctx):
    good = "臭雞雞聯盟違規點紀錄:\n"
    with open("violation_points.json", "r") as f:
        member_points = json.load(f)
        f.close()
    for i in member_points:
        good += f"{i}　{member_points[i]}點\n"
    await ctx.send(good)

bot.run(jdata['TOKEN'])
