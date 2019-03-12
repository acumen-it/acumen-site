from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
import pyqrcode as pyq
from django.urls import reverse
from .models import Profile,Event,EventDetails,Organizer,Team,Otpgenerator,Payments
from django.contrib.auth.decorators import login_required
from .models import Profile
import random
from django.views.decorators.csrf import csrf_exempt
from instamojo_wrapper import Instamojo

API_KEY = 'f1761e15f5415be96a7248dea2bbdaf0'
AUTH_TOKEN = 'f509e1c1b11e28cad3260de8620b1456'

# Create your views here.
def home(request):
    user = request.user
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'acumenapp/home.html', {'user': user})
    else:
        return render(request, 'acumenapp/home.html')


def events(request):
    if request.user.is_authenticated:
        try:
            user = request.user
            user1 = User.objects.get(username=user)
            pro = Profile.objects.get(user=user1)
            eedet = EventDetails.objects.filter(qr_code=pro)
            evreglist=[]
            for eventdet in eedet:
                ev = Event.objects.get(event_id=eventdet.event_id)
                if not eventdet.amount_paid:
                    evreglist.append(ev.event_id)
                    print(eventdet.amount_paid)

            for i in evreglist:
                print(i)
            return render(request,"acumenapp/events.html",{'evreglist':evreglist})
        except:
            return render(request,"acumenapp/events.html")
    else:
        return render(request,"acumenapp/events.html")

def map3d(request):
    return render(request,"acumenapp/map3D.html")

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        user1 = User.objects.get(username=user)
        pro = Profile.objects.get(user=user1)
        ee = EventDetails.objects.filter(qr_code=pro)
        evregdet = []
        evreglist = []
        paidlist=[]
        if(len(evregdet)+1) == 12:
            pro.cost=200
        elif (len(evregdet)+1)%3 == 0:
            pro.cost = (len(evregdet)%3)*100
        else:
            pass
        for eventdet in ee:
            evregdet.append(eventdet)
            ev = Event.objects.get(event_id=eventdet.event_id)
            if eventdet.amount_paid:
                paidlist.append(ev)
            else:
                evreglist.append(ev)
            print(ev.event_name)
        if pro.cost%100 == 0:
            return render(request, 'acumenapp/dashboard.html', {'pro': pro, 'paidlist': paidlist, 'evreglist': evreglist,'combo':'combo'})
        else:
            return render(request, 'acumenapp/dashboard.html', {'pro': pro, 'paidlist': paidlist, 'evreglist': evreglist,'combo':'Normal'})

    else:
        return redirect(reverse('registration'))

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        print(username)
        emailid = request.POST.get("email")
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile')
        user = None
        try:
            user = User.objects.get(email=emailid)
        except:
            user = User.objects.create_user(username=emailid, email=emailid, password=password,first_name=username)
        print(user)
        user.save()
        qrcode =  emailid[:-10]
        sample = pyq.create(qrcode)
        sample.png('/home/acumenit/acumen-site/staticfiles/acusite/users/' + emailid[:-10] + '.png', scale=10)
        profile = Profile(user=user, phone_number=mobile_number, qr_code= emailid[:-10])
        profile.save()
        login(request, user)
        mail_subject = 'Your AcumenIT account has been created.'
        message = 'Show this at the venue. Your Qr is:'
        email = EmailMessage(
            mail_subject, message, to=[emailid]
        )
        email.attach_file('/home/acumenit/acumen-site/staticfiles/acusite/users/' + emailid[:-10] + ".png")
        email.send()
        return redirect(reverse("dashboard"))
    pass


#login Page
def registration(request):
    return render(request,"acumenapp/registration.html")

def sponsers(request):
    return render(request,"acumenapp/sponsers.html")

def map3dHome(request):
    return render(request,"acumenapp/map3dhome.html")


def team(request):
    return render(request,"acumenapp/team.html")

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

def login_view(request):
    if request.method == 'POST':
        # user = User.objects.create_user(**request.POST)
        #print(request.POST['email'],request.POST.get('password'))
        mail=request.POST.get('email')
        pw=request.POST.get('loginpassword')
        user = authenticate(username=mail, password=pw)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            return render(request,"acumenapp/registration.html",{"loggedin" :False})

