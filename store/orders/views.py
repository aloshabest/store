from .models import OrderItem
from .forms import OrderCreateForm
from magazine.models import Product
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Order
from django.urls import reverse


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/detail.html',
                  {'order': order})


def order_create(request):
    cart = request.session.get('cart')

    prod = [(get_object_or_404(Product, slug=k), int(v['quantity'])) for k, v in cart.items() if k != 'subtotal' and k != 'count']

    context = {
        'cart': cart,
        'prod': prod,
    }
    subtotal = cart['subtotal']
    discount = float(15)
    total = float("{:.2f}".format(subtotal - subtotal * (discount / 100)))

    context['subtotal'] = subtotal
    context['discount'] = discount
    context['total'] = total

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                if item != 'subtotal' and item != 'count':
                    prod = get_object_or_404(Product, slug=item)

                    OrderItem.objects.create(order=order,  product=prod, price=prod.price, quantity=cart[item]['quantity'])

            cart.clear()
            order_created.delay(order.id)

            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm
        context['form'] = form
    return render(request, 'orders/create.html', context)