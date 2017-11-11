# Cog for W|A
# Most of this is made by lnmds.
# Some changes were made like removing most logging things.
# (c) 2017 S Stewart, Luna Mendes
# MIT License

import asyncio
import wolframalpha
# noinspection PyPackageRequirements
import discord
import json
# noinspection PyPackageRequirements
import utils.errors as uerrs
# noinspection PyPackageRequirements
from discord.ext import commands

RESULT_PODS = {
    'Result', 'Plot', 'Plots', 'Solution'
}

NOT_PODS = {
    'Input', 'Input interpretation'
}


def pod_finder(pod_list):
    """Finds a probable pod."""
    pod_scores = {}

    for pod in pod_list:
        # convert pod to dict
        pod = dict(pod)

        if pod.get('@title') in RESULT_PODS:
            return pod

        score = 0

        # meh pods
        if pod.get('@title') in NOT_PODS:
            score -= 100

        if isinstance(pod['subpod'], list):
            # subpod has an image
            score += 10 + (len(pod['subpod']) * 10)
        else:
            # subpod is singular

            # plain text
            if pod['subpod'].get('plaintext'):
                score += 50

            # image
            if pod['subpod'].get('img'):
                score += 30

        pod_scores[pod['@id']] = score

    # return pod with highest score
    best_id = max(pod_scores, key=pod_scores.get)
    return discord.utils.find(lambda pod: pod['@id'] == best_id, pod_list)


class Wolfram:
    def __init__(self, bot):
        self.bot = bot
        if self.bot.config['wa']:
            self.wa = wolframalpha.Client(self.bot.config['wa'])
        else:
            self.wa = None

    @commands.command(aliases=['wa', 'wolfram'])
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def wolframalpha(self, ctx, *, q: str):
        """Access Wolfram|Alpha, through lolbot"""
        if self.wa:
            if len(q) < 1:
                raise uerrs.ServiceError('You can\'t make a query with less than 1 character...')

            ftr = self.bot.loop.run_in_executor(None, self.wa.query, q)
            res = None

            async with ctx.typing():
                try:
                    res = await asyncio.wait_for(ftr, 13)
                except asyncio.TimeoutError:
                    raise uerrs.ServiceError('Timeout reached')
                except Exception as e:
                    raise uerrs.ServiceError(f'W|A didn\'t wanna work: {e!r}')

            if res is None:
                raise uerrs.ServiceError('W|A didn\'t reply')

            if not res.success:
                raise uerrs.ServiceError('W|A failed for some reason. Maybe try again later?')

            if not getattr(res, 'pods', False):
                em = discord.Embed(title='No answer', colour=0x690E8)
                return await ctx.send(embed=em)

            pods = list(res.pods)

            pod = pod_finder(pods)

            def subpod_simplify(subpod):
                if subpod.get('img'):
                    return subpod['img']['@src']
                return subpod['plaintext']

            if isinstance(pod['subpod'], dict):
                # in this case, we only have one
                if 'MSPStoreType=image' in subpod_simplify(pod['subpod']):
                    em = discord.Embed(colour=0x690E8)
                    em.set_image(url=subpod_simplify(pod['subpod']))
                    await ctx.send(embed=em)
                else:
                    # but maybe we have 2, or 3, or 4.
                    # we'll just choose the first
                    if 'MSPStoreType=image' in subpod_simplify(pod['subpod'][0]):
                        em = discord.Embed(colour=0x690E8)
                        em.set_image(url=subpod_simplify(pod['subpod']))
                        await ctx.send(embed=em)
                    else:
                        em = discord.Embed(description=subpod_simplify(pod['subpod'][0]), colour=0x690E8)
                        await ctx.send(embed=em)
        else:
            raise uerrs.ServiceError('This instance does not have a'
                                     'Wolfram|Alpha key set up.')


def setup(bot):
    bot.add_cog(Wolfram(bot))
