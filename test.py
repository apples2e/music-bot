from pydoc import source_synopsis
from xmlrpc import client
import discord
from discord.ext import commands
from idna import valid_contextj
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from discord.utils import get
from discord import FFmpegPCMAudio
import bs4
import asyncio
import time

bot = commands.Bot(command_prefix=';;')
clint = discord.Client()

user = []
musictitle = []
song_queue = []
musicnow = []

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    options = Options()
    options.add_argument("headless")

    service = Service("D:\discordbotcode\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"https://www.youtube.com/results?search_query=" + msg + "+lyrics")

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]'))
        )

        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        music = entireNum.text.strip()

        musictitle.append(music)
        musicnow.append(music)
        test1 = entireNum.get('href')
        url = 'https://www.youtube.com' + test1
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']

        return music, URL

    except:
        return None

    finally:
        driver.quit()

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())

@bot.event
async def on_ready():
    print('다음으로 로그인합니다!')
    print(bot.user.name)
    print('봇이 성공적으로 온라인으로 전환되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("어쩔티비"))

@bot.command()
async def 연결(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        print("누군가가 연결 명령어를 사용함")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성채널에 들어가서 해라.")

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("너가 들어가있는 음성 채널에서 이미 나왔는데?")

@bot.command()
async def URL(ctx, *, url):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        print("누군가가 연결 명령어를 사용함")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성채널에 들어가서 해라.")

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed=discord.Embed(title="노래 재생", description="현재 " + url + "을(를) 재생하고 있습니다.", color=0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")

@bot.command()
async def 재생(ctx, *, msg):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        print("누군가가 연결 명령어를 사용함")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성채널에 들어가서 해라.")

    if not vc.is_playing():
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        options = Options()
        options.add_argument('headless')

        service = Service("D:\discordbotcode\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.youtube.com/results?search_query=" + msg + "+lyrics")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]'))
            )

            source = driver.page_source
            bs = bs4.BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            entireText = entireNum.text.strip()
            musicurl = entireNum.get('href')
            url = 'https://www.youtube.com' + musicurl

            musicnow.insert(0, entireText)
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            await ctx.send(embed=discord.Embed(title="노래가 재생 중", description="현재 " + entireText + "을(를) 재생하고 있습니다.",
                                               color=0x00ff00))
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

        except:
            await ctx.reply("시간이 초과되었습니다! 다시 시도하세요.", mention_author=False)

        finally:
            driver.quit()

    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("재생중인 노래가 있어서" + result + "을(를) 대기열에 추가했어요.")
       

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed=discord.Embed(title="노래가 성공적으로 일시정지됨", description=musicnow[0] + "을(를) 성공적으로 일시 정지 하였습니다.",
                                           color=0x00ff00))
    else:
        await ctx.send("지금은 노래가 재생되지 않네요.")


@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
        await ctx.send("지금은 노래가 재생되지 않네요.")
    else:
        await ctx.send(
            embed=discord.Embed(title="노래가 성공적으로 다시 플레이됨", description=musicnow[0] + "을(를) 다시 재생했습니다.", color=0x00ff00))

@bot.command()
async def 노래종료(ctx):
    if vc.is_playing():
        vc.stop()
        global number
        number = 0
        await ctx.send(
            embed=discord.Embed(title="노래가 성공적으로 종료됨", description=musicnow[0] + "을(를) 종료했습니다.", color=0x00ff00))
    else:
        await ctx.send("지금은 노래가 재생되고 있지 않음")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되고 있지 않음")
    else:
        await ctx.send(
            embed=discord.Embed(title="지금노래", description="현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color=0x00ff00))

@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어요!")


@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number) - 1]
        del musicnow[int(number) - 1 + ex]

        await ctx.send("성공! 대기열이 정상적으로 삭제되었어요!")
    except:
        if len(list) == 0:
            await ctx.send("대기열 목록에 아무것도 없어 삭제하지 못했어요...\n등록하려면 '?대기열추가' 을(를) 입력하세요!")
        else:
            if len(list) < int(number):
                await ctx.send("이런, 숫자의 범위가 목록개수를 벗어났어요! 범위가 맞게 숫자를 입력해주세요!")
            else:
                await ctx.send("대기열 목록을 삭제하실 숫자(번호) (을)를 입력해 주세요!")


@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무 노래도 등록하지 않으셨군요!\n이제부터 목록을 등록하여 노래를 즐겁게 즐겨보세요!")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])

        await ctx.send(embed=discord.Embed(title="노래목록", description=Text.strip(), color=0x00ff00))


@bot.command()
async def 목록리셋(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(
            embed=discord.Embed(title="목록초기화", description="""등록하셨던 목록을 초기화했어요!\n다시 등록하려면 ';;대기열추가' (을)를 입력하세요!""",
                                color=0x00ff00))
    except:
        await ctx.send("아직 아무 노래도 등록하지 않으셨어요...\n이제부터 목록을 등록하여 노래를 즐겁게 즐겨보세요!")


@bot.command()
async def 목록재생(ctx):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if len(user) == 0:
        await ctx.send("아직 아무 노래도 등록하지 않으셨군요!\n목록 등록은 ';;대기열추가' 로 할 수 있어요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("다른 노래가 재생되고 있군요! 멈추고 다시 시도하세요.")

bot.run('OTQ3MDg0NjczMzEyNTIyMjUx.YhoHVg.i91ZiEeWPspGhrfL_WsBsMFZnX8')