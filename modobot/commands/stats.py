import logging

from modobot import modobot_client


@modobot_client.command(brief="Statistiques du discrd")
async def stats(ctx):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    # guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    voice_channel_list = ctx.guild.voice_channels

    total = 0

    for voice_channel in voice_channel_list:
        total += len(voice_channel.members)

    # TODO:
    #  https://discordpy.readthedocs.io/en/latest/api.html?highlight=voice%20channel#discord.VoiceChannel.voice_states

    txt = """Nous sommes actuellement {total_count} dans le discord
    Il y a {voice_member_count} de connectés
    """.format(
        total_count=ctx.guild.member_count, voice_member_count=total
    )

    await ctx.channel.send(txt)

    # logging.debug("Creating action log for search")
    # new_log = ActionLog.create(
    #     moderator_name=str(ctx.author),
    #     moderator_id=ctx.author.id,
    #     user_name=str(member),
    #     user_id=member.id,
    #     action="search",
    #     comments=member.id,
    #     guild=guildsettings,
    # )
