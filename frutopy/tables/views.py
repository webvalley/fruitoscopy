from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from rest_framework import viewsets
from tasks import process_file
from .models import ML_Model, SP_Model, Sample
from .serializers import *
import tempfile

class SampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows samples to be viewed or edited.
    """
    queryset = Sample.objects.all().order_by('-id') # Descending order
    serializer_class = SampleSerializer


class ML_ModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows machine learning models to be viewed or edited.
    """
    queryset = ML_Model.objects.all().order_by('-id')
    serializer_class = ML_ModelSerializer


class SP_ModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows signal processing models to be viewed, edited, or deleted.
    """
    queryset = SP_Model.objects.all().order_by('-id')
    serializer_class = SP_ModelSerializer


def handle_uploaded_file(f):
    """
    Handles uploaded file and triggers its processing.
    """
    with tempfile.NamedTemporaryFile(delete=False) as destination:
        name = destination.name
        for chunk in f.chunks():
            destination.write(chunk)
            print('Saving to %s' % name)
        process_file.delay(name)


def upload_file(request):
    """
    Handles requests for file upload.
    """
    if request.method == 'POST':
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect('/success')
    #print('not valid you idiot')
    return render(request, 'upload.html')


def success(request):
    """
    Redirects to Success page on successful file upload.
    """
    return render(request, 'success.html')