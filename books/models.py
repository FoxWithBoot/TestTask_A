from django.core.validators import MaxValueValidator
from django.db import models


class Book(models.Model):
    name = models.CharField("Название", max_length=20)
    title = models.CharField("Заголовок", max_length=30, blank=True, null=True)
    author = models.CharField("Автор", max_length=30)
    description = models.CharField("Описание", max_length=512, blank=True, null=True)
    price = models.PositiveIntegerField("Цена", validators=[MaxValueValidator(99999)])

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return "%s - %s" % (self.name, self.author)


class Profile(models.Model):
    column_name = models.CharField("Название колонки", unique=True, max_length=20)
    is_visible = models.BooleanField("Активна?", default=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return "%s - %s" % (self.column_name, self.is_visible)