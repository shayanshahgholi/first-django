from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Question 


def main_page(request):
    response =  ''
    query_set = Question.objects.all()
    for question in query_set:
        response += '<br>' + str(question.id) + ' ' + question.description + '</br>'

    return HttpResponse(response)
def detail(request, question_id):
    response = ''
    query_set = Question.objects.all()
    for question in query_set:
        if(question.id == question_id):
            response = question.description
            break
    else:
            response = 'invalid id'
    return HttpResponse(response)
    

