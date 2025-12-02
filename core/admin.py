from django.contrib import admin
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    inlines = [QuestionInline]
    ordering = ('-created_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'quiz', 'question_type', 'created_at')
    inlines = [AnswerInline]
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question', 'is_correct')
    list_filter = ('is_correct',)

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user', 'quiz', 'score', 'submitted_at')
    readonly_fields = ('submitted_at',)
    list_filter = ('quiz',)

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'question', 'is_correct')
    list_select_related = ('submission', 'question')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'location')
    ordering = ('date',)

