from django.shortcuts import render, redirect
from .forms import create_cook_form
# Create your views here.


def register_cook(request):
    form = create_cook_form
    if request.method == 'POST':
        form = create_cook_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)
