import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

guia_reciclaje = {
    "plastico": "Limpialo antes de reciclarlo. Botellas, envases y bolsas van en el contenedor amarillo.",
    "vidrio": "Limpialo enjuagando los frascos o botellas de vidrio antes de reciclarlos. Depositarlo en el contenedor verde. NOTA: No reciclar vidrios rotos de ventanas, espejos o ceramicas.",
    "papel": "Limpialo y separalo, asegurandote de que el papel este limpio y seco. Doblalo o aplastalo; los papeles van en el contenedor azul.",
    "metales": "Limpialos enjuagando latas y contenedores de comida. Depositalos en el contenedor amarillo o centros de reciclaje especificos para metales.",
    "electronicos": "Llevalos a puntos de reciclaje especializados. No los deseches con la basura domestica, ya que contienen materiales peligrosos.",
    "organicos": "Depositalos en un contenedor marron o compostaje. Incluye restos de comida como cáscaras de frutas y vegetales, pero evita carnes o grasas en compostaje casero."
}

@bot.event
async def on_ready():
    print(f"Bot de reciclaje conectado como {bot.user}")

@bot.command()
async def reciclar(ctx, material: str):
    material = material.lower()
    if material in guia_reciclaje:
        await ctx.send(f"ℹ️ {guia_reciclaje[material]}")
    else:
        await ctx.send("❌ No tengo información sobre ese material. Intenta con otro.")


bot.run("Token")
