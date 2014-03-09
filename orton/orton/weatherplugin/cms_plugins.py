# coding=utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from models import Weather

class WeatherPlugin(CMSPluginBase):
    model = Weather
    name = _(u"Weather")
    render_template = "plugins/weather.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(WeatherPlugin)
