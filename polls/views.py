from random import choices
from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Choice, Question 
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.http import HttpResponseRedirect

def main_page(request):
    search_text = request.GET.get('Search' , None)
    template = loader.get_template('index.template')


    questions = []
    if (search_text == None):
        query_set = Question.objects.all() [:5]
        for question in query_set:
            questions.append((str(question.id),question.description))
    else:
        query_set = Question.objects.filter(description__contains = (search_text)) [:5]
        for question in query_set:
            questions.append((str(question.id),question.description))


    return HttpResponse(template.render({'questions': questions}, request))

def detail(request, question_id):
    template = loader.get_template('detail.template')
    query_set = Question.objects.all()

    for question in query_set:
        if(question.id == question_id):
            query_set2 = Choice.objects.filter(question__id = question_id)
            choices = []
            for choice in query_set2:
                choices.append(choice.description)
            idd = str(question.id)
            return HttpResponse(template.render({'idd' : idd , 'question': question.description, 'choices': choices}, request))
    else:
            response = '404'

    if (response == '404'):
        raise Http404

def result(request, question_id):
    template = loader.get_template('result.template')
    query_set = Question.objects.all()

    for question in query_set:
        if(question.id == question_id):
            query_set2 = Choice.objects.filter(question__id = question_id)
            choices = []
            for choice in query_set2:
                choices.append((choice.description, str(choice.number_of_vote)))
            back_id = question.id
            return HttpResponse(template.render({'back_id' : back_id , 'choices': choices}, request))
    else:
            response = '404'

    if (response == '404'):
        raise Http404


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