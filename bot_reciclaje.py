import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Diccionarios para almacenar puntos y dinero de los usuarios
puntos = {}
dinero_imaginario = {}

guia_reciclaje = {
    "plastico": "Limpialo antes de reciclarlo. Botellas, envases y bolsas van en el contenedor amarillo.",
    "vidrio": "Limpialo enjuagando los frascos o botellas de vidrio antes de reciclarlos. Depositarlo en el contenedor verde. NOTA: No reciclar vidrios rotos de ventanas, espejos o ceramicas.",
    "papel": "Limpialo y separalo, asegurandote de que el papel este limpio y seco. Doblalo o aplastalo; los papeles van en el contenedor azul.",
    "metales": "Limpialos enjuagando latas y contenedores de comida. Depositalos en el contenedor amarillo o centros de reciclaje específicos para metales.",
    "electronicos": "Llévalos a puntos de reciclaje especializados. No los deseches con la basura doméstica, ya que contienen materiales peligrosos.",
    "organicos": "Deposítalos en un contenedor marrón o compostaje. Incluye restos de comida como cáscaras de frutas y vegetales, pero evita carnes o grasas en compostaje casero."
}

preguntas_reciclaje = [
    {
        "pregunta": "¿En qué contenedor se reciclan las botellas de plástico?",
        "opciones": ["a) Azul", "b) Amarillo", "c) Verde", "d) Marrón"],
        "respuesta_correcta": "b"
    },
    {
        "pregunta": "¿Qué material NO se debe depositar en el contenedor verde?",
        "opciones": ["a) Botellas de vidrio", "b) Tarros de vidrio", "c) Vidrio roto de ventanas", "d) Frascos de perfume"],
        "respuesta_correcta": "c"
    },
    {
        "pregunta": "¿Qué debes hacer antes de reciclar una lata de refresco?",
        "opciones": ["a) Aplastar la lata", "b) Lavarla y secarla", "c) Dejarla tal cual", "d) Pintarla de amarillo"],
        "respuesta_correcta": "b"
    }
]

# Comando para ver el dinero del usuario
@bot.command()
async def dinero(ctx):
    user_id = str(ctx.author.id)
    saldo = dinero_imaginario.get(user_id, 0)
    await ctx.send(f"💰 Tu saldo de dinero imaginario es: {saldo} monedas.")

# Comando para intercambiar puntos por dinero
@bot.command()
async def cambiar(ctx, puntos_a_cambiar: int):
    user_id = str(ctx.author.id)
    
    # Verificar si el usuario tiene puntos suficientes
    if user_id not in puntos or puntos[user_id] < puntos_a_cambiar:
        await ctx.send("❌ No tienes suficientes puntos para realizar el intercambio.")
        return
    
    # Convertir puntos a dinero (por ejemplo, 1 punto = 10 monedas)
    dinero = puntos_a_cambiar * 10
    dinero_imaginario[user_id] = dinero_imaginario.get(user_id, 0) + dinero
    puntos[user_id] -= puntos_a_cambiar  # Restar los puntos que se han intercambiado

    await ctx.send(f"✅ ¡Intercambio exitoso! Has cambiado {puntos_a_cambiar} puntos por {dinero} monedas.")

# Comando para reciclar y ver guía
@bot.command()
async def reciclar(ctx, material: str):
    material = material.lower()
    if material in guia_reciclaje:
        await ctx.send(f"ℹ️ {guia_reciclaje[material]}")
    else:
        await ctx.send("❌ No tengo información sobre ese material. Intenta con otro.")

# Comando para hacer el quiz y ganar puntos
@bot.command()
async def quiz(ctx):
    pregunta = random.choice(preguntas_reciclaje)
    texto_pregunta = f"🤔 **{pregunta['pregunta']}**\n"
    for opcion in pregunta["opciones"]:
        texto_pregunta += f"{opcion}\n"

    await ctx.send(texto_pregunta)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        respuesta = await bot.wait_for("message", timeout=30.0, check=check)
        if respuesta.content.lower() == pregunta["respuesta_correcta"]:
            # Sumar puntos y dinero
            user_id = str(ctx.author.id)
            if user_id not in puntos:
                puntos[user_id] = 0
                dinero_imaginario[user_id] = 0
            puntos[user_id] += 1
            dinero_imaginario[user_id] += 10  # Por ejemplo, 10 monedas por cada punto ganado
            await ctx.send(f"✅ ¡Correcto! Haz ganado +1 punto y +10 monedas.")
        else: 
            await ctx.send(f"❌ Incorrecto. La respuesta correcta era: {pregunta['respuesta_correcta']}")
    except: 
        await ctx.send("⏰ Se acabó el tiempo para responder.")

@bot.event
async def on_ready():
    print(f"Bot de reciclaje conectado como {bot.user}")

bot.run("Token")
