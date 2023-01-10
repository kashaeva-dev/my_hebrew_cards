from django import forms

from .models import *
from .filters_data import topics

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
                                  widget=forms.Select(attrs={'onchange': 'submit();'})
                                  )

