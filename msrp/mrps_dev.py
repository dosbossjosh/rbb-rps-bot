import discord
from discord.ext import commands
import random

TOKEN = "MTE0MTk1NTg5NzE0OTYyODQ0OQ.Gz_6sJ.-aneAT4cc1yyGLDQT-uJ98-jMcy76LrL2T4eR8"
intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

champ_aliases = {
    "cap": "Captain America",
    "captainamerica": "Captain America",
    "iron": "Iron Man",
    "ironman": "Iron Man",
    "spidey": "Spider-Man",
    "spiderman": "Spider-Man",
    "spider-man": "Spider-Man",
    "thanos": "Thanos",
    "purpleman": "Thanos",
    "ultron": "Ultron",
    "strange": "Dr Strange",
    "drstrange": "Dr Strange",
    "witch": "Scarlet Witch",
    "switch": "Scarlet Witch",
    "scarletwitch": "Scarlet Witch",
    "sw": "Scarlet Witch",
    # "joshSoul": "joshSoul"
}

champ_winning_conditions = {
    "Iron Man": ["Captain America", "Ultron", "Dr Strange"],
    "Captain America": ["Spider-Man", "Thanos", "Scarlet Witch"],
    "Spider-Man": ["Iron Man", "Ultron", "Scarlet Witch"],
    "Thanos": ["Spider-Man", "Iron Man", "Dr Strange"],
    "Ultron": ["Captain America", "Thanos", "Scarlet Witch"],
    "Dr Strange": ["Captain America", "Spider-Man", "Ultron"],
    "Scarlet Witch": ["Iron Man", "Thanos", "Dr Strange"],
    # "joshSoul": ["Iron Man", "Captain America", "Spider-Man", "Thanos", "Ultron", "Dr Strange", "Scarlet Witch"]
}

pvp_sessions = {}

def compare_choices(player1_choice, player2_choice):
    player1_choice = champ_aliases.get(player1_choice, player1_choice)
    player2_choice = champ_aliases.get(player2_choice, player2_choice)

    if player1_choice not in champ_winning_conditions or player2_choice not in champ_winning_conditions:
        return "Both players need to choose valid characters."
    elif player1_choice == player2_choice:
        return f"Player 1: {player1_choice} || Player 2: {player2_choice} - it's a tie!"
    elif player2_choice in champ_winning_conditions[player1_choice]:
        return f"Player 1: {player1_choice} || Player 2: {player2_choice} - Player 2 wins!"
    else:
        return f"Player 1: {player1_choice} || Player 2: {player2_choice} - Player 1 wins!"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def pve(ctx, user_choice):
    user_choice = champ_aliases.get(user_choice, user_choice)
    ai_champion = random.choice(list(champ_winning_conditions.keys()))

    if user_choice not in champ_winning_conditions:
        result = "Are you looking for a secret character?"
    elif user_choice == ai_champion:
        result = f"You: {user_choice} || Enemy: {ai_champion} - it's atay (a tie, get it? hehe)!"
    elif user_choice in champ_winning_conditions[ai_champion]:
        result = f"You: {user_choice} || Enemy: {ai_champion} - Winner Winner Sisig Dinner!"
    else:
        result = f"You: {user_choice} || Enemy: {ai_champion} - GG kids disband!"

    await ctx.send(result)

room_channels = {}

@bot.command()
async def underoos(ctx, room_name):
    user = ctx.author
    if room_name in pvp_sessions:
        session = pvp_sessions[room_name]
        if session["player2"] is None:
            session["player2"] = user
            await user.send(f"You've joined the PvP session in '{room_name}'")
            await user.send("Use '!c [character]' to pick your character privately.")
        else:
            await user.send(f"A PvP session named '{room_name}' is already full. Choose another room or create a new one.")
    else:
        room_channels[user] = ctx.channel
        pvp_sessions[room_name] = {"player1": user, "player2": None, "choice": None}
        await user.send(f"{user.mention}, you've started a PvP session in '{room_name}'. Use '!c [character]' to pick your character privately.")

@bot.command()
async def c(ctx, choice):
    user = ctx.author
    for room_name, session in pvp_sessions.items():
        if session["player1"] == user:
            channel = room_channels[session["player1"]]
            if session["choice"] is None:
                session["choice"] = choice
                await user.send(f"You've chosen {choice}. Waiting for both players' choices to be revealed.")
            if session["choice"] and session["player2_choice"]:
                player1_choice = champ_aliases.get(session["choice"], session["choice"])
                player2_choice = champ_aliases.get(session["player2_choice"], session["player2_choice"])
                result = compare_choices(player1_choice, player2_choice)
                result_msg = (
                    f"{session['player1'].mention} chose {player1_choice}.\n"
                    f"{session['player2'].mention} chose {player2_choice}.\n"
                    f"{result}"
                )
                await channel.send(result_msg)  # Send the result to the server channel
                del pvp_sessions[room_name]
            return
        elif session["player2"] == user:
            session["player2_choice"] = choice
            await user.send(f"You've chosen {choice}. Waiting for both players' choices to be revealed.")
            if session["choice"] and session["player2_choice"]:
                player1_choice = champ_aliases.get(session["choice"], session["choice"])
                player2_choice = champ_aliases.get(session["player2_choice"], session["player2_choice"])
                result = compare_choices(player1_choice, player2_choice)
                result_msg = (
                    f"{session['player1'].mention} chose {player1_choice}.\n"
                    f"{session['player2'].mention} chose {player2_choice}.\n"
                    f"{result}"
                )
                channel = room_channels[session["player1"]]
                await channel.send(result_msg)  # Send the result to the server channel
                del pvp_sessions[room_name]
            return
    await ctx.send("You need to start or join an existing PvP session using '!underoos [room_name]' to use this command.")


@bot.command()
async def test(ctx, *, text):
    # Get the public channel where you want to send the message
    public_channel_id = ctx.channel.id
    public_channel = bot.get_channel(public_channel_id)
    
    # Send the user's input to the public channel
    await public_channel.send(f"From {ctx.author.mention}: {text}")

    # Send a confirmation message to the user
    await ctx.author.send(f"ito tinype mo '{text}' anyare")

user_data = {}
@bot.command()
async def pp(ctx):
    await ctx.author.send("Please enter a string for the next command:")
    user_data[ctx.author.id] = {"command": "prompt", "server_channel": ctx.channel}

@bot.command()
async def oo(ctx, *, text):
    user_id = ctx.author.id
    if user_id in user_data and user_data[user_id]["command"] == "prompt":
        server_channel = user_data[user_id]["server_channel"]
        await server_channel.send(f"User {ctx.author.mention} says: {text}")
        del user_data[user_id]
    else:
        await ctx.send("You need to use !prompt first.")


bot.run(TOKEN)
