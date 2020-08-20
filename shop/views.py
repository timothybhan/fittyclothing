from django.shortcuts import render
from .models import Item
# Create your views here.

def item_list(request):
    items = Item.objects.all().order_by('title')
    return render(request, 'shop/item_list.html', {'items': items})