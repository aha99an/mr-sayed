from django.contrib import admin
from .models import (Exam, EssayQuestion, StudentEssayAnswer, TrueFalseQuestion, StudentTrueFalseAnswer,
                     ChoiceQuestion, StudentChoiceAnswer, StudentExam)


class QuizAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Exam, QuizAdmin)
admin.site.register(StudentExam)
admin.site.register(EssayQuestion)
admin.site.register(StudentEssayAnswer)
admin.site.register(TrueFalseQuestion)
admin.site.register(StudentTrueFalseAnswer)
admin.site.register(ChoiceQuestion)
admin.site.register(StudentChoiceAnswer)
