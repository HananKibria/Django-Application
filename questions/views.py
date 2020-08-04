from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from .models import Question,Choice
from django.views import generic

from django.template import loader
from django.http import Http404



# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     #template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#    # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models, forms
from django.http import HttpResponseRedirect


def question_list(request):
    questions = models.Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})


def question_detail(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    return render(request, 'questions/question_detail.html', {
        'question': question,
    })


@login_required
def create_question(request):
    form = forms.QuestionForm()
    if request.method == "POST":
        form = forms.QuestionForm(request.POST)
        if form.is_valid:
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, "Question created successfully")
            return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': question.pk}))
    return render(request, 'questions/question_form.html', {'form': form})


@login_required
def edit_question(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    form_class = forms.QuestionForm
    form = form_class(instance=question)
    if request.method == "POST":
        form = form_class(request.POST, instance=question)
        if form.is_valid:
            form.save()
            messages.success(request, "Question updated successfully")
            return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': question.pk}))
    return render(request, 'questions/question_form.html', {
        'form': form,
        'question': question
    })


@login_required
def delete_question(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    question.delete()
    messages.success(request, "Question deleted")
    return HttpResponseRedirect(reverse_lazy('questions:question_list'))