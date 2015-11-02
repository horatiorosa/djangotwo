# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

# from django.template import RequestContext, loader

from . models import Choice, Question

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	# template = loader.get_template('polls/index.html')
# 	# context = RequestContext(request, {
# 	# 	"latest_question_list": latest_question_list,
# 	# 	})
# 	context = {"latest_question_list": latest_question_list}  # shorthand way of writing above commented out lines
# 	return render(request, 'polls/index.html', context)
# 	# return HttpResponse(template.render(context))  # not needed with shortcut syntax
# 	# output = ', '.join([p.question_date for p in latest_question_list])
# 	# return HttpResponse(output)

##### the above written as Django generic views ######


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		""" Return the last five published questions (not including those to be published in the future) """
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def detail(request, question_id):
# 	# try:
# 		# question = Question.objects.get(pk=question_id)
# 	# except Question.DoesNotExist:
# 	# 	raise Http404("Question does not exist")
# 	#shortcut method below
# 	question = get_object_or_404(Question, pk=question_id)  # django model passed as 1st arguement and arbitrary number of keyword arguments, which it passes to the get() and 404 is the object doesnt exist

##### the above written as Django generic views ######


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question': question})

	##### the above written as Django generic views ######


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'


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


