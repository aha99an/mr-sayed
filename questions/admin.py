from django.contrib import admin
from .models import MrQuestion, MrQuestionFile

class MrQuestionAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)

admin.site.register(MrQuestion, MrQuestionAdmin)
admin.site.register(MrQuestionFile)
