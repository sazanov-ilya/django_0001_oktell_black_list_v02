from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator  # AddProductView, только для админа

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from oktell_app_black_list.forms import AddNumberForm
from oktell_app_black_list.models import BlackListNumber
from oktell_app_black_list.utils import NumbersContext


def page_not_found(request, exception):
    """ Страница не найдена (возвращаем с кодом 404) """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def index(request):
    """ Главная страница """
    # return HttpResponse('Главная страница ')
    context = {'title': 'О сайте'}
    return render(request, 'black_list/index.html', context=context)


def about(request):
    """ Домашняя страница (вызов через клмк по логотипу)
    Можно использовать как общую старницу для всего сайта"""
    return redirect('index')


# ########################
# Добавление нового номера
# ########################
# @method_decoratoor(staff_member_required, name='dispatch')  # Только для авторизованных
class AddNumberView(CreateView):
    # CreateView - базовый класс для добавления новой записи (работает с формами, в не моделями)
    """ Класс формы для страницы добавление нового продукта """
    form_class = AddNumberForm
    template_name = 'black_list/number_add.html'
    extra_context = {'title': 'Добавить номер'}  # Только статический контекст
    success_url = reverse_lazy('add_number')  # или по умолчанию get_absolute_url из модели


# #########################
# Вывод списка всех номеров
# #########################
class ShowNumbersView(NumbersContext, ListView):
    # ListView - базовый класс для отображения списков
    # NumbersContext - миксины для заказов, фийл urls.py
    """ Класс для формы списка всех номеров """
    paginate_by = 3  # Количество записей на странице
    model = BlackListNumber  # Выбирает все записи и пытается отобразить списком
    template_name = 'black_list/numbers.html'  # По умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'numbers'  # Именованный массив для шаблона (по умолчанию object_list)
    extra_context = {'title': 'Все номера'}  # , 'type_selected': 0}  # Только статический контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст (стандартная процедура) """
        # Получаем текущий контент
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu  # Пользовательский тег
        # context['title'] = 'Все номера'
        # context['status_selected'] = 0

        # !Общий код для нескольких view выносим в миксины, файл -> utils.py
        # В процедуру get_numbers_context передаем параметры странички
        # В процедуре get_numbers_context добавляем обшие параметру и возвращаем
        mixin = self.get_numbers_context(title='Все номера',
                                         type_selected=0  # Для выбора "Все номера" как активного
                                         )
        # return context  # Возвращаем контекст
        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари

    def get_queryset(self):
        """ Фильтр на список данных (стандартная процедура) """
        # Избавляемся от дублирующих запросов
        # .select_related('type')
        # - подгрузка данных связанной модели по внешнему ключу один ко многим (ForeignKey)
        # .prefetch_related('type')
        # - подгрузка данных связанной модели по внешнему ключу многие ко многим ()
        # return BlackListNumber.objects.select_related('product_unit').filter(product_is_published=True).order_by('product_name')

        return BlackListNumber.objects.select_related('type').order_by('slug')


# ###############################
# Вывод списка номеров по типу ЧС
# ###############################
# class ShowOrdersByStatusView(LoginRequiredMixin, OrderContext, ListView):
class ShowNumbersByTypeView(NumbersContext, ListView):
    # ListView - базовый класс для отображения списков
    # NumbersContext - миксины для заказов, фийл urls.py
    # LoginRequiredMixin - проверка авторизации
    """ Класс для формы списка всех заказов по выбранному статусу """
    paginate_by = 3  # Количество записей на странице
    model = BlackListNumber  # Модель данных
    template_name = 'black_list/numbers.html'  # По умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'numbers'  # Именованный массив для шаблона (по умолчанию object_list)
    # login_url = 'login'  # Адрес страницы авторизации (или в settings.py)
    allow_empty = False  # Если данных нет, то исключение 404
    # extra_context = {'title': 'Список номеров по типу ЧС'}  # Только статический контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст (стандартная процедура) """
        context = super().get_context_data(**kwargs)  # Получаем текущий контент как словарь
        # context['menu'] = menu  # Пользовательский тег
        # context['title'] = 'Номера по типу ЧС: ' + str(context['numbers'][0].type)  # Передаем в миксин
        # context['type_selected'] = context['numbers'][0].type.id)  #  Передаем в миксин

        # !Общий код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_numbers_context(title='Номера по типу ЧС: ' + str(context['numbers'][0].type),
                                         type_selected=context['numbers'][0].type.id)

        # Избавляемся от отложенных дублирующих запросов
        # status = OrderStatus.objects.get(slug=self.kwargs['status_slug'])
        # mixin = self.get_order_context(title='Заказы в статусе: ' + str(status.status_name),
        #                                status_selected=status.status_id)

        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари

    def get_queryset(self):
        """ Фильтр на список данных (стандартная процедура) """
        # Избавляемся от дублирующих запросов
        # .select_related('type')
        # - подгрузка данных связанной модели по внешнему ключу один ко многим (ForeignKey)
        # .prefetch_related('type')

        # Добавить провкрку на авторизованного пользователя
        # и для суперадминов все заказы по всем (также добавить список пользователей)

        # Чтобы с ссылке был слаг типа ЧС, а не id,
        # передаем из urls.py type_slug и по слагу получаем список номеров
        # type_slug идет из urls.py - 'numbers/<slug:type_slug>/'
        # type__slug - проверка по полю слаг slug связанной модели OrderStatus через ключ type

        # print(self.request.user.id)

        return BlackListNumber.objects.select_related('type').\
            filter(type__slug=self.kwargs['type_slug']).order_by('slug')


