from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from cooks.models import plan
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
    meal_plans = plan.objects.filter(owner=request.user)

    context = {'username': user.username,
               'welcome': welcome_id,
               'plans': meal_plans
               }
    return render(request, 'registration/welcome.html', context=context)


class make_plan(CreateView):
    login_required = True
    model = plan
    fields = ['name']
    success_url = reverse_lazy('welcome')
    template_name_suffix = '_make'

    def form_valid(self, form):
        cook = form.save(commit=False)
        cook.owner = User.objects.get(id=self.request.user.id)
        cook.save()
        return redirect('welcome')
