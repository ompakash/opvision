from django.shortcuts import render

# Create your views here.
def contact(request):
    return render(request, template_name='vision/contact.html')