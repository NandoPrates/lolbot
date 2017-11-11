import json
import logging
# noinspection PyPackageRequirements
import discord

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
try:
    logging.info('stats[datadog]: initalized')
    # noinspection PyPackageRequirements
    from datadog import statsd
except ImportError:
    logging.info('stats[datadog]: datadog not installed')
    logging.info('stats[datadog]: disabling datadog')
    datadog_enabled = False
else:
    logging.info('stats[datadog]: success')
    datadog_enabled = True


async def find_channel(guild):
    """
    Finds a suitable guild channel for posting the
    welcome message. You shouldn't need to call this
    yourself. on_guild_join calls this automatically.

    Thanks FrostLuma for code!
    """
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c


class Stats:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))

    async def dogpost(self):
        """
        This async function does a post of server and shard count to Datadog.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if datadog_enabled:
            statsd.gauge('servers', len(self.bot.guilds))
            statsd.gauge('shards', len(self.bot.shards))
        else:
            pass

    async def dblpost(self):
        """
        This async function does a post of server and shard count to discordbots.org.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if self.config['dbl'] != "":
            headers = {
                'Authorization': self.config['dbl'],
                'Content-Type': 'application/json'
            }
            data = {
                'server_count': len(self.bot.guilds),
                'shard_count': len(self.bot.shards)
            }
            req = await self.bot.session.post(f'https://discordbots.org/api/bots/{ctx.me.id}/stats',
                                              data=json.dumps(data), headers=headers)
            if req.status == 200:
                logging.info('poster[dbl]: done')
            else:
                logging.error(f'poster[dbl]: oops (code {req.status})')
                logging.error(f'poster[dbl]: response: {await req.text()}')
        else:
            pass

    async def dpwpost(self):
        """
        This async function does a post of server and shard count
        to bots.discord.pw.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if self.config['dbots'] != "":
            headers = {
                'Authorization': self.config['dbots'],
                'Content-Type': 'application/json'
            }
            data = {
                'server_count': len(self.bot.guilds),
                'shard_count': len(self.bot.shards)
            }
            info = await self.bot.application_info()
            req = await self.bot.session.post(f'https://bots.discord.pw/api/bots/{info.id}/stats',
                                              data=json.dumps(data), headers=headers)
            status = req.status
            if status == 200:
                logging.info('poster[dbots]: done')
            else:
                resp = await req.text()
                logging.error(f'poster[dbots]: oops (code {status})')
                logging.error(f'poster[dbots]: response: {resp}')

    async def post(self):
        """
        This async function is a wrapper for post functions.
        You shouldn't need to call this yourself, the guild events do this for you.
        """
        logging.info('poster: starting')
        if self.config['dbotsorg']:
            await self.dblpost()
        else:
            pass
        if self.config['dbotspw']:
            await self.dpwpost()
        else:
            pass
        if datadog_enabled:
            await self.dogpost()
        else:
            pass
        logging.info('poster: done')

    async def on_guild_join(self, guild):
        """
        This async function is called whenever a guild adds a lolbot instance.
        You shouldn't need to call this yourself, discord.py does this automatically.
        """
        logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
        welcome_channel = await find_channel(guild)
        we = discord.Embed(title='Hello!',
                           description='Thanks for inviting me.'
                                       ' I am required to tell you that I may'
                                       ' log command usage, user/channel/server IDs, and'
                                       ' other information. Thanks for your understanding!', colour=0x690E8)
        await welcome_channel.send(embed=we)
        await self.post()

    async def on_guild_remove(self, guild):
        """
        This async function is called whenever a guild removes a lolbot instance (rip).
        You shouldn't need to call this yourself, discord.py does this automatically.
        """
        logging.info('Left ' + str(guild.name))
        await self.post()


def setup(bot):
    bot.add_cog(Stats(bot))
