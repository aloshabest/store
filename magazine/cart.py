from django.http import HttpResponseRedirect
from django.utils import timezone
from coupons.models import Coupon
from coupons.forms import CouponApplyForm
from django.shortcuts import redirect


def add_to_cart(request, prod_slug, price):

    if 'cart' not in request.session:
        request.session['cart'] = {'subtotal': 0, 'count': 0, 'discount': 0}

    cart = request.session.get('cart')

    if prod_slug in cart:
        cart[prod_slug]['quantity'] += 1

    else:
        cart[prod_slug] = {
            'quantity': 1
        }

    cart['subtotal'] += float(price)
    cart['count'] += 1
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, prod_slug, price):
    cart = request.session.get('cart')

    cart[prod_slug]['quantity'] -= 1
    cart['subtotal'] -= float(price)
    cart['count'] -= 1
    if cart[prod_slug]['quantity'] == 0:
        del cart[prod_slug]
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_coupon(request):
    cart = request.session.get('cart')
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            cart['discount'] = coupon.discount
        except:
            cart['discount'] = None

    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))