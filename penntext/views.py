from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from penntext.models import User, Subject, Sell, TicketSell, HouseholdSell, Term, SubletsSell, Other, UserProfile
from penntext.forms import SubjectForm, SellForm, TermForm, UserForm, UserProfileForm, TicketSellForm, HouseholdSellForm, SubletsSellForm, OtherForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
from django.core.mail import EmailMessage
from django.http import HttpRequest

def addurl(subject_list):
    for subject in subject_list:
        subject.url = subject.name.replace(' ', '_')

def index(request):
    context = RequestContext(request)
    return render_to_response('penntext/index.html', {}, context)

def about(request):
    context= RequestContext(request)
    return render_to_response('penntext/about.html', {'mymessage': "PennText says: Here is the about page."}, context)

def subject(request, subject_name_url):
    context = RequestContext(request)
    subject_name = subject_name_url.replace('_', ' ')
    context_dict = {'subject_name' : subject_name}
    subject_list = Subject.objects.order_by('views')

    addurl(subject_list)

    context_dict['subjects'] = subject_list

    try:
        subject = Subject.objects.get(name = subject_name)
        sell = Sell.objects.filter(subject=subject)

        sellord = sell.order_by('-time')
        a = 0
        for house in sellord:
            house.uniq = a
            a = a + 1

        context_dict['sells'] = sellord
        context_dict['subject'] = subject
        context_dict['subject_name_url'] = subject_name_url

    except Subject.DoesNotExist:
        pass

    return render_to_response('penntext/subject.html', context_dict, context)

def sublist(request):
    context = RequestContext(request)
    subject_list = Subject.objects.order_by('views')

    addurl(subject_list)

    subject = subject_list

    return render_to_response('penntext/sublist.html', {'subjects': subject}, context)


def termlist(request):
    context = RequestContext(request)
    term_list = Term.objects.order_by('views')
    addurl(term_list)
    term = term_list
    return render_to_response('penntext/termlist.html', {'terms': term}, context)


def term(request, term_name_url):
    context = RequestContext(request)
    term_name = term_name_url.replace('_', ' ')
    context_dict = {'term_name' : term_name}
    term_list = Term.objects.order_by('views')

    try:
        term = Term.objects.get(name = term_name)

        subsell = SubletsSell.objects.filter(term=term)

        subord = subsell.order_by('price')
        a = 0
        for house in subord:
            house.uniq = a
            a = a + 1

        context_dict['subsells'] = subord
        context_dict['term'] = term
        context_dict['term_name_url'] = term_name_url

    except Term.DoesNotExist:
        pass
    addurl(term_list)
    context_dict['terms'] = term_list
    return render_to_response('penntext/term.html', context_dict, context)

def tickets(request):
    context = RequestContext(request)
    ticket_list = TicketSell.objects.order_by('-time')
    a = 0
    for house in ticket_list:
        house.uniq = a
        a = a + 1

    return render_to_response('penntext/tickets.html', {'ticket_list': ticket_list}, context)


def households(request):
    context = RequestContext(request)
    household_list = HouseholdSell.objects.order_by('-time')
    return render_to_response('penntext/household.html', {'household_list': household_list}, context)


def others(request):
    context = RequestContext(request)
    other_list = Other.objects.order_by('-time')
    return render_to_response('penntext/other.html', {'other_list': other_list}, context)


