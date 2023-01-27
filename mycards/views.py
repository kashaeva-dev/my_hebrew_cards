import datetime as dt
import os.path
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pymorphy2
import wordcloud
from bidi.algorithm import get_display
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView

from .forms import *
from .functions import *

morph = pymorphy2.MorphAnalyzer()


# Create your views here.
def cards_main(request):
    today = dt.datetime.now()
    D1 = dt.timedelta(days=3)
    date_limit = today - D1
    new_words = Word.objects.all().order_by('-time_create')[:50]
    words = [" ".join([word.picture.split('.')[0], get_display(word.name)]) for word in new_words]


    # Create an empty dictionary
    word_freq = {}
    # Iterate over the list of words
    for word in words:
        # Assign a random frequency between 1 and 50
        freq = random.randint(1, 50)
        # Add the word and frequency to the dictionary
        word_freq[word] = freq

    cake_mask = np.array(plt.imread(os.path.join(settings.BASE_DIR, 'mycards/static/img/мысль2.jpeg')))

    cloud = wordcloud.WordCloud(font_path=os.path.join(settings.BASE_DIR, 'mycards/static/img/Arimo-Regular.ttf'), mask=cake_mask,
                                background_color='#FFFFFF', colormap='Blues', max_words=40, min_font_size=12, font_step=2, width=1800,
                                height=1600, prefer_horizontal=0.8).generate_from_frequencies(word_freq)



    cloud.to_file(os.path.join(settings.BASE_DIR, 'mycards/static/img/wordcloud.png'))

    
    return render(request, "mycards/cards.html", {'title': 'ГЛАВНАЯ'})


