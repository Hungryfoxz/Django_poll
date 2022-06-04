from multiprocessing import context
import re

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect, redirect, render, reverse
from .models import Candidate, Positions, extra_field

# Create your views here.
 
#############################################  Index.html  ######################################################################

def index(request):
    # adding data to the extra fields ..
    User = get_user_model()
    for i in User.objects.all():
        if not extra_field.objects.filter(users=i).exists():
            instance = extra_field()
            instance.users = i
            instance.save()
            #print(i)
        else:
            continue
    return render(request, 'index.html')


#############################################  Login.html ######################################################################

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return render(request, 'povo_home.html')
        else:
            # Error returns to the login page again..
            return redirect('login_view')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})



########################################## po-voter-home  ########################################################################
@login_required
def povo_home(request):
    return render(request, 'povo_home')


######################################## Preciding officer panel ##############################################################

def officer(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    else:
        return render(request, 'preciding_officer.html')

#########################################  Voters Show Ballot  ##############################################################

def voter_show_ballot(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    else:
        instance_var = extra_field.objects.get(users=request.user)
        if instance_var.validation == 1:
            return redirect('voter')
        else:
            messages.warning(request, '***Waiting for the Preciding officer to allow the access..Please ask the Officer to provide access...')
            return render(request,'voter_show_ballot.html')


############################################  Voter vote panel  ##################################################################

def voter(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    else:
        # Checking the permission from the preciding officer..
        instance_var = extra_field.objects.get(users=request.user)
        if instance_var.validation == 1:
            if request.method == 'POST':
                for position in Positions.objects.only('name'):
                                                                # it will check for the position in the Positions table..
                        choices = request.POST.get(str(position))
                                                                # this will get the id of the selected person from the request..
                        if Candidate.objects.filter(pk=choices).exists():
                            instance = Candidate.objects.get(pk=choices)
                                                                # this statement will create an instance to the primary key related to the candidate
                            instance.votes += 1
                                                                # this statement will add a vote the instance linking to that particular name...
                            instance.save()
                            # this will finally save the vote to the database for the respected field..
                        else:
                            continue
                #CheckPoint here to check if the preciding officer has allowed..
                instance_var.validation = 0
                instance_var.save() 
                messages.success(request, 'Congratulation! Your vote has been recorded.')
                #context = { 'data':'disabled'}
                return render(request, 'voter_show_ballot.html')#, ({'context':context})
            candidates = Candidate.objects.all()
            position = Positions.objects.all().order_by('priority')
            return render(request, 'voter.html',{'candidates': candidates,'positions':position})
        # Checking the returned form from the user..
        else:
            return redirect('voter_show_ballot')

############################################# test Pass to allow vote vs new_vote  ##############################################

# FROM THE ADMIN SIDE ADMITTED FOR THE VOTER TO VOTE....>>>>>>
def admitted_from_po(request):
    if request.user.is_authenticated:
        #currently_accessing = request.user
        instance_var = extra_field.objects.get(users=request.user)
        if instance_var.validation != 0:
            messages.warning(request, '***Waiting for the voter to vote..Please try again after a few seconds...')
            return HttpResponseRedirect(reverse('officer'))
        else:
            instance_var.validation = 1
            instance_var.save()
            messages.warning(request, '***The voter can vote Now...')
            return HttpResponseRedirect(reverse('officer'))
    else:
        messages.warning(request, "Your are not authorized to view this page or your session may have ended..Login again!")
        return HttpResponseRedirect(reverse('officer'))
      
#################################################  Table to show the results #########################################################

def tables(request):
    if request.user.is_authenticated:
        candidates = Candidate.objects.all()
        position = Positions.objects.all().order_by('priority')
        return render(request, 'results.html',{'candidates': candidates,'positions':position})
