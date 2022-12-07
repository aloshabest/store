from .models import OrderItem
from .forms import OrderCreateForm
from magazine.models import Product
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Order
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import os

os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
        "order_{}.pdf"'.format(order.id)
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,  'admin/orders/order/detail.html', {'order': order})


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