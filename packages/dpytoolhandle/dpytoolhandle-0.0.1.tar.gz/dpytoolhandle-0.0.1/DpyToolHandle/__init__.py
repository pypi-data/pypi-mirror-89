#IMPORTS
from discord.ext import commands
import random
import discord
import aiohttp


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball', 'ball'])
    async def _8ball(self, ctx, *, question):
            
              responses = ['As I see it, yes.',
                          'Ask again later.',
                          'Better not tell you now.',
                          'Cannot predict now.',
                          'Concentrate and ask again.',
                          'Don’t count on it.',
                          'It is certain.',
                          'It is decidedly so.',
                          'Most likely.',
                          'My reply is no.',
                          'My sources say no.',
                          'Outlook not so good.',
                          'Outlook good.',
                          'Reply hazy, try again.',
                          'Signs point to yes.',
                          'Very doubtful.',
                          'Without a doubt.',
                          'Yes.',
                          'Yes – definitely.',
                          'You may rely on it.']
              q = ("Question: " + question)
              a = ("Answer: " + random.choice(responses))
              embed = discord.Embed(
                  title=(q),
                  description=(a),
                  colour=discord.Colour.blue()
              )

              await ctx.send(embed=embed)
           

    @commands.command(aliases=["facepalm"])
    async def fp(self, ctx):
              
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://www.reddit.com/r/facepalm/top.json") as response:
                        j = await response.json()

                data = j["data"]["children"][random.randint(0, 25)]["data"]
                image_url = data["url"]
                title = data["title"]
                em = discord.Embed(description=f"[**{title}**]({image_url})", colour=discord.Colour.blue())
                em.set_image(url=image_url)
                em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
                await ctx.send(embed=em)

    @commands.command(aliases=["maymay", "memes"])
    async def meme(self, ctx):
              
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://www.reddit.com/r/memes/top.json") as response:
                        j = await response.json()

                data = j["data"]["children"][random.randint(0, 25)]["data"]
                image_url = data["url"]
                title = data["title"]
                em = discord.Embed(description=f"[**{title}**]({image_url})", colour=discord.Colour.blue())
                em.set_image(url=image_url)
                em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
                await ctx.send(embed=em)

    @commands.command(aliases=['Ko','ko'])
    async def KO(self, ctx,member):
                 
                    gifslist =['https://media.tenor.com/images/e302b70e805f045816c100a92325b824/tenor.gif', 'https://media1.tenor.com/images/3da22c373b5506939514773ad496b170/tenor.gif?itemid=11751811', 'https://media1.tenor.com/images/b3dddda27a439a9951fdd0de5a0644e6/tenor.gif?itemid=15872871', 'https://media1.tenor.com/images/3b0d7cc04fb09adb1ccc96a23b98dd86/tenor.gif?itemid=6032176', 'https://media1.tenor.com/images/97248cf32942f467c4a049acbae8981e/tenor.gif?itemid=3555140', 'https://media1.tenor.com/images/c7dece5cdd4cee237e232e0c5d955042/tenor.gif?itemid=4902914']
                    gifs=random.choice(gifslist)
                    
                    embed = discord.Embed(
                        description=(f"{member} Has been Knocked Out!"),
                        colour=discord.Colour.blue()
                        )
                    embed.set_image(url=gifs)    
                    await ctx.send(embed=embed)

                    


      

      


def setup(bot):
  bot.add_cog(Fun(bot))