def cards_verbs(request):
    verbs = Word.objects.filter(type_id=6, printed=0)
    verbs_info = []
    type = Type.objects.all()
    form_type = FormType.objects.all()
    for verb in verbs:
        verb_info = dict()
        verb_info['name'] = verb.name
        verb_info['picture'] = verb.picture
        for form in verb.forms.all():
            if form.form_type == form_type[0]:
                verb_info['vocal_name'] = form.vocal_name
                verb_info['translation'] = form.translation
                verb_info['pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'мужской' and form.number == 'единственное':
                verb_info['m1_name'] = form.vocal_name
                verb_info['m1_pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'мужской' and form.number == 'множественное':
                verb_info['m2_name'] = form.vocal_name
            elif form.time == 'настоящее' and form.gender == 'женский' and form.number == 'единственное':
                verb_info['f1_name'] = form.vocal_name
                verb_info['f1_pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'женский' and form.number == 'множественное':
                verb_info['f2_name'] = form.vocal_name
        verb_info['binyan_id'] = verb.binyan.pk
        verb_info['binyan_name'] = verb.binyan.name
        verb_info['binyan_type'] = verb.binyan.type
        verbs_info.append(verb_info)
    return render(request, "mycards/verbs_print.html", {'verbs_info': verbs_info, 'title': 'ГЛАГОЛЫ'})


def table_nouns_exceptions(request):
    nouns = Word.objects.filter(type_id=1, animacy='inan')
    nouns_info = []
    only_1form = []
    type = Type.objects.all()
    form_type = FormType.objects.all()
    for noun in nouns:
        for nform in noun.forms.all():
            if nform.exception != 0 and nform.exception != 100:
                noun_info = dict()
                noun_info['exception'] = nform.exception
                forms = noun.forms.all()
                for form in forms:
                    if form.form_type == form_type[0]:
                        noun_info['name'] = form.vocal_name
                        noun_info['translation'] = form.translation
                        noun_info['pronunciation'] = form.pronunciation
                        noun_info['gender'] = form.gender
                        noun_info['number'] = form.number
                        noun_info['picture'] = noun.picture
                    elif form.form_type == form_type[1]:
                        noun_info['2form_name'] = form.vocal_name
                        noun_info['2form_translation'] = form.translation
                        noun_info['2form_pronunciation'] = form.pronunciation
                nouns_info.append(noun_info)
            elif nform.exception == 100:
                only_1form_info = dict()
                only_1form_info['name'] = nform.vocal_name
                only_1form_info['translation'] = nform.translation
                only_1form_info['pronunciation'] = nform.pronunciation
                only_1form_info['gender'] = nform.gender
                only_1form_info['number'] = nform.number
                only_1form_info['picture'] = noun.picture
                only_1form.append(only_1form_info)
    nouns_info = sorted(nouns_info, key=lambda noun: [noun['gender'], noun['translation']], reverse=False)
    return render(request, "mycards/nouns_exсeptions.html", {'nouns_info': nouns_info, 'only_1form': only_1form, 'title': 'ИСКЛЮЧЕНИЯ'})


def question_words(request):
    questions = Word.objects.filter(type_id=18)
    questions_info = []
    form_type = FormType.objects.all()
    for question in questions:
        question_info = dict()
        expressions_info = []
        other_forms = []
        question_info['picture'] = question.picture
        for question_form in question.forms.all():
            if question_form.form_type == form_type[0]:
                question_info['name'] = question_form.vocal_name
                question_info['translation'] = question_form.translation
                question_info['pronunciation'] = question_form.pronunciation
                question_info['gender'] = question_form.gender
                question_info['number'] = question_form.number
            else:
                other_form = dict()
                other_form['name'] = question_form.vocal_name
                other_form['translation'] = question_form.translation
                other_form['pronunciation'] = question_form.pronunciation
                other_form['gender'] = question_form.gender
                other_form['number'] = question_form.number
                other_forms.append(other_form)
        for expression in question.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        question_info['other_forms'] = other_forms
        question_info['expressions'] = expressions_info
        questions_info.append(question_info)
    questions_info = sorted(questions_info, key=lambda word: word['translation'], reverse=True)
    return render(request, "mycards/questions.html", {'questions_info': questions_info, 'title': 'ВОПРОСЫ'})


def adjectives(request):
    topics = Topic.objects.exclude(pk=0)

    adjectives = Word.objects.filter(type_id=2, is_antonym=1)
    adjectives_info = []
    form_type = FormType.objects.all()
    for adjective in adjectives:
        adjective_info = dict()
        expressions_info = []
        other_forms = []
        antonyms = []
        if Path(os.path.join(settings.BASE_DIR, 'mycards/static/img', adjective.picture)).exists():
            adjective_info['picture'] = adjective.picture
        else:
            adjective_info['picture'] = 'нет фото.jpg'
        adjective_info['id'] = adjective.pk
        for form in adjective.forms.all():
            if form.form_type == form_type[0]:
                adjective_info['name'] = form.vocal_name
                adjective_info['translation'] = form.translation
                adjective_info['pronunciation'] = form.pronunciation
            elif form.gender == 'мужской' and form.number == 'множественное':
                adjective_info['m2_name'] = form.vocal_name
                adjective_info['m2_translation'] = form.translation
                adjective_info['m2_pronunciation'] = form.pronunciation
            elif form.gender == 'женский' and form.number == 'единственное':
                adjective_info['f1_name'] = form.vocal_name
                adjective_info['f1_pronunciation'] = form.pronunciation
            elif form.gender == 'женский' and form.number == 'множественное':
                adjective_info['f2_name'] = form.vocal_name
                adjective_info['f2_pronunciation'] = form.pronunciation
            else:
                other_form = dict()
                other_form['name'] = form.vocal_name
                other_form['translation'] = form.translation
                other_form['pronunciation'] = form.pronunciation
                other_form['gender'] = form.gender
                other_form['number'] = form.number
                other_forms.append(other_form)
        for expression in adjective.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        antonym = adjective.antonym.first()
        antonym_info = dict()
        if antonym != None:
            if Path(os.path.join("C:\Django\Django_hebrew_new_cards\cards_project\static\mycards\img",
                                 antonym.picture)).exists():
                antonym_info['picture'] = antonym.picture
            else:
                antonym_info['picture'] = 'нет фото.jpg'
            aother_forms = []
            antonym_info['id'] = antonym.pk
            for aform in antonym.forms.all():
                if aform.form_type == form_type[0]:
                    antonym_info['name'] = aform.vocal_name
                    antonym_info['translation'] = aform.translation
                    antonym_info['pronunciation'] = aform.pronunciation
                elif aform.gender == 'мужской' and aform.number == 'множественное':
                    antonym_info['m2_name'] = aform.vocal_name
                    antonym_info['m2_translation'] = aform.translation
                    antonym_info['m2_pronunciation'] = aform.pronunciation
                elif aform.gender == 'женский' and aform.number == 'единственное':
                    antonym_info['f1_name'] = aform.vocal_name
                    antonym_info['f1_pronunciation'] = aform.pronunciation
                elif aform.gender == 'женский' and aform.number == 'множественное':
                    antonym_info['f2_name'] = aform.vocal_name
                    antonym_info['f2_pronunciation'] = aform.pronunciation
                else:
                    aother_form = dict()
                    aother_form['name'] = aform.vocal_name
                    aother_form['translation'] = aform.translation
                    aother_form['pronunciation'] = aform.pronunciation
                    aother_form['gender'] = aform.gender
                    aother_form['number'] = aform.number
                    aother_forms.append(aother_form)
                antonym_info['aother_forms'] = aother_forms
        adjective_info['antonyms'] = antonym_info
        adjective_info['other_forms'] = other_forms
        adjective_info['expressions'] = expressions_info
        adjectives_info.append(adjective_info)


    return render(request, "mycards/adjectives.html", {'adjectives_info': adjectives_info, 'topics': topics, 'title': 'ПРИЛАГАТЕЛЬНЫЕ'})


def adjectives_filter(request, topic):
    topics = Topic.objects.exclude(pk=0)

    adjectives = Word.objects.filter(type_id=2, is_antonym=0)
    adjectives = adjectives.filter(topic=topic)
    adjectives_info = []
    form_type = FormType.objects.all()
    for adjective in adjectives:
        adjective_info = dict()
        expressions_info = []
        other_forms = []
        antonyms = []
        if Path(os.path.join(settings.BASE_DIR, 'mycards/static/img', adjective.picture)).exists():
            adjective_info['picture'] = adjective.picture
        else:
            adjective_info['picture'] = 'нет фото.jpg'
        adjective_info['id'] = adjective.pk
        for form in adjective.forms.all():
            if form.form_type == form_type[0]:
                adjective_info['name'] = form.vocal_name
                adjective_info['translation'] = form.translation
                adjective_info['pronunciation'] = form.pronunciation
            elif form.gender == 'мужской' and form.number == 'множественное':
                adjective_info['m2_name'] = form.vocal_name
                adjective_info['m2_translation'] = form.translation
                adjective_info['m2_pronunciation'] = form.pronunciation
            elif form.gender == 'женский' and form.number == 'единственное':
                adjective_info['f1_name'] = form.vocal_name
                adjective_info['f1_pronunciation'] = form.pronunciation
            elif form.gender == 'женский' and form.number == 'множественное':
                adjective_info['f2_name'] = form.vocal_name
                adjective_info['f2_pronunciation'] = form.pronunciation
            else:
                other_form = dict()
                other_form['name'] = form.vocal_name
                other_form['translation'] = form.translation
                other_form['pronunciation'] = form.pronunciation
                other_form['gender'] = form.gender
                other_form['number'] = form.number
                other_forms.append(other_form)
        for expression in adjective.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        antonym = adjective.antonym.first()
        antonym_info = dict()
        if antonym != None:
            if Path(os.path.join("C:\Django\Django_hebrew_new_cards\cards_project\static\mycards\img",
                                 antonym.picture)).exists():
                antonym_info['picture'] = antonym.picture
            else:
                antonym_info['picture'] = 'нет фото.jpg'
            aother_forms = []
            antonym_info['id'] = antonym.pk
            for aform in antonym.forms.all():
                if aform.form_type == form_type[0]:
                    antonym_info['name'] = aform.vocal_name
                    antonym_info['translation'] = aform.translation
                    antonym_info['pronunciation'] = aform.pronunciation
                elif aform.gender == 'мужской' and aform.number == 'множественное':
                    antonym_info['m2_name'] = aform.vocal_name
                    antonym_info['m2_translation'] = aform.translation
                    antonym_info['m2_pronunciation'] = aform.pronunciation
                elif aform.gender == 'женский' and aform.number == 'единственное':
                    antonym_info['f1_name'] = aform.vocal_name
                    antonym_info['f1_pronunciation'] = aform.pronunciation
                elif aform.gender == 'женский' and aform.number == 'множественное':
                    antonym_info['f2_name'] = aform.vocal_name
                    antonym_info['f2_pronunciation'] = aform.pronunciation
                else:
                    aother_form = dict()
                    aother_form['name'] = aform.vocal_name
                    aother_form['translation'] = aform.translation
                    aother_form['pronunciation'] = aform.pronunciation
                    aother_form['gender'] = aform.gender
                    aother_form['number'] = aform.number
                    aother_forms.append(aother_form)
                antonym_info['aother_forms'] = aother_forms
        adjective_info['antonyms'] = antonym_info
        adjective_info['other_forms'] = other_forms
        adjective_info['expressions'] = expressions_info
        adjectives_info.append(adjective_info)

    adjectives_info = sorted(adjectives_info, key=lambda word: word['translation'], reverse=False)
    return render(request, "mycards/adjectives.html", {'adjectives_info': adjectives_info, 'topics': topics, 'title': 'ПРИЛАГАТЕЛЬНЫЕ'})


def nouns_all(request):
    today = dt.datetime.now()
    D1 = dt.timedelta(days=1)
    yesterday = today - D1
    nouns = Word.objects.filter(type_id=1)
    form1 = NounsFilterForm(request.GET)
    if form1.is_valid():
        if form1.cleaned_data["gender"]:
            nouns = nouns.filter(forms__gender=form1.cleaned_data['gender']).distinct()
        if form1.cleaned_data['exception']:
            lst = list(map(int, form1.cleaned_data['exception'].strip('[]').split(', ')))
            nouns = nouns.filter(forms__exception__in=lst).distinct()
        if form1.cleaned_data["date"]:
            DD = dt.timedelta(days=int(form1.cleaned_data['date']))
            earlier = today - DD
            if int(form1.cleaned_data['date']) == "":
                nouns = Word.objects.filter(type_id=1)
            else:
                nouns = nouns.filter(time_create__gt=earlier)
    nouns_info = []
    form_type = FormType.objects.all()
    classes = Classes.objects.all()
    classes_info = []
    for class_ in classes:
        class_info = dict()
        class_info['pk'] = class_.pk
        class_info['name'] = class_.name
        class_info['icon'] = class_.icon
        cats = class_.categories.all()
        cats_ids_form = []  # формирующиеся айди подкатегорий, выбранной категории
        cats_info = []
        for cat in cats:
            cat_info = dict()
            cat_info['id'] = cat.pk
            cat_info['name'] = cat.name
            cat_info['icon'] = cat.icon
            cats_info.append(cat_info)
            cats_ids_form.append(cat.pk)
        class_info['cats_ids_form'] = cats_ids_form
        class_info['cats_info'] = cats_info
        classes_info.append(class_info)
    for noun in nouns:
        noun_info = dict()
        expressions_info = []
        other_forms = []
        antonyms = []
        noun_info['id'] = noun.pk
        noun_info['animacy'] = noun.animacy
        if Path(os.path.join(settings.BASE_DIR, 'mycards/static/img', noun.picture)).exists():
            noun_info['picture'] = noun.picture
        else:
            noun_info['picture'] = 'нет фото.jpg'
        for form in noun.forms.all():
            if form.form_type == form_type[0]:
                noun_info['name'] = form.vocal_name
                noun_info['translation'] = form.translation
                noun_info['pronunciation'] = form.pronunciation
                noun_info['gender'] = form.gender
                noun_info['number'] = form.number
                noun_info['main'] = form.number
                noun_info['exception'] = form.exception
            elif form.form_type == form_type[1]:
                noun_info['n2_name'] = form.vocal_name
                noun_info['n2_translation'] = form.translation
                noun_info['n2_pronunciation'] = form.pronunciation
                noun_info['n2_exception'] = form.exception
            else:
                other_form = dict()
                other_form['name'] = form.vocal_name
                other_form['translation'] = form.translation
                other_form['pronunciation'] = form.pronunciation
                other_form['gender'] = form.gender
                other_form['number'] = form.number
                other_forms.append(other_form)
        for expression in noun.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        noun_info['other_forms'] = other_forms
        noun_info['expressions'] = expressions_info
        nouns_info.append(noun_info)

    return render(request, "mycards/nouns_all.html", {'nouns_info': nouns_info,
                                                'form1': form1,
                                                'classes': classes_info,
                                                'title': 'СУЩЕСТВИТЕЛЬНЫЕ',
                                                  })


def nouns_filter(request, cats_ids):
    nouns = Word.objects.filter(type_id=1).exclude(topic=2)

    form1 = NounsFilterForm(request.GET)

    nouns_info = []
    cats_ids = list(map(int, cats_ids.strip('[]').split(', ')))
    classes = Classes.objects.all()
    classes_info = []
    for class_ in classes:
        class_info = dict()
        class_info['pk'] = class_.pk
        class_info['name'] = class_.name
        class_info['icon'] = class_.icon
        cats = class_.categories.all()
        cats_ids_form = []  # формирующиеся айди подкатегорий, выбранной категории
        cats_info = []
        for cat in cats:
            cat_info = dict()
            cat_info['id'] = cat.pk
            cat_info['name'] = cat.name
            cat_info['icon'] = cat.icon
            cats_info.append(cat_info)
            cats_ids_form.append(cat.pk)
        class_info['cats_ids_form'] = cats_ids_form
        class_info['cats_info'] = cats_info
        classes_info.append(class_info)

    nouns = nouns.filter(categories__in=cats_ids).distinct()
    if form1.is_valid():
        if form1.cleaned_data["gender"]:
            nouns = nouns.filter(forms__gender=form1.cleaned_data['gender']).distinct()
        if form1.cleaned_data['exception']:
            lst = list(map(int, form1.cleaned_data['exception'].strip('[]').split(', ')))
            nouns = nouns.filter(forms__exception__in=lst).distinct()
        if form1.cleaned_data["date"]:
            today = dt.datetime.now()
            DD = dt.timedelta(days=int(form1.cleaned_data['date']))
            earlier = today - DD
            nouns = nouns.filter(time_create__gt=earlier)

    form_type = FormType.objects.all()
    for noun in nouns:
        noun_info = dict()
        noun_info['id'] = noun.pk
        expressions_info = []
        other_forms = []
        antonyms = []
        noun_info['animacy'] = noun.animacy
        if Path(os.path.join(settings.BASE_DIR, 'mycards/static/img', noun.picture)).exists():
            noun_info['picture'] = noun.picture
        else:
            noun_info['picture'] = 'нет фото.jpg'
        for form in noun.forms.all():
            if form.form_type == form_type[0]:
                noun_info['name'] = form.vocal_name
                noun_info['translation'] = form.translation
                noun_info['pronunciation'] = form.pronunciation
                noun_info['gender'] = form.gender
                noun_info['number'] = form.number
                noun_info['main'] = form.number
                noun_info['exception'] = form.exception
            elif form.form_type == form_type[1]:
                noun_info['n2_name'] = form.vocal_name
                noun_info['n2_translation'] = form.translation
                noun_info['n2_pronunciation'] = form.pronunciation
                noun_info['n2_exception'] = form.exception
            else:
                other_form = dict()
                other_form['name'] = form.vocal_name
                other_form['translation'] = form.translation
                other_form['pronunciation'] = form.pronunciation
                other_form['gender'] = form.gender
                other_form['number'] = form.number
                other_forms.append(other_form)
        for expression in noun.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        noun_info['other_forms'] = other_forms
        noun_info['expressions'] = expressions_info
        nouns_info.append(noun_info)

    nouns_info = sorted(nouns_info, key=lambda word: word['translation'], reverse=False)
    return render(request, "mycards/nouns.html", {'nouns_info': nouns_info,
                                                  'form1': form1,
                                                  'cats_ids': cats_ids,
                                                  'classes': classes_info,
                                                  'title': 'СУЩЕСТВИТЕЛЬНЫЕ',
                                                  })


def verbs_all(request):
    # Формируем список биньянов
    binyans = Binyan.objects.exclude(pk=99)

    verbs_form = VerbsFilterForm(request.GET)

    # Формируем словарь с данными по каждому глаголу:
    verbs = Word.objects.filter(type_id=6)


    if verbs_form.is_valid():
        if verbs_form.cleaned_data["binyan"]:
            verbs = verbs.filter(binyan__pk=verbs_form.cleaned_data['binyan']).distinct()
        if verbs_form.cleaned_data["date"]:
            today = dt.datetime.now()
            DD = dt.timedelta(days=int(verbs_form.cleaned_data['date']))
            earlier = today - DD
            verbs = verbs.filter(time_create__gt=earlier)

    verbs_info = []
    form_type = FormType.objects.all()[0]
    for verb in verbs:
        verb_info = dict()
        verb_info['name'] = verb.name
        verb_info['picture'] = verb.picture
        for form in verb.forms.all():
            if form.form_type == form_type:
                verb_info['vocal_name'] = form.vocal_name
                verb_info['translation'] = form.translation
                verb_info['pronunciation'] = form.pronunciation
                verb_info['preps'] = form.example
            elif form.time == 'настоящее' and form.gender == 'мужской' and form.number == 'единственное':
                verb_info['m1_name'] = form.vocal_name
                verb_info['m1_pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'мужской' and form.number == 'множественное':
                verb_info['m2_name'] = form.vocal_name
            elif form.time == 'настоящее' and form.gender == 'женский' and form.number == 'единственное':
                verb_info['f1_name'] = form.vocal_name
                verb_info['f1_pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'женский' and form.number == 'множественное':
                verb_info['f2_name'] = form.vocal_name
        verb_info['id'] = verb.pk
        verb_info['binyan_id'] = verb.binyan.pk
        verb_info['binyan_name'] = verb.binyan.name
        verb_info['binyan_type'] = verb.binyan.type
        verb_info['binyan_output'] = verb.binyan.output
        expressions_info = []
        for expression in verb.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        verb_info['expressions'] = expressions_info
        verbs_info.append(verb_info)

    verbs_info = sorted(verbs_info, key=lambda word: word['translation'], reverse=False)
    return render(request, "mycards/verbs.html", {'verbs_info': verbs_info,
                                                  'binyans': binyans,
                                                  'form_type': form_type,
                                                  'form': verbs_form,
                                                  'title': 'ГЛАГОЛЫ',
                                                  })


def verbs_filter(request, cats_ids):
    # Формируем список классов и категорий
    cats_ids = list(map(int, cats_ids.strip('[]').split(', ')))
    classes = Classes.objects.all()
    classes_info = []
    for class_ in classes:
        class_info = dict()
        class_info['pk'] = class_.pk
        class_info['name'] = class_.name
        class_info['icon'] = class_.icon
        cats = class_.categories.all()
        cats_ids_form = []  # формирующиеся айди подкатегорий, выбранной категории
        cats_info = []
        for cat in cats:
            cat_info = dict()
            cat_info['id'] = cat.pk
            cat_info['name'] = cat.name
            cat_info['icon'] = cat.icon
            cats_info.append(cat_info)
            cats_ids_form.append(cat.pk)
        class_info['cats_ids_form'] = cats_ids_form
        class_info['cats_info'] = cats_info
        classes_info.append(class_info)
    # Формируем список биньянов
    binyans = Binyan.objects.exclude(pk=99)
    # Формируем словарь с данными по каждому глаголу:
    verbs = Word.objects.filter(type_id=6)
    verbs = verbs.filter(categories__in=cats_ids).distinct()
    verbs_info = []
    form_type = FormType.objects.all()
    for verb in verbs:
        verb_info = dict()
        verb_info['name'] = verb.name
        verb_info['picture'] = verb.picture
        for form in verb.forms.all():
            if form.form_type == form_type[0]:
                verb_info['vocal_name'] = form.vocal_name
                verb_info['translation'] = form.translation
                verb_info['pronunciation'] = form.pronunciation
                verb_info['preps'] = form.example
            elif form.time == 'настоящее' and form.gender == 'мужской' and form.number == 'единственное':
                verb_info['m1_name'] = form.vocal_name
                verb_info['m1_pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'мужской' and form.number == 'множественное':
                verb_info['m2_name'] = form.vocal_name
            elif form.time == 'настоящее' and form.gender == 'женский' and form.number == 'единственное':
                verb_info['f1_name'] = form.vocal_name
                verb_info['f1_pronunciation'] = form.pronunciation
            elif form.time == 'настоящее' and form.gender == 'женский' and form.number == 'множественное':
                verb_info['f2_name'] = form.vocal_name
        verb_info['binyan_id'] = verb.binyan.pk
        verb_info['binyan_name'] = verb.binyan.name
        verb_info['binyan_type'] = verb.binyan.type
        verb_info['binyan_output'] = verb.binyan.output
        expressions_info = []
        for expression in verb.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        verb_info['expressions'] = expressions_info
        verbs_info.append(verb_info)
    return render(request, "mycards/verbs.html", {'verbs_info': verbs_info,
                                                  'classes': classes_info,
                                                  'binyans': binyans,
                                                  'cats_ids': cats_ids,
                                                  'title': 'ГЛАГОЛЫ',
                                                  })


def numbers(request):
    numbers = Word.objects.filter(type_id=10)
    form1 = NounsFilterForm(request.GET)
    if form1.is_valid():
        if form1.cleaned_data["gender"]:
            nouns = numbers.filter(forms__gender=form1.cleaned_data['gender']).distinct()

    numbers_info = []
    form_type = FormType.objects.all()

    for number in numbers:
        number_info = dict()
        expressions_info = []
        other_forms = []
        number_info['id'] = number.pk
        if Path(os.path.join(settings.BASE_DIR, 'mycards/static/img', number.picture)).exists():
            number_info['picture'] = number.picture
        else:
            number_info['picture'] = 'нет фото.jpg'
        for form in number.forms.all():
            if form.form_type == form_type[0]:
                number_info['name'] = form.vocal_name
                number_info['translation'] = form.translation
                number_info['pronunciation'] = form.pronunciation
                number_info['gender'] = form.gender
                number_info['number'] = form.number
                number_info['main'] = form.number
                number_info['exception'] = form.exception
                if form.gender == 'женский':
                    if int(form.translation) >= 0 and int(form.translation) < 10:
                        number_info['type'] = 'единицы'
                    elif int(form.translation) >= 11 and int(form.translation) < 20:
                        number_info['type'] = 'второй десяток'
                    elif int(form.translation) >= 21 and int(form.translation) <= 29:
                        number_info['type'] = 'третий десяток'
                    elif int(form.translation) in range(10, 100, 10):
                        number_info['type'] = 'десятки'
                    elif int(form.translation) in range(100, 1000, 100):
                        number_info['type'] = 'сотни'
                    elif int(form.translation) in range(1000, 10000, 1000):
                        number_info['type'] = 'тысячи'
                else:
                    number_info['type'] = 'порядковые'
            elif form.form_type == form_type[1]:
                number_info['n2_name'] = form.vocal_name
                number_info['n2_translation'] = form.translation
                number_info['n2_pronunciation'] = form.pronunciation
                number_info['n2_exception'] = form.exception
            else:
                other_form = dict()
                other_form['name'] = form.vocal_name
                other_form['translation'] = form.translation
                other_form['pronunciation'] = form.pronunciation
                other_form['gender'] = form.gender
                other_form['number'] = form.number
                other_forms.append(other_form)
        for expression in number.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        number_info['other_forms'] = other_forms
        number_info['expressions'] = expressions_info
        numbers_info.append(number_info)

    numbers_info = sorted(numbers_info, key=lambda word: word['id'], reverse=False)
    return render(request, "mycards/numbers.html", {'numbers_info': numbers_info,
                                                    'title': 'ЧИСЛИТЕЛЬНЫЕ',
                                                  })


def pronouns(request):
    pronouns = Word.objects.filter(type_id=12).order_by('id')
    pronouns_info = []
    for pronoun in pronouns:
        pronoun_info = dict()
        expressions_info = []
        pronoun_info['id'] = pronoun.pk
        forms_info = []
        for pronoun_form in pronoun.forms.all():
            form = dict()
            form['type'] = pronoun_form.form_type
            form['name'] = pronoun_form.vocal_name
            form['translation'] = pronoun_form.translation
            form['pronunciation'] = pronoun_form.pronunciation
            form['gender'] = pronoun_form.gender
            form['number'] = pronoun_form.number
            forms_info.append(form)
            forms_info = sorted(forms_info, key=lambda form: form['type'].pk, reverse=True)
        pronoun_info['forms'] = forms_info
        for expression in pronoun.expressions.all():
            answers_info = []
            expression_info = dict()
            expression_info['name'] = expression.expression
            expression_info['translation'] = expression.translation
            expression_info['pronunciation'] = expression.pronunciation
            for answer in expression.answers.all():
                answer_info = dict()
                answer_info['name'] = answer.expression
                answer_info['translation'] = answer.translation
                answer_info['pronunciation'] = answer.pronunciation
                answers_info.append(answer)
            expression_info['answers'] = answers_info
            expressions_info.append(expression_info)
        pronoun_info['expressions'] = expressions_info
        pronouns_info.append(pronoun_info)


    return render(request, "mycards/pronouns.html", {'pronouns_info': pronouns_info, 'title': 'МЕСТОИМЕНИЯ',})


def add_noun(request):
    form_types = FormType.objects.all()
    data = ""
    names = ""
    word = ""
    wordforms = ""
    morph = pymorphy2.MorphAnalyzer()
    if request.method == 'POST':
        form = NounsAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            names = data['text'].splitlines()
            single_translation = data['translation'].split(', ')[0]
            word = dict()
            word['type'] = data['type']
            word['animacy'] = data['animacy']
            word['name'] = only_letters(names[0])
            word['picture'] = ".".join([single_translation, 'jpg'])
            try:
                new_noun = Word.objects.create(**word)
                wordforms = []
                if data['only_plural']:
                    data['number'] = 'множественное'
                else:
                    data['number'] = 'единственное'
                i = 0
                while i < len(names):
                    wordform = dict()
                    wordform['gender'] = data['gender']
                    if i == 0:
                        wordform['number'] = data['number']
                        wordform['form_type'] = form_types[0]
                        wordform['translation'] = data['translation']
                        if data['only_plural']:
                            wordform['exception'] = 100
                        else:
                            wordform['exception'] = 0
                    elif i == 2:
                        wordform['number'] = 'множественное'
                        wordform['form_type'] = form_types[1]
                        translation = morph.parse(single_translation)[0]
                        wordform['translation'] = translation.make_agree_with_number(2).word
                        wordform['exception'] = data['exception']

                    wordform['name'] = only_letters(names[i])
                    wordform['vocal_name'] = names[i]
                    wordform['pronunciation'] = names[i + 1]
                    wordform['word'] = new_noun
                    try:
                        WordForm.objects.create(**wordform)
                    except:
                        form.add_error(None, "Ошибка добавления формы слова " + i)

                    i += 2
                cat = {'category': data['category'], 'word': new_noun}
                try:
                    Grouping.objects.create(**cat)
                    return redirect('add_noun')
                except:
                    form.add_error(None, "Ошибка добавления слова в категорию")
            except:
                form.add_error(None, "Ошибка добавления слова")

    else:
        form = NounsAddForm()
    return render(request, 'mycards/add_nouns.html', {'form': form, 'title': 'ДОБАВИТЬ'})


def add_verb(request):
    if request.method == 'POST':
        form_new_binyan = BinyanAddForm(request.POST)
        if form_new_binyan.is_valid():
            form_new_binyan.save()
    else:
        form_new_binyan = BinyanAddForm()


    if request.method == 'POST':
        form_new_root = RootAddForm(request.POST)
        if form_new_root.is_valid():
            form_new_root.save()
            redirect('add_verb')
    else:
        form_new_root = RootAddForm()


    form_types = FormType.objects.all()
    data = ""
    names = ""
    word = ""
    wordforms = ""
    morph = pymorphy2.MorphAnalyzer()
    if request.method == 'POST':
        form = VerbsAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            names = data['text'].splitlines()
            word_forms_now = data['word_forms_now'].splitlines()
            word = dict()
            word['type'] = data['type']
            word['name'] = only_letters(names[0])
            word['picture'] = ".".join([data['translation'], 'jpg'])
            word['binyan'] = data['binyan']
            word['root'] = data['root']
            wordforms=[]
            try:
                new_verb = Word.objects.create(**word)
                wordform = dict()
                wordform['form_type'] = form_types[0]
                wordform['name'] = only_letters(names[0])
                wordform['vocal_name'] = names[0]
                wordform['pronunciation'] = names[1]
                wordform['translation'] = data['translation']
                wordform['word'] = new_verb
                try:
                    WordForm.objects.create(**wordform)
                except:
                    form.add_error(None, "Ошибка добавления основной формы слова")
                i = 0
                gender = {0:'мужской', 2:'женский', 4:'мужской', 6:'женский'}
                number = {0: 'единственное', 2: 'единственное', 4: 'множественное', 6: 'множественное'}
                while i < len(word_forms_now):
                    wordform = dict()
                    wordform['gender'] = gender[i]
                    wordform['number'] = number[i]
                    wordform['time'] = 'настоящее'
                    wordform['form_type'] = form_types[1]
                    parsed_word = morph.parse(data['translation'])[0]
                    if wordform['number'] == 'единственное':
                        first_person_form = parsed_word.inflect({'1per', 'pres', 'sing'}).word
                        wordform['translation'] = first_person_form
                    elif wordform['number'] == 'множественное':
                        third_person_plural_form = parsed_word.inflect({'3per', 'plur', 'pres'}).word
                        wordform['translation'] = third_person_plural_form
                    wordform['name'] = only_letters(word_forms_now[i])
                    wordform['vocal_name'] = word_forms_now[i]
                    wordform['pronunciation'] = word_forms_now[i + 1]
                    wordform['word'] = new_verb
                    try:
                        WordForm.objects.create(**wordform)
                    except:
                        form.add_error(None, "Ошибка добавления формы слова " + i)
                    i += 2
                return redirect('add_verb')
            except:
                form.add_error(None, "Ошибка добавления слова")
    else:
        form = VerbsAddForm()



    return render(request, "mycards/add_verbs.html", {'form_new_binyan': form_new_binyan,
                                                      'form_new_root': form_new_root,
                                                      'form': form,
                                                      'title': 'ДОБАВИТЬ',
                                                      })


def add_adjective(request):
    form_types = FormType.objects.all()
    data = ""
    names = ""
    word = ""
    wordforms = ""
    morph = pymorphy2.MorphAnalyzer()
    if request.method == 'POST':
        form = AdjectivesAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            word_forms = data['text'].splitlines()
            word = dict()
            word['type'] = data['type']
            word['name'] = only_letters(word_forms[0])
            word['picture'] = ".".join([data['translation'], 'jpg'])
            word['is_antonym'] = data['is_antonym']
            word['antonym_word'] = data['antonym']
            word['topic'] = data['topic']
            wordforms=[]
            try:
                new_adjective = Word.objects.create(**word)
                i = 0
                gender = {0:'мужской', 2:'женский', 4:'мужской', 6:'женский'}
                number = {0: 'единственное', 2: 'единственное', 4: 'множественное', 6: 'множественное'}
                while i < len(word_forms):
                    wordform = dict()
                    wordform['gender'] = gender[i]
                    wordform['number'] = number[i]
                    if i == 0:
                        wordform['form_type'] = form_types[0]
                    else:
                        wordform['form_type'] = form_types[1]
                    parsed_word = morph.parse(data['translation'])[0]
                    if wordform['number'] == 'единственное' and wordform['gender'] == 'женский':
                        feminine_nominative = parsed_word.inflect({'femn', 'nomn'}).word
                        wordform['translation'] = feminine_nominative
                    elif wordform['number'] == 'единственное' and wordform['gender'] == 'мужской':
                        wordform['translation'] = data['translation']
                    elif wordform['number'] == 'множественное' and wordform['gender'] == 'мужской':
                        plural = parsed_word.inflect({'plur', 'nomn'}).word
                        wordform['translation'] = plural
                    elif wordform['number'] == 'множественное' and wordform['gender'] == 'женский':
                        plural = parsed_word.inflect({'plur', 'nomn'}).word
                        wordform['translation'] = plural
                    wordform['name'] = only_letters(word_forms[i])
                    wordform['vocal_name'] = word_forms[i]
                    wordform['pronunciation'] = word_forms[i + 1]
                    wordform['word'] = new_adjective
                    try:
                        WordForm.objects.create(**wordform)
                    except:
                        form.add_error(None, "Ошибка добавления формы слова " + i)
                    i += 2
                return redirect('add_adjective')
            except:
                form.add_error(None, "Ошибка добавления слова")
    else:
        form = AdjectivesAddForm()

    return render(request, "mycards/add_adjectives.html", {'form': form, 'title': 'ДОБАВИТЬ'})


class WordsToLearn(ListView):
    paginate_by = 1
    model = WordForm
    template_name = 'mycards/learn_words.html'
    context_object_name = 'words'
    form = WordsToLearnForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Запомнить"
        context['form'] = self.form(self.request.GET)
        # Create new QueryDict without 'page'
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['query_string'] = query.urlencode()
        return context

    def get_queryset(self):
        word_queryset = WordForm.objects.filter(form_type=1)
        form = self.form(self.request.GET)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            date = form.cleaned_data.get('date')
            today = timezone.now()
            try:
                DD = dt.timedelta(days=int(date))
            except:
                DD = dt.timedelta(days=int(10000))
            earlier = today - DD
            if type:
                word_queryset = word_queryset.filter(word__type=type)
            if date:
                word_queryset = word_queryset.filter(word__time_create__gt=earlier)
        return word_queryset