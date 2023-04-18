from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def only_letters(value,field_label):
    if not (all(c.isalpha() or c.isspace() for c in value)):
        raise ValidationError(
            _('The field "%(field_label)s" must contain only letters'),
            params={'field_label': field_label},
        )

