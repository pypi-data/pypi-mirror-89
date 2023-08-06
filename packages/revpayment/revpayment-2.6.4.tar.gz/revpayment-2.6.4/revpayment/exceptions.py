class PaymentException(Exception):
    pass


class HttpActionError(PaymentException):
    def __init__(self, status_code, detail):
        msg = f'status_code: {status_code}, detail: {detail}'
        super().__init__(msg)
