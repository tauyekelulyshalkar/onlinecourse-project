# OnlineCourse — Django assessment project

A standalone implementation of an online course application with lessons, multiple-answer exams, saved attempts, automatic grading and Django administration. Built for the seven supplied assignment requirements. This is a fresh implementation, not a copy of the IBM starter repository; if your course requires its exact starter schema, compare that requirement before submitting.

## Start on Windows

1. Install Python 3.10 or newer.
2. Extract this ZIP. Double-click `start_windows.bat`.
3. On the first run, enter your own administrator username, optional email and password. Password characters are intentionally invisible.
4. Keep the terminal open. Visit http://127.0.0.1:8000/ .
5. Log in with the account you created. Open **Django Fundamentals**, read the lessons and take the exam.

The first run needs internet to install Django. Bootstrap is loaded from a CDN; basic fallback CSS keeps pages readable offline. SQLite and a random local secret key are generated locally and must not be uploaded to GitHub.

## Manual setup (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_demo
.venv\Scripts\python.exe manage.py ensure_admin
.venv\Scripts\python.exe manage.py runserver
```

On macOS/Linux, use `python3 -m venv .venv` and `.venv/bin/python` instead.

## Assignment submission

Create a **public** GitHub repository. Upload the extracted source files and folders, not the ZIP itself. Preserve the folder structure; `manage.py` should be at the repository root. Upload the original clean extracted files before running, or use Git with the included `.gitignore` after running. Never upload `.venv`, `.local-secret-key`, `db.sqlite3` or credentials. Browser uploads do not apply `.gitignore` automatically.

| Task | File / evidence |
| --- | --- |
| 1 | `onlinecourse/models.py` — Question, Choice, Submission |
| 2 | `onlinecourse/admin.py` — seven model imports; QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin |
| 3 | `03-admin-site.png` — logged-in `/admin/`, showing Authentication and Authorization plus OnlineCourse |
| 4 | `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` |
| 5 | `onlinecourse/views.py` — submit and show_exam_result |
| 6 | `onlinecourse/urls.py` — submit and show_exam_result routes |
| 7 | `07-final.png` — your successful mock-exam attempt showing Congratulations, score and results |

For tasks 1, 2, 4, 5 and 6, open each file on GitHub and copy its browser URL. Use the actual repository URL and actual branch name, not a placeholder. GitHub stores the code; it does not execute this Django app through GitHub Pages.

## Screenshots

Take real screenshots after running the application. Use Windows + Shift + S. Save the admin screenshot as `03-admin-site.png`; save a passing result as `07-final.png`. Zoom the page out if needed so the required information fits. Screenshots are not included in this source ZIP.

The supplied course is practice material. Answer explanations are in its lessons. The sample exam has five questions, each worth 20 points. Pass mark is 80%. Multiple-answer questions require all correct options and no incorrect options; partial or extra selections earn zero for that question. An unanswered exam scores zero.

## Verification and design

```powershell
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test
```

Tests cover a passing attempt, unanswered attempts, exact-set grading, invalid/foreign choices, authentication, HTTP methods, result ownership and admin sections. Results include a snapshot so later question edits do not alter historical grades. This project defaults to local development. For public deployment, configure a secret key, disable debug, set allowed hosts and configure HTTPS/static hosting.

## References

- Assignment context: https://github.com/ibm-developer-skills-network/final-cloud-app-with-database
- Django installation: https://docs.djangoproject.com/en/5.2/intro/install/
- Django tests: https://docs.djangoproject.com/en/5.2/topics/testing/overview/
