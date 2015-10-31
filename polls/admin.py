from django.contrib import admin

from .models import Question, Choice

# Register your models here.


class ChoiceInLine(admin.TabularInline):  #displays inline as opposed to StackedInline, which diplays one a top the other
	model = Choice
	extra = 3


class QuestionAdmin(admin.ModelAdmin):  # admin model objects
	# fields = ['pub_date', 'question_date']  # changed the order in the admin edit section
	fieldsets = [
				(None,								{'fields': ['question_date']}),
				('Date Information',	{'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInLine]
	list_display = ('question_date', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question_date']


admin.site.register(Question, QuestionAdmin)


#below is one way to display our choices to the Admin page but this is an inefficient method. The inlines method above is the way to go
# class ChoiceAdmin(admin.ModelAdmin):
# 	# fields = ['question', 'choice_text', 'votes']
# 	fieldsets = [
# 				("Question", 								{'fields': ['question']}),
# 				("Choice Selection",	{'fields': ['choice_text']}),
# 				('Vote Tally',				{'fields': ['votes'], 'classes': ['collapse']}),
# 	]

# admin.site.register(Choice, ChoiceAdmin)
