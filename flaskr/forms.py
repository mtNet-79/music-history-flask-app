# mypy: ignore-errors
# from datetime import datetime, date
# from flask_wtf import FlaskForm  # type: ignore
# from wtforms import (
#     StringField, DateField, SelectField,
#     SelectMultipleField, DateTimeField,
#     BooleanField, IntegerField
# )  # type: ignore
# from wtforms.validators import (
#     ValidationError, DataRequired,
#     AnyOf, URL, Optional, InputRequired
# )  # type: ignore


# class ShowForm(FlaskForm):
#     artist_id = StringField(
#         'artist_id',
#         validators=[DataRequired()]
#     )
#     venue_id = StringField(
#         'venue_id',
#         validators=[DataRequired()]
#     )
#     start_time = DateTimeField(
#         'start_time',
#         validators=[DataRequired()],
#         default=datetime.today()
#     )


# def range_validator(form, field):

#     if not(field.data and field.data > date(1000,1,1) and field.data < date(2100,1,1)):
#         print("BAD")
#         raise ValidationError("TEST")
    # print(f"RANGE data {form} and field {field}")
    # if field.data and field.data < datetime(1000, 1, 1) or field.data > datetime(2100, 1, 1):
    #         raise ValidationError('Date out of Range')


# class ComposerForm(FlaskForm):
#     from .models import Period, Title, Composer, Performer

#     name = StringField(
#         'name', validators=[DataRequired()]
#     )
#     born = DateField('Year', validators=[DataRequired()])
#     deceased = DateField('Year', validators=[Optional()])
#     nationality = StringField(
#         'nationality', validators=[DataRequired()]
#     )
#     period = SelectField(
#         'period',
#         choices=[(period.id, period.name) for period in Period.query.all()]
#     )
#     performers = SelectField(
#         'period',
#         choices=[(performer.id, performer.name)
#                  for performer in Performer.query.all()]
#     )
#     titles = SelectField(
#         'title',
#         choices=[(title.id, title.name) for title in Title.query.all()]

#     )
#     compositions = StringField("compositions")
#     contemporaries = SelectField(
#         'contemporary',
#         choices=[(contemporary.id, contemporary.name)
#                  for contemporary in Composer.query.all()]

#     )

    # def __init__(self, genres_choices: list = None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if genres_choices:
    #         self.genres.choices = genres_choices


# class PerformerForm(FlaskForm):
#     from .models import Period, Title, Composer, Style

#     name = StringField(
#         'name', validators=[DataRequired()]
#     )
#     born = IntegerField(
#         'born', validators=[DataRequired()]
#     )
#     deceased = IntegerField(
#         'deceased', validators=[Optional()]
#     )
#     nationality = StringField(
#         'nationality', validators=[DataRequired()]
#     )
#     titles = SelectField(
#         'title',
#         choices=[(title.id, title.name) for title in Title.query.all()]
#     )

#     styles = SelectField(
#         'style',
#         choices=[(style.id, style.name) for style in Style.query.all()]

#     )
#     composers = SelectField(
#         'period',
#         choices=[(composer.id, composer.name)
#                  for composer in Composer.query.all()]
#     )
#     recordings = StringField("recordings", validators=[Optional()])
#     rating = SelectField(
#         'rating',
#         choices=[
#             (1, '1'),
#             (2, '2'),
#             (3, '3'),
#             (4, '4'),
#             (5, '5'),
#         ]
#     )


# class TitleForm(FlaskForm):
#     """form for admins to add """
#     name = StringField(
#         'name', validators=[DataRequired()]
#     )


# class NullableDateField(DateField):
#     """Native WTForms DateField throws error for empty dates.
#     Let's fix this so that we could have DateField nullable."""

#     def process_formdata(self, valuelist):
#         if valuelist:
#             date_str = ' '.join(valuelist).strip()
#             if date_str == '':
#                 self.data = None
#                 return
#             try:
#                 self.data = datetime.datetime.strptime(
#                     date_str, self.format).date()
#             except ValueError:
#                 self.data = None
#                 raise ValueError(self.gettext('Not a valid date value'))
