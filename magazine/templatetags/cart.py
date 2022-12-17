from django import template
from magazine.models import Product
from django.shortcuts import get_object_or_404
from coupons.forms import CouponApplyForm

register = template.Library()


@register.inclusion_tag('magazine/header_cart_tpl.html')
def header_cart_area(session):
    context = {
    }
    cart = session.get('cart', None)

    if cart:
        context['count'] = cart['count']
    return context


@register.inclusion_tag('magazine/cart_tpl.html')
def cart_area(session):
    context = {
    }
    cart = session.get('cart', None)

    if cart:
        context['cart'] = cart
        context['count'] = cart['count']

        prod = [(get_object_or_404(Product, slug=k), int(v['quantity'])) for k, v in cart.items() if k != 'subtotal' and k != 'count' and k != 'discount']
        context['prod'] = prod

        subtotal = float("{:.2f}".format(cart['subtotal']))
        discount = cart['discount']
        if discount == None:
            total = subtotal
        else:
            total = float("{:.2f}".format(subtotal - subtotal * (discount / 100)))

        context['subtotal'] = subtotal
        context['discount'] = discount
        context['total'] = total
        context['coupon_apply_form'] = CouponApplyForm()

    return context
