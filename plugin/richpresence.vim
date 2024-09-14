vim9script noclear
# vim global plugin for rich presence on discord
# maintainer: rufus193 <rufus09173@gmail.com>
if exists("g:loaded_richpresence")
	finish
endif
g:loaded_richpresence = 1
var pid = getpid()
python3 << EOF
from sys import path
path.insert(0,"../python") #allows module importing
import discord_rich_presence
discord = discord_rich_presence.discord_ipc()
discord_rich_presence.set_presence(pid=9000)
EOF
var update_command = "/usr/bin/python3 ../python/discord-rich-presence.py " .. pid
call system(update_command)
finish
