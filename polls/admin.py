from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    '''
    如果管理类有多个fields，可以用一个fieldset表示多个field，分别处理不同的表单
    fieldsets中，每个fields对应一个元组，元组的第一个元素是这个fields的小标题
    '''
    fieldsets = [
        ('Question', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    '''
    在question界面显示选择选项
    '''
    inlines = [ChoiceInline]
    '''
    Django默认显示每个object的str()返回的内容
    使用list_display可以显示更多有用的fields
    list_display列表中的元组可以是一个回调函数，QuestionAdmin中的属性，Question的属性或者方法
    '''
    list_display = ('question_text', 'pub_date', 'was_published_recently')
admin.site.register(Question, QuestionAdmin)
