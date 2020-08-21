from django.shortcuts import render, get_object_or_404
from .models import Item
# Create your views here.

def item_list(request):
    context = {
        'items': Item.objects.all().order_by('title')
    }
    return render(request, 'shop/item_list.html', context)

def item_detail(request,pk):
    item = get_object_or_404(Item,pk=pk)
    return render(request, 'shop/item_detail.html', {'item':item})