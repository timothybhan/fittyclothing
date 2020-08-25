from django.urls import path
from . import views
from mysite import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('shirts', views.shirts_list, name='shirts_list'),
    path('sportswear', views.sportswear_list, name='sportswear_list'),
    path('outwear', views.outwear_list, name='outwear_list'),
    path('order_summary/', views.order_summary, name = 'order_summary'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('remove-one-from-cart/<int:pk>', views.remove_one_from_cart, name='remove_one_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('payment/<payment_option>', views.payment, name='payment'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'), # new
    path('success', views.success, name='success'),
    path('cancelled', views.cancelled, name='cancelled'),
    path('contact', views.contact, name='contact'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)