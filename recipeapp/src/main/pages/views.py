from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# A view is where you tell django what to do/display


def home_view(request, *args, **kwargs):
    if request.method == 'POST' and 'run_script' in request.POST:
        # import function to run
        from pages.testmatch import test_function
    # call function
        test_function()
    # return user to required page
    return render(request, "home.html", {})
