from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RevpaymentInvoiceConfig(AppConfig):
    name = 'revpayment.invoice'
    verbose_name = _('Invoice')
    label = 'revpayment.invoice'
