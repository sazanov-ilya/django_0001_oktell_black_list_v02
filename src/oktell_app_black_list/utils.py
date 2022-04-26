
menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Продукты', 'url_name': 'products'},
    {'title': 'Мои заказы', 'url_name': 'orders'},
    {'title': 'Новый заказ', 'url_name': 'new_order'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
 ]


class NumbersContext:
    def get_numbers_context(self, **kwargs):
        context = kwargs  # Получаем переданный контекст в параметре с локальной странички

        # Добавляем общий контекст
        # statuses = OrderStatus.objects.all()  # пользовательский тег
        # context['statuses'] = statuses
        # context['menu'] = menu  # пользовательский тег

        if 'type_selected' not in context:
            context['type_selected'] = -1  # Меню типов номера не активен ни один пункт

        return context  # Возвращаем весь контекст
