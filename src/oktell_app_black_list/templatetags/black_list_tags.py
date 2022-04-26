"""
Пользовательские теги
Для исключения дублирования кода
"""

from django import template
from django.db.models import Count

from oktell_app_black_list.forms import ShowNumbersBySearchForm
from oktell_app_black_list.models import BlackListType

register = template.Library()

# ###########
# Простой тег
# ###########

# Передает набор данных для использования в шаблоне
# Базовый вариант без параметров
@register.simple_tag(name='get_black_list_type_without_parameters')
def get_types_without_params():
    """ Список всех статусов заказа """
    return BlackListType.objects.order_by('id')

# # В шаблоне вызываем как
# {% get_black_list_type_without_parameters as black_list_type %}
# {% for black_list_typ in black_list_type %}
# <p> {{ black_list_typ }} </p>
# {% endfor %}


# ???Простой тег (с передачей параметра)
@register.simple_tag(name='get_black_list_type_with_parameters')
def get_types_with_params(filter=None):
    if not filter:
        return BlackListType.objects.order_by('id')
    else:
        return BlackListType.objects.filter(id=filter).order_by('id')


# ##############
# Включающий тег
################

# Передает шаблон-фрагмент страницы для использования в основном шаблоне
# Базовый вариант без параметров
@register.inclusion_tag('black_list_tags/list_types_test.html')
def show_types_test1():
    types = BlackListType.objects.order_by('id')

    print(types)

    return {'types': types}

# # В шаблоне вызываем как
# {% show_types_test1 %}


# # включающий тег
# # с передачей пользователя
# @register.inclusion_tag('order/order_tags/list_statuses.html')
# def show_statuses(user, sort=None, type_selected=0):
#     if not sort:
#         # statuses = OrderStatus.objects.all()
#         # statuses = OrderStatus.objects.annotate(count=Count('orders'))
#         statuses = OrderStatus.objects.filter(orders__user=user).annotate(count=Count('orders'))
#     else:
#         # statuses = OrderStatus.objects.order_by(sort)
#         # statuses = OrderStatus.objects.annotate(count=Count('orders')).order_by(sort)
#         statuses = OrderStatus.objects.filter(orders__user=user).annotate(count=Count('orders')).order_by(sort)
#
#     return {'statuses': statuses, 'status_selected': type_selected}
#
# # ===
# # - Вам нужно передать пользователя в свой тег включения.
# # @register.inclusion_tag('Kappa/sidebar.html')
# # def get_game_list(user):
# #     return {'game_list': Game.objects.all(),  'user': user}
# #
# # Затем в вашем шаблоне вызовите тег с
# # {% get_game_list user %}
# #
# # - Кроме того, вы можете установить takes_context=True в теге включения,
# # чтобы получить доступ к пользователю из контекста шаблона.
# # @register.inclusion_tag('Kappa/sidebar.html', takes_context=True)
# # def get_game_list(context):
# #     return {'game_list': Game.objects.all(),  'user': context['user']}
# #
# # В этом случае вам больше не нужно передавать пользователя в тег шаблона.
# # {% get_game_list %}
# # ===


# #################################### #
# Список-меню типов ЧС  ############## #
# Включающий тег ##################### #
# (Просто кнопка с выпадающим списком) #
# #################################### #
@register.inclusion_tag('black_list_tags/list_types.html')
def show_types(user, sort=None, type_selected=0):
    if not sort:
        # types = BlackListType.objects.all()
        # statuses = OrderStatus.objects.annotate(count=Count('orders'))
        # Список типов только авторизованного пользователя связаных с его номерами (заказами)
        # statuses = OrderStatus.objects.filter(orders__user=user).annotate(count=Count('orders'))
        types = BlackListType.objects.annotate(count=Count('blacklistnumber'))
    else:
        # types = BlackListType.objects.order_by(sort)
        # statuses = OrderStatus.objects.annotate(count=Count('orders')).order_by(sort)
        # statuses = OrderStatus.objects.filter(orders__user=user).annotate(count=Count('orders')).order_by(sort)
        types = BlackListType.objects.annotate(count=Count('blacklistnumber')).order_by(sort)

    return {'user': user, 'types': types, 'type_selected': type_selected}

# В шаблоне вызываем как
# {% show_types user=user sort='name' type_selected=type_selected %}


