
from ast import Str
from collections import UserString
from http import client
from operator import mod
from random import choices, random, randrange
from secrets import choice
from turtle import up
from typing import Final, final
import discord
from discord.ext import commands
import json
import os

os.chdir("D:\\Bot discord\\Bò bập bùng")


#intents
intents = discord.Intents.all()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix="bo", intents=intents)

#Events (hành động sự kiện)
@client.event
async def on_ready():
    activity = discord.Game(name= "trái tim những con nghiện", type=3)
    await client.change_presence(status= discord.Status.online, activity=activity)
    print("bố m đây!!!")


#Command (lệnh bot)
#bank economy
#lệnh số dư
@client.command()
async def sodu(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"Số dư của {ctx.author.name}!!!", color= discord.Color.blue())
    em.add_field(name="Số dư",value= wallet_amt)
    em.add_field(name="Tài khoản ngân hàng",value= bank_amt)
    await ctx.send(embed = em)

#lệnh cho tiền
@client.command()
async def chotien(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = randrange(1)

    await ctx.send(f"ai đó đã ném vào mặt con đỗ nghèo khỉ {ctx.author.name} {earnings} coins!!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)


#Lệnh rút tiền
@client.command()
async def ruttien(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Vui lòng nhập số dư")
        return
    bal = await update_bank(ctx.author)
    
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Nghèo mà bày đặt rút tiền!!")
        return
    if amount<0:
        await ctx.send("Số dư phải hợp lệ !!!")
        return

    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount,"bank")

    await ctx.send(f"Bạn đã rút {amount} Bof coins!!")

#Lệnh thêm tiền

@client.command()
async def themtien(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Vui lòng nhập số dư")
        return
    bal = await update_bank(ctx.author)
    
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Nghèo mà bày đặt thêm tiền!!")
        return
    if amount<0:
        await ctx.send("Số dư phải hợp lệ !!!")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount,"bank")

    await ctx.send(f"Bạn đã thêm {amount} Bof coins!!")


#bot game
@client.command()
async def slot(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Vui lòng nhập số dư")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Nghèo mà bày đặt nghiện!!")
        return
    if amount<0:
        await ctx.send("Số dư phải hợp lệ !!!")
        return

    final = []
    for i in range(3):
        a = choice(["O", "X", "Y"])

        final.append(a)
    await ctx.send(str(final)) 
    if final[0] == final[1] == final[2]:
        await update_bank(ctx.author, 10*amount)
        await ctx.send(f"U win !!! {10*amount}")
    else:  
        await update_bank(ctx.author, -1*amount)
        await ctx.send("Asian parents said: you failure!!")






#Lệnh gửi tiền
@client.command()
async def nemtien(ctx,member:discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Vui lòng nhập số dư")
        return
    bal = await update_bank(ctx.author)
    
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Nghèo mà bày đặt thêm tiền!!")
        return
    if amount<0:
        await ctx.send("Số dư phải hợp lệ !!!")
        return

    await update_bank(ctx.author, -1*amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"Bạn đã ném {member.name} {amount} Bof coins!!")



#Lệnh gán
async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)
    
    return users


async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal




#lệnh say
@client.command()
async def mqh(ctx):
    await ctx.reply("mqh trap!!!")

@client.command()
async def info(ctx):
    await ctx.reply("hỗn hỗn sau bố m đéo cho tiền")

@client.command()
async def hello(ctx):
    await ctx.reply("Xin chèooo")






client.run('MTAyNTgyNDQwOTY5ODcxNzc4OQ.GVsROz.1CnJVI99ayEpIbTAuhcMKfARs_8wVLEyeSH4VQ')