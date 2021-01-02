from flask import Blueprint
from flask import render_template

from modobot.forms.banappeal import NewBanAppealForm
from modobot.models.banappeal import BanAppeal
from modobot.models.userban import UserBan
from modobot.utils.france_datetime import clean_format


appeal_bp = Blueprint("appeal", __name__)


@appeal_bp.route("/appeal/<ban_id>", methods=["GET", "POST"])
def appeal_ban(ban_id: int):
    try:
        ban = UserBan.get_by_id(int(ban_id))
    except UserBan.DoesNotExist:
        return render_template(
            "banappeal/index.html",
            type="danger",
            text="Impossible de trouver l'identifiant du ban, verifiez l'URL.",
        )

    existing_banappeal = BanAppeal.get_or_none(BanAppeal.ban == ban)
    if existing_banappeal:
        if existing_banappeal.is_resolved:
            if existing_banappeal.result == "accepted":
                return render_template(
                    "banappeal/index.html",
                    type="success",
                    text="Votre appel à été accepté, vous êtes unban. À tout de suite sur https://discord.gg/amongusfr",
                )
            else:
                return render_template(
                    "banappeal/index.html",
                    type="danger",
                    text="Votre appel à été refusé.",
                )
            # TODO: DISPLAY RESOLUTION STATUS (REASON)
        else:
            return render_template(
                "banappeal/index.html",
                type="info",
                text="Appel reçu, merci de patienter et de garder ce lien pour verifier l'état de votre appel.",
            )

    form = NewBanAppealForm()
    if form.validate_on_submit():
        BanAppeal.create(ban=ban, appeal_reason=form.appeal_reason.data)
        return render_template(
            "banappeal/index.html",
            type="primary",
            text="Appel envoyé, merci de patienter et de garder ce lien pour verifier l'état de votre appel.",
        )
    return render_template(
        "banappeal/new_appeal.html",
        server_name=ban.guild.guild_name,
        ban_date=clean_format(ban.dt_banned),
        ban_reason=ban.reason,
        ban_id=ban.id,
        form=form,
    )
