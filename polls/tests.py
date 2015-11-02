import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question


class QuestionMethodTests(TestCase):
	def test_was_published_recently_with_future_question(self):
			"""
				was_published_recently() should return False for questions whose pub_date is in the future.
			"""
			time = timezone.now() + datetime.timedelta(days=30)
			future_question = Question(pub_date=time)
			self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
			"""
				was_published_recently() should return False for questions whose pub_date is older than 1 day.
			"""
			time = timezone.now() - datetime.timedelta(days=30)
			old_question = Question(pub_date=time)
			self.assertEqual(old_question.was_published_recently(), False)
	
	def test_was_published_recently_with_recent_question(self):
			"""
				was_published_recently() should return False for questions whose pub_date is within the last day.
			"""
			time = timezone.now() - datetime.timedelta(hours=1)
			recent_question = Question(pub_date=time)
			self.assertEqual(recent_question.was_published_recently(), True)
	
	def create_question(question_date, days):
			"""
				creates a question with the given 'question_date' (which should read question_text but I made an error in creating my model) was_published_recentlythe given number of 'days' offset to now(negative for questions published in the past and positive for questions that have yet to be published).
			"""
			time = timezone.now() + datetime.timedelta(days=days)
			return Question.objects.create(question_date=question_date, pub_date=time)

	class QuestionViewTests(TestCase):
		def test_index_view_with_no_questions(self):
			"""
				if no questions exist, an appropriate message should be displayed.
			"""
			response = self.client.get(reverse('polls:index'))
			self.assertEqual(response.status_code, 200)
			self.assertContains(response, "No polls are available.")
			self.assertQuerysetEqual(response.context['latest_question_list'], [])
		
		def test_index_view_with_a_past_question(self):
				"""
				Question with a pub_date in the past should be displayed on the index page.
			"""
				create_question(question_date="Past Question", days=-30)
				response = self.client.get(reverse('polls:index'))
				self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])
		
		def test_index_with_a_future_question(self):
				"""
					Question with a pub_date in the future should not be displayed on the index page
				"""
				create_question(question_date="Future question", days=30)
				response = self.client.get(reverse('polls:index'))
				self.assertContains(response, "No polls are available", status_code=200)
				self.assertQuerysetEqual(response.context['latest_question_list'], [])
		
		def test_index_view_with_future_question_and_past_question(self):
				"""
					Even if both past and future questions exist, only past questions should be displayed.
				"""
				create_question(question_date='Past question', days=-30)
				create_question(question_date='Future question', days=30)
				response = self.client.get(reverse('polls:index'))
				self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

		def test_index_view_with_two_past_questions(self):
				"""
					The questions index page may display multiple questions.
				"""
				create_question(question_date='Past question #1', days=-30)
				create_question(question_date='Past question_date #2', days=-5)
				response = self.client.get(reverse('polls:index'))
				self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question #2>', '<Question: Past question #1>'])

	class QuestionIndexDetailTests(TestCase):
		def test_detail_view_with_a_future_question(self):
			"""
				The detail view of a question with a pub_date in the future should return a 404 not found.
			"""
			future_question = create_question(question_date='Future Question', days=5)
			response = self.client.get(reverse('polls:detail', args=(future_question.id)))
			self.assertEqual(response.status_code, 404)

			def test_detail_view_with_a_past_question(self):
				"""
					The detail view of a question with a pub_date on the past should display the question's text.
				"""
				past_question = create_question(question_date='Past Question.', days=-5)
				response = self.client.get(reverse('polls:detail', args=(past_question.id)))
				self.assertContains(response, past_question.question_date, status_code=200)


	# Ideas for more tests

	# We ought to add a similar get_queryset method to ResultsView and create a new test class for that view. It’ll be very similar to what we have just created; in fact there will be a lot of repetition.

	# We could also improve our application in other ways, adding tests along the way. For example, it’s silly that Questions can be published on the site that have no Choices. So, our views could check for this, and exclude such Questions. Our tests would create a Question without Choices and then test that it’s not published, as well as create a similar Question with Choices, and test that it is published.

	# Perhaps logged-in admin users should be allowed to see unpublished Questions, but not ordinary visitors. Again: whatever needs to be added to the software to accomplish this should be accompanied by a test, whether you write the test first and then make the code pass the test, or work out the logic in your code first and then write a test to prove it.


