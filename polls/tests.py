from django.test import TestCase
from django.urls import reverse
from django.utils import  timezone
from polls.models import Choice, Question

class QuestionModelTest(TestCase):

    def test_publish_time_test(self):
        time_p = (timezone.now() - timezone.timedelta(days=2)).date()
        time_r = (timezone.now()).date()
        time_f = (timezone.now() + timezone.timedelta(days=1)).date()

        question1 = Question(pub_date = time_p)
        question2 = Question(pub_date = time_r)
        question3 = Question(pub_date = time_f)

        self.assertFalse(question1.is_pub_recently())
        self.assertTrue(question2.is_pub_recently())
        self.assertFalse(question3.is_pub_recently())

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['questions'], [])
    
    def test_detail_view(self):
        question1 = Question(description = 'hello')
        question1.save()
        choice = Choice(description = 'salam', question = question1)
        choice.save()
        response = self.client.get(reverse('detail', args=[1,]))
        print("+++++++++++++++++++++")
        print(response.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['idd'], '1')
        self.assertQuerysetEqual(response.context['choices'], Choice.objects.filter(question__id = 1).values_list('description', flat=True) )