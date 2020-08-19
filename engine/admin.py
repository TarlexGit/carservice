from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Master, FixDate


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthday', 'work_status')


@admin.register(FixDate)
class FixDateAdmin(admin.ModelAdmin):
    list_display = ('master', 'date_pub', 'start_time')
