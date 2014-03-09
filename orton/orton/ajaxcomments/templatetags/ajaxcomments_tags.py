from django import template
from django.template import Context

register = template.Library()

@register.inclusion_tag('ajaxcomments/submit_form.html')
def render_comment_form(item):
    return Context({'item':item})
