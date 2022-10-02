from django.shortcuts import render
from . forms import MyForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
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
    queryset=approvals.objects.all()
    serializer_class=approvalsSerializers
def myform(request):
    if request.method="POST":
        form=MyForm(request.POST)
        if form.is_valid():
            myform=form.save(commit=False)
    else:
        form=MyForm()
@api_view(["POST"])
def approvereject(request):
    try:
        mdl=joblib.load("C:\Users\tamanna13505\ML_with_django\ML_CODE")
        mydata=request.data
        unit=np.array(list(mydata.values()))
        unit=unit.reshape(1,-1)
        scalers=joblib.load("")
        X=scalers.transform(unit)
        y_pred=mdl.predict(X)
        y_pred=(y_pred>0.58)
        newdf=pd.DataFrame(y_pred,columns=['Status'])
        newdf=newdf.replace({True:'Approved', False:'Rejected'})
        return JsonResponse('Your Status is {}'.format(newdf), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)