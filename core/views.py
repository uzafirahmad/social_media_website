from django.conf import settings
import stripe
from django.shortcuts import render, redirect
from .models import Accounts, ChatFather, sections, subsections, posts, followerslist, followinglist, ChatModel,notifications
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from datetime import datetime
import uuid
import string
import random
from django.contrib.auth.hashers import make_password
import re
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse
import pytz
import os

stripe.api_key=settings.STRIPE_SECRET_KEY
if settings.DEBUG:
    suggested_profiles_emails_list = ['followbesideme@gmail.com', 'uzafirahmad@followbesideme.com']
    publishablekey=""
    product_id=""
    path_to_profile_img = "media//profile_images"
else:
    publishablekey=""
    product_id=""
    suggested_profiles_emails_list = ['winternshk@gmail.com', 'uzafir525@gmail.com',
                                  'followbesideme@gmail.com', 'uzafirahmad@followbesideme.com','ayeshamunir80ee@gmail.com','sherry07msr@gmail.com']
    path_to_profile_img = "profile_images"
    
def create_paymentintent(followfee):
    paymentintent= stripe.PaymentIntent.create(
    amount=followfee*100,
    currency="usd",
    payment_method_types=["card"],
    )
    return paymentintent.client_secret

# def create_checkout_session(followfee):
#     prices = stripe.Price.create(
#         unit_amount=followfee*100,
#         currency="usd",
#         recurring={"interval": "month"},
#         product="prod_MgZbd3fBLJAtMk",
#         )
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         line_items=[
#             {
#                 'price': prices.id,
#                 'quantity': 1,
#             },
#         ],
#         mode='subscription',
#         success_url=YOUR_DOMAIN +
#             '/success.html?session_id={CHECKOUT_SESSION_ID}',
#         cancel_url=YOUR_DOMAIN + '/cancel.html',
#     )
#     return checkout_session

access_emails = ['uzafir525@gmail.com', 'uzafirahmad@followbesideme.com']

monthdict = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}


def cmp(timestr):
    yearsplit = timestr.split(",")
    year = yearsplit[1]
    monthanddatesplit = yearsplit[0].split()
    month = monthanddatesplit[0]
    month = monthdict[month]
    date = monthanddatesplit[1]

    # conv to int
    strnumber = ''
    finaltimestrlist = year, month, date
    for stritem in finaltimestrlist:
        strnumber += stritem
    finaltimeint = int(strnumber)
    return finaltimeint


timezonedict = {
    'GMT-12:00': 'Etc/GMT+12',
    'GMT-11:00': 'Pacific/Pago_Pago',
    'GMT-10:00': 'Etc/GMT+10',
    'GMT-09:00': 'Etc/GMT+9',
    'GMT-08:00': 'Etc/GMT+8',
    'GMT-07:00': 'Etc/GMT+7',
    'GMT-06:00': 'Etc/GMT+6',
    'GMT-05:00': 'Etc/GMT+5',
    'GMT-04:00': 'Etc/GMT+4',
    'GMT-03:00': 'Etc/GMT+3',
    'GMT-02:00': 'Etc/GMT+2',
    'GMT-01:00': 'Etc/GMT+1',
    'GMT+00:00': 'Etc/GMT-0',
    'GMT+01:00': 'Etc/GMT-1',
    'GMT+02:00': 'Etc/GMT-2',
    'GMT+03:00': 'Etc/GMT-3',
    'GMT+03:30': 'Asia/Tehran',
    'GMT+04:00': 'Etc/GMT-4',
    'GMT+04:30': 'Asia/Kabul',
    'GMT+05:00': 'Etc/GMT-5',
    'GMT+05:30': 'Asia/Kolkata',
    'GMT+06:00': 'Etc/GMT-6',
    'GMT+06:30': 'Indian/Cocos',
    'GMT+07:00': 'Etc/GMT-7',
    'GMT+08:00': 'Etc/GMT-8',
    'GMT+09:00': 'Etc/GMT-9',
    'GMT+09:30': 'Australia/Darwin',
    'GMT+10:00': 'Etc/GMT-10',
    'GMT+11:00': 'Etc/GMT-11',
    'GMT+12:00': 'Etc/GMT-12',
    'GMT+13:00': 'Etc/GMT-13',
}


