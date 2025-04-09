from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Question, Answer
from .forms import UserRegisterForm, QuestionForm, AnswerForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'qanda/register.html', {'form': form})


class QuestionListView(ListView):
    model = Question
    template_name = 'qanda/home.html'
    context_object_name = 'questions'
    ordering = ['-date_posted']
    paginate_by = 10


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = AnswerForm()
        return context


@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Your question has been posted!')
            return redirect('question-detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qanda/post_question.html', {'form': form})


@login_required
def post_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            messages.success(request, 'Your answer has been posted!')
            return redirect('question-detail', pk=question.pk)
    return redirect('question-detail', pk=question.pk)


@login_required
def like_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        answer = get_object_or_404(Answer, id=answer_id)

        if request.user in answer.likes.all():
            answer.likes.remove(request.user)
            liked = False
        else:
            answer.likes.add(request.user)
            liked = True

        return JsonResponse({'liked': liked, 'likes_count': answer.total_likes()})
    return JsonResponse({}, status=400)
