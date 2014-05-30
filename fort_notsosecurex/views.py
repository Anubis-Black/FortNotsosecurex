from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from fort_notsosecurex.models import Account


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Invalid username and/or password.')
    return render_to_response('login.html', context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return render_to_response('login.html', context_instance=RequestContext(request))


def register_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            messages.error(request, 'Username and/or password empty.')
            return render_to_response('register.html', context_instance=RequestContext(request))
        user = User(username=username, password=password)
        user.save()
        messages.success(request, 'Registration successful!')
        return render_to_response('login.html', context_instance=RequestContext(request))
    return render_to_response('register.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request):
    return render_to_response('index.html', {'user': request.user})


@login_required(login_url='/login/')
def get_account(request, account_id):
    account = request.user.account_set.filter(number=account_id)
    if account:
        account = account[0]
    else:
        raise Http404

    return render_to_response('account.html', {'account': account, 'user': request.user})


@login_required(login_url='/login/')
def make_transfer(request):
    if request.POST:
        from_account = request.POST['from_account']
        to_account = request.POST['to_account']
        sum = request.POST['sum']
        if not from_account or not to_account or not sum:
            messages.error(request, 'Insufficient data.')
        else:
            from_account = Account.objects.filter(number=int(from_account))[0]
            to_account = Account.objects.filter(number=int(to_account))[0]
            sum = Decimal(sum)

            if from_account.user != request.user or to_account.user != request.user:
                messages.error(request, 'Invalid data.')
            elif from_account.number == to_account.number:
                messages.error(request, 'Source and target accounts must be different.')
            elif sum < 0:
                messages.error(request, 'You cannot transfer a negative amount.')
            else:
                from_account.balance -= sum
                to_account.balance += sum
                from_account.save()
                to_account.save()
                messages.success(request, 'Successfully transferred ${0} from account {1} to account {2}.'.format(sum, from_account, to_account))
    return render_to_response('transfer.html', context_instance=RequestContext(request))