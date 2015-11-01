# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# from django.template import RequestContext, loader

from . models import Choice, Question

# Create your views here.


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# template = loader.get_template('polls/index.html')
	# context = RequestContext(request, {
	# 	"latest_question_list": latest_question_list,
	# 	})
	context = {"latest_question_list": latest_question_list}  # shorthand way of writing above commented out lines
	return render(request, 'polls/index.html', context)
	# return HttpResponse(template.render(context))  # not needed with shortcut syntax
	# output = ', '.join([p.question_date for p in latest_question_list])
	# return HttpResponse(output)


def detail(request, question_id):
	# try:
		# question = Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
	# 	raise Http404("Question does not exist")
	#shortcut method below
	question = get_object_or_404(Question, pk=question_id)  # django model passed as 1st arguement and arbitrary number of keyword arguments, which it passes to teh get() and 404 is the object doesnt exist
	# return HttpResponse("You're looking at question %s." % question_id)
	return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	retun render(request, 'polls:results.html', {'question': question})

	response = "You're looking at the results of a question %s."
	return HttpResponse(response % question_id)


def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
			selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
			# redisplay the question voting form
			return render(request, 'polls/detail.html', {
					'question': p,
					'error_message': "You didn't select a choice",
				})
	else:
			selected_choice.votes += 1
			selected_choice.save()  # Always return an HttpResponseRedirect after #successfully dealing with POST data. This prevents date from being posted twice
			# if a user hits the Back button
			return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

	# return HttpResponse("You're voting on a question %s." % question_id)

