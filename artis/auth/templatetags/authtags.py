from django import template
from django.template import Template, RequestContext
from django.template.loader import get_template

register = template.Library()

@register.tag    
def login_control(parser, token):
    return LoginControlNode()
    
class LoginControlNode(template.Node):
    def render(self, context):
        t = get_template('login_control.html')
        html = t.render(context)
        return html