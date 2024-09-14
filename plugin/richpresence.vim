vim9script noclear
# vim global plugin for rich presence on discord
# maintainer: rufus193 <rufus09173@gmail.com>
if exists("g:loaded_richpresence")
	finish
endif
g:loaded_richpresence = 1
var pid = getpid()
var s:plugin_dir = expand("<sfile>:p:h:h")
python3 << EOF
from sys import path
import vim

python_root = f"{vim.eval('s:plugin_dir')}/python" #get to the python dir to import module
print(python_root)
print(path.insert(0,python_root)) #allows module importing

import discord_rich_presence
discord = discord_rich_presence.discord_ipc()
discord_rich_presence.set_presence(pid=9000)
EOF
finish
