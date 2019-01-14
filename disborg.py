# Disborg, a custom Discord bot written by Justin Cuozzo / Cosmopath#0001
# This bot makes use of the alpha rewrite version of the discord.py API, as well as various third-party libraries to help commands work.
# Licensed under the GNU GPLv3 open-source license. To learn more about the GNU GPLv3, read the full licensing terms here: https://www.gnu.org/licenses/gpl-3.0.en.html
# Last updated: January 13, 2019

# ------------ #
#     Setup    #
# ------------ #

# Importing necessary libraries
import asyncio
import discord
import geopy
import re
import xkcd
from currency_converter import CurrencyConverter
from discord.ext import commands
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from googletrans import Translator
from random import randint 
from yahoofinancials import YahooFinancials

# Creating objects
bot = commands.Bot(command_prefix='?')
c = CurrencyConverter()
xk = xkcd;
translator = Translator()

# Log-in confirmation to console
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# ------------ #
#   Commands   #
# ------------ #

# Test ping command
@bot.command()
async def ping(ctx):
	await ctx.send('Pong!')

# Dice roll
@bot.command()
async def dice(ctx, dieCount):
	await ctx.send('Ta-da! You rolled a ' + str(randint(1, 6*(int(dieCount)))))

# Distance
@bot.command()
async def distance (ctx, loc1, loc2):	
	geolocator = Nominatim(user_agent="Disborg")
	location1 = geolocator.geocode(loc1)
	location2 = geolocator.geocode(loc2)
	miles = geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).miles
	km = miles*1.609;
	await ctx.send ('The distance between ' + loc1.title() + ' and ' + loc2.title() + ' is ' + str(round(miles, 2)) + ' miles (' + str(round(km, 2)) + ' km)')

# Currency conversion
@bot.command()
async def cur (ctx, amount, cur1, cur2):
	cur1 = cur1.upper()
	cur2 = cur2.upper()
	await ctx.send (amount + " " + cur1 + " = "  + str(round((c.convert(amount, cur1, cur2)), 2)) + " " +  cur2)

# Anonymously PM given user
@bot.command()
async def msg (ctx, user: discord.User, message):
	await user.send(message)
	await ctx.send ('Message to ' + str(user) + ' sent.')

# xkcd puller
@bot.command()
async def xkcd (ctx, comic):
	embed = discord.Embed()
	if (comic == "latest"):
		embed = discord.Embed(title = xk.getLatestComic().getTitle(), description = xk.getLatestComic().getAltText())
		embed.set_image(url=xk.getLatestComic().getImageLink())
	elif (comic == "random"):
		rand = xk.getRandomComic();
		embed = discord.Embed(title = rand.getTitle(), description = rand.getAltText())
		embed.set_image(url=rand.getImageLink())
	else:
		embed = discord.Embed(title = xk.getComic(comic, silent=False).getTitle(), description = xk.getComic(comic, silent=False).getAltText())
		embed.set_image(url=xk.getComic(comic, silent=False).getImageLink())
	await ctx.send(content=None, embed=embed)

# Unit conversions
@bot.command()
async def convert(ctx, amount, unit1, unit2):
	if (unit1 == "cm" and unit2 == "in"):
		resultant = round((float(amount))/2.54, 2)
		await ctx.send(amount + ' centimetres = ' + str(resultant) + ' inches')
	elif (unit1 == "in" and unit2 == "cm"):
		resultant = round((float(amount))*2.54, 2)
		await ctx.send(amount + ' inches = ' + str(resultant) + ' centimetres')
	elif (unit1 == "kg" and unit2 == "lb"):
		resultant = round((float(amount))*2.205, 2)
		await ctx.send(amount + ' kilograms = ' + str(resultant) + ' pounds')
	elif (unit1 == "lb" and unit2 == "kg"):
		resultant = round((float(amount))/2.205, 2)
		await ctx.send(amount + ' pounds = ' + str(resultant) + ' kilograms')
	elif (unit1 == "c" and unit2 == "f"):
		resultant = round((float(amount))*(9/5) + 32, 1)
		await ctx.send(amount + ' degrees Celsius = ' + str(resultant) + ' degrees Fahrenheit')
	elif (unit1 == "f" and unit2 == "c"):
		resultant = round(((float(amount)) - 32) * (5/9), 1)
		await ctx.send(amount + ' degrees Fahrenheit = ' + str(resultant) + ' degrees Celsius')
	elif (unit1 == "miles" and unit2 == "km"):
		resultant = round((float(amount))*1.609, 2)
		await ctx.send(amount + ' miles = ' + str(resultant) + ' kilometres')
	elif (unit1 == "km" and unit2 == "miles"):
		resultant = round((float(amount))/1.609, 2)
		await ctx.send(amount + ' kilometres = ' + str(resultant) + ' miles')

# Translate
@bot.command()
async def translate(ctx, string):
	translated = translator.translate(string)
	await ctx.send(translated.src.upper()+ " to English: " + translated.text)

