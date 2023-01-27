from django import forms

from .models import *
from .filters_data import topics

binyans = [('', ''),
           (1, 'ПААЛЬ (шломим) - לומד'),
           (2, 'ПААЛЬ (2 буквы) - גר'),
           (3, 'ПААЛЬ (3-я ה) - רוצה'),
           (4, 'ПААЛЬ (1-я י) - יודע'),
           (5, 'ПИЭЛЬ - מדבר'),
           (6, 'ХИФИЛЬ - מתחיל'),
           (7, 'ХИТПАЭЛЬ'),
           (99, 'Прочие'),
           ]

periods = [('', ''),
           (1, 'день'),
           (2, '2 дня'),
           (3, '3 дня'),
           (4, '4 дня'),
           (5, '5 дней'),
           (6, '6 дней'),
           (7, 'неделя'),
           (14, 'две недели'),
           (31, 'месяц'),
           ]


class NounsFilterForm(forms.Form):
    gender = forms.ChoiceField(label='Пол  ',
                               initial='',
                               required=False,
                               choices=[('', ''),
                                        ('мужской', 'мужской'),
                                        ('женский', 'женский'),
                                        ],
                               widget=forms.Select(attrs={'onchange': 'submit();'}))
    exception = forms.ChoiceField(label='Искл.:',
                                  initial='',
                                  required=False,
                                  choices=[('', ''),
                                           ('[2, 3, 99, -1]', 'искл.'),
                                           ('[100]', 'только мн.'),
                                           ],
                                  widget=forms.Select(attrs={'onchange': 'submit();'}))
    date = forms.ChoiceField(label='Добавлено',
                             initial="",
                             required=False,
                             choices=periods,
                             widget=forms.Select(attrs={'onchange': 'submit();'})
                             )


class VerbsFilterForm(forms.Form):
    binyan = forms.ChoiceField(label='Биньян  ',
                               initial='',
                               required=False,
                               choices=binyans,
                               widget=forms.Select(attrs={'onchange': 'submit();'}))
    date = forms.ChoiceField(label='Добавлено',
                             initial='',
                             required=False,
                             choices=periods,
                             widget=forms.Select(attrs={'onchange': 'submit();'})
                             )


class NounsAddForm(forms.Form):
    text = forms.CharField(label="Слово и произношение", widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))
    translation = forms.CharField(max_length=255, label="Перевод")
    animacy = forms.BooleanField(required=False, label="Одушевленный")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")
    gender = forms.ChoiceField(choices=[('мужской', 'мужской'), ('женский', 'женский')], initial='мужской', label="Пол")
    only_plural = forms.BooleanField(required=False, label="Только множественное")
    exception = forms.ChoiceField(choices=[('2', 'другое окончание'), ('-1', 'измн. первое слово'), ('0', 'не искл.')],
                                  initial=0, label="Исключение")
    type = forms.ModelChoiceField(label="Часть речи", queryset=Type.objects.filter(pk=1), initial=1,
                                  widget=forms.HiddenInput())


class VerbsAddForm(forms.Form):
    text = forms.CharField(label="Инфинитив и произношение", widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))
    word_forms_now = forms.CharField(label="Формы настоящего времени",
                                     widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))
    translation = forms.CharField(max_length=255, label="Перевод инфинитива")
    binyan = forms.ModelChoiceField(queryset=Binyan.objects.all(), label="Биньян")
    root = forms.ModelChoiceField(queryset=Root.objects.all(), label="Корень")
    type = forms.ModelChoiceField(label="Часть речи", queryset=Type.objects.filter(pk=6), initial=6,
                                  widget=forms.HiddenInput())


class BinyanAddForm(forms.ModelForm):
    class Meta:
        model = Binyan
        fields = ['type', 'name', 'output']


class RootAddForm(forms.ModelForm):
    class Meta:
        model = Root
        fields = ['name']


class AdjectivesAddForm(forms.Form):
    text = forms.CharField(label="Формы слова и их произношение", widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))
    translation = forms.CharField(max_length=255, label="Перевод слова")
    type = forms.ModelChoiceField(label="Часть речи", queryset=Type.objects.filter(pk=2), initial=2,
                                  widget=forms.HiddenInput())
    is_antonym = forms.BooleanField(required=False, label="Как антоним", initial=False)
    antonym = forms.ModelChoiceField(queryset=Word.objects.filter(type=2, is_antonym=False).order_by('picture'),
                                     required=False, label="Антоним")
    topic = forms.ModelChoiceField(queryset=Topic.objects.all().order_by('category'))


class WordsToLearnForm(forms.Form):
    date = forms.ChoiceField(label='Добавлено',
                             required=False,
                             initial='',
                             choices=periods,
                             widget=forms.Select(attrs={'onchange': 'submit();'})
                             )
    type = forms.ModelChoiceField(label='Часть речи',
                                  initial='',
                                  required=False,
                                  queryset=Type.objects.filter(
                                      pk__in=[1, 2, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]),
                                  widget=forms.Select(attrs={'onchange': 'submit();'})
                                  )
    form_type = forms.ChoiceField(label='Форма слова',
                                  choices=[('[0]', ''),
                                           ('[1]', 'начальная'),
                                           ('[1, 2, 3, 4]',
                                            'основные'),
                                           ('[6]', 'с предлогом "של"'),
                                           ('[7]', 'с предлогом "ל"'),
                                           ('[8]', 'с предлогом "ב"'),
                                           ('[9]', 'с предлогом "את"'),
                                           ],
                                  required=False,
                                  widget=forms.Select(attrs={'onchange': 'submit();'})
                                  )
    sort = forms.ChoiceField(label='Сортировка',
                             choices=[('id', 'по id'),
                                      ('?', 'перемешать'),
                                      ],
                             required=False,
                             widget=forms.Select(attrs={'onchange': 'submit();'})
                             )
