
from django.shortcuts import render
#from . forms import MyForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from . forms import ApprovalForm
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . models import approvals
from . serializers import approvalsSerializers
import pickle
from sklearn.externals import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd


# When called , get the all objects/data
class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers

'''def myform(request):
    if request.method="POST":
        form=MyForm(request.POST)
        if form.is_valid():
            myform=form.save(commit=False)
    else:
        form=MyForm()'''
#@api_view(["POST"])
def approvereject(request):
    try:
        #ohe_col=joblib.load("C:\Users\tamanna13505\ML_with_django\DjangoAPI\MyAPI\loan_model.pkl")
        mdl=joblib.load("C:/Users/tamanna13505/ML_with_django/DjangoAPI/MyAPI/loan_model.pkl")
        mydata=request.data
        unit=np.array(list(mydata.values()))
        unit=unit.reshape(1,-1)
        scalers=joblib.load("C:/Users/tamanna13505/ML_with_django/DjangoAPI/MyAPI/scalers.pkl")
        X=scalers.transform(unit)
        y_pred=mdl.predict(X)
        y_pred=(y_pred>0.58)
        newdf=pd.DataFrame(y_pred,columns=['Status'])
        newdf=newdf.replace({True:'Approved', False:'Rejected'})
        return JsonResponse('Your Status is {}'.format(newdf), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
        
def cxcontact(request):
	if request.method=='POST':
		form=ApprovalForm(request.POST)
		if form.is_valid():
				firstname = form.cleaned_data['firstname']
				lastname = form.cleaned_data['lastname']
				dependants = form.cleaned_data['dependants']
				applicantincome = form.cleaned_data['applicantincome']
				coapplicatincome = form.cleaned_data['coapplicatincome']
				loanamt = form.cleaned_data['loanamt']
				loanterm = form.cleaned_data['loanterm']
				credithistory = form.cleaned_data['credithistory']
				gender = form.cleaned_data['gender']
				married = form.cleaned_data['married']
				graduatededucation = form.cleaned_data['graduatededucation']
				selfemployed = form.cleaned_data['selfemployed']
				area = form.cleaned_data['area']
				#myDict = (request.POST).dict()
				#df=pd.DataFrame(myDict, index=[0])
				#answer=approvereject(ohevalue(df))[0]
				#Xscalers=approvereject(ohevalue(df))[1]
				#print(Xscalers)
				#messages.success(request,'Application Status: {}'.format(answer))
	
	form=ApprovalForm()
				
	return render(request, 'myform/cxform.html', {'form':form})