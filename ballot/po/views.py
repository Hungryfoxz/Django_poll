from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render, reverse
from .models import Candidate, Mock, Mock_Positions, Positions, extra_field



# # Integrating Pusher js Here
import pusher
pusher_client = pusher.Pusher(
  app_id='1422023',
  key='2cd0f0edd98809e00ff2',
  secret='669c6efed9bc1566af99',
  cluster='ap2',
  ssl=True
)


# Create your views here.
 
#Create a global variable to chechk the no. of students voted...
voted = 0 
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
            messages.warning(request,"Wrong Username or Password !")
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
        if instance_var.status == True:
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
        if instance_var.status == True:
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
                instance_var.status = False
                instance_var.save() 
                messages.success(request, 'Congratulation! Your vote has been recorded..')
                #context = { 'data':'disabled'}

                #########################################################################
                # Integrating Pusher js here...
                #name = request.user
                #channel_name = u"{}".format(request.user)
                #print(channel_name)
                pusher_client.trigger([str(request.user.id)], 'my-event', {'message': 'The Voter has Voted Successfully.'})
                #########################################################################
                # COunter to increase the no of students voted...
                global voted
                voted +=1 
                return render(request, 'voter_show_ballot.html')#, ({'context':context})
            candidates = Candidate.objects.all()
            position = Positions.objects.all().order_by('priority')
            return render(request, 'voter.html',{'candidates': candidates,'positions':position})
        # Checking the returned form from the user..
        else:
            return redirect('voter_show_ballot')

############################################# test Pass to allow vote vs new_vote  ##############################################

# FROM THE ADMIN SIDE ADMITTED FOR THE VOTER TO VOTE....>>>>>>
'''def admitted_from_po(request):
    if request.user.is_authenticated:
        #currently_accessing = request.user
        instance_var = extra_field.objects.get(users=request.user)
        if instance_var.status != False:
            messages.warning(request, '***Waiting for the voter to vote..Please try again after a few seconds...')
            return HttpResponseRedirect(reverse('officer'))
        else:
            instance_var.status = True
            instance_var.save()
            messages.warning(request, '***The voter can vote Now...')
            return HttpResponseRedirect(reverse('officer'))
    else:
        messages.warning(request, "Your are not authorized to view this page or your session may have ended..Login again!")
        return HttpResponseRedirect(reverse('officer'))'''
def admitted_from_po(request):
    if request.user.is_authenticated:
        #currently_accessing = request.user
        instance_var = extra_field.objects.get(users=request.user)
        if instance_var.status != False:
            return HttpResponseRedirect(reverse('officer'))
        else:
            instance_var.status = True
            instance_var.save()
            #messages.warning(request, '***The voter can vote Now...')
            return HttpResponseRedirect(reverse('officer'))
    else:
        #messages.warning(request, "Your are not authorized to view this page or your session may have ended..Login again!")
        return HttpResponseRedirect(reverse('officer'))
      
#################################################  Table to show the results #########################################################

def tables(request):
    if request.user.is_authenticated:
        candidates = Candidate.objects.all()
        position = Positions.objects.all().order_by('priority')
        return render(request, 'results.html',{'candidates': candidates,'positions':position})

##################################################   Logout the user   #################################################################
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have successfully logged out.") 
        return redirect('login_view')
    else:
        logout(request)
        messages.info(request, "You have successfully logged out.") 
        return redirect('login_view')

################################################   Clear all the votes   #############################################################
def clear_votes(request):
    if request.user.is_authenticated:
        x = Candidate.objects.values_list('id', flat=True)
        print(x)
        for ids in x:
            if Candidate.objects.filter(pk=ids).exists():
                instance = Candidate.objects.get(pk=ids)
                #print(instance)                                                # this statement will create an instance to the primary key related to the candidate
                instance.votes = 0
                                                                # this statement will add a vote the instance linking to that particular name...
                instance.save()
                            # this will finally save the vote to the database for the respected field..
                global voted
                voted = 0
            else:
                continue
        #candidates = Candidate.objects.all()
        #for x in candidates.name:
            #candidates.votes = 0
        return redirect('officer')

################################################  Mock panel  ########################################################################### 
def mock_panel(request):
    if request.user.is_authenticated:
        #count the votes if the request is post request...
        if request.method == 'POST':
                for position in Mock_Positions.objects.only('name'):
                                                                # it will check for the position in the Positions table..
                        choices = request.POST.get(str(position))
                                                                # this will get the id of the selected person from the request..
                        if Mock.objects.filter(pk=choices).exists():
                            instance = Mock.objects.get(pk=choices)
                                                                # this statement will create an instance to the primary key related to the candidate
                            instance.votes += 1
                                                                # this statement will add a vote the instance linking to that particular name...
                            instance.save()
                            # this will finally save the vote to the database for the respected field..
                        else:
                            continue
                messages.success(request, 'Congratulation! Mock vote has been recorded..')
                #context = { 'data':'disabled'}
                return render(request, 'preciding_officer.html')#, ({'context':context})
                

        mock = Mock.objects.all()
        position = Mock_Positions.objects.all().order_by('priority')
        return render(request, 'mock_panel.html',{'candidates': mock,'position':position})

############################################### total_students_voted ##################################################################

def total_students_voted(request):
    if request.user.is_authenticated:
        global voted
        context = { 'data':voted }
        return render(request, 'total_students_voted.html', {'total':context})
    else:
        return redirect('login')

##############################################     mock_results    ###################################################################

def mock_results(request):
    if request.user.is_authenticated:
        mock = Mock.objects.all()
        position = Mock_Positions.objects.all().order_by('priority')
        print(mock)
        print(position)
        return render(request, 'mock_results.html',{'candidates': mock,'positions':position})
        # return render(request, 'mock_results.html')
    else:
        return redirect('login')

########################################## CLear mock poll results #################################################################
def mock_clear(request):
    if request.user.is_authenticated:
        x = Mock.objects.values_list('id', flat=True)
        print(x)
        for ids in x:
            if Mock.objects.filter(pk=ids).exists():
                instance = Mock.objects.get(pk=ids)
                #print(instance)                                                # this statement will create an instance to the primary key related to the candidate
                instance.votes = 0
                                                                # this statement will add a vote the instance linking to that particular name...
                instance.save()
                            # this will finally save the vote to the database for the respected field..
            else:
                continue
        #candidates = Candidate.objects.all()
        #for x in candidates.name:
            #candidates.votes = 0
        messages.success(request, " All votes are cleared from the Mock Poll Database..")
        return render(request, 'preciding_officer.html')
      
######################################################  Ajax listener   #######################################################
# def my_ajax_check(request):
#     if request.user.is_authenticated:
#         instance_ajax = extra_field.objects.get(users=request.user)
#         if instance_ajax.status == True:
#             return HttpResponse(status=403)
#         else:
#             return HttpResponse(status=200)    
