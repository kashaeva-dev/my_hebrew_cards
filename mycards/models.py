from django.db import models

# Create your models here.
class Binyan(models.Model):
    type = models.CharField(max_length=15, verbose_name="Биньян")
    name = models.CharField(max_length=15, verbose_name="Подгруппа", null=True)
    output = models.CharField(max_length=4, verbose_name="Обозначение", null=True)


    def __str__(self):
        return str(self.name)


class Root(models.Model):
    name = models.CharField(max_length=15, verbose_name="Подгруппа")


    def __str__(self):
        return str(self.name)


class Type(models.Model):
    grammema = models.CharField(max_length=4, verbose_name='Код')
    name = models.CharField(max_length=64, verbose_name='Название')
    example = models.CharField(max_length=25, verbose_name='Пример')



    def __str__(self):
        return str(self.name)

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
    def __str__(self):
        return str(self.name)

class Classifing(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Word(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Часть речи')
    animacy = models.BooleanField(default=False, verbose_name='Одушевленность', null=True, blank=True)
    name = models.CharField(max_length=64, verbose_name='Название (для поиска)')
    root = models.ForeignKey(Root, on_delete=models.PROTECT, related_name='words', verbose_name='Корень', null=True, blank=True)
    binyan = models.ForeignKey(Binyan, on_delete=models.PROTECT, verbose_name='Биньян с подгруппой', null=True, blank=True)
    picture = models.URLField(default='https://place-hold.it/300x200', verbose_name='Картинка')
    printed = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='words', verbose_name='Тема', null=True, blank=True)
    is_antonym = models.BooleanField(default=False, null=True)
    antonym_word = models.ForeignKey('self', on_delete=models.PROTECT, related_name='antonym', verbose_name='Антоним', null=True, blank=True)
    categories = models.ManyToManyField(Category, through='Grouping', related_name='words')
    time_create = models.DateTimeField(auto_now_add=True)
    

    #def __str__(self):
    #    return self.name + ' ' + self.picture.split('.')[0] + ' (' + str(self.pk) + ')'


    class Meta:
        verbose_name = "слово"
        verbose_name_plural = "слово"
        ordering = ['time_create', 'name']
        unique_together = [("name", "picture")]


class Grouping(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class WordForm(models.Model):
    time = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=7, null=True, blank=True)
    number = models.CharField(max_length=13, null=True, blank=True)
    name = models.CharField(max_length=64, verbose_name='Название (для поиска)')
    vocal_name = models.CharField(max_length=64, verbose_name='Название с огласовками')
    exception = models.IntegerField(default=0)
    pronunciation = models.CharField(max_length=64, verbose_name='Произношение')
    translation = models.CharField(max_length=64, verbose_name='Перевод')
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='forms', verbose_name='Основная форма')
    example = models.TextField(null=True, blank=True)
    form_type = models.ForeignKey(FormType, on_delete=models.PROTECT, related_name='words', verbose_name='Тип формы', null=True)
    comment = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.name)

class Expression(models.Model):
    expression = models.CharField(max_length=256, verbose_name='Выражение')
    translation = models.CharField(max_length=256, verbose_name='Перевод')
    pronunciation = models.CharField(max_length=256, verbose_name='Произношение')
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='expressions', verbose_name='Основная форма', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='expressions', verbose_name='Тема', null=True)
    question_id = models.ForeignKey('self', on_delete=models.PROTECT, related_name='answers', verbose_name='Номер вопроса', null=True)
    comment = models.TextField(null=True)



