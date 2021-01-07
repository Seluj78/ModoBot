import datetime
import logging
import re

from discord.ext import commands

from modobot import modobot_client
from modobot.models.guildsettings import GuildSettings
from modobot.models.role import Role
from modobot.models.rolecategory import RoleCategory
from modobot.models.unautorized_report import UnauthorizedReport
from modobot.utils.errors import IncorrectTimeError
from modobot.utils.errors import PunishBotError
from modobot.utils.errors import PunishStaffError
from modobot.utils.errors import RoleCatDoesntExist
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


class RoleCategoryConverter(commands.Converter):
    async def convert(self, ctx, argument):
        guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)
        try:
            argument = int(argument)
        except ValueError:
            try:
                return RoleCategory.get(
                    (RoleCategory.guild == guildsettings)
                    & (RoleCategory.name == argument)
                )
            except RoleCategory.DoesNotExist:
                raise RoleCatDoesntExist("Unknow name")
        else:
            try:
                return RoleCategory.get(
                    (RoleCategory.guild == guildsettings)
                    & (RoleCategory.position == int(argument))
                )
            except RoleCategory.DoesNotExist:
                raise RoleCatDoesntExist("Unknown position")


class BaseMember(commands.Converter):
    async def convert(self, ctx, member):
        logging.debug("Checking if member passed is not staff or bot")
        member = await commands.MemberConverter().convert(
            ctx, member
        )  # gets a member object
        guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

        if member.id == modobot_client.user.id:
            logging.debug("User tried to do action on bot")
            UnauthorizedReport.create(
                moderator_name=str(ctx.author),
                moderator_id=ctx.author.id,
                command=ctx.command,
                type="bot_action",
                guild=guildsettings,
            )
            raise PunishBotError(
                "Pourquoi me faire tant de mal, je ne suis qu'un bot :robot:"
            )

        for role in member.roles:
            member_role = Role.get_or_none(role_id=role.id, guild=guildsettings)
            if member_role:
                break

        if not member_role:
            logging.debug("Member is not staff or doesn't have perms, all good")
            return member

        for role in ctx.author.roles:
            author_role = Role.get_or_none(role_id=role.id, guild=guildsettings)
            if author_role:
                break

        if not author_role:
            raise ValueError("Error getting staff role")

        if author_role.category.can_punish_staff:
            logging.debug("Author can punish staff, all good")
            return member
        else:
            logging.debug("Author cannot punish staff")
            UnauthorizedReport.create(
                moderator_name=str(ctx.author),
                moderator_id=ctx.author.id,
                command=ctx.command,
                type="staff_action",
                guild=guildsettings,
            )
            raise PunishStaffError("Vous ne pouvez pas punir un autre membre du staff")
