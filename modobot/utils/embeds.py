import logging

import discord


async def send_error_embed(ctx, message, solution):
    logging.error("Sending error embed")
    embed = discord.Embed(
        title="Modobot",
        description="Une erreur s'est produite",
        color=discord.Color.red(),
    )

    embed.add_field(name="Message d'erreur", value=message, inline=True)
    embed.add_field(name="Solution possible", value=solution, inline=False)

    await ctx.send(embed=embed)
