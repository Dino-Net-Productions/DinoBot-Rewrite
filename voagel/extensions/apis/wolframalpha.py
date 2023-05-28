from io import BytesIO

import disnake
from disnake.ext import commands

from voagel.main import Bot
from voagel.utils import escape_url


class WolframAlphaCommand(commands.Cog):
    """Wolfram Alpha"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def wolframalpha(self,
        inter: disnake.ApplicationCommandInteraction,
        query: str
    ):
        """
        Ask questions to Wolfram Alpha

        Parameters
        ----------
        query: Query for Wolfram Alpha
        """

        await inter.response.defer()
        req = await self.bot.session.get(
            f'http://api.wolframalpha.com/v1/simple?appid={self.bot.get_api_key("wolframalpha")}&layout=labelbar&ip=None&units=metric&background=2F3136&foreground=white&i={escape_url(query)}'
        )

        if req.status != 200:
            err = req.text()
            if not err:
                err = '[unknown error]'

            if req.status == 501:
                raise Exception('WolframAlpha could not parse the query', err)
            raise Exception(f'WolframAlpha returned an error status {req.status}', err)

        data = await req.read()
        if len(data) == 0:
            raise Exception('WolframAlpha did not return any data.')

        file = disnake.File(BytesIO(data), 'wolfram.png')
        await inter.send(file=file)


def setup(bot: Bot):
    bot.add_cog(WolframAlphaCommand(bot))