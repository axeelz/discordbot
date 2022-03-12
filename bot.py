import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix='!')
client.remove_command('help')


@client.event
async def on_ready():
    print('Connecté en tant que {0.user}'.format(client))
    game = discord.Game("servir le discord | !help")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.command(aliases=['aide', 'cmd', 'commandes'])
async def help(ctx):
    embed = discord.Embed(title="Les commandes disponibles",
                          description="Préfixe avant une commande - '!'", color=0x8000ff)
    embed.add_field(name="help", value="affiche ce message", inline=False)
    embed.add_field(name="prefix", value="affiche le préfixe du bot", inline=False)
    embed.add_field(name="ping", value="affiche la latence du bot", inline=False)
    embed.add_field(name="send [texte]", value="le bot enverra le texte que vous avez indiqué", inline=False)
    embed.add_field(name="8ball [question]", value="répondra à votre question", inline=False)
    embed.add_field(name="rate", value="t'attribues une note /20", inline=False)
    embed.add_field(name="rateuser [@user]", value="attribue une note /20  à la personne que tu mentionne",
                    inline=False)
    embed.add_field(name="love [@user1 @user2]", value="affiche le % de love entre @user1 et @user2", inline=False)
    embed.add_field(name="servers", value="affiche les serveurs dans lesquels le bot est", inline=False)
    embed.add_field(name="users", value="affiche le nombre d'utilisateurs dans ce serveur", inline=False)
    embed.add_field(name="force", value="affiche ton % de force", inline=False)
    embed.add_field(name="forceuser [@user]", value="affiche le % de force de quelqu'un", inline=False)
    embed.add_field(name="dm", value="t'envoie un message privé", inline=False)
    embed.add_field(name="dmuser [@user] [texte]", value="enverra en message privé à [@user] le [texte] mentionné",
                    inline=False)
    embed.add_field(name="salut", value="le bot te passera le bonjour", inline=False)
    embed.set_footer(text="des commandes seront rajoutées au fur et à mesure")
    await ctx.send(content=None, embed=embed)


@client.command(aliases=['prefix'])
async def prefixe(ctx):
    embed = discord.Embed(title="Mon préfixe",
                          description=":information_source: Le préfixe du bot est actuellement : !",
                          color=0x8000ff)
    await ctx.send(content=None, embed=embed)


@client.command(aliases=['latence', 'latency'])
async def ping(ctx):
    embed = discord.Embed(description=":hourglass: Latence : " + str(round(client.latency * 1000)) + "ms", color=0x8000ff)
    await ctx.send(content=None, embed=embed)


@client.command()
async def send(ctx, arg):
    await ctx.send(arg)


@client.command()
async def version(ctx):
    await ctx.send('Ceci est la **dernière version** du bot :ghost: ```v.3```')


@client.command()
async def dm(ctx):
    emoji = '\N{THUMBS UP SIGN}'
    await ctx.message.add_reaction(emoji)
    channel = await ctx.author.create_dm()
    await channel.send("hey!")


@client.command()
async def dmuser(ctx, member: discord.Member, *, content):
    emoji = '\N{THUMBS UP SIGN}'
    await ctx.message.add_reaction(emoji)
    channel = await member.create_dm()
    await channel.send(content)


@client.command()
async def salut(ctx):
    await ctx.send(':wave: Salut {}'.format(ctx.message.author.mention))


@client.command(aliases=['8ball', 'question', '8b'])
async def _8ball(ctx, *, question):
    responses = ["C'est non.",
                 "Peu probable",
                 "Faut pas rêver",
                 "N'y compte pas",
                 "Impossible",
                 "Oui absolument",
                 "Tu peux compter dessus",
                 "Sans aucun doute",
                 "Tu peux compter dessus",
                 "Très probable",
                 "Oui",
                 "C'est bien parti",
                 "D'après moi oui",
                 "C'est certain",
                 "Essaye plus tard",
                 "Pas d'avis",
                 "C'est ton destin",
                 "Essaye encore"]
    await ctx.send(f'Hmmm :thinking:')
    await ctx.send(f'{random.choice(responses)} :partying_face:')


@client.command(aliases=['note'])
async def rate(ctx):
    nb = (random.randint(1, 20))
    await ctx.send(':thumbsup: Je te note ' + str(nb) + '/20 ' + ctx.message.author.mention)


@client.command(aliases=['noteuser'])
async def rateuser(ctx, user1: discord.Member):
    nb = (random.randint(1, 20))
    await ctx.send(':thumbsup: Je note ' + user1.mention + ' ' + str(nb) + '/20')


@client.command()
async def love(ctx, user1: discord.Member, user2: discord.Member):
    love = random.randint(0, 100)
    await ctx.send(':heart: ' + str(love) + '% :heart: \n ' + user1.mention + ' + ' + user2.mention)


@client.command()
async def force(ctx):
    force = random.randint(0, 100)
    await ctx.send(ctx.message.author.mention + ', Tu es fort(e) à** ' + str(force) + '%** :muscle:')


@client.command()
async def forceuser(ctx, user1: discord.Member):
    force = random.randint(0, 100)
    await ctx.send(user1.mention + ' est fort(e) à** ' + str(force) + '%** :muscle:')


@client.command(aliases=['serveurs'])
async def servers(ctx):
    servers = list(client.guilds)
    await ctx.send(f"**Connecté sur {str(len(servers))} serveurs :**")
    await ctx.send('\n'.join(server.name for server in servers))


@client.command(aliases=['utilisateurs', 'membres', 'members'])
async def users(ctx):
    await ctx.send(" Il y a {0.member_count} utilisateurs sur **{0.name}**".format(ctx.message.guild))

@client.command(aliases=['exit', 'stop', 'close', 'logout'])
@commands.is_owner()
async def disconnect(ctx):
    await ctx.send("**Déconnexion en cours... :ghost:**")
    await client.close()
    print("Déconnecté")

@client.command()
async def update(ctx, arg):
    if ctx.message.author.guild_permissions.administrator:
        msg = "**Changement du statut en cours... :ghost:** {0.author.mention}".format(ctx.message)
        await ctx.send(msg)
        await client.change_presence(activity=discord.Game(name=arg))
    else:
        msg = "**Tu n'as pas les permissions nécessaires pour faire celà {0.author.mention}".format(ctx.message)  
        await ctx.send(msg)

@client.command()
async def restore(ctx):
    if ctx.message.author.guild_permissions.administrator:
        msg = "**Restauration du statut... :ghost:** {0.author.mention}".format(ctx.message)  
        await ctx.send(msg)
        game = discord.Game("servir le discord | !help")
        await client.change_presence(status=discord.Status.online, activity=game)
    else:
        msg = "**Tu n'as pas les permissions nécessaires pour faire celà {0.author.mention}".format(ctx.message)  
        await ctx.send(msg)

token = '' # mettre son token discord développeur ici
client.run(token)
