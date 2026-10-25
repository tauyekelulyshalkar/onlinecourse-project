from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Enrollment, Submission


def index(request):
    return render(request, "onlinecourse/course_list.html", {"courses": Course.objects.all()})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.question_set.prefetch_related("choice_set")
    return render(request, "onlinecourse/course_details_bootstrap.html", {
        "course": course, "questions": questions,
    })


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = list(course.question_set.prefetch_related("choice_set"))
    if not questions:
        return HttpResponseBadRequest("This course has no exam yet.")
    try:
        selected = {int(value) for value in request.POST.getlist("choices")}
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid choice ID.")
    valid_ids = {choice.pk for question in questions for choice in question.choice_set.all()}
    if not selected.issubset(valid_ids):
        return HttpResponseBadRequest("A selected choice does not belong to this course.")
    earned, total, results = 0, 0, []
    for question in questions:
        choices = list(question.choice_set.all())
        question_selected = selected & {choice.pk for choice in choices}
        correct = question.is_get_score(question_selected)
        total += question.grade
        earned += question.grade if correct else 0
        results.append({
            "question": question.question_text, "correct": correct,
            "points": question.grade if correct else 0, "max_points": question.grade,
            "choices": [{"text": c.choice_text, "selected": c.pk in selected,
                         "is_correct": c.is_correct} for c in choices],
        })
    with transaction.atomic():
        enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
        submission = Submission.objects.create(enrollment=enrollment, earned_points=earned,
            total_points=total, result_snapshot=results)
        submission.choices.set(selected)
    return redirect("onlinecourse:show_exam_result", course_id=course.pk, submission_id=submission.pk)


@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission.objects.select_related("enrollment__course"),
        pk=submission_id, enrollment__course_id=course_id, enrollment__user=request.user)
    return render(request, "onlinecourse/exam_result_bootstrap.html", {
        "course": submission.enrollment.course, "submission": submission,
        "results": submission.result_snapshot, "passed": submission.score >= 80,
    })
