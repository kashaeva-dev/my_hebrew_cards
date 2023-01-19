from django import forms

from .models import *
from .filters_data import topics


binyans = [('', ''),
           (1,'ПААЛЬ (шломим) - לומד'),
           (2,'ПААЛЬ (2 буквы) - גר'),
           (3,'ПААЛЬ (3-я ה) - רוצה'),
           (4,'ПААЛЬ (1-я י) - יודע'),
           (5,'ПИЭЛЬ - מדבר'),
           (6,'ХИФИЛЬ - מתחיל'),
           (7, 'ХИТПАЭЛЬ'),
           (99,'Прочие'),
            ]


periods = [('',''),
           (1, 'день'),
           (7, 'неделя'),
           (14, 'две недели'),
           (31, 'месяц'),
           ]


class NounsFilterForm(forms.Form):
    gender = forms.ChoiceField(label='Пол  ',
                               initial='',
                               required=False,
                               choices=[('', ''),
                                   ('мужской','мужской'),
                                    ('женский','женский'),
                                        ],
                               widget=forms.Select(attrs={'onchange': 'submit();'}))
    exception = forms.ChoiceField(label='Искл.:',
                                  initial='',
                                  required=False,
                                  choices=[('',''),
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