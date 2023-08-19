import discord, random
from discord.ext import commands

intents = discord.Intents.all()
TOKEN = "MTE0MTk1NTg5NzE0OTYyODQ0OQ.Gz_6sJ.-aneAT4cc1yyGLDQT-uJ98-jMcy76LrL2T4eR8"
client = commands.Bot(command_prefix=".", intents=intents)

@client.event
async def on_ready():
	print("Underoos!")

@client.command()
async def rps(ctx, message):
	#input
	user_champion = message.lower()

	#roster, update when necesary. find a way to automate lol
	champ_roster = ["ironman", "captainamerica","spiderman", "thanos",
				"ultron", "drstrange", "scarletwitch"]
	ai_cnampion = random.choice(champ_roster)

	#the game logic
	if user_champion not in champ_roster:
		await ctx.send("Wait for the update to use that character")
	else:
		#tie
		if ai_cnampion == user_champion:
			await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - it's a tie!")

		#ironman
		elif ai_cnampion == "ironman":
			if user_champion == 'captainamerica' or user_champion == "ultron" or user_champion == "drstrange":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")
		#cap
		elif ai_cnampion == "captainamerica":
			if user_champion == 'spiderman' or user_champion == "thanos" or user_champion == "scarletwitch":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")
		#spiderman
		elif ai_cnampion == "spiderman":
			if user_champion == 'ironman' or user_champion == "ultron" or user_champion == "scarletwitch":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")
		#thanos
		elif ai_cnampion == "thanos":
			if user_champion == 'spiderman' or user_champion == "ironman" or user_champion == "drstrange":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")
		#ultron
		elif ai_cnampion == "ultron":
			if user_champion == 'captainamerica' or user_champion == "thanos" or user_champion == "scarletwitch":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")
		#drstrange
		elif ai_cnampion == "drstrange":
			if user_champion == 'captainamerica' or user_champion == "spiderman" or user_champion == "ultron":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")
		#scarletwitch
		elif ai_cnampion == "scarletwitch":
			if user_champion == 'ironman' or user_champion == "thanos" or user_champion == "drstrange":
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Winner!")
			else:
				await ctx.send(f"You: {user_champion} || Enemy: {ai_cnampion} - Loser!")

client.run(TOKEN)