def index(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is None:
            context = {
                'errormessage': "Invalid email or password"
            }
            return render(request, 'index.html', context)
        elif user.is_active == False:
            # login(request, user)
            return render(request, 'signupdone.html')
        elif user.ban == True:
            context = {
                'errormessage': user.description
            }
            return render(request, 'index.html', context)
        else:
            gen_new_pass_auth_offlineuser(user)
            login(request, user)
            checkinactivesubscription(request,request.user.username)
            return redirect(home)

    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if Accounts.objects.filter(username=username):
            context = {
                'errormessage': "Username already exists"
            }
            return render(request, 'signup.html', context)

        elif Accounts.objects.filter(email=email):
            context = {
                'errormessage': "Email already linked to another account"
            }
            return render(request, 'signup.html', context)

        elif len(username) > 30:
            context = {
                'errormessage': "Username too long"
            }
            return render(request, 'signup.html', context)

        elif len(email) > 60:
            context = {
                'errormessage': "Email too long"
            }
            return render(request, 'signup.html', context)

        elif not username.isalnum():
            context = {
                'errormessage': "Username can only contain letters and numbers"
            }
            return render(request, 'signup.html', context)

        elif password != confirmpassword:
            context = {
                'errormessage': "Passwords do not match"
            }
            return render(request, 'signup.html', context)

        elif password == confirmpassword:
            # Account creation
            newuser = Accounts.objects.create_user(email, username, password)
            newuser.is_active = False
            newuser.description = "Please verify your account to log in"
            newuser.auth_token = str(uuid.uuid4())
            # for adminemail in access_emails:
            #     followerslist.objects.create(fuser=newuser, email=adminemail)
            #     admin = Accounts.objects.get(email=adminemail)
            #     followinglist.objects.create(fuser=admin, email=newuser.email)
            gen_new_pass_auth_offlineuser(newuser)
            # signeduser = authenticate(email=email, password=password)
            # login(request, signeduser)
            # Section creation Workouts
            sec_name1 = "Workouts"
            sec_viewable1 = "Everyone"
            sec_desc1 = "My daily workout routine"
            sections.objects.create(section_name=sec_name1, viewable_to=sec_viewable1,
                                    sec_description=sec_desc1, section_owner=newuser)
            # Section creation Diet
            sec_name2 = "Diet"
            sec_viewable2 = "Everyone"
            sec_desc2 = "My daily food schedule"
            sections.objects.create(section_name=sec_name2, viewable_to=sec_viewable2,
                                    sec_description=sec_desc2, section_owner=newuser)
            # Welcome Email
            current_site = get_current_site(request)
            message2 = render_to_string('email_confirmation.html', {
                'domain': current_site.domain,
                'authtoken': newuser.auth_token
            })
            subject = "Account creation successful"
            message = "Hello " + username + "! \n" + \
                "Welcome to Follow Beside Me. Please verify your account to log in \n" + message2
            to_list = [email]
            send_mail(subject, message, "Follow Beside Me <uzafirahmad@followbesideme.com>",
                      to_list, fail_silently=True)

            return render(request, 'signupdone.html')
    return render(request, 'signup.html')

def getsignupvalidation(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirmpassword = request.POST['confirmpassword']
    if Accounts.objects.filter(username=username):
        context = {
            'errormessage': "Username already exists"
        }
        return JsonResponse({'context': context})

    elif Accounts.objects.filter(email=email):
        context = {
            'errormessage': "Email already linked to another account"
        }
        return JsonResponse({'context': context})

    elif len(username) > 30:
        context = {
            'errormessage': "Username too long"
        }
        return JsonResponse({'context': context})

    elif len(email) > 60:
        context = {
            'errormessage': "Email too long"
        }
        return JsonResponse({'context': context})

    elif not username.isalnum():
        context = {
            'errormessage': "Username can only contain letters and numbers"
        }
        return JsonResponse({'context': context})

    elif password != confirmpassword:
        context = {
            'errormessage': "Passwords do not match"
        }
        return JsonResponse({'context': context})

    elif password == confirmpassword:
        context = {
            'errormessage': "Done"
        }
        return JsonResponse({'context': context})
    
    else:
        context = {
            'errormessage': "Unknown error"
        }
        return JsonResponse({'context': context})

def resendemail(request):
    # Welcome Email
    current_site = get_current_site(request)
    message2 = render_to_string('email_confirmation.html', {
        'domain': current_site.domain,
        'authtoken': request.user.auth_token
    })
    subject = "Account creation successful"
    message = "Hello " + request.user.username + "! \n" + "Welcome to Follow Beside Me. Please verify your account to log in \n" + message2
    to_list = ["uzafir525@gmail.com"]
    send_mail(subject, message, "Follow Beside Me <uzafirahmad@followbesideme.com>",
              to_list, fail_silently=True)

    return render(request, 'signupdone.html')


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            forgotuser = Accounts.objects.get(email=email)
        except Accounts.DoesNotExist:
            context = {
                'emailsent': "No account associated with this address",
            }
            return render(request, 'forgotpassword.html', context)
        gen_new_pass_auth_offlineuser(forgotuser)
        current_site = get_current_site(request)
        message2 = render_to_string('email_resetpassword.html', {
            'domain': current_site.domain,
            'token': forgotuser.password_auth,
        })
        subject = "Password reset"
        message = "Hello " + forgotuser.username + "! \n" + \
            "It seems like you have forgotten your password. It's ok, we will now recover it \n" + message2
        to_list = [email]
        send_mail(subject, message, "Follow Beside Me <uzafirahmad@followbesideme.com>",
                  to_list, fail_silently=True)
        context = {
            'emailsent': "A password reset email has been sent to this address",
        }
        return render(request, 'forgotpassword.html', context)
    return render(request, 'forgotpassword.html')


def changepassword(request):
    if request.method == "POST":
        currentpassword = request.POST['currentpassword']
        newpassword = request.POST['newpassword']
        confirmnewpassword = request.POST['confirmnewpassword']
        if currentpassword == "" or newpassword == "" or confirmnewpassword == "":
            context = {
                "errormessage": "Empty entry"
            }
            return render(request, 'changepassword.html', context)
        elif newpassword != confirmnewpassword:
            context = {
                "errormessage": "Passwords do not match"
            }
            return render(request, 'changepassword.html', context)
        elif not check_password(currentpassword, request.user.password):
            context = {
                "errormessage": "Wrong current password"
            }
            return render(request, 'changepassword.html', context)
        else:
            request.user.set_password(confirmnewpassword)
            request.user.save()
            context = {
                "succcessmessage": "Password Successfully Changed"
            }
            return render(request, 'changepassword.html', context)
    return render(request, 'changepassword.html')


def reset(request, token):
    if Accounts.objects.filter(password_auth=token):
        resetpassuser = Accounts.objects.get(password_auth=token)
        if request.method == "POST":
            password = request.POST['password']
            confirmpassword = request.POST['confirmpassword']
            if password == confirmpassword:
                resetpassuser.set_password(password)
                context = {
                    'successmessage': 'Password changed successfully'
                }
                logout(request)
                gen_new_pass_auth_offlineuser(resetpassuser)
                return render(request, 'index.html', context)
            else:
                context = {
                    'errormessage': "Passwords do not match"
                }
                return render(request, 'resetpassword.html', context)
        return render(request, 'resetpassword.html')
    else:
        context = {
            'emailsent': 'Link expired. Request a new link'
        }
        return render(request, 'forgotpassword.html', context)


def home(request):
    topusersaccs = Accounts.objects.all().order_by('-followers')
    topusers = []
    suggestedprofiles = []
    suggestedprofileposts = suggestedpagepostsdef()
    for email in suggested_profiles_emails_list:
        account = Accounts.objects.get(email=email)
        suggestedprofiles.append(account)
    n = 0
    while n < 3:
        topusers.append(topusersaccs[n])
        n = n+1
    current_user = request.user
    if current_user.is_authenticated:
        final_homepage_list = gethomepagequery(request)
        context = {
            "users": current_user,
            "topusers": topusers,
            "final_homepage_list": final_homepage_list,
            "suggestedprofiles": suggestedprofiles,
            "suggestedprofileposts": suggestedprofileposts
        }
        gen_new_pass_auth_onlineuser(request)
        return render(request, 'home.html', context)
    else:
        context = {
            "users": None,
            "topusers": topusers,
            "suggestedprofiles": suggestedprofiles,
            "suggestedprofileposts": suggestedprofileposts
        }
        return render(request, 'home.html', context)


def messages(request):
    current_user = request.user
    if current_user.is_authenticated:
        following_list = followinglist.objects.filter(fuser=current_user)
        follower_list = followerslist.objects.filter(fuser=current_user)
        follistuser = []
        follower_and_following_emails = []
        following_list_emails = []
        follower_list_emails = []
        for following in following_list:
            following_list_emails.append(following.email)

        for follower in follower_list:
            follower_list_emails.append(follower.email)

        follower_and_following_emails = following_list_emails + follower_list_emails
        follower_and_following_emails = list(
            dict.fromkeys(follower_and_following_emails))
        if request.user.email in follower_and_following_emails:
            follower_and_following_emails.remove(request.user.email)
        for email in follower_and_following_emails:
            useracc = Accounts.objects.get(email=email)
            if email in access_emails and email not in following_list_emails:
                pass
            else:
                follistuser.append(useracc)

        context = {
            "users": current_user,
            "followedusers": follistuser,
            "otheruser": False
        }
        gen_new_pass_auth_onlineuser(request)
        return render(request, 'messages.html', context)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def bookmarks(request):
    current_user = request.user
    if current_user.is_authenticated:
        context = {
            "users": current_user
        }
        gen_new_pass_auth_onlineuser(request)
        return render(request, 'bookmarks.html', context)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def following(request):
    current_user = request.user
    if current_user.is_authenticated:
        follist = followinglist.objects.filter(fuser=current_user)
        follistusers = []
        for followeduseremail in follist:
            followeruseracc = Accounts.objects.get(
                email=followeduseremail.email)
            follistusers.append(followeruseracc)
        context = {
            "users": current_user,
            "followedusers": follistusers
        }
        gen_new_pass_auth_onlineuser(request)
        return render(request, 'following.html', context)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def notificationsdef(request):
    current_user = request.user
    if current_user.is_authenticated:
        notificationslist=notifications.objects.filter(notification_owner=current_user).order_by('-id')
        context = {
            "users": current_user,
            "notifications":notificationslist
        }
        gen_new_pass_auth_onlineuser(request)
        return render(request, 'notifications.html', context)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def settings(request):
    current_user = request.user
    if current_user.is_authenticated:
        context = {
            "users": current_user
        }
        gen_new_pass_auth_onlineuser(request)
        return render(request, 'settings.html', context)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def signout(request):
    current_user = request.user
    if current_user.is_authenticated:
        gen_new_pass_auth_onlineuser(request)
        logout(request)
        return redirect(home)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def verify(request, token):
    try:
        newuser = Accounts.objects.get(auth_token=token)
        newuser.is_active = True
        newuser.description = ""
        newuser.save()
        context = {
            'successmessage': 'Account verification successful'
        }
        return render(request, 'index.html', context)
    except (TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        newuser = None
        context = {
            'errormessage': "No registered account"
        }
        return render(request, 'index.html', context)


def gen_new_pass_auth_onlineuser(request):
    current_user = request.user
    current_user.password_auth = make_password(str(uuid.uuid4()))
    current_user.password_auth = "".join(
        c for c in current_user.password_auth if c.isalnum())
    current_user.password_auth = re.sub(
        r'.', '', current_user.password_auth, count=20)
    current_user.save()


def gen_new_pass_auth_offlineuser(offlineuser):
    # generate a 35character string and encrypt using SHA256
    offlineuser.password_auth = make_password(str(uuid.uuid4()))

    # remove all alphanumeric characters from the encrypted string
    offlineuser.password_auth = "".join(
        c for c in offlineuser.password_auth if c.isalnum())

    # remove first 20 characters which show the type of hashing algorithm and number of iterations
    offlineuser.password_auth = re.sub(
        r'.', '', offlineuser.password_auth, count=20)

    offlineuser.save()


def search(request):
    if request.method == "GET":
        query = request.GET.get("searchquery")
        if len(query) > 0:
            search_results = Accounts.objects.filter(username__icontains=query)
            accounts = []
            for account in search_results:
                accounts.append(account)
            context = {
                'accounts': accounts
            }
            return render(request, 'search.html', context)
        else:
            return render(request, 'search.html')


def viewprofile(request, username):
    u = username
    return redirect(profile, u)


def profile(request, username):
    try:
        account = Accounts.objects.get(username=username)
        sections_of_user = sections.objects.filter(section_owner=account)
    except Accounts.DoesNotExist:
        context = {
            "errormessage": "Account does not exist"
        }
        return render(request, 'index.html', context)

    if account:
        is_self = True
        viewsec = False
        authenticateduser = request.user
        if authenticateduser.is_authenticated and authenticateduser != account:
            is_self = False
        elif not authenticateduser.is_authenticated:
            is_self = False
        flist = followerslist.objects.filter(fuser=account)
        if authenticateduser.is_authenticated:
            if flist.filter(email=authenticateduser.email):
                is_follower = True
            else:
                is_follower = False
        else:
            is_follower = False

        if is_self:
            is_follower = True

        checkaccessfollower=checkaccess(request)
        if checkaccessfollower:
            is_follower=True

        paymentintent=create_paymentintent(account.follow_fee)
        context = {
            "users": account,
            "is_self": is_self,
            "is_follower": is_follower,
            "sections": sections_of_user,
            "viewsection": viewsec,
            "paymentintent":paymentintent,
            "publishablekey":publishablekey,
        }

        return render(request, 'profile.html', context)


def editprofile(request, saveuser):
    account = request.user
    oldusername = account.username
    is_self = True
    if request.method == "POST":
        userbio = request.POST['profilepageheaderinfoareaeditu']
        accusername = request.POST['usernameedit']
        timezone = request.POST['timezone']
        try:
            follow_fee = float(request.POST['profilepageheadersubscriptionfeeeditinput'])
        except:
            context = {
                    "users": account,
                    "is_self": is_self,
                    'errormessage': "Enter a number fee"
                }
            return render(request, 'profile.html', context)
        if (account.username != accusername):
            if Accounts.objects.filter(username=accusername):
                context = {
                    "users": account,
                    "is_self": is_self,
                    'errormessage': "Username already exists"
                }
                return render(request, 'profile.html', context)
            elif not accusername.isalnum():
                context = {
                    "users": account,
                    "is_self": is_self,
                    "errormessage": "Username is not alpha-numeric"
                }
                return render(request, 'profile.html', context)
            elif len(accusername) > 30:
                context = {
                    "users": account,
                    "is_self": is_self,
                    'errormessage': "Username too long"
                }
                return render(request, 'profile.html', context)
            else:
                account.username = accusername
        elif follow_fee < 5.00:
            context = {
                "users": account,
                "is_self": is_self,
                'errormessage': "Fee can't be less than 5$"
            }
            return render(request, 'profile.html', context)
        elif follow_fee % 1 != 0:
            context = {
                "users": account,
                "is_self": is_self,
                'errormessage': "Fee must be a whole number"
            }
            return render(request, 'profile.html', context)
        elif follow_fee > 999:
            context = {
                "users": account,
                "is_self": is_self,
                'errormessage': "Fee can't be more than $999"
            }
            return render(request, 'profile.html', context)
        account.biodescription = userbio
        account.follow_fee = follow_fee
        account.timezone = timezone
        messagesfromuser = ChatModel.objects.filter(sender=oldusername)
        for message in messagesfromuser.iterator():
            message.sender = accusername
            message.save(update_fields=['sender'])
        account.save()
        context = {
            "users": account,
            "is_self": is_self
        }
    return redirect(profile, account.username)
    # return render(request,'profile.html',context)


def crop_image(request, username):
    account = request.user
    val1 = request.POST.get('image')
    print(val1)
    format, imgstr = val1.split(';base64,')
    imgdata = base64.b64decode(imgstr)
    data = ContentFile(imgdata)
    account = request.user
    account.profile_image.save("profile_image.png", data, save=True)
    account.save()
    return render(request, 'signup.html')


def deletesection(request, secname):
    sections_current_user = sections.objects.filter(section_owner=request.user)
    sections_current_user.get(section_name=secname).delete()
    return redirect(profile, request.user.username)


def addsection(request):
    if request.method == "POST":
        try:
            sec_name = request.POST['sectionname']
        except:
            sec_name = ""

        sec_viewable = request.POST['viewableselect']

        try:
            sec_desc = request.POST['sectiondescription']
        except:
            sec_desc = ""

        sections_of_current_user = sections.objects.filter(
            section_owner=request.user)

        if sec_name.isspace():
            context = {
                "users": request.user,
                "is_self": True,
                "sections": sections_of_current_user,
                'errormessage': "Empty section name"
            }
            return render(request, 'profile.html', context)
        elif sec_name == "":
            context = {
                "users": request.user,
                "is_self": True,
                "sections": sections_of_current_user,
                'errormessage': "Empty section name"
            }
            return render(request, 'profile.html', context)
        elif sections_of_current_user.filter(section_name=sec_name):
            context = {
                "users": request.user,
                "is_self": True,
                "sections": sections_of_current_user,
                'errormessage': "A section by this name already exists"
            }
            return render(request, 'profile.html', context)
        elif len(sec_name) > 30:
            context = {
                "users": request.user,
                "is_self": True,
                "sections": sections_of_current_user,
                'errormessage': "Section name is longer than 30 characters"
            }
            return render(request, 'profile.html', context)
        else:
            print("eeeee")
            sections.objects.create(section_name=sec_name, viewable_to=sec_viewable,
                                    sec_description=sec_desc, section_owner=request.user)
            return redirect(viewsection, request.user.username, sec_name)
    context = {
        "users": request.user,
        "is_self": True,
        "sections": sections_of_current_user,
        'errormessage': "Failed to add section"
    }
    return render(request, 'profile.html', context)


def editsection(request, secname):
    sections_of_user = sections.objects.filter(section_owner=request.user)
    current_section = sections_of_user.get(section_name=secname)
    if request.method == "POST":
        sec_name = request.POST['sectionname']
        sec_viewable = request.POST['viewableselect']
        sec_desc = request.POST['profilepagefootercontentsdescriptioninfotextarea']
        if current_section.section_name != sec_name:
            if sections_of_user.filter(section_name=sec_name):
                context = {
                    "users": request.user,
                    "is_self": True,
                    "sections": sections_of_user,
                    'errormessage': "A section by this name already exists"
                }
                return render(request, 'profile.html', context)
            elif sec_name == "":
                context = {
                    "users": request.user,
                    "is_self": True,
                    "sections": sections_of_user,
                    'errormessage': "Empty section name"
                }
                return render(request, 'profile.html', context)
            else:
                current_section.section_name = sec_name
                current_section.viewable_to = sec_viewable
                current_section.sec_description = sec_desc
                current_section.save()

            return redirect(viewsection, request.user.username, current_section.section_name)
        else:
            current_section.section_name = sec_name
            current_section.viewable_to = sec_viewable
            current_section.sec_description = sec_desc
            current_section.save()
    return redirect(viewsection, request.user.username, current_section.section_name)


def viewsection(request, username, secname):
    try:
        try:
            account = Accounts.objects.get(username=username)
            sections_of_user = sections.objects.filter(section_owner=account)
        except Accounts.DoesNotExist:
            context = {
                "errormessage": "Account does not exist"
            }
            return render(request, 'index.html', context)
        currentsection = sections_of_user.get(section_name=secname)
        if account:
            is_self = True
            viewsec = True
            authenticateduser = request.user
            if authenticateduser.is_authenticated and authenticateduser != account:
                is_self = False
            elif not authenticateduser.is_authenticated:
                is_self = False
            flist = followerslist.objects.filter(fuser=account)
            if authenticateduser.is_authenticated:
                if flist.filter(email=authenticateduser.email):
                    is_follower = True
                else:
                    is_follower = False
            else:
                is_follower = False
            allsubsections = subsections.objects.filter(
                subsection_owner=currentsection)
            allposts = []
            for subsection in allsubsections:
                temppost = posts.objects.filter(post_owner=subsection)
                allposts.append(temppost)
            if is_self:
                is_follower = True
            if is_self:
                currentuserstimezone = request.user.timezone
                gmttimezoneequivalent = timezonedict[currentuserstimezone]
                tt = pytz.timezone(gmttimezoneequivalent)
                dateTimeOBJ = datetime.now(tt)
                date_str = dateTimeOBJ.strftime("%B %d, %Y")
                tdaysdateint=cmp(date_str)
                maxsubsectiondate=0
                for subsection in allsubsections:
                    dateofsubsectionstr=subsection.subsection_add_date
                    temp=cmp(dateofsubsectionstr)
                    if temp>maxsubsectiondate:
                        maxsubsectiondate=temp
                if tdaysdateint>maxsubsectiondate:
                    yesyesterday=True
                else:
                    yesyesterday=False
            else:
                yesyesterday=False
            
            checkaccessfollower=checkaccess(request)
            if checkaccessfollower:
                is_follower=True

            paymentintent=create_paymentintent(account.follow_fee)
            context = {
                "users": account,
                "is_self": is_self,
                "sections": sections_of_user,
                "currentsection": currentsection,
                "viewsection": viewsec,
                "subsections": allsubsections,
                "posts": allposts,
                "is_follower": is_follower,
                "yesyesterday":yesyesterday,
                "paymentintent":paymentintent,
                "publishablekey":publishablekey,
            }

            return render(request, 'profile.html', context)
    except sections.DoesNotExist:
        return redirect(profile, username)


def addsubsection(request, secname):
    sections_of_user = sections.objects.filter(section_owner=request.user)
    current_section = sections_of_user.get(section_name=secname)
    number_of_subsections = subsections.objects.filter(
        subsection_owner=current_section)
    number_of_subsections = number_of_subsections.count() + 1
    currentuserstimezone = request.user.timezone
    gmttimezoneequivalent = timezonedict[currentuserstimezone]
    tt = pytz.timezone(gmttimezoneequivalent)
    dateTimeOBJ = datetime.now(tt)
    date_str = dateTimeOBJ.strftime("%B %d, %Y")
    subsections.objects.create(subsection_serial=number_of_subsections,
                               subsection_add_date=date_str, subsection_owner=current_section)
    datestroftoday=str(cmp(date_str))
    deletedatethreshold=calculatetodayddatedeletehtreshold(datestroftoday)
    for subsection in subsections.objects.filter(subsection_owner=current_section):
        subsectionadddate=subsection.subsection_add_date
        subsectionadddateint=cmp(subsectionadddate)
        if deletedatethreshold>subsectionadddateint:
            subsection.delete()
            n = 1
            for item in subsections.objects.filter(subsection_owner=current_section).iterator():
                item.subsection_serial = n
                item.save(update_fields=['subsection_serial'])
                n = n+1

    return redirect(viewsection, request.user.username, current_section.section_name)


def deletesubsection(request, username, secname):
    serialid = request.POST.get('serialid')
    sections_of_user = sections.objects.filter(section_owner=request.user)
    current_section = sections_of_user.get(section_name=secname)
    allsubsections = subsections.objects.filter(
        subsection_owner=current_section)
    allsubsections.get(subsection_serial=serialid).delete()
    n = 1
    for item in allsubsections.iterator():
        item.subsection_serial = n
        item.save(update_fields=['subsection_serial'])
        n = n+1
    return redirect(viewsection, request.user.username, current_section.section_name)


def sizeofimg(b64string):
    return (len(b64string) * 3) / 4 - b64string.count('=', -2)


def addpost(request, username, secname):
    data = {}
    # get post data
    postdata = request.POST
    posttext = postdata.get("post_text", None)
    subsectionserial = postdata.get("post_serial", None)
    postimg = postdata.get("post_image", None)
    try:
        postvid = request.FILES['post_video']
    except Exception as e:
        postvid = "null"
    if postvid == "null" and posttext == "" and postimg == "null":
        account = Accounts.objects.get(username=username)
        sections_of_user = sections.objects.filter(section_owner=account)
        is_self = True
        viewsec = True
        currentsection = sections_of_user.get(section_name=secname)
        allsubsections = subsections.objects.filter(
            subsection_owner=currentsection)
        allposts = []
        for subsection in allsubsections:
            temppost = posts.objects.filter(post_owner=subsection)
            allposts.append(temppost)
        if is_self:
            is_follower = True
        context = {
            "users": account,
            "is_self": True,
            "sections": sections_of_user,
            "currentsection": currentsection,
            "viewsection": viewsec,
            "subsections": allsubsections,
            "posts": allposts,
            "is_follower": is_follower,
        }

        return render(request, 'profile.html', context)
    # get timezone format in hour and minutes am/pm
    currentuserstimezone = request.user.timezone
    gmttimezoneequivalent = timezonedict[currentuserstimezone]
    tt = pytz.timezone(gmttimezoneequivalent)
    dateTimeOBJ = datetime.now(tt)
    hourandminute = dateTimeOBJ.strftime("%I:%M %p")

    # get the sub-section to where post will be made
    account = Accounts.objects.get(username=request.user.username)
    sections_of_user = sections.objects.filter(section_owner=account)
    currentsection = sections_of_user.get(section_name=secname)
    allsubsections = subsections.objects.filter(
        subsection_owner=currentsection)
    currentsubsection = allsubsections.get(subsection_serial=subsectionserial)

    # image configuration
    if postimg != "null":
        format, imgstr = postimg.split(';base64,')
        imgdata = base64.b64decode(imgstr)
        contentfiledata = ContentFile(imgdata)
        ext = format.split('/')[-1]
        file_name = "'profile_image." + ext

    # video configuration
    if postvid != "null":
        file_name = "'profile_image." + "mp4"

    # create post
    currentpost1 = posts.objects.create(
        post_time=hourandminute, post_text=posttext, post_owner=currentsubsection)
    currentpost1.post_hash = make_password(str(uuid.uuid4()))
    currentpost1.post_hash = "".join(
        c for c in currentpost1.post_hash if c.isalnum())
    currentpost1.post_hash = re.sub(
        r'.', '', currentpost1.post_hash, count=20)
    currentpost1.save()
    if postimg != "null":
        currentpost1.post_image.save(file_name, contentfiledata, save=True)
        currentpost1.save()
    if postvid != "null":
        currentpost1.post_video.save(file_name, postvid, save=True)
        currentpost1.save()

    listoffolloweraccounts=[]
    
    followerslistofposter=followerslist.objects.filter(fuser=request.user)
    for follower in followerslistofposter:
        acc=Accounts.objects.get(email=follower.email)
        listoffolloweraccounts.append(acc)
    
    createpostnotification(listoffolloweraccounts,request.user,secname)

    data['success'] = 'ok'
    return render(request, 'index.html')


def deletepost(request, username, secname):
    posthash = request.POST.get('posthash')
    posts.objects.get(post_hash=posthash).delete()
    return render(request, 'index.html')


def followuser(request, username):
    authenticated_user = request.user
    if authenticated_user.is_authenticated:
        tobefolloweduser = Accounts.objects.get(username=username)
        if authenticated_user.stripe_customer_id is None:
            customer=stripe.Customer.create(
                name=request.POST['fullname'],
                email=request.user.email,
                source=request.POST['stripeToken']
            )
            authenticated_user.stripe_customer_id=customer.id
            authenticated_user.save()
        else:
            customer=stripe.Customer.retrieve(authenticated_user.stripe_customer_id)
        
        subscription=stripe.Subscription.create(
            customer=customer,
            currency= "usd",
            description=request.user.username + " follows " + username,
            items=[
                {"price_data": {
                    "unit_amount_decimal":tobefolloweduser.follow_fee*100,
                    "recurring":{
                        "interval":"month"
                    },
                    "product":product_id,
                    "currency":"usd"
                }},
            ],
        )
        # create a new follower and following object
        followerslist.objects.create(
            fuser=tobefolloweduser, email=authenticated_user.email,subscription_id=subscription.id)
        followinglist.objects.create(
            fuser=authenticated_user, email=tobefolloweduser.email,subscription_id=subscription.id)

        # increment the follower count of the to be followed user
        followercount=followerslist.objects.filter(fuser=tobefolloweduser).count()
        tobefolloweduser.followers = followercount
        tobefolloweduser.save()
        
        followingcount = followinglist.objects.filter(fuser=authenticated_user).count()
        authenticated_user.following = followingcount
        authenticated_user.save()
        tobefolloweduser.earnings=int(tobefolloweduser.earnings)+int(tobefolloweduser.follow_fee)
        tobefolloweduser.save()
        subject = "New Follower"
        message = message = "Hello " + tobefolloweduser.username + "! \n" + "You have a new follower called " + request.user.username + " and your Follow Beside Me wallet is now valued at $" + str(tobefolloweduser.earnings)
        to_list = [tobefolloweduser.email]
        send_mail(subject, message, "Follow Beside Me <uzafirahmad@followbesideme.com>",
                  to_list, fail_silently=True)
        createfollownotification(authenticated_user,tobefolloweduser)
        return redirect(profile, username)
    else:
        context = {
            'errormessage': "Log in to view this page"
        }
        return render(request, 'index.html', context)


def startmessage(request, username):
    current_user = request.user
    if current_user is not None and current_user.is_active == True:
        otheruser = Accounts.objects.get(username=username)
        following_list = followinglist.objects.filter(fuser=current_user)
        follower_list = followerslist.objects.filter(fuser=current_user)
        follistuser = []
        follower_and_following_emails = []
        following_list_emails = []
        follower_list_emails = []
        for following in following_list:
            following_list_emails.append(following.email)

        for follower in follower_list:
            follower_list_emails.append(follower.email)

        follower_and_following_emails = following_list_emails + follower_list_emails
        follower_and_following_emails = list(
            dict.fromkeys(follower_and_following_emails))
        if request.user.email in follower_and_following_emails:
            follower_and_following_emails.remove(request.user.email)
        for email in follower_and_following_emails:
            useracc = Accounts.objects.get(email=email)
            if email in access_emails and email not in following_list_emails:
                pass
            else:
                follistuser.append(useracc)
            if useracc.email == otheruser.email:
                match = True

        if request.user.id > otheruser.id:
            thread_name = f'chat_{request.user.id}-{otheruser.id}'
        else:
            thread_name = f'chat_{otheruser.id}-{request.user.id}'

        # msgthread=ChatFather.objects.get(thread_name=thread_name)
        if ChatFather.objects.filter(thread_name=thread_name):
            msgthread = ChatFather.objects.get(thread_name=thread_name)
        else:
            msgthread = ChatFather.objects.create(thread_name=thread_name)
        msgobj = ChatModel.objects.filter(thread_owner=msgthread)
        chat100=msgobj.order_by('-id')[:100]
        n=0
        print(msgobj.count())
        if msgobj.count()>100:
            val=msgobj.count()
            while n<val:
                try:
                    if msgobj[n] not in chat100:
                        msgobj[n].delete()
                except:
                    n=val
                n=n+1

        chat100=reversed(chat100)
        if match:
            context = {
                "users": current_user,
                "followedusers": follistuser,
                "otheruser": otheruser,
                "messages": chat100
            }
            gen_new_pass_auth_onlineuser(request)
            return render(request, 'messages.html', context)
        else:
            return redirect(messages)


def contactus(request):
    if request.method == "POST":
        email = request.POST['email']
        title = request.POST['Title']
        description = request.POST['Description']
        if email == "" or title == "" or description == "":
            context = {
                "errormessage": "Empty entry"
            }
            return render(request, 'contactus.html', context)
        else:
            subject = title
            message = description + "\n" + "Reply at: " + email
            to_list = ["uzafirahmad@followbesideme.com"]
            send_mail(subject, message, "Support <uzafirahmad@followbesideme.com>",
                      to_list, fail_silently=True)
            context = {
                'succcessmessage': "Email has been sent to support.",
            }
            return render(request, 'contactus.html', context)
    return render(request, 'contactus.html')


def helpandsupport(request):
    return render(request, 'helpandsupport.html')


def suggestedpagepostsdef():
    users_in_authenticated_users_following_list = []
    for email in suggested_profiles_emails_list:
        acc = Accounts.objects.get(email=email)
        users_in_authenticated_users_following_list.append(acc)
    all_following_user_posts = []
    all_following_user_sections = []
    all_following_user_subsections = []
    final_homepage_list = []
    for following_user in users_in_authenticated_users_following_list:
        following_users_section = sections.objects.filter(
            section_owner=following_user)

        for section in following_users_section:
            if section.viewable_to == "Everyone":
                all_following_user_sections.append(section)
                following_user_subsections = subsections.objects.filter(
                    subsection_owner=section)
                for subsection in following_user_subsections:
                    all_following_user_subsections.append(subsection)
                    following_user_post = posts.objects.filter(
                        post_owner=subsection)
                    for post in following_user_post:
                        all_following_user_posts.append(post)
                    final_homepage_list.append(
                        [following_user, section.section_name, subsection.subsection_add_date, all_following_user_posts])
                    all_following_user_posts = []
    return sorted(final_homepage_list, key=lambda l: cmp(l[2]), reverse=True)


def gethomepagequery(request):
    logged_in_user_following_list = followinglist.objects.filter(
        fuser=request.user)
    users_in_authenticated_users_following_list = []
    for following_user in logged_in_user_following_list:
        if following_user.email == request.user.email:
            pass
        else:
            account_obj = Accounts.objects.get(email=following_user.email)
            users_in_authenticated_users_following_list.append(account_obj)
    all_following_user_posts = []
    all_following_user_sections = []
    all_following_user_subsections = []
    final_homepage_list = []
    for following_user in users_in_authenticated_users_following_list:
        following_users_section = sections.objects.filter(
            section_owner=following_user)

        for section in following_users_section:
            all_following_user_sections.append(section)
            following_user_subsections = subsections.objects.filter(
                subsection_owner=section)
            for subsection in following_user_subsections:
                all_following_user_subsections.append(subsection)
                following_user_post = posts.objects.filter(
                    post_owner=subsection)
                for post in following_user_post:
                    all_following_user_posts.append(post)
                final_homepage_list.append(
                    [following_user, section.section_name, subsection.subsection_add_date, all_following_user_posts])
                all_following_user_posts = []
    # print(sorted(final_homepage_list,key=lambda l:l[2], reverse=True))
    return sorted(final_homepage_list, key=lambda l: cmp(l[2]), reverse=True)


def sendmessage(request, username):
    message = request.POST['message']
    myusername = request.POST['myusername']
    otheruser = Accounts.objects.get(username=username)

    if request.user.id > otheruser.id:
        thread_name = f'chat_{request.user.id}-{otheruser.id}'
    else:
        thread_name = f'chat_{otheruser.id}-{request.user.id}'

    if ChatFather.objects.filter(thread_name=thread_name):
        father = ChatFather.objects.get(thread_name=thread_name)
        ChatModel.objects.create(
            sender=myusername, message=message, thread_owner=father, message_id=id_generator())
    else:
        father = ChatFather.objects.create(thread_name=thread_name)
        ChatModel.objects.create(
            sender=myusername, message=message, thread_owner=father, message_id=id_generator())

    return JsonResponse({'message': message, 'username': myusername})


def getmessages(request, username):
    otheruser = Accounts.objects.get(username=username)
    if request.user.id > otheruser.id:
        thread_name = f'chat_{request.user.id}-{otheruser.id}'
    else:
        thread_name = f'chat_{otheruser.id}-{request.user.id}'
    father = ChatFather.objects.get(thread_name=thread_name)

    chat = ChatModel.objects.filter(thread_owner=father).order_by('-id')[:100]

    return JsonResponse({'data': list(chat.values())})

def calculatetodayddatedeletehtreshold(todayddatestr):
    yearint=int(todayddatestr[0:4])
    monthint=int(todayddatestr[4:6])
    dayint=int(todayddatestr[6:8])
    tempdayint=dayint-7
    if tempdayint<1:
        dayint=30+tempdayint
        monthint=monthint-1
        if monthint<1:
            monthint=12
            yearint=yearint-1
    else:
        dayint=tempdayint
    
    if len(str(dayint))<2:
        finaldaystr='0'+str(dayint)
    else:
        finaldaystr=str(dayint)

    if len(str(monthint))<2:
        finalmonthstr='0'+str(monthint)
    else:
        finalmonthstr=str(monthint)

    combinedint=int(str(yearint) + finalmonthstr + finaldaystr)
    return combinedint

def DMCA(request):
    return render(request, 'DMCA.html')

def termsandconditions(request):
    return render(request, 'termsandconditions.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def cookiepolicy(request):
    return render(request, 'cookiepolicy.html')

def acceptableusepolicy(request):
    return render(request, 'acceptableusepolicy.html')

def refundpolicy(request):
    return render(request, 'refundpolicy.html')

def checkaccess(request):
    if request.user.is_authenticated:
        if request.user.email in access_emails:
            return True
        else:
            return False
    else:
        return False

def unfollow(request,username):
    tobeunfolloweduser=Accounts.objects.get(username=username)
    if request.user.email in access_emails:
        return redirect(profile, request.user.username)
    
    follwinglistofauthuser=followinglist.objects.filter(fuser=request.user)
    ff=follwinglistofauthuser.get(email=tobeunfolloweduser.email)

    stripe.Subscription.delete(
        ff.subscription_id,
    )
    
    follwerslistofauthuser=followerslist.objects.filter(fuser=tobeunfolloweduser)
    follwerslistofauthuser.get(email=request.user.email)
    
    follwinglistofauthuser.get(email=tobeunfolloweduser.email).delete()
    follwerslistofauthuser.get(email=request.user.email).delete()

    followercount=followerslist.objects.filter(fuser=tobeunfolloweduser).count()
    tobeunfolloweduser.followers = followercount
    tobeunfolloweduser.save()
    
    followingcount = followinglist.objects.filter(fuser=request.user).count()
    request.user.following = followingcount
    request.user.save()
    return redirect(profile, username)

def checkinactivesubscription(request,username):
    theuser=Accounts.objects.get(username=username)
    followinglistofuser=followinglist.objects.filter(fuser=theuser)
    for item in followinglistofuser:
        subscription=stripe.Subscription.retrieve(
            item.subscription_id,
        )
        if subscription.status!="active":
            tobeunfolloweduser=Accounts.objects.get(email=item.email)
            unfollow(request,tobeunfolloweduser.username)

def createfollownotification(user_who_is_following,user_who_is_being_followed):
    dir_list = os.listdir(path_to_profile_img+"//"+user_who_is_being_followed.email)
    profile_image_name=dir_list[0]
    path=path_to_profile_img+"//"+user_who_is_being_followed.email+"//"+profile_image_name
    with open(path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    imgdata = base64.b64decode(b64_string)
    data = ContentFile(imgdata)
    noti1=notifications.objects.create(notification_text="You have successfully followed "+user_who_is_being_followed.username,
                                notification_owner=user_who_is_following,
                                notification_type="follow_key",
                                notification_id= id_generator(),
                                notification_username_case=user_who_is_being_followed.username,
                                ) 
    noti1.notification_image.save("notification_image.png", data, save=True)
    noti1.save()


    dir_list = os.listdir(path_to_profile_img+"//"+user_who_is_following.email)
    profile_image_name=dir_list[0]
    path=path_to_profile_img+"//"+user_who_is_following.email+"//"+profile_image_name
    with open(path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    imgdata = base64.b64decode(b64_string)
    data = ContentFile(imgdata)
    noti2=notifications.objects.create(notification_text=user_who_is_following.username + " started following you",
                                notification_owner=user_who_is_being_followed,
                                notification_type="follow_key",
                                notification_id= id_generator(),
                                notification_username_case=user_who_is_following.username,
                                )
    noti2.notification_image.save("notification_image.png", data, save=True)
    noti2.save()

def marknotiasread(request,username,secname,noti_type,noti_id):
    noti=notifications.objects.get(notification_id=noti_id)
    noti.notification_read=True
    noti.save()
    if noti_type=="follow_key":
        return redirect(profile, username)

    elif noti_type=="posted_key":
        return redirect(viewsection, username,secname)

    elif noti_type=="message_key":
        return redirect(startmessage, username)

    elif noti_type=="website_key":
        return redirect(profile, username)
    

def createpostnotification(list_of_followers,postinguser, sectionname):
    dir_list = os.listdir(path_to_profile_img+"//"+postinguser.email)
    profile_image_name=dir_list[0]
    path=path_to_profile_img+"//"+postinguser.email+"//"+profile_image_name
    with open(path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    imgdata = base64.b64decode(b64_string)
    data = ContentFile(imgdata)
    for follower in list_of_followers:
        noti=notifications.objects.create(notification_owner=follower,
                                    notification_text=postinguser.username + " made a post in " + sectionname,
                                    notification_type="posted_key",
                                    notification_id= id_generator(),
                                    notification_username_case=postinguser.username,
                                    notification_sectionname_case=sectionname
                                    )
        noti.notification_image.save("notification_image.png", data, save=True)
        noti.save()

def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
