from flask_wtf          import FlaskForm
from wtforms            import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EncryptForm(FlaskForm):
    plaintext = StringField('Plaintext',
                           validators=[DataRequired()])
    encrypt   = SubmitField('Encrypt')

class DecryptForm(FlaskForm):
    cyphertext       = StringField('Cyphertext',
                           validators=[DataRequired()])
    decrypt          = SubmitField('Decrypt')