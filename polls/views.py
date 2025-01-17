from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


def index(request):
    #recuperer les 5 derniers résultats de la listes 
    latest_question_list = Question.objects.order_by("-pub_date")[:5]    
    context = {"latest_question_list" : latest_question_list }  

    return render(request, "polls/index.html", context)

def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, "polls/detail.html", {"question": question})    

def results(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, "polls/results.html", {"question": question}) 

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError,Choice.DoesNotExist): 
        #Redisplay the question voting form.
        return render(
            request,
            "/polls/detail.html",
            {
                "question": question,
                "error_message": "Vous n'avez pas selectionné de choix.",
            },
        )
    else:
        selected_choice.votes += 1 
        selected_choice.save()
        #Always return an HttpResponseRedirect after succesfully dealing
        #with POST data. This prevents data form being posted twice if a user hits th back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))