# @register.inclusion_tag('oktell_app_black_list/tag_list_menu.html')
# def show_menu(user, item_selected=0):
#     menu = [
#         {'title': 'О сайте', 'url_name': 'about'},
#         # {'title': 'Номера', 'url_name': 'products'},
#         {'title': 'Добавить номер', 'url_name': 'add_number'},  # еще редирект в new_product_x.html
#         # {'title': 'Мои заказы', 'url_name': 'orders'},
#         # {'title': 'Новый заказ', 'url_name': 'new_order_form'},  # еще редирект в new_order_form.html
#         # {'title': 'Обратная связь', 'url_name': 'contact'},
#     ]
#
#     # # Проверка авторизации и корректировка списка меню
#     # user_menu = menu.copy()
#     # if not user.is_authenticated:
#     #     user_menu.pop(1)  # Удаляем "Продукты"
#
#     return {'user': user, 'menu': menu, 'item_selected': item_selected}


# ##################### #
# Общее меню приложения #
# Включающий тег ###### #
# ##################### #
@register.inclusion_tag('black_list_tags/list_menu_old_20220416.html')
def show_menu_old_20220416(item_selected=0):
    menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Список номеров', 'url_name': 'numbers'},
        {'title': 'Добавить номер', 'url_name': 'add_number'},  # еще редирект в new_product_x.html
    ]

    # # Проверка авторизации и корректировка списка меню
    # user_menu = menu.copy()
    # if not user.is_authenticated:
    #     user_menu.pop(1)  # Удаляем "Продукты"

    return {'menu': menu, 'item_selected': item_selected}

# В шаблоне вызываем как
# {% show_menu %}


# Новый вариант
@register.inclusion_tag('black_list_tags/list_menu.html')
def show_menu(user, menu_selected=-1, type_selected=-1):
    # Формируем список пунктов меню
    menu = [
        {'title': 'О сайте',
         'menu_selected': 1,
         'type': 'item',
         'url_name': 'about'
         },
        {'title': 'Список номеров',
         'menu_selected': 2,
         'type': 'dropdown_types',
         'url_name': 'numbers'
         },
        {'title': 'Добавить номер',
         'menu_selected': 3,
         'type': 'item',
         'url_name': 'add_number'  # еще редирект в new_product_x.html
         },
    ]

    # Формируем список типов ЧС для выпадающего списка
    types = BlackListType.objects.annotate(count=Count('blacklistnumber')).order_by('name')

    # # Проверка авторизации и корректировка списка меню
    # user_menu = menu.copy()
    # if not user.is_authenticated:
    #     user_menu.pop(1)  # Удаляем "Продукты"

    return {'user': user,
            'menu': menu,
            'menu_selected': menu_selected,
            'types': types,
            'type_selected': type_selected
            }

# В шаблоне вызываем как
# {% show_menu user=user menu_selected=menu_selected type_selected=type_selected %}


# ######################### #
# Форма поиска по номеру ## #
# Включающий тег ########## #
# (поле для ввода и кнопка) #
# ######################### #
# https://djbook.ru/rel1.9/howto/custom-template-tags.html
# @register.inclusion_tag('black_list_tags/form_search.html', takes_context=True)
# def form_search_by_number(context):
@register.inclusion_tag('black_list_tags/form_search_old_20220416.html')
def form_search_by_number_old_20220416(link, btn_title):
    # # Проверка авторизации и корректировка списка меню
    # user_menu = menu.copy()
    # if not user.is_authenticated:
    #     user_menu.pop(1)  # Удаляем "Продукты"

    # Пример подключения формы
    # form = ShowNumbersBySearchForm
    # return {'form': form, 'link': link, 'btn_title': btn_title}

    return {'link': link, 'btn_title': btn_title}


@register.inclusion_tag('black_list_tags/form_search.html')
def form_search_by_number(link, btn_title):
    # # Проверка авторизации и корректировка списка меню
    # user_menu = menu.copy()
    # if not user.is_authenticated:
    #     user_menu.pop(1)  # Удаляем "Продукты"

    # Пример подключения формы
    # form = ShowNumbersBySearchForm
    # return {'form': form, 'link': link, 'btn_title': btn_title}

    return {'link': link, 'btn_title': btn_title}



