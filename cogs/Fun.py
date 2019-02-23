import datetime
import asyncio
import json
import os

import requests
import discord
from discord.ext import commands
import urllib.request
import urllib
from bs4 import BeautifulSoup
from newsapi import NewsApiClient

newsapi_key = os.getenv('NEWSAPI_KEY')
apixu_key = os.getenv('APIXU_KEY')
od_app_id = os.getenv('OD_APP_ID')
od_app_key = os.getenv('OD_APP_KEY')


class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='urban', aliases=['ud'])
    async def urban(self, ctx, *, word):
        """
        Fetches urban dictionary definitions using the urban dictionary API.

        Usage examples:
        - f.urban furry
        - f.ud wave check
        """
        try:
            async with ctx.typing():
                index = 0
                session = requests.session()
                link = f'http://api.urbandictionary.com/v0/define?term={word}'
                req_link = session.get(link).text
                req_json = json.loads(req_link)

                if not req_json['list']:
                    return await ctx.send(f'No search results found for "**{word}**"')

                definition = req_json['list'][index]['definition']
                example = req_json['list'][index]['example']
                thumbs_up = req_json['list'][index]['thumbs_up']
                thumbs_down = req_json['list'][index]['thumbs_down']

                emb = discord.Embed(title=f'Definition for: {word}',
                                    description=definition.replace('[', '').replace(']', ''),
                                    colour=discord.Colour.dark_green(),
                                    timestamp=datetime.datetime.utcnow())
                emb.add_field(name='Example', value=example.replace('[', '').replace(']', ''), inline=False)
                emb.set_footer(text=f'👍 {thumbs_up} - 👎 {thumbs_down}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
        except KeyError:
            return await ctx.send("No results found")

    @commands.command(name='weather')
    async def weather(self, ctx, *, city):
        """
        Fetches weather information for <city>

        Usage examples:
        - f.weather Auckland
        - f.weather London, uk
        - f.weather new york city
        """

        session = requests.session()
        link = f'https://api.apixu.com/v1/current.json?key={apixu_key}&q={city}'

        try:
            async with ctx.typing():
                req_link = session.get(link).text
                req_json = json.loads(req_link)

                city_name = req_json['location']['name']
                region = req_json['location']['region']
                country = req_json['location']['country']
                time_zone = req_json['location']['tz_id']
                city_info = f'{city_name}, {region}, {country} (timezone: {time_zone})'

                current_temp = f"{req_json['current']['temp_c']}°C"
                feels_like = f"{req_json['current']['feelslike_c']}°C"
                temp_info = f'Measured: {current_temp}\nFeels like: {feels_like}'

                condition = req_json['current']['condition']['text']
                cloud_coverage = f"{req_json['current']['cloud']}%"
                cloud_info = f'{condition} (cloud coverage: {cloud_coverage})'

                wind_strength = req_json['current']['wind_kph']
                wind_direction = f"{req_json['current']['wind_degree']}° ({req_json['current']['wind_dir']})"
                wind_info = f'{wind_strength}km/h at direction {wind_direction}'

                pressure = f"{req_json['current']['pressure_mb']} millibars"
                precipitate = f"{req_json['current']['precip_mm']}"
                other_info = f'Pressure: {pressure}\nPrecipitate: {precipitate}mm'

                uv = req_json['current']['uv']

                emb = discord.Embed(title=f'Weather info for {city_name}', colour=discord.Colour.lighter_grey(),
                                    timestamp=datetime.datetime.utcnow())
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

                emb.add_field(name='Location info', value=city_info, inline=True)
                emb.add_field(name='Temperature', value=temp_info, inline=True)
                emb.add_field(name='Condition', value=cloud_info, inline=True)
                emb.add_field(name='Wind', value=wind_info, inline=False)
                emb.add_field(name='UV level', value=uv, inline=False)
                emb.add_field(name='Other info', value=other_info, inline=False)
            await ctx.send(embed=emb)
        except KeyError:
            return await ctx.send(f'No results found')

    @commands.command(name='anime')
    async def anime(self, ctx, *, name):
        """
        Search for an anime. NOTE: Paging is slow at the moment so be patient (and don't spam)!

        Usage examples:
        - f.anime one punch man
        - f.anime Fairy Tail
        """
        index = 0
        session = requests.session()
        link = f"https://api.jikan.moe/search/anime/{name}"

        try:
            async with ctx.typing():
                req_link = session.get(link).text
                req_json = json.loads(req_link)

                limit = len(req_json['result']) - 1
                title = req_json['result'][index]['title']
                direct_link = f"[Direct Link]({req_json['result'][index]['url']})"
                description = req_json['result'][index]['description']
                mov_type = req_json['result'][index]['type']
                episodes = req_json['result'][index]['episodes']
                score = f"{req_json['result'][index]['score']}/10"
                image_url = req_json['result'][index]['image_url']

                emb = discord.Embed(title='Anime search', description=direct_link, colour=discord.Colour.dark_orange(),
                                    timestamp=datetime.datetime.utcnow())
                emb.set_image(url=image_url)
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

                emb.add_field(name='Title', value=title, inline=False)
                emb.add_field(name='Description', value=description, inline=False)
                emb.add_field(name='Type', value=mov_type, inline=False)
                emb.add_field(name='Episodes', value=episodes, inline=False)
                emb.add_field(name='Score', value=score, inline=False)
            em = await ctx.send(embed=emb)
            await em.add_reaction('◀')
            await em.add_reaction('▶')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['◀', '▶'] and reaction.message.id == em.id

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=20, check=check)
                except asyncio.TimeoutError:
                    await em.clear_reactions()
                else:
                    if str(reaction.emoji) == '▶':
                        index += 1
                        await em.remove_reaction('▶', ctx.message.author)
                        if index > limit:
                            index -= 1
                            continue

                    elif str(reaction.emoji) == '◀':
                        index -= 1
                        await em.remove_reaction('◀', ctx.message.author)
                        if index < 0:
                            index += 1
                            continue

                    async with ctx.typing():
                        an = req_json
                        title = an['result'][index]['title']
                        direct_link = f"[Direct Link]({an['result'][index]['url']})"
                        description = an['result'][index]['description']
                        mov_type = an['result'][index]['type']
                        episodes = an['result'][index]['episodes']
                        score = f"{an['result'][index]['score']}/10"
                        image_url = an['result'][index]['image_url']

                        emb = discord.Embed(title='Anime search', description=direct_link,
                                            colour=discord.Colour.dark_orange(),
                                            timestamp=datetime.datetime.utcnow())
                        emb.set_image(url=image_url)
                        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

                        emb.add_field(name='Title', value=title, inline=False)
                        emb.add_field(name='Description', value=description, inline=False)
                        emb.add_field(name='Type', value=mov_type, inline=False)
                        emb.add_field(name='Episodes', value=episodes, inline=False)
                        emb.add_field(name='Score', value=score, inline=False)
                    await em.edit(embed=emb)
                    asyncio.sleep(20)
        except KeyError:
            return await ctx.send("No results found (or API is having problems)")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='define')
    async def define(self, ctx, *, word):
        """
        Fetches definition of a word using the Oxford dictionary API (case insensitive)

        Usage examples:
        - f.define impostor
        - f.define Apocalypse
        """
        session = requests.session()
        link = f'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/{word.lower()}'
        try:
            async with ctx.typing():
                header = {"app_id": od_app_id, 'app_key': od_app_key}
                req_link = session.get(link, headers=header).text
                req_json = json.loads(req_link)
                etymology, examples = '', ''
                et, ex = True, True

                try:
                    etymology = req_json['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0]
                except KeyError:
                    et = False
                    pass

                try:
                    examples = req_json['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0][
                        'text']
                except KeyError:
                    ex = False
                    pass

                definition = req_json['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                category = req_json['results'][0]['lexicalEntries'][0]['lexicalCategory']
                # tit = f"[{word}](https://en.oxforddictionaries.com/definition/{word})"

                emb = discord.Embed(title=word, colour=discord.Colour.blurple(),
                                    timestamp=datetime.datetime.utcnow(), url=f"https://en.oxforddictionaries.com/definition/{word}")
                emb.add_field(name='Definition', value=definition, inline=False)
                emb.add_field(name='Type', value=category, inline=False)
                if et:
                    emb.add_field(name='Etymology', value=etymology, inline=False)
                if ex:
                    emb.add_field(name='Example', value=examples, inline=False)
                    emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

            await ctx.send(embed=emb)
        except json.JSONDecodeError:
            return await ctx.send("No results found")
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='yt', aliases=['youtube'])
    async def youtube(self, ctx, *, search_query):
        """
        Searches a youtube video
        
        Usage examples:
        - f.yt never gonna give you up
        - f.youtube U9BwWKXjVaI
        """
        try:
            async with ctx.typing():
                query = search_query.replace(' ', '+')
                search_url = f'https://www.youtube.com/results?search_query={query}'
                page = urllib.request.urlopen(search_url)
                soup = BeautifulSoup(page.read(), "html.parser")
                video_id = soup.find("div", {"class": "yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix"}).get(
                    "data-context-item-id")
            await ctx.send(f'**Search result:**\nhttps://www.youtube.com/watch?v={video_id}')
        except:
            return ctx.send('Error searching for video')
       
    @commands.command(name='secret')
    async def secret(self, ctx, *, words):
        """
        Replaces a string where each character is a spoiler block
        
        Usage examples:
        - f.secret @Farid#0001 is a crap mod
        - f.secret bush did 9/11
        """
        if len(words) > 300:
            return await ctx.send('Sentence is too long!')
        final = []
        for letter in words:
            final.append('||')
            final.append(letter)
            final.append('||')
        
        emb = discord.Embed(
            title='A secret message... 👀',
            description=(''.join(final))
        )
        await ctx.message.delete()
        await ctx.send(embed=emb)
    
    @commands.command(name='spoilerfy', aliases=['sf'])
    async def spoilerfy(self, ctx, *, words):
        """
        Just like f.secret, but with raw formatting!
        
        Usage examples:
        - f.spoilerfy qwertyuiop
        - f.sf quit wasting time
        """
        if len(words) > 300:
            return await ctx.send('Sentence is too long!')
        final = []
        for letter in words:
            final.append('||')
            final.append(letter)
            final.append('||')
        
        emb = discord.Embed(
            title='Spoilerfied!',
            description=(f"```{''.join(final)}```"),
            timestamp=datetime.datetime.utcnow()
        )
        
        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    
    @commands.command(name='newsbeta')
    async def newsbeta(self, ctx, *, argument):
        """
        Retrieve news article/s

        Args:
        Query comes first, then language, then sort
        
        --q
          The keywords to search for
        
        --lang
          The language for the article
        Options:
        ar: Arabic
        de: Deustch (German)
        en: English
        es: Espanol
        fr: French
        he: Hebrew
        it: Italian
        nl: Dutch
        no: Norwegian
        pt: Portuguese
        ru: Russian
        
        --sort
          The order to sort the article by
        Options:
          relevancy, popularity, publishedAt
        ____________________________
        --q:
        Advanced search is supported:
        Surround phrases with quotes (") for exact match.
        Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
        Prepend words that must not appear with a - symbol. Eg: -bitcoin
        Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
        ____________________________
        Usage examples:
        - f.news --q Donald Trump +twitter -covfefe --language fr --sort relevancy
        - f.news --q youtube NOT pewdiepie --sort publishedAt
        - f.news --q discordapp
        """
        args = argument.replace('--q', '|[]|').replace('--lang', '|[]|').replace('--sort', '|[]|')
        args = args.split('|[]|')
        arg = [ar.rstrip().lstrip() for ar in args if ar != '']
        await ctx.send(f'{len(arg)}\n{arg}')  # Temp
            
        if len(arg) != 3:
            return await ctx.send('All parameters required. Type `f.help news` for more info')
        query = arg[0]
        lang = arg[1]
        sortby = arg[2]
        # This is gonna be improved
        
        # await ctx.send(f'{query}, {lang}, {sortby})\
        news = NewsApiClient(newsapi_key)
        
        try:
            async with ctx.typing():
                result = news.get_everything(q=query, language=lang, sort_by=sortby, page_size=10)
                index = 0
                limit = len(result['articles']) - 1

                src_link = result['articles'][index]['url']
                author = result['articles'][index]['author']
                source = f"{result['articles'][index]['source']['name']} ({author})\n[Direct Link]({src_link})"
                title = result['articles'][index]['title']
                desc = result['articles'][index]['description']
                preview = result['articles'][index]['content']
                date = f"{str(result['articles'][index]['publishedAt'])[:10]}\n*yyyy-dd-mm*"
                img = result['articles'][index]['urlToImage']

                emb = discord.Embed(title=title,
                                    description=desc,
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=discord.Colour.dark_gold())
                emb.add_field(name='Preview', value=preview, inline=False)
                emb.add_field(name='Source', value=source, inline=True)
                emb.add_field(name='Date', value=date, inline=True)
                emb.set_thumbnail(url=img)
                emb.set_footer(text=f'{ctx.author} | Page {index + 1}/{len(result["articles"])}', icon_url=ctx.author.avatar_url)
                emb.set_author(name='Powered by News API', url='https://newsapi.org/', icon_url='https://i.imgur.com/KROyhZT.png')
        except KeyError:
            return await ctx.send('Not found')
        except ValueError:
            return await ctx.send('Wrong language or wrong sort. Type `f.help news` for more info')

        em = await ctx.send(embed=emb)
        await em.add_reaction('◀')
        await em.add_reaction('▶')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['◀', '▶'] and reaction.message.id == em.id

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                return await em.clear_reactions()
            else:
                if str(reaction.emoji) == '▶':
                    index += 1
                    await em.remove_reaction('▶', ctx.message.author)
                    if index > limit:
                        index -= 1
                        continue

                elif str(reaction.emoji) == '◀':
                    index -= 1
                    await em.remove_reaction('◀', ctx.message.author)
                    if index < 0:
                        index += 1
                        continue

                src_link = result['articles'][index]['url']
                author = result['articles'][index]['author']
                source = f"{result['articles'][index]['source']['name']} ({author})\n[Direct Link]({src_link})"
                title = result['articles'][index]['title']
                desc = result['articles'][index]['description']
                preview = result['articles'][index]['content']
                date = f"{str(result['articles'][index]['publishedAt'])[:10]}\n*yyyy-dd-mm*"
                img = result['articles'][index]['urlToImage']

                emb = discord.Embed(title=title,
                                    description=desc,
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=discord.Colour.dark_gold())
                emb.add_field(name='Preview', value=preview, inline=False)
                emb.add_field(name='Source', value=source, inline=True)
                emb.add_field(name='Date', value=date, inline=True)
                emb.set_thumbnail(url=img)
                emb.set_footer(text=f'{ctx.author} | Page {index + 1}/{len(result["articles"])}', icon_url=ctx.author.avatar_url)
                emb.set_author(name='Powered by News API', url='https://newsapi.org/', icon_url='https://i.imgur.com/KROyhZT.png')

                await em.edit(embed=emb)
                asyncio.sleep(20)
    
    @commands.command(name='news')
    async def news(self, ctx, *, argument):
        """
        Retrieve news article/s
        <argument> : News search query. Sorting = relevancy, language = English
        ____________________________
        --q:
        Advanced search is supported:
        Surround phrases with quotes (") for exact match.
        Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
        Prepend words that must not appear with a - symbol. Eg: -bitcoin
        Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
        ____________________________
        Usage examples:
        - f.news Discordapp
        - f.news telegram +security
        - f.news bush "conspiracy"
        """
        news = NewsApiClient(newsapi_key)
        
        try:
            async with ctx.typing():
                result = news.get_everything(q=argument, language='en', sort_by='relevancy', page_size=10)
                index = 0
                limit = len(result['articles']) - 1

                src_link = result['articles'][index]['url']
                author = result['articles'][index]['author']
                source = f"{result['articles'][index]['source']['name']} ({author})\n[Direct Link]({src_link})"
                title = result['articles'][index]['title']
                desc = result['articles'][index]['description']
                preview = result['articles'][index]['content']
                date = f"{str(result['articles'][index]['publishedAt'])[:10]}\n*yyyy-dd-mm*"
                img = result['articles'][index]['urlToImage']

                emb = discord.Embed(title=title,
                                    description=desc,
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=discord.Colour.dark_gold())
                emb.add_field(name='Preview', value=preview, inline=False)
                emb.add_field(name='Source', value=source, inline=True)
                emb.add_field(name='Date', value=date, inline=True)
                emb.set_thumbnail(url=img)
                emb.set_footer(text=f'{ctx.author} | Page {index + 1}/{len(result["articles"])}', icon_url=ctx.author.avatar_url)
                emb.set_author(name='Powered by News API', url='https://newsapi.org/', icon_url='https://i.imgur.com/KROyhZT.png')
        except KeyError:
            return await ctx.send('Not found')
        except ValueError:
            return await ctx.send('Wrong language or wrong sort. Type `f.help news` for more info')

        em = await ctx.send(embed=emb)
        await em.add_reaction('◀')
        await em.add_reaction('▶')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['◀', '▶'] and reaction.message.id == em.id

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                return await em.clear_reactions()
            else:
                if str(reaction.emoji) == '▶':
                    index += 1
                    await em.remove_reaction('▶', ctx.message.author)
                    if index > limit:
                        index -= 1
                        continue

                elif str(reaction.emoji) == '◀':
                    index -= 1
                    await em.remove_reaction('◀', ctx.message.author)
                    if index < 0:
                        index += 1
                        continue

                src_link = result['articles'][index]['url']
                author = result['articles'][index]['author']
                source = f"{result['articles'][index]['source']['name']} ({author})\n[Direct Link]({src_link})"
                title = result['articles'][index]['title']
                desc = result['articles'][index]['description']
                preview = result['articles'][index]['content']
                date = f"{str(result['articles'][index]['publishedAt'])[:10]}\n*yyyy-dd-mm*"
                img = result['articles'][index]['urlToImage']

                emb = discord.Embed(title=title,
                                    description=desc,
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=discord.Colour.dark_gold())
                emb.add_field(name='Preview', value=preview, inline=False)
                emb.add_field(name='Source', value=source, inline=True)
                emb.add_field(name='Date', value=date, inline=True)
                emb.set_thumbnail(url=img)
                emb.set_footer(text=f'{ctx.author} | Page {index + 1}/{len(result["articles"])}', icon_url=ctx.author.avatar_url)
                emb.set_author(name='Powered by News API', url='https://newsapi.org/', icon_url='https://i.imgur.com/KROyhZT.png')

                await em.edit(embed=emb)
                asyncio.sleep(20)
    
    @commands.command(name='rhyme')
    async def rhyme(self, ctx, *, phrase):
        """Tries to find a rhyme for a certain phrase"""
        session = requests.session()
        link = f"http://rhymebrain.com/talk?function=getRhymes&word={phrase.lower()}"

        async with ctx.typing():
            req_link = session.get(link).text
            req_json = json.loads(req_link)

            if req_json is None:
                return await ctx.send('No rhyme/s found')

            em = []
            desc = ''
            for entry in req_json:
                if len(em) >= 5:
                    break
                em.append(entry)

            if not em:
                desc = 'None found'
            else:
                for entry in em:
                    desc += f"**Word:** {entry['word']}\n**Accuracy:** {round((entry['score']/3), 2)}%\n\n"
            emb = discord.Embed(title=f'Rhymes of "{phrase}"', timestamp=datetime.datetime.utcnow(),
                                color=discord.Colour.blue(), description=desc)
            emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=emb)
    
    @commands.command(name='achievement', aliases=['ach'])
    async def achivement(self, ctx, *, text):
        """
        Gets a minecraft achivement message with text <text>
        
        Usage examples:
        - f.achievement studying
        - f.ach actually not dying
        """
        text = urllib.parse.quote(text)
        url = f"https://api.alexflipnote.xyz/achievement?text={text}"
        emb = discord.Embed(title=discord.Embed.Empty)
        emb.set_image(url=url)
        await ctx.send(embed=emb)
    
    @commands.command(name='gifsearch')
    async def gifsearch(self, ctx, *, text):
        """
        lmgtfy a text
        
        Usage examples:
        - f.gifsearch how to make a bot
        """
        url = f"lmgtfy.com/?q{text}" 
        emb = discord.Embed(title=discord.Embed.Empty)
        emb.set_image(url=url)
                               
        await ctx.send(embed=emb)
            
                               
def setup(bot):
    bot.add_cog(Fun(bot))
