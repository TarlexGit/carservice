from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from users.models import Profile 
import datetime

class Master(models.Model):
    """Профиль специалиста автосервиса"""
    user = models.OneToOneField(
        User,
        verbose_name="Специалист",
        related_name='master',
        on_delete=models.CASCADE)
    birthday = models.DateField()
    last_name = models.CharField("Фамилия", max_length=30, default="")
    first_name = models.CharField("Имя", max_length=30, default="")
    father_name = models.CharField("Отчество", max_length=30, default="")

    work_status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"

    def __str__(self):
        return "Id:{}, {} {}".format(self.id, self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.id})

 
class FixDate(models.Model):
    """Запись к специалисту"""
    master = models.ForeignKey(
        Master,
        verbose_name="Специалист",
        related_name='master',
        on_delete=models.CASCADE)

    profile = models.ForeignKey(
        Profile,
        verbose_name="Клиент",
        related_name='profile',
        on_delete=models.CASCADE)
    
    start_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['start_date', 'start_time']

    def start_datetime(self):
        return datetime.combine(self.start_date, self.start_time)