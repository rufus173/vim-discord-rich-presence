vim9script noclear
# vim global plugin for rich presence on discord
# maintainer: rufus193 <rufus09173@gmail.com>
if exists("g:loaded_richpresence")
	finish
endif
g:loaded_richpresence = 1

#prepare for talking to discord
var s:plugin_dir = expand("<sfile>:p:h:h")
function g:Init_rich_presence()
	let pid = getpid()
	python3 << EOF
from sys import path
import vim
import time

python_root = f"{vim.eval('s:plugin_dir')}/python" #get to the python dir to import module
print(python_root)
print(path.insert(0,python_root)) #allows module importing

pid = int(vim.eval("pid"))

import discord_rich_presence
discord = discord_rich_presence.discord_ipc(pid)
EOF
endfunction

#refresh the prersence
function g:Set_presence()
	python3 discord.set_presence()
	echo done
endfunction

#kill the socket
function g:Stop_presence()
	python3 discord_rich_presence.set_presence(pid=pid)
	echo done
endfunction

#commands
command Initpresence call Init_rich_presence()
command Setpresence call Set_presence()

finish
