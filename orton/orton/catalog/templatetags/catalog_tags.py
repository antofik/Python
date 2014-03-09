# coding=utf-8
import os
from django import template
from catalog import REVISION
from catalog.models import CatalogCategoryModel
import settings
from classytags.arguments import Argument, MultiValueArgument
from cms.templatetags.cms_tags import Placeholder, PlaceholderOptions
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('plugins/catalog/item-details.html', takes_context=True)
def show_catalog_item(context, item, full = True):
    context.update({'item':item, 'full': full})
    return context

@register.inclusion_tag('plugins/catalog/item-details-short.html', takes_context=True)
def show_catalog_item_short(context, item):
    context.update({'item':item})
    return context

@register.inclusion_tag('plugins/catalog/menu.html', takes_context=True)
def show_catalog_menu(context, selected_category = None, full_view = True):
    categories = []
    all = CatalogCategoryModel.objects.select_related('parent').all()
    for category in all:
        category.selected = False
        category.active = False
    for category in all:
        category.full_view = full_view
        if category.name==selected_category.name:
            category.selected = True
            category.active = True
        if not category.parent:
            category.subcategories = []
            categories.append(category)
    for category in categories:
        for sub in all:
            if not sub.parent:
                continue
            if sub.parent.name==category.name:
                if sub.selected:
                    category.active = True
                category.subcategories.append(sub)
    context.update({'categories':categories})

    return context


@register.inclusion_tag('plugins/catalog/video_player.html', takes_context=True)
def show_catalog_video(context, item, size = "600x400"):
    width, height = size.split('x')
    return {'item':item, 'height':height, 'width':width, 'size':size}

@register.filter
def file_image(filename):
    media = settings.MEDIA_URL
    EXTENSION = {
        "doc": os.path.join(media, 'images/filetypes/word.png'),
        "docx":os.path.join(media, 'images/filetypes/word.png'),
        "xls": os.path.join(media, 'images/filetypes/excel.png'),
        "xlsx":os.path.join(media, 'images/filetypes/excel.png'),
        "pdf": os.path.join(media, 'images/filetypes/pdf.png'),
        "txt": os.path.join(media, 'images/filetypes/text.png'),
        "zip": os.path.join(media, 'images/filetypes/archive.png'),
        "rar": os.path.join(media, 'images/filetypes/archive.png'),
        "gz2": os.path.join(media, 'images/filetypes/archive.png'),
        "tar": os.path.join(media, 'images/filetypes/archive.png'),
    }
    DEFAULT_IMAGE = os.path.join(media, 'images/filetypes/file.png')

    ext = os.path.splitext(filename)[1][1:]
    return EXTENSION.pop(ext, DEFAULT_IMAGE)

@register.simple_tag
def revision():
    """displays the revision number

    {% revision %}"""
    return REVISION

MONTHES = (u"Январь", u"Февраль", u"Март", u"Апрель", u"Май", u"Июнь", u"Июль", u"Август", u"Сентябрь", u"Октябрь", u"Ноябрь", u"Декабрь")
IN_MONTHES = (u"В январе", u"В феврале", u"В марте", u"В апреле", u"В мае", u"В июне", u"В июле", u"В августе", u"В сентябре", u"В октябре", u"В ноябре", u"В декабре")

@register.filter
def month_name(month, short = None):
    return IN_MONTHES[int(month)] if short=="when" else MONTHES[int(month)]


class RenderPlaceholder(Placeholder):
    """
    Render the content of a placeholder to a variable.

    {% placeholder "placeholder_name" as variable_name %}
    """
    name = "render_placeholder"

    options = PlaceholderOptions(
        Argument('name', resolve=False),
        MultiValueArgument('extra_bits', required=False, resolve=False),
        'as',
        Argument('varname', resolve=False),
        blocks=[
            ('endplaceholder', 'nodelist'),
            ],
        )

    def render_tag(self, context, name, extra_bits, varname, nodelist=None):
        content = super(RenderPlaceholder, self).render_tag(context, name, extra_bits, nodelist)
        context[varname] = mark_safe(content)
        return ""

register.tag(RenderPlaceholder)