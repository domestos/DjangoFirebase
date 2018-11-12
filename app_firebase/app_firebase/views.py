from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {
    'apiKey': "AIzaSyAsHr9i_UJL3ndSXHsD_PAqKGa8elOXKX8",
    'authDomain': "items-18814.firebaseapp.com",
    'databaseURL': "https://items-18814.firebaseio.com",
    'projectId': "items-18814",
    'storageBucket': "items-18814.appspot.com",
    'messagingSenderId': "400494160334"
  };
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()

def sinIn(request):

    return render(request,'signIn.html')


def postsign(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        massage = "Invalid credentials"
        return render(request, "signIn.html",{'massage':massage} )
    print(user['idToken'])
    session_idToken = user['idToken']
    request.session['uid']=str(session_idToken)
    return render(request,'welcome.html', {'e':email})


def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')
