from django.http import HttpResponseRedirect


def add_to_cart(request, prod_slug, price):

    if 'cart' not in request.session:
        request.session['cart'] = {'subtotal': 0, 'count': 0}

    cart = request.session.get('cart')

    if prod_slug in cart:
        cart[prod_slug]['quantity'] += 1

    else:
        cart[prod_slug] = {
            'quantity': 1,
        }

    cart['subtotal'] += float(price)
    cart['count'] += 1

    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, prod_slug):
    cart = request.session.get('cart')

    cart[prod_slug]['quantity'] -= 1

    if cart[prod_slug]['quantity'] == 0:
        del cart[prod_slug]

    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))