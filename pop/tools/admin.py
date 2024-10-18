from django.contrib import admin
from .models import TextAnalysis, Specification, NeuralNetwork


@admin.register(TextAnalysis)
class TextAnalysisAdmin(admin.ModelAdmin):
    pass


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    pass


@admin.register(NeuralNetwork)
class NeuralNetworkAdmin(admin.ModelAdmin):
    pass
