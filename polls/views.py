from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Choice, Question 
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.http import HttpResponseRedirect

class MainPage(generic.ListView):
    model = Question
    template_name = 'index.template'
    context_object_name = 'questions'

    def get_queryset(self):
        search_text = self.request.GET.get('Search' , None)
        questions = []
        if (search_text == None):
            query_set = Question.objects.all() [:5]
            for question in query_set:
                questions.append((str(question.id),question.description))
        else:
            query_set = Question.objects.filter(description__contains = (search_text)) [:5]
            for question in query_set:
                questions.append((str(question.id),question.description))
        return questions


class Detail(generic.DetailView):
    model = Question
    template_name = 'detail.template'
    context_object_name = 'question'

class Result(generic.DetailView):
    model = Choice
    template_name = 'result.template'
    content_object_name = 'Choices'

    def get_context_data(self, **kwargs) :
        print(super().get_context_data(**kwargs))
        q = super().get_context_data(**kwargs)['question']
        return Choice.objects.filter(question__id = q.id)


def vote(request, question_id):
    template = loader.get_template('vote.template')
    question = Question.objects.filter(id = question_id).get()
    question_id = str(question.id)
    question_description = question.description
    choices = []
    for choice in Choice.objects.filter(question__id = question_id):
        choices.append((str(choice.id), choice.description))
    return HttpResponse(template.render({'q_id': question_id, 'q_describe': question_description, "choices": choices}, request))


def add_vote(request, question_id):
    choice_id = request.POST.get('choice', None)
    if(choice_id == None):
        return HttpResponse("Please choose one option")
    choice = Choice.objects.filter(id = choice_id).get()
    choice.number_of_vote = F('number_of_vote') + 1
    choice.save()
    return HttpResponseRedirect('/polls/main')