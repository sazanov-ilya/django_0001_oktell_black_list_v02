"""
Пользовательские теги
Для исключения дублирования кода
"""

from django import template
from django.db.models import Count

from oktell_app_black_list.models import BlackListType

register = template.Library()


# #################################### #
# Выпадающий список меню-пользователя  #
# Включающий тег ##################### #
# (Выпадающий список) ################ #
# #################################### #
@register.inclusion_tag('accounts_tags/menu_accounts.html')
def show_menu_accounts(user):

    # types = BlackListType.objects.annotate(count=Count('blacklistnumber')).order_by(sort)

    return {'user': user}

# В шаблоне вызываем как
# {% show_menu_accounts user=user %}
