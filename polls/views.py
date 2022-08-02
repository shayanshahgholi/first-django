from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Choice, Question 
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm

class MainPage(LoginRequiredMixin, generic.ListView):
    model = Question
    template_name = 'index.template'
    context_object_name = 'questions'
    login_url = '/polls/login'

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



class Detail(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'detail.template'
    context_object_name = 'question'
    login_url = '/polls/login'



class Result(LoginRequiredMixin, generic.DetailView):
    model = Choice
    template_name = 'result.template'
    content_object_name = 'Choices'
    login_url = '/polls/login'
    def get_context_data(self, **kwargs) :
        print(super().get_context_data(**kwargs))
        q = super().get_context_data(**kwargs)['question']
        return Choice.objects.filter(question__id = q.id)


@login_required(login_url='/polls/login')
def vote(request, question_id):
    if request.session.get('name' + str(question_id) ) != ('guest'):
        request.session['name' + str(question_id)] = 'guest'
        template = loader.get_template('vote.template')
        question = Question.objects.filter(id = question_id).get()
        question_id = str(question.id)
        question_description = question.description
        choices = []
        for choice in Choice.objects.filter(question__id = question_id):
            choices.append((str(choice.id), choice.description))
        return HttpResponse(template.render({'q_id': question_id, 'q_describe': question_description, "choices": choices}, request))
    else:
        print(request.session.get('name'))
        return HttpResponse('You voted before.')


@login_required(login_url='/polls/login')
def add_vote(request, question_id):
    choice_id = request.POST.get('choice', None)
    if(choice_id == None):
        return HttpResponse("Please choose one option")
    choice = Choice.objects.filter(id = choice_id).get()
    choice.number_of_vote = F('number_of_vote') + 1
    choice.save()
    return HttpResponseRedirect('/polls/main')

@login_required(login_url='/polls/login')
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/polls/login')

def login_page(request):
    template = loader.get_template('login.template')
    return HttpResponse(template.render({}, request))


def login_user(request):
    username = request.POST.get('uname', None)
    password = request.POST.get('psw', None)
    print(username, password) 
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/polls/main')
    else:
        return HttpResponse('Wrong password')

def register_page(request):
    template = loader.get_template('register.template')
    return HttpResponse(template.render({'form': RegisterForm}, request))

def register(request):
    form = RegisterForm(data=request.POST)

    if not form.is_valid():
        form.errors
    else:
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['Email']
        user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 first_name=first_name,
                                 last_name=last_name)
        return HttpResponseRedirect('/polls/login')