# #####################################
# Вывод списка номеров, поиск по номеру
# #####################################
# def show_numbers_by_search_view(request, search_number=''):
#     number = request.GET['number']
#     return HttpResponse(f'<h2>Посиск по номеру</h2><p>{number}</p>')

# class ShowOrdersByStatusView(LoginRequiredMixin, OrderContext, ListView):
class ShowNumbersBySearchView(NumbersContext, ListView):
    # ListView - базовый класс для отображения списков
    # NumbersContext - пользовательские миксины, файл urls.py
    # LoginRequiredMixin - проверка авторизации
    """ Класс для формы списка номеров по поиску """
    paginate_by = 3  # Количество записей на странице
    model = BlackListNumber  # Модель данных
    template_name = 'black_list/numbers.html'  # По умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'numbers'  # Именованный массив для шаблона (по умолчанию object_list)
    # login_url = 'login'  # Адрес страницы авторизации (или в settings.py)
    # allow_empty = False  # Если данных нет, то исключение 404
    # extra_context = {'title': 'Список номеров по типу ЧС'}  # Только статический контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст (стандартная процедура) """
        context = super().get_context_data(**kwargs)  # Получаем текущий контент как словарь
        # !Общий код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_numbers_context(title='Список номеров по шаблону: ' + self.request.GET.get('number'),
                                         )
        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари

    def get_queryset(self):
        """ Фильтр на список данных (стандартная процедура) """
        # Избавляемся от дублирующих запросов
        # .select_related('type')
        # - подгрузка данных связанной модели по внешнему ключу один ко многим (ForeignKey)
        # .prefetch_related('type')

        # return BlackListNumber.objects.all()
        # return BlackListNumber.objects.select_related('type').filter(slug__icontains=self.kwargs['search_number'])
        # get('number') -> <input name="number" ...> (из шаблона)

        return BlackListNumber.objects.select_related('type')\
            .filter(slug__icontains=self.request.GET.get('number')).order_by('slug')


# ######################
# Вывод данных по номеру
# ######################
class ShowNumberView(DetailView):
    # DetailView - базовый класс для отображения одной записи
    """ Класс формы для страницы вывода данных по номеру """
    model = BlackListNumber
    template_name = 'black_list/number.html'
    # pk_url_kwarg = "order_id"  # Для pk
    slug_url_kwarg = 'slug'  # Для слага
    # query_pk_and_slug = True
    context_object_name = 'number'  # имя переменной для шаблона (по умолчанию object_list)
    extra_context = {'title': 'Данные по номеру'}  # Только статический контекст

    # def get_context_data(self, *, object_list=None, **kwargs):
    #    """ Добавляем статический и динамический контекст """
    #    ! Общмй код для нескольких view выносим в миксины, файл -> utils.py
    #    !!! сейчас через пользовательский тег """
    #    # получаем текущий контент
    #    context = super().get_context_data(**kwargs)
    #    context['menu'] = menu
    #    context['title'] = 'Данные по номеру'
    #    context['status_selected'] = 0
    #    return context  # и возвращаем контекст


# ###############
# Удаление номера
# ###############
# def delete_number_view(request, id_number):
#     try:
#         number = BlackListNumber.objects.get(id=id_number)
#         number.delete()
#         return redirect('numbers')
#     except BlackListNumber.DoesNotExist:
#         return HttpResponseNotFound("<h4>Номер не найден</h2>")


class DeleteNumberView(NumbersContext, DeleteView):
    model = BlackListNumber
    template_name = 'black_list/number_delete.html'
    success_url = reverse_lazy('numbers')
    context_object_name = 'number'  # Имя переменной для шаблона (по умолчанию object_list)

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст (стандартная процедура) """
        context = super().get_context_data(**kwargs)  # Получаем текущий контент как словарь
        # !Общий код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_numbers_context(title='Удаление номера: ' + str(context['number'].number)
                                         )

        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари


# ############################
# Обновление даннных по номеру
# ############################
class UpdateNumberView(NumbersContext, UpdateView):
    """ Класс обновления статьи """
    # model = BlackListNumber
    form_class = AddNumberForm
    template_name = 'black_list/number_update.html'
    # fields = ['type', 'number', 'comment']
    context_object_name = 'number'  # Имя переменной для шаблона (по умолчанию object_list)

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Добавляем статический и динамический контекст (стандартная процедура) """
        context = super().get_context_data(**kwargs)  # Получаем текущий контент как словарь
        # !Общий код для нескольких view выносим в миксины, файл -> utils.py
        mixin = self.get_numbers_context(title='Редактирование номера: ' + str(context['number'].number)
                                         )

        return dict(list(context.items()) + list(mixin.items()))  # Объединяем словари

    def get_queryset(self):
        """ Фильтр на список данных (стандартная процедура) """
        return BlackListNumber.objects.select_related('type').filter(slug=self.kwargs['slug'])

