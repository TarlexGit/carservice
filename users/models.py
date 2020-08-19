from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


# for registration
class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(
        User,
        verbose_name="Клиент", 
        on_delete=models.CASCADE,
        null=True,
        default=None)
    last_name = models.CharField("Фамилия", max_length=30, default="")
    first_name = models.CharField("Имя", max_length=30, default="")
    father_name = models.CharField("Отчество", max_length=30, default="")
    car_mark = models.CharField("Мака авто", max_length=60, default="")


    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return "Id:{}, {} {}".format(self.id, self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.id})