from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Item, OrderItem, Order, ShippingAddress, UserProfile
from .forms import CheckoutForm
from django.utils import timezone
from django.contrib import messages

import stripe
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new

# Create your views here.

def item_list(request):
    context = {
        'items': Item.objects.all().order_by('title')
    }
    return render(request, 'shop/item_list.html', context)

def shirts_list(request):
    context = {
        'items': Item.objects.all().filter(category="S")
    }
    return render(request, 'shop/item_list.html', context)

def sportswear_list(request):
    context = {
        'items': Item.objects.all().filter(category="SW")
    }
    return render(request, 'shop/item_list.html', context)

def outwear_list(request):
    context = {
        'items': Item.objects.all().filter(category="OW")
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
            return redirect("order_summary")
        else:
            # add a message saying the order does not contain the item
            messages.info(request, "This item was not in your cart.")
            return redirect("order_summary")
            
    else:
        # add a message saying the user doesnt have an order
        messages.info("You do not have an active order.")
        return redirect("order_summary")


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

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            order = Order.objects.get(user=request.user, ordered = False)
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order.")
            return redirect("/order_summary")
        if form.is_valid():
            print(form.cleaned_data)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            #country = form.cleaned_data.get('country')
            #state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            zipcode = form.cleaned_data.get('zipcode')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            #same_billing_address = form.cleaned_data.get('same_shipping_address')
            #save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')
            shipping_address = ShippingAddress(
                user = request.user,
                first_name = first_name,
                last_name = last_name,
                street_address = street_address,
                apartment_address = apartment_address,
                #country = country,
                #state = state,
                city = city,
                zipcode = zipcode,
                phone = phone,
                email = email,
                #same_shipping_address = same_shipping_address,
                #save_info = save_info,
                #payment_option = payment_option,
            )
            shipping_address.save()
            order.shipping_address = shipping_address
            order.save()
        print(form.cleaned_data.get('payment_option'))
        if (form.cleaned_data.get('payment_option') == 'S'):
            return redirect('/payment/stripe')
        elif (form.cleaned_data.get('payment_option') == 'P'):
            return redirect('/payment/paypal')
        else:
            return redirect('/')

    form = CheckoutForm()
    context = {
        'form': form
    }
    return render(request, 'shop/checkout.html', context)

def payment(request, payment_option):
    context = {
        'order': Order.objects.get(user=request.user, ordered = False),
    }
    
    return render(request, 'shop/payment.html', context)

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            order = Order.objects.get(user=request.user, ordered = False)
            line_items = []

            for order_item in order.items.all():
                if order_item.item.discount_price:
                    price = str(int(order_item.item.discount_price*100))
                else:
                    price = str(int(order_item.item.price*100))
                line_items.append(
                    {
                        'name':order_item.item.title,
                        'quantity':order_item.quantity,
                        'currency':'usd',
                        'amount':price,
                    }
                )
            checkout_session = stripe.checkout.Session.create(
                # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                success_url=domain_url + 'success',
                cancel_url=domain_url + 'order_summary',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items,

            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request):
    return render(request, 'shop/success.html')

def cancelled(request):
    return render(request, 'shop/cancelled.html')

@login_required
def contact(request):
    context = {
        #'user': UserProfile.objects.get(user=request.user),
    }
    
    return render(request, 'shop/contact.html', context)