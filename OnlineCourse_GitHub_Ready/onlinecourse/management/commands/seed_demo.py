from django.core.management.base import BaseCommand
from django.db import transaction
from onlinecourse.models import Course, Lesson, Question, Choice

class Command(BaseCommand):
    help = "Create a sample course and exam; preserve existing course content on reruns."

    @transaction.atomic
    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(name="Django Fundamentals", defaults={
            "description": "Learn Django models, URLs and templates, then complete a short assessment."})
        if not created:
            self.stdout.write("Demo course already exists; no changes made.")
            return
        lessons = [
            ("Models and databases", "Django models are Python classes that describe database tables. A ForeignKey creates a many-to-one relationship. SQLite is the default database for this local project."),
            ("Views and URL routes", "A view receives a request and returns a response. The urls.py file maps URL paths to views. POST requests submit exam answers."),
            ("Templates and assessment", "Django templates can use for loops and if conditions. Bootstrap styles the page. Choose every correct option in a multiple-answer question."),
        ]
        for order, (title, content) in enumerate(lessons, 1):
            Lesson.objects.create(course=course, title=title, order=order, content=content)
        questions = [
            ("Which file defines Django database models?", [("models.py", True), ("urls.py", False), ("admin.py", False)]),
            ("Which file maps URL paths to views?", [("settings.py", False), ("urls.py", True), ("models.py", False)]),
            ("Which template tags support loops and conditions? Select TWO.", [("for", True), ("if", True), ("import", False)]),
            ("Which HTTP method should submit exam answers?", [("GET", False), ("POST", True), ("TRACE", False)]),
            ("Which field represents a many-to-one relationship?", [("CharField", False), ("BooleanField", False), ("ForeignKey", True)]),
        ]
        for text, choices in questions:
            question = Question.objects.create(course=course, question_text=text, grade=20)
            for label, correct in choices:
                Choice.objects.create(question=question, choice_text=label, is_correct=correct)
        self.stdout.write(self.style.SUCCESS("Created Django Fundamentals with 3 lessons and 5 questions."))
