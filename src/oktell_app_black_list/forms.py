from django import forms
from django.core.exceptions import ValidationError

from oktell_app_black_list.models import BlackListNumber


class AddNumberForm(forms.ModelForm):
    """ Класс формы нового продукта СВЯЗАННЫЙ с моделью """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = 'Тип не выбран'

    class Meta:
        model = BlackListNumber
        # fields = '__all__'
        # fields = ['type', 'number', 'slug', 'comment']
        fields = ['type', 'number', 'comment']
        widgets = {
            'type': forms.Select(attrs={'id': 'select_type', 'required': True,
                                        'class': 'form-select form-select-sm',
                                        'aria-label': 'form-select-sm example'}),
            'number': forms.TextInput(attrs={'id': 'input_number', 'required': True,
                                             'class': 'form-control phone_mask',
                                             'data-mask': '000-000-0000',
                                             'aria-label': 'Sizing example input',
                                             'aria-describedby': 'inputGroup-sizing-sm',
                                             #'pattern': '[\+]\d{1}[\(]\d{3}[\)]\d{3}[\-]\d{4}'
                                             'pattern': '\+\d{1}\(\d{3}\)\d{3}\-\d{4}'
                                             #'pattern': '[+]\d{1}[(]\d{3}[)]\d{3}[-]\d{4}'
                                             # +7(999)999-9999
                                             }),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'id': 'input_description',
                                             'class': 'form-control',
                                             'rows': 5})
        }

    # def clean_product_name(self):
    #     """ Пользовательский валидатор
    #     начинается с clean_... """
    #     product_name = self.cleaned_data['product_name']
    #     if len(product_name) > 10:
    #         raise ValidationError('Длина превышает 10 символов')
    #     return product_name


# Не используется
class ShowNumbersBySearchForm(forms.Form):
    """ Класс формы обратной связи """
    number = forms.CharField(max_length=255,
                             widget=forms.TextInput(
                                 attrs={'id': 'number_id',
                                        'name': 'number',
                                        'type': 'search',
                                        'class': 'form-control mr-2',
                                        'placeholder': 'Введите номер для поиска',
                                        'aria-label': 'Search',
                                        }
                             ))
