# coding=utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from models import SlideshowPlugin

class SlideShowPlugin(CMSPluginBase):
    model = SlideshowPlugin
    name = _(u"Slideshow")
    render_template = "plugins/slideshow.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(SlideShowPlugin)
