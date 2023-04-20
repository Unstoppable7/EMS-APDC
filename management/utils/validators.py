from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

def validate_age_limit(value):
    min_age = 18
    today = date.today()
    age_limit = today - timedelta(days=min_age*365)
    if value > age_limit:
        raise ValidationError(_("You must be over %s to continue") % min_age)

def only_letters(value,field_label):
    if not (all(c.isalpha() or c.isspace() for c in value)):
        raise ValidationError(
            _('The field "%(field_label)s" must contain only letters'),
            params={'field_label': field_label},
        )
    
def date_range(startDate,endDate,field_label1, field_label2):
    if endDate < startDate:
        raise ValidationError(
            _('Fields "%(field_label1)s" and "%(field_label2)s" must be a valid date range'),
            params={'field_label1': field_label1, 'field_label2':field_label2},
        )

