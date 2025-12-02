from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event
from django.utils import timezone

def home(request):
    quizzes_count = Quiz.objects.count()
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).count()
    return render(request, 'home.html', {'quizzes': quizzes_count, 'events': upcoming_events})

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('answers').all()
    return render(request, 'quiz_attempt.html', {'quiz': quiz, 'questions': questions})

@transaction.atomic
def quiz_submit(request, quiz_id):
    if request.method != 'POST':
        return redirect('quiz_attempt', quiz_id=quiz_id)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user if request.user.is_authenticated else None
    user_name = request.POST.get('user_name', '')
    # prefer user's username if logged in
    if user and not user_name:
        user_name = user.username

    submission = UserSubmission.objects.create(
        quiz=quiz,
        user=user,
        user_name=user_name,
        score=0
    )

    score = 0
    for q in quiz.questions.all():
        key = f"q_{q.id}"
        user_answer_value = request.POST.get(key, "").strip()

        if q.question_type == 'MCQ':
            correct = q.answers.filter(text=user_answer_value, is_correct=True).exists()
            UserAnswer.objects.create(submission=submission, question=q, answer=user_answer_value, is_correct=correct)
            if correct:
                score += 1
        else:
            # TEXT: match case-insensitive against any correct answers
            correct = q.answers.filter(is_correct=True, text__iexact=user_answer_value).exists()
            UserAnswer.objects.create(submission=submission, question=q, answer=user_answer_value, is_correct=correct)
            if correct:
                score += 1

    submission.score = score
    submission.save()

    return redirect('quiz_result', submission_id=submission.id)

def quiz_result(request, submission_id):
    submission = get_object_or_404(UserSubmission, id=submission_id)
    answers = submission.user_answers.select_related('question').all()
    total_questions = submission.quiz.questions.count()
    
    # Calculate score percentage
    if total_questions > 0:
        score_percentage = (submission.score / total_questions) * 100
    else:
        score_percentage = 0
    
    # Determine status
    if submission.score == total_questions:
        status = "Excellent"
    elif submission.score >= total_questions * 0.75:
        status = "Excellent"
    elif submission.score >= total_questions * 0.5:
        status = "Good"
    else:
        status = "Keep Trying"
    
    return render(request, 'quiz_result.html', {
        'submission': submission,
        'answers': answers,
        'total_questions': total_questions,
        'score_percentage': score_percentage,
        'status': status
    })

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

# AUTH: signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login after signup
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

# AUTH: login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

# AUTH: logout view
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')

# Bonus: quiz history, only for logged in users
@login_required
def quiz_history(request):
    # show submissions by this logged-in user
    submissions = UserSubmission.objects.filter(user=request.user).select_related('quiz').order_by('-submitted_at')
    return render(request, 'quiz_history.html', {'submissions': submissions})
