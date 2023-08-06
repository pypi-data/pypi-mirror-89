class PaymentException(Exception):
    pass


class HttpActionError(PaymentException):
    def __init__(self, status_code, detail):
        msg = f'status_code: {status_code}, detail: {detail}'
        super().__init__(msg)


class CreditNotEnough(PaymentException):
    def __init__(self, current, paid):
        msg = f'current credit: {current} not enough for paid: {paid}'
        super().__init__(msg)
