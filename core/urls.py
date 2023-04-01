from django.urls import path
from core import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signup/getsignupvalidation/',views.getsignupvalidation,name='getsignupvalidation'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('bookmarks/',views.bookmarks,name='bookmarks'),
    path('following/',views.following,name='following'),
    path('messages/',views.messages,name='messages'),
    path('messages/<username>/',views.startmessage,name='startmessage'),
    path('messages/<username>/sendmessage/',views.sendmessage,name='sendmessage'),
    path('messages/<str:username>/getmessages/',views.getmessages,name='getmessages'),
    path('search/',views.search,name='search'),
    path('resendemail/',views.resendemail,name='resendemail'),
    path('notifications/',views.notificationsdef,name='notifications'),
    path('notifications/<username>/<secname>/<noti_type>/<noti_id>/',views.marknotiasread,name='marknotifications'),
    path('settings/',views.settings,name='settings'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('contactus/',views.contactus,name='contactus'),
    path('helpandsupport/',views.helpandsupport,name='helpandsupport'),
    path('profile/<username>/', views.profile,name='profile'),
    path('section/<username>/<secname>/', views.viewsection,name='viewsection'),
    path('profile/<username>/crop_image/', views.crop_image, name="crop_image"),
    path('viewprofilef/<username>/', views.viewprofile,name='viewprofilef'),
    path('editprofile/<saveuser>/', views.editprofile,name='editprofile'),
    path('signout/',views.signout,name='signout'),
    path('unfollow/<username>/',views.unfollow,name='unfollow'),
    path('addsection/',views.addsection,name='addsection'),
    path('section/<username>/<secname>/addpost/',views.addpost,name='addpost'),
    path('section/<username>/<secname>/delete_post/',views.deletepost,name='delete_post'),
    path('addsubsection/<secname>/',views.addsubsection,name='addsubsection'),
    path('section/<username>/<secname>/deletesubsection/',views.deletesubsection,name='deletesubsection'),
    path('deletesection/<secname>/',views.deletesection,name='deletesection'),
    path('editsection/<secname>/',views.editsection,name='editsection'),
    path('verify/<token>/',views.verify,name='verify'),
    path('followuser/<username>/',views.followuser,name='followuser'),
    path('reset/<token>/',views.reset,name='resetpassword'),
    path('DMCA/',views.DMCA,name='DMCA'),
    path('termsandconditions/',views.termsandconditions,name='termsandconditions'),
    path('privacypolicy/',views.privacypolicy,name='privacypolicy'),
    path('cookiepolicy/',views.cookiepolicy,name='cookiepolicy'),
    path('acceptableusepolicy/',views.acceptableusepolicy,name='acceptableusepolicy'),
    path('refundpolicy/',views.refundpolicy,name='refundpolicy'),
]
