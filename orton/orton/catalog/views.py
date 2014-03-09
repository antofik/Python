# coding=utf-8
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from models import *
from cms.utils.page_resolver import get_page_from_request
import settings

def category(request, name=None):
    selected_category = CatalogCategoryModel.objects.filter(name=name)[:1]
    if not selected_category and CatalogCategoryModel.objects.count()>0:
        selected_category = CatalogCategoryModel.objects.filter(parent=None).order_by('orderindex', 'name').all()[:1]
    items = get_items(selected_category)

    selected_category = selected_category[0] if selected_category else None
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/category.html', {'selected_category':selected_category, 'items': items, 'current_page':page}, context_instance=RequestContext(request))

def image_category(request, name=None):
    selected_category = CatalogCategoryModel.objects.filter(name=name)[:1]
    if not selected_category and CatalogCategoryModel.objects.count()>0:
        selected_category = CatalogCategoryModel.objects.filter(parent=None).order_by('orderindex', 'name').all()[:1]
    items = get_items(selected_category)

    selected_category = selected_category[0] if selected_category else None
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/image_category.html', {'selected_category':selected_category, 'items': items, 'current_page':page}, context_instance=RequestContext(request))

def item(request, name=None):
    selected_item = CatalogItemModel.objects.filter(name=name)[:1]
    selected_item = selected_item[0] if len(selected_item)>0 else None
    selected_category = selected_item.category if selected_item else []
    items = get_items([selected_category] if selected_item else [])

    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/item.html', {'items':items, 'selected_category': selected_category, 'selected_item':selected_item, 'current_page':page}, context_instance=RequestContext(request))

def video_catalog(request):
    items = CatalogVideoModel.objects.all()
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/video_catalog.html', {'items':items, 'current_page':page}, context_instance=RequestContext(request))

def video_item(request, id):
    item = get_object_or_404(CatalogVideoModel, pk=id)
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/video_item.html', {'item':item, 'current_page':page}, context_instance=RequestContext(request))

def articles_list(request):
    items = CatalogArticleModel.objects.all()
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/articles_list.html', {'items':items, 'current_page':page}, context_instance=RequestContext(request))

def articles_item(request, id):
    item = get_object_or_404(CatalogArticleModel, pk=id)
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/articles_item.html', {'item':item, 'current_page':page}, context_instance=RequestContext(request))

def news_list(request):
    items = CatalogNewsModel.objects.all()
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/news_list.html', {'items':items, 'current_page':page}, context_instance=RequestContext(request))

def news_item(request, id):
    item = get_object_or_404(CatalogNewsModel, pk=id)
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/news_item.html', {'item':item, 'current_page':page}, context_instance=RequestContext(request))

def advices_list(request):
    items = CatalogAdviceModel.objects.all()
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/advices_list.html', {'items':items, 'current_page':page}, context_instance=RequestContext(request))

def advices_item(request, id):
    item = get_object_or_404(CatalogAdviceModel, pk=id)
    page = get_page_from_request(request)
    return render_to_response('plugins/catalog/advices_item.html', {'item':item, 'current_page':page}, context_instance=RequestContext(request))

def get_categories():
    """
     Returns grouped list of categories/subcategories and item
    """
    categories = []

    all = CatalogCategoryModel.objects.select_related("description_page").all()
    for category in all:
        if not category.parent:
            categories.append(category)
    return categories, all


def get_items(categories):
    """
    Returns items from given categories
    """
    if len(categories)==0:
        return []
    items = []
    for category in categories:
        for item in category.items.all():
            items.append(item)
        items.extend(get_items(category.children.all()))
    return items


def send_feedback_notification(feedback):
    try:
        emails = FeedbackModel.options.emails.split(',')
        send_mail("[orton.ru] Оставлен отзыв с просьбой перезвонить", "%s\n\n%s\n\n%s" % (feedback.name, feedback.phone, feedback.comment), "feedback@orton.ru", emails)
    except Exception, e:
        print 'Email error:', str(e)


def feedback(request):
    try:
        if request.method=="POST":
            name = request.POST.get("name", u"Неизвестный")
            phone = request.POST.get("phone", u"")
            comment = request.POST.get("comment", u"")
            recall = request.POST.get("recall", False)
            feedback = FeedbackModel()
            feedback.name = name
            feedback.phone = phone
            feedback.comment = comment
            feedback.recall = recall
            feedback.save()
            if feedback.recall:
                send_feedback_notification(feedback)
        else:
            raise Http404
    except Exception, e:
        print 'Feedback error:', str(e)
    return HttpResponse("ok")