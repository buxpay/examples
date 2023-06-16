import discord, requests, asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
api_key = ""
bot_token = ""

@bot.event
async def on_ready():
    print("Online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="donate")
async def donate(interaction: discord.Interaction, amount_of_robux: int):
    await interaction.response.send_message("Creating gamepass...",ephemeral=True)
    res = requests.post("https://buxpay.xyz/payments/create",json={"api_key":api_key,"price":int(amount_of_robux)}).json() # create an invoice
    gamepass = res["data"]["gamepass"] # gamepass id
    uid = res["data"]["uid"] #unique id for checking the status, etc.
    await interaction.edit_original_response(content=f"Please purchase this gamepass: https://www.roblox.com/game-pass/{gamepass}/")

    def check_if_bought():
      check = requests.get(f"https://buxpay.xyz/payments/info",json={"api_key":api_key,"uid":uid})
      if check.json()["data"]["status"] == "unpaid": 
          return False
      else:
          return True

    while check_if_bought() == False: # since they havent bought the gamepass yet
        await asyncio.sleep(10) # waits 10 seconds before checking again if they bought the gamepass.
    else: # since they have bought the gamepass
        # do something here (eg. give them a role), i just made it say thank you for donating.
        return await interaction.followup.send("Thank you for donating to us!",ephemeral=True)


bot.run(bot_token)
