import datetime
import re

from discord.ext import commands

from modobot import modobot_client
from modobot.models.roleperms import RolePerms
from modobot.utils.errors import IncorrectTimeError
from modobot.utils.errors import PunishSelfError
from modobot.utils.france_datetime import datetime_now_france


class TimeConverter(commands.Converter):
    async def convert(self, ctx, time):
        matches = re.fullmatch("(\d+)([mhd])", time)  # noqa
        if not matches:
            raise IncorrectTimeError("Doit être `0000m/h/d`")
        count = int(matches[1])
        s_type = matches[2]

        if s_type == "m":
            delta = datetime.timedelta(minutes=count)
        elif s_type == "h":
            delta = datetime.timedelta(hours=count)
        elif s_type == "d":
            delta = datetime.timedelta(days=count)
        else:
            raise IncorrectTimeError("Doit être `0000m/h/d`")

        dt_unmute = datetime_now_france() + delta
        return dt_unmute


class BaseMember(commands.Converter):
    async def convert(self, ctx, member):
        member = await commands.MemberConverter().convert(
            ctx, member
        )  # gets a member object

        if member.id == modobot_client.user.id:
            raise commands.BadArgument(
                "Pourquoi me faire tant de mal, je ne suis qu'un bot :robot:"
            )

        role_names = [role.name for role in member.roles]
        for role in role_names:
            member_roleperms = RolePerms.get_or_none(name=role)
            if member_roleperms:
                break

        if not member_roleperms.is_staff:
            return member

        role_names = [role.name for role in ctx.author.roles]
        for role in role_names:
            author_roleperms = RolePerms.get_or_none(name=role)
            if author_roleperms:
                break

        if author_roleperms.can_punish_staff:
            return member
        else:
            raise PunishSelfError(
                "You cannot punish other staff members"
            )  # tells user that target is a staff member
