from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    frontend_stuff = {'search': search}
    return render(request, 'my_app/new_search.html', frontend_stuff)
