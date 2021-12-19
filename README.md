# Custom slash commands - The bot 💀

<a href="https://discord.gg/vZRrpBXFNT"><img src="https://img.shields.io/discord/787773373748740128?label=Discord%20Server&style=for-the-badge"></img></a>
<br><br>

This is a bot for our university server that ties in together with my scraping bot to provide custom, user generatable, editable, and removable slash commands.
Now, this could break at any time as this pip library is probably not going to be supported once discord.py rewrite hits version 2.0, but hey, I'm inpatient.
It saves the commands as cogs located in `/cogs` and reloads them on any modification. It should work flawlessly.

## If for some reason you want to use it, this is how.

1. Run 
```sh
 git clone https://github.com/omznc/discord-custom-slashes.git
```
2. Edit `bot.py`:
   * Add your token
   * Add your guild ID (yes it's a list, no you can't use more than 1 item, I'm too lazy to replace a few square brackets, you can do that yourself)
   * Maybe translate the error messages I provide to your own language as these were targeted towards `Bosnian`, which can be awkward if you're let's say Italian.
4. Install requirements (these might break, let me know) with:
```sh
pip install -r requirements.txt
```
5. Run using:
```sh
python3 bot.py
```
