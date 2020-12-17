import datetime
import logging
import re

from discord.ext import commands

from modobot import modobot_client
from modobot.models.roleperms import RolePerms
from modobot.models.unautorized_report import UnauthorizedReport
from modobot.utils.errors import IncorrectTimeError
from modobot.utils.errors import PunishBotError
from modobot.utils.errors import PunishStaffError
from modobot.utils.france_datetime import datetime_now_france


class TimeConverter(commands.Converter):
    async def convert(self, ctx, time):
        logging.debug(f"Trying to convert {time} to datetime")
        matches = re.fullmatch("(\d+)([mhd])", time)  # noqa
        if not matches:
            logging.debug(f"No matches found for {time}")
            raise IncorrectTimeError("Doit être `0000m/h/d`")
        count = int(matches[1])
        s_type = matches[2]

        if s_type == "m":
            logging.debug("Time type is minutes")
            delta = datetime.timedelta(minutes=count)
        elif s_type == "h":
            logging.debug("Time type is hours")
            delta = datetime.timedelta(hours=count)
        elif s_type == "d":
            logging.debug("Time type is days")
            delta = datetime.timedelta(days=count)
        else:
            raise IncorrectTimeError("Doit être `0000m/h/d`")

        dt_unmute = datetime_now_france() + delta
        return dt_unmute


class BaseMember(commands.Converter):
    async def convert(self, ctx, member):
        logging.debug("Checking if member passed is not staff or bot")
        member = await commands.MemberConverter().convert(
            ctx, member
        )  # gets a member object

        if member.id == modobot_client.user.id:
            logging.debug("User tried to do action on bot")
            UnauthorizedReport.create(
                moderator_name=str(ctx.author),
                moderator_id=ctx.author.id,
                command=ctx.command,
                type="bot_action",
            )
            raise PunishBotError(
                "Pourquoi me faire tant de mal, je ne suis qu'un bot :robot:"
            )

        role_names = [role.name for role in member.roles]
        for role in role_names:
            member_roleperms = RolePerms.get_or_none(name=role)
            if member_roleperms:
                break

        if not member_roleperms or not member_roleperms.is_staff:
            logging.debug("Member is not staff or doesn't have perms, all good")
            return member

        role_names = [role.name for role in ctx.author.roles]
        for role in role_names:
            author_roleperms = RolePerms.get_or_none(name=role)
            if author_roleperms:
                break

        if author_roleperms.can_punish_staff:
            logging.debug("Author can punish staff, all good")
            return member
        else:
            logging.debug("Author cannot punish staff")
            UnauthorizedReport.create(
                moderator_name=str(ctx.author),
                moderator_id=ctx.author.id,
                command=ctx.command,
                type="staff_action",
            )
            raise PunishStaffError("Vous ne pouvez pas punir un autre membre du staff")
