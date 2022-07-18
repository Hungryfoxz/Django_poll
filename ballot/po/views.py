from multiprocessing import context
import re
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render, reverse
from .models import Candidate, Mock, Mock_Positions, Positions, extra_field,Voted, po_vote_showing



# # Integrating Pusher js Here
# '''import pusher
# pusher_client = pusher.Pusher(
#   app_id='1425713',
#   key='7abfa1c5b2f52b98dc73',
#   secret='dc23817db4dc788e065d',
#   cluster='ap2',
#   ssl=True
# )
# '''

# Create your views here.
 
#Create a global variable to chechk the no. of students voted...
# voted = 0 
# print(voted)
print(" If you are seeing this message in the terminal that this means that it is working properly ")
#############################################  Index.html  ######################################################################

def index(request):
    # adding data to the extra fields ..
    User = get_user_model()
    for i in User.objects.all():
        if not extra_field.objects.filter(users=i).exists():
            instance = extra_field()
            instance.users = i
            instance.save()
            new_instance = po_vote_showing()
            new_instance.users = i
            new_instance.save()
            print(i)
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
            if user.is_superuser:
                login(request, user)
                return render(request, 'preciding_officer.html')
                
            else:
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

# def voter_show_ballot(request):
#     if not request.user.is_authenticated:
#         return redirect('login_view')
#     else:
#         instance_var = extra_field.objects.get(users=request.user)
#         if instance_var.status == True:
#             return redirect('voter')
#         else:
#             messages.warning(request, '***Waiting for the Preciding officer to allow the access..Please ask the Officer to provide access...')
#             return render(request,'voter_show_ballot.html')


############################################  Voter vote panel  ##################################################################

def voter(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    else:
        # Checking the permission from the preciding officer..
        if request.method == 'POST':
            instance_var = extra_field.objects.get(users=request.user)
            if instance_var.status == True:
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
                messages.success(request, 'Congratulations ! Your vote has been recorded..')
                #context = { 'data':'disabled'}

                #########################################################################
                # Integrating Pusher js here...
                #name = request.user
                #channel_name = u"{}".format(request.user)
                #print(channel_name)
                # pusher_client.trigger([str(request.user.id)], 'my-event', {'message': 'The Voter has Voted Successfully.'})
                #########################################################################
                # Counter to increase the no of students voted...
                # global voted
                # voted +=1 
                # print(voted)
                if(Voted.objects.filter(pk=1).exists()):
                    inst_tot_vot = Voted.objects.get(pk=1)
                    inst_tot_vot.voted += 1
                    inst_tot_vot.save()
                    # print(inst_tot_vot.voted)
                return redirect('voter')#, ({'context':context})
            else:
                candidates = Candidate.objects.all()
                position = Positions.objects.all().order_by('priority')
                messages.warning(request, 'Request the Presiding officer to allow the Voting !')
                return render(request, 'voter.html',{'candidates': candidates,'positions':position})
        #If the condition is false..ie the po has not allowed the user to vote still now..
        else:
            # messages.warning(request, 'Waiting for the Presiding officer to allow the Vote !')
            # return redirect('voter.html')

            candidates = Candidate.objects.all()
            position = Positions.objects.all().order_by('priority')
            return render(request, 'voter.html',{'candidates': candidates,'positions':position})
                # Checking the returned form from the user..
                # else:
                #     return redirect('voter_show_ballot')

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
        if request.user.is_superuser:
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
        # print(x)
        for ids in x:
            if Candidate.objects.filter(pk=ids).exists():
                instance = Candidate.objects.get(pk=ids)
                #print(instance)                                                # this statement will create an instance to the primary key related to the candidate
                instance.votes = 0
                                                                # this statement will add a vote the instance linking to that particular name...
                instance.save()
                            # this will finally save the vote to the database for the respected field..
                if Voted.objects.filter(pk=1).exists():
                    inst_tot_vot = Voted.objects.get(pk=1)
                    inst_tot_vot.voted = 0
                    inst_tot_vot.save()
            else:
                continue
        #candidates = Candidate.objects.all()
        #for x in candidates.name:
            #candidates.votes = 0
        return redirect('officer')

################################################  Mock panel  ########################################################################### 
def mock_panel(request):
    if request.user.is_authenticated:
        return render(request, 'mock_panel.html')

############################################### total_students_voted ##################################################################

def total_students_voted(request):
    if request.user.is_authenticated:
        #global voted
        #print(voted)
        int_tot_vot = Voted.objects.get(pk=1)
        context = { 'data': int_tot_vot.voted }
        return render(request, 'total_students_voted.html', {'total':context})
    else:
        return redirect('login')

##############################################     mock_results    ###################################################################

def mock_results(request):
    if request.user.is_authenticated:
        # user_is = request.user
        user_instance = po_vote_showing.objects.get(users=request.user)
        if user_instance.status == True:
            if user_instance.final_status == False:
                user_instance.final_status = True
                user_instance.save()
                mock = Candidate.objects.all()
                position = Positions.objects.all().order_by('priority')
                messages.warning(request, 'Please, Keep a copy/print of this result. After this time you will not be able to view the result.')
                return render(request, 'mock_results.html',{'candidates': mock,'positions':position})
            else:
                messages.warning(request,' You cannot view the results anymore, Because the Mock poll has ended ! Also you have exceeded the limit to view the results. For any querries ,contact Admin. ')
                return HttpResponseRedirect(reverse('mock_panel'))
        mock = Candidate.objects.all()
        position = Positions.objects.all().order_by('priority')
        return render(request, 'mock_results.html',{'candidates': mock,'positions':position})
    else:
        return redirect('login')

########################################## CLear mock poll results #################################################################

def mock_clear(request):
    if request.user.is_authenticated:

        # user_is = request.user
        user_instance = po_vote_showing.objects.get(users=request.user)
        if user_instance.status == True:
            return HttpResponse(status=202)
        else:
            user_instance.status = True
            user_instance.save()
            x = Candidate.objects.values_list('id', flat=True)
            # print(x)
            if Voted.objects.filter(pk=1).exists():
                        inst_tot_vot = Voted.objects.get(pk=1)
                        inst_tot_vot.voted = 0
                        inst_tot_vot.save()
            for ids in x:
                if Candidate.objects.filter(pk=ids).exists():
                    instance = Candidate.objects.get(pk=ids)
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
            # return render(request, 'mock_panel.html')
            return HttpResponse(status=200)
      
######################################################  Ajax listener   #######################################################
def my_ajax_check(request):
    if request.user.is_authenticated:
        instance_ajax = extra_field.objects.get(users=request.user)
        if instance_ajax.status == True:
            return HttpResponse(status=202)
        else:
            return HttpResponse(status=200)    

####################################################   tot Mock Votes  ###########################################################
def tot_mock(request):
    if request.user.is_authenticated:
        #global voted
        #print(voted)
        int_tot_vot = Voted.objects.get(pk=1)
        context = { 'data': int_tot_vot.voted }
        return render(request, 'tot_mock.html', {'total':context})
    else:
        return redirect('login')



##################################################### Original Voting #######################################################
def original_voting(request):
    return render(request, 'original_voting.html')
    # return HttpResponse(200)
