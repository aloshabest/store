from django.shortcuts import render, get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from magazine.models import Product
from decimal import Decimal



def order_create(request):
    cart = request.session.get('cart')

    prod = [(get_object_or_404(Product, slug=k), int(v['quantity'])) for k, v in cart.items()]

    context = {
        'cart': cart,
        'prod': prod,
    }
    subtotal = float()
    for v in cart.values():
        subtotal += v['subtotal']

    discount = float(15)
    total = subtotal - subtotal * (discount / 100)

    context['subtotal'] = subtotal
    context['discount'] = discount
    context['total'] = total

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                prod = get_object_or_404(Product, slug=item)

                OrderItem.objects.create(order=order,  product=prod, price=prod.price, quantity=cart[item]['quantity'])

            cart.clear()
            return render(request, 'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
        context['form'] = form
    return render(request, 'orders/create.html', context)