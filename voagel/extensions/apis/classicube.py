import disnake
from disnake.ext import commands
from datetime import datetime
from voagel.main import Bot
from voagel.utils import escape_url, timedelta_format

class ClassicubeCommand(commands.Cog):
    """Classicube commands"""

    def __init__(self, bot: Bot):
        self.bot = bot

    FLAGS = {
        'b': 'Banned from forums',
        'd': 'Developer',
        'm': 'Forum moderator',
        'a': 'Forum admin',
        'e': 'Blog editor',
        'p': 'Patron',
        'u': 'Unverified',
        'r': 'Recovering account'
    }

    @commands.slash_command()
    async def classicube(self, _: disnake.ApplicationCommandInteraction):
        ...

    @classicube.sub_command()
    async def player(self,
        inter: disnake.ApplicationCommandInteraction,
        username: str
    ):
        """Looks up information about a player

        Parameters
        ----------
        username: Username of the player
        """
        await inter.response.defer()
        username = escape_url(username)

        req = await self.bot.session.get(f'https://www.classicube.net/api/player/{username}')
        data = await req.json()
        if not data or data['error'] != '':
            raise Exception(data['error'] if data and data['error'] else 'User not found')

        flags = data['flags']
        embed = disnake.Embed(title='ClassiCube User', colour=0x977dab)
        embed.set_footer(text=f'ID: {data["id"]}', icon_url='https://www.classicube.net/static/img/cc-cube-small.png')
        embed.timestamp = datetime.utcnow()
        delta = datetime.utcnow() - datetime.utcfromtimestamp(data['registered'])

        embed.set_image(url='https://123dmwm.com/img/3d.php?user='+data['username'])
        embed.set_author(name=data['username'], icon_url=f'https://classicube.s3.amazonaws.com/face/{data["username"]}.png')
        embed.add_field(name='Account created', value=f'<t:{data["registered"]}:F>\n`{timedelta_format(delta)}` ago')

        if flags:
            embed.add_field(name='Notes', value=', '.join([self.FLAGS[n] for n in flags]))
        if data['forum_title']:
            embed.add_field(name='Forum Title', value=data['forum_title'])

        await inter.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(ClassicubeCommand(bot))