# Stock price 
@bot.command()
async def stock (ctx, ticker, info):
	yahoo_financials = YahooFinancials(ticker)
	if (info == "current"): 
		await ctx.send(ticker.upper() + " current share price: $" + str(yahoo_financials.get_current_price()))
	if (info == "open"):
		await ctx.send(ticker.upper() + " share price at opening: $" + str(yahoo_financials.get_open_price()))
	if (info == "prevclose"):
		await ctx.send(ticker.upper() + " share priced at previous close: $" + str(yahoo_financials.get_prev_close_price()))
	if (info == "cap"):
		await ctx.send(ticker.upper() + " market cap: $" + str("{:,}".format(yahoo_financials.get_market_cap())))
	if (info == "dailylow"):
		await ctx.send(ticker.upper() + " daily low: $" + str(yahoo_financials.get_daily_low()))
	if (info == "dailyhigh"):
		await ctx.send(ticker.upper() + " daily high: $" + str(yahoo_financials.get_daily_high()))
	if (info == "yearlow"):
		await ctx.send(ticker.upper() + " yearly low: $" + str(yahoo_financials.get_yearly_low()))
	if (info == "yearhigh"):
		await ctx.send(ticker.upper() + " yearly high: $" + str(yahoo_financials.get_yearly_high()))
	if (info == "rev"):
		await ctx.send(ticker.upper() + " total revenue: $" + str("{:,}".format(yahoo_financials.get_total_revenue())))
	if (info == "net"):
		await ctx.send(ticker.upper() + " net income: $" + str("{:,}".format(yahoo_financials.get_net_income())))
	if (info == "op"):
		await ctx.send(ticker.upper() + " operating income: $" + str("{:,}".format(yahoo_financials.get_operating_income())))
	if (info == "profit"):
		await ctx.send(ticker.upper() + " gross profit: $" + str("{:,}".format(yahoo_financials.get_gross_profit())))

# ------------ #
#    Events    #
# ------------ #

# Amazon affiliate auto-add
@bot.event
async def on_message(message):
	if message.author.id != "533881524924186624":
		if "https://www.amazon.com" in message.content.lower():
			regex = re.compile('B[A-Z0-9]{9}')
			result = regex.search(message.content)

			embed = discord.Embed(title="Amazon link converted!", description="Ordering through this referral link gives Gaming For Global Change, a non-profit organization, a small kickback from your order while adding nothing to your overall cost.", color=0x9400D3)
			embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThGU9r2Vi7WLYoTQGuT48UeU0p6hfhsiP75Ubaz0mg3xzgC185')
			embed.add_field(name="Affiliate link:", value="https://www.amazon.com/dp/" + result.group(0) + "/?tag=gfgc-org-20", inline=False)
			await message.channel.send(embed=embed)
			
		if "https://www.amazon.ca" in message.content.lower():
			regex = re.compile('B[A-Z0-9]{9}')
			result = regex.search(message.content)

			embed = discord.Embed(title="Amazon link converted!", description="Ordering through this referral link gives Gaming For Global Change, a non-profit organization, a small kickback from your order while adding nothing to your overall cost.", color=0x9400D3)
			embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThGU9r2Vi7WLYoTQGuT48UeU0p6hfhsiP75Ubaz0mg3xzgC185')
			embed.add_field(name="Affiliate link:", value="https://www.amazon.ca/dp/" + result.group(0) + "/?tag=gfgc_org-20", inline=False)
			await message.channel.send(embed=embed)
			
		if "https://www.amazon.co.uk" in message.content.lower():
			regex = re.compile('B[A-Z0-9]{9}')
			result = regex.search(message.content)

			embed = discord.Embed(title="Amazon link converted!", description="Ordering through this referral link gives Gaming For Global Change, a non-profit organization, a small kickback from your order while adding nothing to your overall cost.", color=0x9400D3)
			embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThGU9r2Vi7WLYoTQGuT48UeU0p6hfhsiP75Ubaz0mg3xzgC185')
			embed.add_field(name="Affiliate link:", value="https://www.amazon.co.uk/dp/" + result.group(0) + "/?tag=gfgcorg07-21", inline=False)
			await message.channel.send(embed=embed)
			
		if "https://www.amazon.de" in message.content.lower():
			regex = re.compile('B[A-Z0-9]{9}')
			result = regex.search(message.content)

			embed = discord.Embed(title="Amazon link converted!", description="Ordering through this referral link gives Gaming For Global Change, a non-profit organization, a small kickback from your order while adding nothing to your overall cost.", color=0x9400D3)
			embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThGU9r2Vi7WLYoTQGuT48UeU0p6hfhsiP75Ubaz0mg3xzgC185')
			embed.add_field(name="Affiliate link:", value="https://www.amazon.de/dp/" + result.group(0) + "/?tag=gfgcorg-21", inline=False)
			await message.channel.send(embed=embed)
			
		if "https://www.amazon.es" in message.content.lower():
			regex = re.compile('B[A-Z0-9]{9}')
			result = regex.search(message.content)

			embed = discord.Embed(title="Amazon link converted!", description="Ordering through this referral link gives Gaming For Global Change, a non-profit organization, a small kickback from your order while adding nothing to your overall cost.", color=0x9400D3)
			embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThGU9r2Vi7WLYoTQGuT48UeU0p6hfhsiP75Ubaz0mg3xzgC185')
			embed.add_field(name="Affiliate link:", value="https://www.amazon.es/dp/" + result.group(0) + "/?tag=gfgcorg-21", inline=False)
			await message.channel.send(embed=embed)
			
		if message.content.startswith("!gfgc"):
			embed = discord.Embed(title="Gaming For Global Change", description="Gaming For Global Change is a non-profit organization that hosts various livestreamed gaming marathons and other events to raise money and awareness for global charities. All revenue earned from the Amazon Affiliate program will be used directly to cover costs of the organization's events. ", color=0x00ff00)
			embed.set_thumbnail(url='https://cdn.discordapp.com/icons/212001438447042561/d1a8ca0ed04e184af968a49159c88a1d.png')
			embed.add_field(name="Learn more at:", value="https://gamingforglobalchange.org/", inline=False)
			await message.channel.send(embed=embed)
	await bot.process_commands(message)

# Token for bot to run here
bot.run("TOKEN", bot=True)