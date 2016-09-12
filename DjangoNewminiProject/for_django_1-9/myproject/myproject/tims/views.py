# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.tims.models import Stream
#from myproject.myapp import models as m
from myproject.tims.forms import StreamForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = StreamForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Stream(streamfile=request.FILES['StreamName'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = StreamForm()  # A empty, unbound form

    # Load documents for the list page
    streams = Stream.objects.all()
    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'Streams': streams, 'form': form}
    )
