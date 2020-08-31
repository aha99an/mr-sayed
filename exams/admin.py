from django.contrib import admin
from .models import (Quiz, StudentQuiz, EssayQuestion, StudentEssayAnswer, TrueFalseQuestion, StudentTrueFalseAnswer,
                     ChoiceQuestion, StudentChoiceAnswer)


class QuizAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(StudentQuiz)
admin.site.register(EssayQuestion)
admin.site.register(StudentEssayAnswer)
admin.site.register(TrueFalseQuestion)
admin.site.register(StudentTrueFalseAnswer)
admin.site.register(ChoiceQuestion)
admin.site.register(StudentChoiceAnswer)
