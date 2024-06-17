from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='as_bootstrap')
def as_bootstrap(field: BoundField):
    return field.as_widget(attrs={"class": "form-control"})

