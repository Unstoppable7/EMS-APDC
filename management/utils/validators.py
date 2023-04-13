from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def only_letters(value):
    if not (all(c.isalpha() or c.isspace() for c in value)):
        raise ValidationError(
            _('%(value)s should be just letters.'),
            params={'value': value},
        )

