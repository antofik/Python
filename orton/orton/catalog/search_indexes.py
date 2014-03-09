from haystack.indexes import *
from haystack import site
from models import CatalogItemModel


class CatalogItemIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    purpose = CharField(model_attr='purpose')
    action = CharField(model_attr='action')
    usage = CharField(model_attr='usage')
    name = CharField(model_attr='name')

    def index_queryset(self):
        return CatalogItemModel.objects.all()

site.register(CatalogItemModel, CatalogItemIndex)