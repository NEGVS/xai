from DateUtils import DateUtils


class OrderDateService:
    def __init__(self):
        self.order_date_format = '%Y-%m-%d'


if __name__ == '__main__':
    order_service = OrderDateService()

    print(DateUtils.get_date())
