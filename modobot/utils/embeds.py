import discord


async def send_error_embed(ctx, message, solution):
    embed = discord.Embed(
        title="Modobot", description="An error has occured", color=discord.Color.red()
    )

    embed.add_field(name="Error Message", value=message, inline=True)
    embed.add_field(name="Possible solution", value=solution, inline=False)

    await ctx.send(embed=embed)
