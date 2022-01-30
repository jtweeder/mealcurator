from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import create_cook_form

# Create your views here.


def register_cook(request):
    form = create_cook_form
    if request.method == 'POST':
        form = create_cook_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)

@login_required
def cook_profile(request):
    user = request.user
    name = f'{user.first_name} {user.last_name}'
    email = user.email
    # TODO: Make a test to check for name
    welcome_id = 'Hello Mysterious...'
    if len(name) > 1:
        welcome_id = name
    if len(name) <= 1 and len(email) > 0:
        welcome_id = email
    if len(email) > 1 and len(name) > 1:
        welcome_id = f'{name} : {email}'
    context = {'username': user.username,
               'welcome': welcome_id,
               }
    return render(request, 'registration/welcome.html', context=context)
