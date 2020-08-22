from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib import messages
# Create your views here.

def item_list(request):
    context = {
        'items': Item.objects.all().order_by('title')
    }
    return render(request, 'shop/item_list.html', context)

@login_required
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered = False)
    except ObjectDoesNotExist:
        messages.error(request, "You do not have an active order.")
        return redirect("/")
    context = {
        'object': order
    }
    return render(request, 'shop/order_summary.html',context)

def item_detail(request,pk):
    item = get_object_or_404(Item,pk=pk)
    return render(request, 'shop/item_detail.html', {'item':item})

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order_summary")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk = pk)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("item_list")
        else:
            # add a message saying the order does not contain the item
            messages.info(request, "This item was not in your cart.")
            return redirect("item_list")
            
    else:
        # add a message saying the user doesnt have an order
        messages.info("You do not have an active order.")
        return redirect("item_list")


@login_required
def remove_one_from_cart(request, pk):
    item = get_object_or_404(Item, pk = pk)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
            else:
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
            return redirect("order_summary")
        else:
            # add a message saying the order does not contain the item
            messages.info(request, "This item was not in your cart.")
            return redirect("order_summary")
            
    else:
        # add a message saying the user doesnt have an order
        messages.info("You do not have an active order.")
        return redirect("order_summary")
