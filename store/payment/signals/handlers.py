from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from orders.models import Order
from io import BytesIO
import weasyprint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint.text.fonts import FontConfiguration


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        order = get_object_or_404(Order, id=ipn_obj.invoice)

        order.paid = True
        order.save()

        subject = 'My Shop - Invoice no. {}'.format(order.id)
        message = 'Please, find attached the invoice for your recent purchase.'
        email = EmailMessage(subject, message, 'admin@myshop.com',
                             [order.email])
        html = render_to_string('orders/pdf.html', {'order': order})
        out = BytesIO()
        font_config = FontConfiguration()
        weasyprint.HTML(string=html).write_pdf(out, font_config=font_config)
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(),
                     'application/pdf')
        email.send()


valid_ipn_received.connect(payment_notification)