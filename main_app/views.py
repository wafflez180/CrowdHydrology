from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

# Create your views here.
@login_required
def index(request):
    return render(request, 'main_app/index.html')

@login_required
def download(request):
    path = request.GET['path']
    file_path = os.path.join(settings.STATIC_DIR, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
