from django.db import models

# Create your models here.
class Binyan(models.Model):
    type = models.CharField(max_length=15, verbose_name="Биньян")
    name = models.CharField(max_length=15, verbose_name="Подгруппа", null=True)
    output = models.CharField(max_length=4, verbose_name="Обозначение", null=True)


    def __str__(self):
        return self.name


class Root(models.Model):
    name = models.CharField(max_length=15, verbose_name="Подгруппа")


    def __str__(self):
        return self.name


class Type(models.Model):
    grammema = models.CharField(max_length=4, verbose_name='Код')
    name = models.CharField(max_length=64, verbose_name='Название')
    example = models.CharField(max_length=25, verbose_name='Пример')



    def __str__(self):
        return self.name

class Topic(models.Model):
    category = models.CharField(max_length=25, verbose_name='Категория')
    name = models.CharField(max_length=25, verbose_name='Название', null=True)
    name_icon = models.CharField(max_length=25, verbose_name='Иконка', null=True)

class FormType(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название')


class Classes(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название класса')
    icon = models.CharField(max_length=25, verbose_name='Иконка', null=True)


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название категории')
    icon = models.CharField(max_length=25, verbose_name='Иконка', null=True)
    classes = models.ManyToManyField(Classes, through='Classifing', related_name='categories')


class Classifing(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Word(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Часть речи')
    animacy = models.CharField(max_length=4, verbose_name='Одушевленность', null=True)
    name = models.CharField(max_length=64, verbose_name='Название (для поиска)')
    root = models.ForeignKey(Root, on_delete=models.PROTECT, related_name='words', verbose_name='Корень', null=True)
    binyan = models.ForeignKey(Binyan, on_delete=models.PROTECT, verbose_name='Биньян с подгруппой', null=True)
    picture = models.URLField(default='https://place-hold.it/300x200', verbose_name='Картинка')
    printed = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='words', verbose_name='Тема', null=True)
    is_antonym = models.BooleanField(default=False, null=True)
    antonym_word = models.ForeignKey('self', on_delete=models.PROTECT, related_name='antonym', verbose_name='Антоним', null=True)
    categories = models.ManyToManyField(Category, through='Grouping', related_name='words')


class Grouping(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class WordForm(models.Model):
    time = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=6, null=True)
    number = models.CharField(max_length=12, null=True)
    name = models.CharField(max_length=64, verbose_name='Название (для поиска)')
    vocal_name = models.CharField(max_length=64, verbose_name='Название с огласовками')
    exception = models.IntegerField(default=0)
    pronunciation = models.CharField(max_length=64, verbose_name='Произношение')
    translation = models.CharField(max_length=64, verbose_name='Перевод')
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='forms', verbose_name='Основная форма')
    example = models.TextField(null=True)
    form_type = models.ForeignKey(FormType, on_delete=models.PROTECT, related_name='words', verbose_name='Тип формы', null=True)
    comment = models.TextField(null=True)


    def __str__(self):
        return self.name

class Expression(models.Model):
    expression = models.CharField(max_length=256, verbose_name='Выражение')
    translation = models.CharField(max_length=256, verbose_name='Перевод')
    pronunciation = models.CharField(max_length=256, verbose_name='Произношение')
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='expressions', verbose_name='Основная форма', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='expressions', verbose_name='Тема', null=True)
    question_id = models.ForeignKey('self', on_delete=models.PROTECT, related_name='answers', verbose_name='Номер вопроса', null=True)
    comment = models.TextField(null=True)



