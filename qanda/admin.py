from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'date_posted', 'total_likes')
    list_filter = ('date_posted', 'author')
    search_fields = ('content',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
