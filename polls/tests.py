import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question


'''
    python manage.py test polls

    What happened is this:

        python manage.py test polls looked for tests in the polls application
        it found a subclass of the django.test.TestCase class
        it created a special database for the purpose of testing
        it looked for test methods - ones whose names begin with test
        in test_was_published_recently_with_future_question it created a Question instance whose pub_date field is 30 days in the future
        ... and using the assertEqual() method, it discovered that its was_published_recently() returns True, though we wanted it to return False
        The test informs us which test failed and even the line on which the failure occurred.
'''

def create_quesiton(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionMethodTests(TestCase):

    def test_was_piblished_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

class QuestionViewTests(TestCase):

    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertCountEqual(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_last_quesiton(self):
        create_quesiton(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        create_quesiton(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertCountEqual(response, "No polls are available.",
                              status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

# Create your tests here.
