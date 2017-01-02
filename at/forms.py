# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField, RadioField, SelectField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, NumberRange, optional, ValidationError, Length

import re

def _check_phone_number(form, field):
    pattern = re.compile("^[0-9]+$")
    if not pattern.match(field.data):
        raise ValidationError(u'Số điện thoại không chính xác')

class BankForm(Form):
    day_logchange = TextField('Day logchange', validators=[DataRequired(message=u'Day logchange chính xác')])
    folder_logchange = TextField('Folder logchange', validators = [DataRequired(message=u'Folder logchange chính xác')])
    submit = SubmitField('Submit')
