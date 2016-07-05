from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from tasks import process_file
from .models import ML_Model, SP_Model, Sample
from tables.choices import RIPENESS_LABELS
from .serializers import *
import tempfile

class SampleViewSet(viewsets.ModelViewSet):
    """
    Allows samples to be viewed or edited.
    """
    queryset = Sample.objects.all().order_by('-id') # Descending order
    serializer_class = SampleSerializer


class ML_ModelViewSet(viewsets.ModelViewSet):
    """
    Allows machine learning models to be viewed or edited.
    """
    queryset = ML_Model.objects.all().order_by('-id')
    serializer_class = ML_ModelSerializer


class SP_ModelViewSet(viewsets.ModelViewSet):
    """
    Allows signal processing models to be viewed, edited, or deleted.
    """
    queryset = SP_Model.objects.all().order_by('-id')
    serializer_class = SP_ModelSerializer

class SampleListView(View):
    """
    Allows user to check and modify labels.
    """
    template_name = 'samples_list.html'

    def get(self, request):
        samples = Sample.objects.all()

        return render(request, self.template_name, context={'samples': samples})

    def post(self, request):
        samples = Sample.objects.all()
        for s in samples:
            s.label = RIPENESS_LABELS[str(request.POST[str(s.pk)]).lower()]
            # label_is_right doesn't make too much sense tbh
            s.save()
        return render(request, self.template_name, context={'samples': samples})

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