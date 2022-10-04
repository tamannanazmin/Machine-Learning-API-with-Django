
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
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
from django.contrib import messages



# When called , get the all objects/data
class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers
def ohevalue(df):
	ohe_col=joblib.load("C:/Users/tamanna13505/ML_with_django/DjangoAPI/MyAPI/allcol.pkl")
	cat_columns=['Gender','Married','Education','Self_Employed','Property_Area']
	df_processed = pd.get_dummies(df, columns=cat_columns)
	newdict={}
	for i in ohe_col:
		if i in df_processed.columns:
			newdict[i]=df_processed[i].values
		else:
			newdict[i]=0
	newdf=pd.DataFrame(newdict)
	return newdf
def approvereject(unit):
	try:
		mdl=joblib.load("/Users/tamanna13505/ML_with_django/DjangoAPI/MyAPI/loan_model.pkl")
		scalers=joblib.load("/Users/tamanna13505/ML_with_django/DjangoAPI/MyAPI/scalers.pkl")
		X=scalers.transform(unit)
		y_pred=mdl.predict(X)
		y_pred=(y_pred>0.58)
		newdf=pd.DataFrame(y_pred, columns=['Status'])
		newdf=newdf.replace({True:'Approved', False:'Rejected'})
		#k.clear_session()
		return newdf.values[0][0]
	except ValueError as e:
		print(e)
		return (e.args[0])
        
def cxcontact(request):
	if request.method=='POST':
		form=ApprovalForm(request.POST)
		if form.is_valid():
			Firstname = form.cleaned_data['firstname']
			Lastname = form.cleaned_data['lastname']
			Dependents = form.cleaned_data['Dependents']
			ApplicantIncome = form.cleaned_data['ApplicantIncome']
			CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
			LoanAmount = form.cleaned_data['LoanAmount']
			Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
			Credit_History = form.cleaned_data['Credit_History']
			Gender = form.cleaned_data['Gender']
			Married = form.cleaned_data['Married']
			Education = form.cleaned_data['Education']
			Self_Employed = form.cleaned_data['Self_Employed']
			Property_Area = form.cleaned_data['Property_Area']
			print(Firstname, Lastname, Dependents, ApplicantIncome,
			 CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,Gender,Married,Education,Self_Employed,Property_Area)
			myDict = (request.POST).dict()
			print('my Dictonary: ',myDict)
			df=pd.DataFrame(myDict, index=[0])
			print('DF: ',df)
			answer=approvereject(ohevalue(df))[0]
			print('Answer:',answer)
			#Xscalers=approvereject(ohevalue(df))[1]
			#print(Xscalers)
			messages.success(request,'Application Status: {}'.format(answer))
	
	form = ApprovalForm()
				
	return render(request, 'myform/cxform.html', {'form':form})