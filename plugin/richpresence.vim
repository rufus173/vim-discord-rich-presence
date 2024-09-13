vim9script noclear
# vim global plugin for rich presence on discord
# maintainer: rufus193 <rufus09173@gmail.com>
if exists("g:loaded_richpresence")
	finish
endif
g:loaded_richpresence = 1
var pid = getpid()
python3 << EOF
import time
import vim 
EOF
var update_command = "/usr/bin/python3 ../python/discord-rich-presence.py " .. pid
call system(update_command)
finish
