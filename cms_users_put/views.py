from django.shortcuts import render
from models import Page
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden

# Create your views here.

@csrf_exempt
def main(request, resource):
    if request.user.is_authenticated():
        logged = ("Logged in as " + request.user.username
                + " <a href='/admin/logout/'>Log out</a>")
    else:
        logged = ("Not logged in. "
                + "<a href='/admin/login/?next=/admin/'>Log in</a>")

    if request.method == "GET":
        try:
            page_entry = Page.objects.get(name=resource)
            return HttpResponse(logged + "<br/>" + page_entry.page)
        except Page.DoesNotExist:
            if resource == "":
                resource = "Main Page"
            return HttpResponseNotFound(logged + "<br/>"
                + "Page not found: %s." % resource)
    elif request.method == "PUT":
        new_entry = Page(name=resource, page=request.body)
        new_entry.save()
        return HttpResponse(logged + "<br/>"
                + "Succesful PUT operation: " + request.body)
    else:
        return HttpResponseForbidden(logged + "<br/>"
            + "Operation not available")