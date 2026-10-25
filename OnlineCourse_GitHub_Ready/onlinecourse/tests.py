from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from .models import Course, Choice, Question, Submission


class ExamTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo', verbosity=0)
        cls.course = Course.objects.get(name='Django Fundamentals')
        cls.user = get_user_model().objects.create_user('student', password='Example-Secret123')
        cls.other = get_user_model().objects.create_user('other', password='Example-Secret123')
        cls.admin = get_user_model().objects.create_superuser('admin', password='Example-Secret123')

    def setUp(self):
        self.url = reverse('onlinecourse:submit', args=[self.course.pk])
        self.client.force_login(self.user)

    def correct_ids(self):
        return list(Choice.objects.filter(question__course=self.course, is_correct=True).values_list('pk', flat=True))

    def test_pass_and_persistent_snapshot(self):
        response = self.client.post(self.url, {'choices': self.correct_ids()}, follow=True)
        self.assertContains(response, 'Congratulations, student!')
        submission = Submission.objects.get()
        self.assertEqual(submission.score, 100)
        self.assertEqual(submission.total_points, 100)
        self.assertEqual(len(submission.result_snapshot), 5)
        Question.objects.filter(course=self.course).update(grade=1)
        result = self.client.get(response.request['PATH_INFO'])
        self.assertContains(result, '100 / 100')

    def test_blank_attempt_is_zero(self):
        response = self.client.post(self.url, {}, follow=True)
        self.assertContains(response, 'Not passed')
        self.assertEqual(Submission.objects.get().score, 0)

    def test_partial_multiple_answer_earns_zero_for_question(self):
        multi = self.course.question_set.get(question_text__contains='TWO')
        selected = self.correct_ids()
        selected.remove(multi.choice_set.filter(is_correct=True).first().pk)
        self.client.post(self.url, {'choices': selected})
        self.assertEqual(Submission.objects.get().score, 80)

    def test_extra_incorrect_choice_earns_zero_for_question(self):
        selected = self.correct_ids()
        selected.append(Choice.objects.filter(question__course=self.course, is_correct=False).first().pk)
        self.client.post(self.url, {'choices': selected})
        self.assertEqual(Submission.objects.get().score, 80)

    def test_rejects_foreign_and_malformed_choice_ids(self):
        foreign_course = Course.objects.create(name='Other', description='Other')
        question = Question.objects.create(course=foreign_course, question_text='Other?')
        foreign = Choice.objects.create(question=question, choice_text='Yes', is_correct=True)
        for value in [foreign.pk, 'invalid', 999999]:
            response = self.client.post(self.url, {'choices': [value]})
            self.assertEqual(response.status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_authentication_post_and_result_ownership(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        response = self.client.post(self.url, {'choices': self.correct_ids()})
        result_url = response['Location']
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(result_url).status_code, 404)
        self.client.logout()
        self.assertEqual(self.client.post(self.url, {'choices': []}).status_code, 302)
        self.assertEqual(self.client.get(result_url).status_code, 302)

    def test_admin_sections_and_course_template(self):
        self.client.force_login(self.admin)
        response = self.client.get('/admin/')
        self.assertContains(response, 'Authentication and Authorization')
        self.assertContains(response, 'OnlineCourse')
        response = self.client.get(reverse('onlinecourse:course_details', args=[self.course.pk]))
        self.assertContains(response, 'Django Fundamentals')
        self.assertContains(response, 'Models and databases')
        self.assertContains(response, 'Submit exam')

    def test_seed_is_idempotent(self):
        call_command('seed_demo', verbosity=0)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 5)
