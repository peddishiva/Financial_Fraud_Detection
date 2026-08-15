import os
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import pandas as pd

from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,detect_financial_fraud,detection_ratio,detection_accuracy

def login(request):

    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            users = ClientRegister_Model.objects.filter(username=username)
            for enter in users:
                if check_password(password, enter.password) or enter.password == password:
                    request.session["userid"] = enter.id
                    return redirect('ViewYourProfile')
        except Exception:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        hashed_password = make_password(password)
        ClientRegister_Model.objects.create(username=username, email=email, password=hashed_password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def predict_financial_transaction_type(request):
    if request.method == "POST":

        Fid= request.POST.get('Fid')
        trans_datetime= request.POST.get('trans_datetime')
        Acc_num= request.POST.get('Acc_num')
        bankingtype= request.POST.get('bankingtype')
        category= request.POST.get('category')
        amt= request.POST.get('amt')
        Name= request.POST.get('Name')
        gender= request.POST.get('gender')
        street= request.POST.get('street')
        city= request.POST.get('city')
        zip= request.POST.get('zip')
        lat= request.POST.get('lat')
        lon= request.POST.get('lon')
        job= request.POST.get('job')
        dob= request.POST.get('dob')
        trans_num= request.POST.get('trans_num')
        merch_lat= request.POST.get('merch_lat')
        merch_long= request.POST.get('merch_long')


        dataset_path = os.path.join(settings.BASE_DIR, 'Datasets.csv')
        df = pd.read_csv(dataset_path)

        def apply_results(label):
            if (label == 0):
                return 0  # Fraud Not Detected
            elif (label == 1):
                return 1  # Fraud Detected

        df['Results'] = df['Label'].apply(apply_results)

        cv = CountVectorizer()
        X = df['Fid'].apply(str)
        y = df['Results']

        print("Fid")
        print(X)
        print("Label")
        print(y)

        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape


        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("KNeighborsClassifier")
        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))
        models.append(('KNeighborsClassifier', kn))


        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Fraud Not Detected'
        elif prediction == 1:
            val = 'Fraud Detected'

        print(val)
        print(pred1)

        detect_financial_fraud.objects.create(
        Fid=Fid,
        trans_datetime=trans_datetime,
        Acc_num=Acc_num,
        bankingtype=bankingtype,
        category=category,
        amt=amt,
        Name=Name,
        gender=gender,
        street=street,
        city=city,
        zip=zip,
        lat=lat,
        lon=lon,
        job=job,
        dob=dob,
        trans_num=trans_num,
        merch_lat=merch_lat,
        merch_long=merch_long,
        Prediction=val)

        return render(request, 'RUser/predict_financial_transaction_type.html',{'objs': val})
    return render(request, 'RUser/predict_financial_transaction_type.html')