@login_required
def add_ticket(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = TicketSellForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.url = (ticket.ticket).replace(' ','_')

            ticket.name = request.user.get_username()
            ticket.email = request.user.email
            ticket.userid = (request.user).id
            if 'picture' in request.FILES:
                ticket.picture = request.FILES['picture']
            form.save()
            return tickets(request)
        else:
            print form.errors
    else:
        form = TicketSellForm()
    return render_to_response('penntext/add_ticket.html', {'form': form}, context)


@login_required
def add_household(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = HouseholdSellForm(request.POST, request.FILES)
        if form.is_valid():
            household =form.save(commit=False)
            household.url = (household.item).replace(' ','_')
            household.userid = (request.user).id

            household.name = request.user.get_username()
            household.email = request.user.email
            if 'picture' in request.FILES:
                household.picture = request.FILES['picture']

            form.save()
            return households(request)
        else:
            print form.errors
    else:
        form = HouseholdSellForm()
    return render_to_response('penntext/add_household.html', {'form': form}, context)

@login_required
def add_other(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = OtherForm(request.POST, request.FILES)
        if form.is_valid():

            other = form.save(commit=False)
            other.userid = (request.user).id
            other.url = (other.title).replace(' ','_')
            other.name = request.user.get_username()
            other.email = request.user.email


            if 'picture' in request.FILES:
                other.picture = request.FILES['picture']

            form.save()
            return others(request)
        else:
            print form.errors
    else:
        form = OtherForm()
    return render_to_response('penntext/add_other.html', {'form': form}, context)






@login_required
def add_subject(request):
    context = RequestContext(request)
    subject_list = Subject.objects.order_by('views')
    addurl(subject_list)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return sublist(request)
        else:
            print form.errors
    else:
        form = SubjectForm()
    return render_to_response('penntext/add_subject.html', {'form': form, 'subjects': subject_list}, context)


@login_required
def add_term(request):
    context = RequestContext(request)
    term_list = Term.objects.order_by('views')
    addurl(term_list)
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return termlist(request)
        else:
            print form.errors
    else:
        form = TermForm()
    return render_to_response('penntext/add_term.html', {'form': form, 'terms': term_list}, context)


@login_required
def add_sale(request, subject_name_url):

    context = RequestContext(request)
    subject_name = subject_name_url.replace('_', ' ')

    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)

        if form.is_valid():
            sell = form.save(commit=False)

            try:
                subj = Subject.objects.get(name=subject_name)
                sell.subject = subj
                sell.userid = (request.user).id
                sell.url = (sell.book).replace(' ','_')
                sell.subjurl = (sell.subject.name).replace(' ','_')
                sell.name = request.user.get_username()
                sell.email = request.user.email
            except Subject.DoesNotExist:
                render_to_response('penntext/add_subject.html', {}, context)

            if 'picture' in request.FILES:
                sell.picture = request.FILES['picture']

            sell.save()

            return subject(request, subject_name_url)
        else:
            print form.errors
    else:
        form = SellForm()

    return render_to_response('penntext/add_sale.html',
                              {'subject_name_url':subject_name_url,
                               'subject_name': subject_name,
                               'form': form,
                               }, context)

@login_required
def add_subsell(request, term_name_url):

    context = RequestContext(request)
    term_name = term_name_url.replace('_', ' ')

    if request.method == 'POST':
        form = SubletsSellForm(request.POST, request.FILES)
        if form.is_valid():
            subsell = form.save(commit=False)

            try:
                term = Term.objects.get(name=term_name)
                subsell.term = term
                subsell.userid = (request.user).id
                subsell.url = (subsell.title).replace(' ','_')

                subsell.termurl = (subsell.term.name).replace(' ','_')
                subsell.name = request.user.get_username()
                subsell.email = request.user.email
            except Subject.DoesNotExist:
                render_to_response('penntext/add_term.html', {}, context)

            if 'picture' in request.FILES:
                subsell.picture = request.FILES['picture']



            subsell.save()
            go = '/localquaker/term/' + term_name_url
            return HttpResponseRedirect(go)
        else:
            print form.errors
    else:
        form = SubletsSellForm()

    return render_to_response('penntext/add_subsell.html',
                              {'term_name_url':term_name_url,
                               'term_name':term_name,
                               'form': form}, context)

@login_required
def my_sale(request):
    context = RequestContext(request)
    current_user = request.user.id
    sell = Sell.objects.filter(userid=current_user)
    subsell = SubletsSell.objects.filter(userid=current_user)
    ticketsell = TicketSell.objects.filter(userid=current_user)
    householdsell = HouseholdSell.objects.filter(userid=current_user)
    othersell = Other.objects.filter(userid=current_user)
    return render_to_response('penntext/my_sale.html', {'sells': sell, 'subsells': subsell,
                                                        'ticketsells': ticketsell,
                                                        'householdsells': householdsell,
                                                        'othersells': othersell
                                                        }, context)

@login_required
def del_sale(request, sell_name_url, sell_id):
    sell_name= sell_name_url.replace('_', ' ')
    todel= Sell.objects.get(book = sell_name, userid = request.user.id,id = sell_id)
    todel.picture.delete()
    todel.delete()
    return HttpResponseRedirect('/localquaker/my_sale/')


@login_required
def del_subsale(request, sell_name_url, sell_id):
    sell_name= sell_name_url.replace('_', ' ')
    todel= SubletsSell.objects.get(title = sell_name, userid = request.user.id,id = sell_id)
    todel.picture.delete()
    todel.delete()
    return HttpResponseRedirect('/localquaker/my_sale/')

@login_required
def del_ticketsale(request, sell_name_url, sell_id):
    sell_name= sell_name_url.replace('_', ' ')
    todel= TicketSell.objects.get(ticket = sell_name, userid = request.user.id,id = sell_id)
    todel.picture.delete()
    todel.delete()
    return HttpResponseRedirect('/localquaker/my_sale/')

@login_required
def del_othersale(request, sell_name_url, sell_id):
    sell_name= sell_name_url.replace('_', ' ')
    todel= Other.objects.get(title = sell_name, userid = request.user.id,id = sell_id)
    todel.picture.delete()
    todel.delete()



    return HttpResponseRedirect('/localquaker/my_sale/')

@login_required
def del_housesale(request, sell_name_url, sell_id):
    sell_name= sell_name_url.replace('_', ' ')
    todel= HouseholdSell.objects.get(item = sell_name, userid = request.user.id,id = sell_id)
    todel.picture.delete()
    todel.delete()
    return HttpResponseRedirect('/localquaker/my_sale/')



def register(request):

    # Like before, get the request's context.
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/localquaker/')



    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data= request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid:

            # Save the user's form data to the database.
            user = user_form.save()


            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)

            profile.user=user

            profile.activation_key = str(random.randint(0, 9999999))
            # Update our variable to tell the template registration was successful.
            # Send an email with the confirmation link
            email_subject = 'PennText Confirmation'
            email_body = "To activate your account, click this link: \n\n http://tahmidshahriar.pythonanywhere.com/localquaker/confirm/%s" % (
                profile.activation_key)
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send()
            profile.save()
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render_to_response(
            'penntext/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)



def confirm(request, activation_key):
    userprofile = UserProfile.objects.get(activation_key=activation_key)
    userprofile.user.is_active = True
    userprofile.user.save()
    userprofile.save()

    return HttpResponseRedirect('/localquaker/login/')

def offer(request, username, book, req):

    user = User.objects.get(username=username)
    book = str(book.replace('_',' '))
    email_subject = book + ' offer'
    email_body = str(request.REQUEST["name"]) + " wishes to purchase the item " + str(book) + " for $" +str(request.REQUEST["price"]) +". Please reply to the following email address: " + str(request.REQUEST["email"])
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()
    go = '/localquaker/' + req
    return HttpResponseRedirect(go)


def offerTerm(request, username, book, req, term):

    user = User.objects.get(username=username)
    book = str(book.replace('_',' '))
    email_subject = book + ' offer'
    email_body = str(request.REQUEST["name"]) + " wishes to purchase the item " + str(book) + " for $" +str(request.REQUEST["price"]) +". Please reply to the following email address: " + str(request.REQUEST["email"])
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()
    go = '/localquaker/' + term + '/' + req
    return HttpResponseRedirect(go)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context= RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/localquaker/')

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/localquaker/')
            else:
                # An inactive account was used - no logging in!
                context_dict = {'error' :'An inactive account was used.'}
                return render_to_response('penntext/login.html', context_dict, context)

        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)

            context_dict = {'error' :  'Wrong username or password.'}
            return render_to_response('penntext/login.html', context_dict, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('penntext/login.html',{}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/localquaker/')







