from django.shortcuts import redirect, render
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
from django.urls import path
import os

# Create your views here.
def home(request):
    mydata=MyFileUpload.objects.all()    
    myform=MyFileForm()
    if mydata!='':
        context={'form':myform,'mydata':mydata}
        return render(request,'index.html',context)
    else:
        context={'form':myform}
        return render(request,"index.html",context)

def uploadfile(request):
    if request.method=="POST":
        myform=MyFileForm(request.POST,request.FILES)        
        if myform.is_valid():
            MyFileName = request.POST.get('file_name') 
            MyFile = request.FILES.get('file')

            exists=MyFileUpload.objects.filter(my_file=MyFile).exists()

            if exists:
                messages.error(request,'The file %s is already exists...!!!'% MyFile)
            else:
                MyFileUpload.objects.create(file_name=MyFileName,my_file=MyFile).save()
                messages.success(request,"File uploaded successfully.")
        return redirect('index')

def deleteFile(request,id):
    mydata=MyFileUpload.objects.get(id=id)    
    mydata.delete()    
    os.remove(mydata.my_file.path)
    messages.success(request,'File deleted successfully.')  
    return redirect('home')