from django.shortcuts import render,redirect
import requests
from django.contrib import messages
from bs4 import BeautifulSoup
from .models import getLinkData,contactForm
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def getLinks(request):
    if(request.method == "POST"):
        getlinkinfo = request.POST.get('getlinkinfo','')
        page = requests.get(getlinkinfo)
        soup = BeautifulSoup(page.text,'html.parser')
        getLinkData.objects.all().delete()
        for link in soup.find_all('a'):
            get_address = link.get('href')
            get_name = link.string
            getLinkData.objects.create(link_name=get_name,link_address=get_address)
        return redirect("/")
    else:
        searchLink = request.GET.get('searchLink')
        if(searchLink!='' and searchLink is not None):
            all_links = getLinkData.objects.filter(Q(link_name__icontains=searchLink) | Q(link_address__icontains=searchLink))
            if not all_links:
                messages.warning(request,f"No matching keyword for {searchLink}")
                all_links = getLinkData.objects.all()
            else:
                messages.success(request,f"Following are results for {searchLink}")
        elif(searchLink==''):
            messages.warning(request,f"Enter a valid Search...")
        else:
            all_links = getLinkData.objects.all()
        paginator = Paginator(all_links,5)
        page = request.GET.get('page')
        all_links = paginator.get_page(page)
    
    return render(request,"scraperApp/index.html",{'all_links':all_links})

def getContact(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        feedback = request.POST.get('feedback')
        contactForm.objects.create(first_name=first_name,last_name=last_name,email=email,subject=subject,feedback=feedback)
    return render(request,"scraperApp/contact.html")
 