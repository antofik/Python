from django.http import HttpResponse
from models import *
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from forms import PollForm
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")


def test(request):
    polls = Poll.objects.order_by('-pub_date')[:5]
    return render(request, 'list.html', {'polls': polls, 'poll': polls[0]})


def detail(request, id):
    poll = Poll.objects.filter(id=id)[0]
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            choice = Choice.objects.filter(id=form.cleaned_data['choice_id'])[0]
            choice.votes += 1
            choice.save()
            return HttpResponseRedirect('/test/thanks/')

    return render(request, 'detail.html', {
        'poll': poll,
        'choices': poll.choice_set,
    })


def thanks(request):
    return render(request, 'thanks.html')


def results(request, id):
    poll = Poll.objects.filter(id=id)[0]

    sum = 0
    choices = poll.choice_set.all()
    for choice in choices:
        sum += choice.votes

    return render(request, 'results.html', {
        'poll': poll,
        'sum': sum,
        'choices': choices,
    })