# from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
# from rest_framework.routers import SimpleRouter

from .views import index, AddNumberView, ShowNumberView, ShowNumbersView, ShowNumbersByTypeView, \
    ShowNumbersBySearchView, DeleteNumberView, UpdateNumberView

# router = SimpleRouter()
#
# router.register(r'get_products', ProductsViewSet, basename='get_products')
# router.register(r'get_areas', AreasViewSet, basename='get_areas')
# router.register(r'get_orders', OrdersViewSet, basename='get_orders')

urlpatterns = [

    # http://127.0.0.1:8000/about/
    path('about', index, name='about'),


    # Добавить новый номер
    # http://127.0.0.1:8000/black_list/add_number/
    path('', AddNumberView.as_view(), name='add_number'),


    # Список всех номеров
    # http://127.0.0.1:8000/numbers/
    path('numbers/', ShowNumbersView.as_view(), name='numbers'),  # класс


    # Список номеров по типу ЧС
    # http://127.0.0.1:8000/numbers/general/
    # path('numbers/<int:id>/', ShowNumbersByTypeView.as_view(), name='numbers_by_types'),  # класс и id
    path('numbers/<slug:type_slug>/', ShowNumbersByTypeView.as_view(), name='numbers_by_types'),  # класс и slug


    # Список номеров, поиск по номеру
    # http://127.0.0.1:8000/search/1/
    # path('search/<str:search_number>/', show_numbers_by_search_view, name='show_numbers_by_search_view'),
    # path('search/<str:search_number>/', ShowNumbersBySearchView.as_view(), name='show_numbers_by_search_view'),  # класс и slug

    # 20220404
    # http://127.0.0.1:8000/search_by_number/?number=71
    # number -> <input name="number" ...> (из шаблона)
    # path('search/', show_numbers_by_search_view, name='show_numbers_by_search_view'),
    path('search_by_number/', ShowNumbersBySearchView.as_view(), name='show_numbers_by_search_view'),

    # path('numbers/<int:id>/', ShowNumbersByTypeView.as_view(), name='numbers_by_types'),  # класс и id
    # path('numbers/<slug:type_slug>/', ShowNumbersByTypeView.as_view(), name='numbers_by_types'),  # класс и slug


    # Вывод данных по номеру
    # http://127.0.0.1:8000/number/72222222222/
    path('number/<slug:slug>/', ShowNumberView.as_view(), name='number'),  # класс и slug


    # Удаление номера
    # http://127.0.0.1:8000/delete_number/1/
    # path('delete_number/<int:id_number>/', delete_number_view, name='delete_number'),  # процедура  и id

    # http://127.0.0.1:8000/number/72222222222/delete/
    # path('number/<slug:slug>/delete/', DeleteNumberView.as_view(), name='delete_number'),  процедура  и слаг

    # http://127.0.0.1:8000/delete_number/72222222222/
    path('delete_number/<slug:slug>/', DeleteNumberView.as_view(), name='delete_number'),  # класс


    # Обновление номера
    path('update_number/<slug:slug>/', UpdateNumberView.as_view(), name='update_number'),  # класс
]

# urlpatterns += router.urls
