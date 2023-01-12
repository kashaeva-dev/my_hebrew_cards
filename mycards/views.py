from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import NounsFilterForm
from .filters_data import topics
from pathlib import Path
import os.path
from django.conf import settings


# Create your views here.
def index(request):
    return HttpResponse("Здесь будут карточки для изучения иврита")


def cards_main(request):
    binyan = Binyan.objects.all()
    return render(request, "mycards/cards.html", {'binyan': binyan})

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
    return render(request, "mycards/verbs_print.html", {'verbs_info': verbs_info, 'tl': 2})


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
    return render(request, "mycards/nouns_exсeptions.html", {'nouns_info': nouns_info, 'only_1form': only_1form})

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
    return render(request, "mycards/questions.html", {'questions_info': questions_info})


def adjectives(request):
    adjectives = Word.objects.filter(type_id=2, is_antonym=0).exclude(topic=2)
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


    return render(request, "mycards/adjectives.html", {'adjectives_info': adjectives_info})


def nouns_filter_old(request, id):
    nouns = Word.objects.filter(type_id=1, animacy='inan').exclude(topic=2)
    nouns_info = []
    top = topics
    nouns = nouns.filter(topic=id)
    form_type = FormType.objects.all()
    for noun in nouns:
        noun_info = dict()
        noun_info['id'] = noun.pk
        expressions_info = []
        other_forms = []
        antonyms = []
        if Path(os.path.join(settings.BASE_DIR, noun.picture)).exists():
            noun_info['picture'] = noun.picture
        else:
            noun_info['picture'] = 'нет фото.jpg'
        for form in noun.forms.all():
            if form.form_type == form_type[0] and form.number == 'единственное':
                noun_info['name'] = form.vocal_name
                noun_info['translation'] = form.translation
                noun_info['pronunciation'] = form.pronunciation
                noun_info['gender'] = form.gender
                noun_info['number'] = form.number
                noun_info['main'] = form.number
            elif form.form_type == form_type[1]:
                noun_info['n2_name'] = form.vocal_name
                noun_info['n2_translation'] = form.translation
                noun_info['n2_pronunciation'] = form.pronunciation
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

    return render(request, "mycards/nouns_old.html", {'nouns_info': nouns_info, 'topics': top})

def nouns_all_old(request):
    nouns = Word.objects.filter(type_id=1, animacy='inan').exclude(topic=2)
    nouns_info = []
    form_type = FormType.objects.all()
    top = topics
    for noun in nouns:
        noun_info = dict()
        expressions_info = []
        other_forms = []
        antonyms = []
        noun_info['id'] = noun.pk
        if Path(os.path.join(settings.BASE_DIR, noun.picture)).exists():
            noun_info['picture'] = noun.picture
        else:
            noun_info['picture'] = 'нет фото.jpg'
        for form in noun.forms.all():
            if form.form_type == form_type[0] and form.number == 'единственное':
                noun_info['name'] = form.vocal_name
                noun_info['translation'] = form.translation
                noun_info['pronunciation'] = form.pronunciation
                noun_info['gender'] = form.gender
                noun_info['number'] = form.number
                noun_info['main'] = form.number
            elif form.form_type == form_type[1]:
                noun_info['n2_name'] = form.vocal_name
                noun_info['n2_translation'] = form.translation
                noun_info['n2_pronunciation'] = form.pronunciation
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

    return render(request, "mycards/nouns_old.html", {'nouns_info': nouns_info, 'topics': top})


def nouns_all(request):
    nouns = Word.objects.filter(type_id=1, animacy='inan').exclude(topic=2)
    form1 = NounsFilterForm(request.GET)
    if form1.is_valid():
        if form1.cleaned_data["gender"]:
            nouns = nouns.filter(forms__gender=form1.cleaned_data['gender']).distinct()
        if form1.cleaned_data['exception']:
            lst = list(map(int, form1.cleaned_data['exception'].strip('[]').split(', ')))
            nouns = nouns.filter(forms__exception__in=lst).distinct()
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

    return render(request, "mycards/nouns_all.html", {'form1': form1,
                                                  'classes': classes_info,
                                                  })


def nouns_filter(request, cats_ids):
    nouns = Word.objects.filter(type_id=1, animacy='inan').exclude(topic=2)

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


    form_type = FormType.objects.all()
    for noun in nouns:
        noun_info = dict()
        noun_info['id'] = noun.pk
        expressions_info = []
        other_forms = []
        antonyms = []
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
                                                  })


def verbs_all(request):
    # Формируем список классов и категорий
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
        verbs_info.append(verb_info)
    return render(request, "mycards/verbs.html", {'verbs_info': verbs_info,
                                                  'classes': classes_info,
                                                  'binyans': binyans,
                                                  'form_type': form_type,
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
    return render(request, "mycards/verbs.html", {'verbs_info': verbs_info,
                                                  'classes': classes_info,
                                                  'binyans': binyans,
                                                  'cats_ids': cats_ids,
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
                                                  })


def pronouns(request):
    pronouns = Word.objects.filter(type_id=12)
    pronouns_info = []
    form_type = FormType.objects.all()
    for pronoun in pronouns:
        pronoun_info = dict()
        expressions_info = []
        for pronoun_form in pronoun.forms.all():
            if pronoun_form.form_type == form_type[0]:
                pronoun_info['name'] = pronoun_form.vocal_name
                pronoun_info['translation'] = pronoun_form.translation
                pronoun_info['pronunciation'] = pronoun_form.pronunciation
                pronoun_info['gender'] = pronoun_form.gender
                pronoun_info['number'] = pronoun_form.number
            elif pronoun_form.form_type == form_type[4]:
                pronoun_info['name_prs'] = pronoun_form.vocal_name
                pronoun_info['pronunciation_prs'] = pronoun_form.pronunciation
            if pronoun_form.form_type == form_type[5]:
                pronoun_info['name_shl'] = pronoun_form.vocal_name
                pronoun_info['translation_shl'] = pronoun_form.translation
                pronoun_info['pronunciation_shl'] = pronoun_form.pronunciation
                pronoun_info['gender_shl'] = pronoun_form.gender
                pronoun_info['number_shl'] = pronoun_form.number
            elif pronoun_form.form_type == form_type[6]:
                pronoun_info['name_l'] = pronoun_form.vocal_name
                pronoun_info['translation_l'] = pronoun_form.translation
                pronoun_info['pronunciation_l'] = pronoun_form.pronunciation
                pronoun_info['gender_l'] = pronoun_form.gender
                pronoun_info['number_l'] = pronoun_form.number
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


    return render(request, "mycards/pronouns.html", {'pronouns_info': pronouns_info})