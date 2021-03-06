"""
The MIT License (MIT)

Copyright (c) 2018 tilda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
# noinspection PyPackageRequirements
import discord
import json
# noinspection PyPackageRequirements
from discord.ext import commands
# noinspection PyPackageRequirements
import utils.errors
from cogs.common import user_agent

class Animemes:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))

    @commands.command()
    async def neko(self, ctx):
        """Shows a random neko picture"""
        async with self.bot.session.get('https://nekos.life/api/neko', headers=user_agent) as neko:
            if neko.status == 200:
                img = await neko.json()
                neko_em = discord.Embed(colour=0x690E8)
                neko_em.set_image(url=img['neko'])
                neko_em.set_footer(text='Powered by nekos.life - use ^lneko to get lewd version')
                await ctx.send(embed=neko_em)
            else:
                raise utils.errors.ServiceError(f'dude rip (http {neko.status})')

    @commands.command()
    async def lneko(self, ctx):
        """NSFW: Shows a random lewd neko pic
        Disable this command by putting "[lb:no_nsfw]" in your channel topic.
        """
        if ctx.channel.is_nsfw():
            if '[lb:no_nsfw]' in ctx.channel.topic:
                raise utils.errors.NSFWException()
            else:
                async with self.bot.session.get('https://nekos.life/api/lewd/neko', headers=user_agent) as lneko:
                    if lneko.status == 200:
                        img = await lneko.json()
                        # noinspection PyPep8Naming
                        lneko_em = discord.Embed(colour=0x690E8)
                        lneko_em.set_image(url=img['neko'])
                        await ctx.send(embed=lneko_em)
                        lneko_em.set_footer(text='Powered by nekos.life - use ^neko to get non-nsfw version')
                    else:
                        raise utils.errors.ServiceError(f'dude rip (http {lneko.status})')
        else:
            raise utils.errors.NSFWException('you really think you can do this'
                                             'in a non nsfw channel? lol')


def setup(bot):
    bot.add_cog(Animemes(bot))
