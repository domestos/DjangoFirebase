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
database = firebase.database()
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

def signUp(request):
    return  render(request, 'signUp.html')

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user=authe.create_user_with_email_and_password(email, password)
    except:
        massage = "Unable to create account try again"
        return render(request, 'signUp.html', {'massage':massage})

    uid = user['localId']
    data={'name':name, 'status':'1'}
    database.child('users').child(uid).child('details').set(data)

    return render(request, 'signIn.html')


def createreport(request):
    return render(request, 'createreport.html')


def post_create_report(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Europe/Kiev')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    milis = int(time.mktime(time_now.timetuple()))

    work = request.POST.get('work')
    progress = request.POST.get('progress')
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a ['localId']
    print(str(a))
    data = {
        'work':work,
        'progress':progress
    }
    database.child('users').child(a).child('reports').child(milis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request, 'welcome.html',{'e':name})


def check_report(request):
    import datetime
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a ['localId']
    timestamps = database.child('users').child(a).child('reports').shallow().get().val()
    lis_times = []
    #careate array with times and sort it
    for i in timestamps:
        lis_times.append(i)
    lis_times.sort(reverse=True)
    #get  works from times
    works = []
    for i in lis_times:
        work = database.child("users").child(a).child('reports').child(i).child('work').get().val()
        works.append(work)

    print(timestamps)
    print(works)
    date = []
    for i in lis_times:
        i = float(i)
        d = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(d)

    comb_lis = zip(lis_times, date, works)
    name = database.child('users').child(a).child('details').child('name').get().val()
    print(comb_lis)
    #return render(request, "welcome.html", {'comb_lis':comb_lis,'e':name })
    return render(request, "checkreport.html", {'comb_lis':comb_lis,'e':name })


def post_check(request):
    import datetime
    time = request.GET.get('z')
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a ['localId']
    print("HELLO")
    work = database.child('users').child(a).child('reports').child(time).child('work').get().val()
    progress = database.child('users').child(a).child('reports').child(time).child('progress').get().val()
    i = float(time)
    d = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    return render(request, 'post_check.html', {'work':work, 'progress':progress,'date':d})
