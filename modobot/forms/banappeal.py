from flask_wtf import FlaskForm
from wtforms import fields
from wtforms import validators


class NewBanAppealForm(FlaskForm):
    appeal_reason = fields.TextAreaField(validators=[validators.DataRequired()])
    checkbox = fields.BooleanField(validators=[validators.DataRequired()])