def event_reg(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "GET":
            event = request.GET.get('event')
            ee=Event.objects.get(event_id=event)
            print(event,ee.event_cost)
            user1 = User.objects.get(username=user)
            print(user1)
            pro = Profile.objects.get(user=user1)
            pro.cost=pro.cost+ee.event_cost
            pro.save()
            print(pro.pk)
            ed=EventDetails(event_id=ee,team_id='none',qr_code=pro,status_choice='WAITING')
            ed.save()
            print(request.user.username)
            return HttpResponse("success")
    else:
        return redirect('registration')


def event_del(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "GET":
            event = request.GET.get('event')
            ee = Event.objects.get(event_id=event)
            user1 = User.objects.get(username=user.username)
            pro = Profile.objects.get(user=user1)
            evdel = []
            evdel = EventDetails.objects.filter(qr_code=pro, event_id=ee)
            for edel in evdel:
                if not edel.amount_paid:
                    edel.delete()
                    break
            pro.cost = pro.cost - ee.event_cost
            pro.save()

            return redirect(reverse('dashboard'))
    else:
        return redirect(reverse('home'))

@csrf_exempt
def change_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
            user = request.user
            user1 = User.objects.get(username=user.username)
            pro = Profile.objects.get(user=user1)
            user1.first_name=request.POST['first_name']
            user1.save()
            pro.roll_number=request.POST['roll_number']
            pro.phone_number=request.POST['phone_number']
            pro.college=request.POST['college']
            pro.branch=request.POST['branch']
            pro.year=request.POST['year']
            pro.save()
        return redirect(reverse('dashboard'))
    else:
        return redirect(reverse('home'))

def forgotpwd(request):
    return render(request,"acumenapp/forgot.html")

def gallery(request):
    return render(request,"acumenapp/gallery.html")


def otpgenerator(request):
    if request.method == 'GET':
        emailid = request.GET.get('email')
        otp = random.randint(999, 9999)
        obj = Otpgenerator(mailid = emailid, otp = otp)
        obj.save()
        mail_subject = 'Change password for your AcumenIT account.'
        message = 'Your OTP is:' + str(otp)
        email = EmailMessage(
            mail_subject, message, to=[emailid]
        )
        email.send()
        return redirect("forgotpwd")

def otpcomparator(request):
    if request.method == 'GET':
        gototp = request.GET.get('otp')
        email = request.GET.get('email')
        print(gototp)
        user1 = User.objects.get(email=email)
        if user1 is not None:
            obj = Otpgenerator.objects.get(mailid=user1.email)
            if obj.otp == gototp:
                return HttpResponse('Success')
            else:
                return redirect('registration')
        else:
            return redirect('registration')
    pass

def changepwd(request):
    if request.method == 'POST':
        pwd = request.POST.get('password')
        email = request.POST.get('emailid')
        user1 = User.objects.get(email=email)
        user1.set_password(pwd)
        user1.save()
        obj = Otpgenerator.objects.get(mailid=user1.email)
        obj.delete()
        return redirect('registration')
    else:
        return redirect('registration')
    pass


def payment_request(request):
    '''
    Creates a payment request and redirects to instamojo payments page and on completion returns to payment_response page.
    '''
    api = Instamojo(api_key=API_KEY,
                    auth_token=AUTH_TOKEN)
    eventid =request.GET['event']
    price = request.GET['price']
    variable=''
    if eventid =='all':
        variable='payment for acumen it registered events'
    else:
        eventdetail = Event.objects.get(event_id= eventid )
        variable='payment for acumen it '+str(eventdetail.event_name)+' event'
    response = api.payment_request_create(
        amount=price,
        purpose=variable,
        buyer_name=request.user.first_name,
        send_email=True,
        email=request.user.email,
        redirect_url="https://www.acumenit.in/payment_response/"+str(eventid)+"/",
    )

    print(response['payment_request']['id'])

    return redirect(response['payment_request']['longurl'])

def payment_response(request,event):
    '''
    An acknowledgment page for the user about the payment status.
    (May use the index page and show the status)
    '''
    payment = Payments(
        user = request.user,
        payment_id =request.GET.get('payment_id'),
        payment_status = request.GET.get('payment_status'),
        payment_request_id=request.GET.get('payment_request_id')
    )
    eventlist=''
    if request.GET.get('payment_status') == 'Credit':
        user1 = User.objects.get(username=user.username)
        pro = Profile.objects.get(user=user1)
        evdetails = []
        if event=='all':
            pro.cost=0
            pro.save()
            evdetails = EventDetails.objects.filter(qr_code=pro)
            for i in evdetails:
                eventlist=eventlist+i.event_id.event_name
                i.amount_paid = True
                i.save()
            payment.eventname=eventlist
        else:
            edetail=Event.objects.get(event_id=event)
            pro.cost=pro.cost - edetail.event_cost
            pro.save()
            evdetail = EventDetails.objects.filter(qr_code=pro , event_id=event)
            evdetail.amount_paid=True
            evdetail.save()
            payment.eventname = edetail.event_name
        payment.save()
        return redirect(reverse('dashboard'))
    elif request.GET.get('payment_status') == 'Failed':
        return redirect(reverse('dashboard'))
    else:
        return redirect(reverse('dashboard'))