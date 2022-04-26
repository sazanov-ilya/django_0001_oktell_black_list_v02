# from django.conf.urls import url
from django.contrib import admin
# from rest_framework.routers import SimpleRouter
from django.urls import path, include, re_path
from oktell_app_black_list.views import index


# router = SimpleRouter()
#
# router.register(r'get_products', ProductsViewSet, basename='get_products')
# router.register(r'get_areas', AreasViewSet, basename='get_areas')
# router.register(r'get_orders', OrdersViewSet, basename='get_orders')


urlpatterns = [
    path('admin/', admin.site.urls),

    # !URL маршруты для системы аутентификации (авторизации)
    # Как отмечается в документации к LoginView,
    # по умолчанию Django будет искать файл login.html в папке registration.
    # Таким образом, нам нужно создать новую директорию под названием registration,
    # а внутри нее создать необходимый HTML файл шаблона
    # templates/registration/login.html
    # ! Отдельно создавать View НЕ нужно
    # ! Но нужно в "settings.py" прописать страницу для переадресации "LOGIN_REDIRECT_URL = 'home"
    # http://127.0.0.1:8000/accounts/login/
    path('accounts/', include('django.contrib.auth.urls')),

    # !URL маршруты приложение черного списка
    path('', include('oktell_app_black_list.urls')),

    # url('', include('social_django.urls', namespace='social')),
    # path('auth/', auth, name='auth/'),

    # path('', index, name='index'),  # http://127.0.0.1:8000/black_list/
    # path('black_list/', include('oktell_app_black_list.urls')),
    # path('black_list/', include('oktell_app_black_list.urls'))  # http://127.0.0.1:8000/black_list/

]

# urlpatterns += router.urls