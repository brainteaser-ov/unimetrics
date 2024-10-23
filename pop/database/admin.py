from django.contrib import admin

from .models import Database, DataObject, FileModel


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'db_type', 'created_at')
    list_filter = ('db_type', 'created_at')
    search_fields = ('name', 'author__username')


@admin.register(DataObject)
class DataObjectAdmin(admin.ModelAdmin):
    list_display = ('sequence_number', 'name', 'database', 'language')
    list_filter = ('language', 'gender', 'age', 'region')
    search_fields = ('name', 'database__name')


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_by', 'upload_date')
    list_filter = ('upload_date',)
    search_fields = ('file', 'uploaded_by__username')
