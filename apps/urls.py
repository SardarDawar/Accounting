from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    url(r'^$',views.home, name = "home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name= "logout"),

    #----------------------------------------------------------------------------
    url(r'^profile/$', views.edit_profile, name= "profile"),
    #---------------------------------------------------------------------------
    url(r'^register/$', views.register_user, name= "register"),
    
    url(r'^profile/$', views.edit_profile, name = "edit_profile"),
    
    
    # ****************************************************************
    # User Dashboard
    # ****************************************************************
    url(r'^dashbaord/$', views.dashboard, name = "dashboard"),
    
    #Password Change URL............
    url(r'^change_password/$', views.change_password, name = "change_password"),

    #password Reset URLS...........
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Email Confirm URLs.....
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

    #Contact Us Page ...
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^search/$', views.search, name="search"),
    ######### Plans ##################
    
    
    
    # ****************************************************************
    # Plan List that user creates
    # ****************************************************************
    url(r'^plan/$', views.Plans, name="plan"),



    url(r'^plandetail/(?P<id>\d+)/$', views.plandetail, name="plandetail"),
    
    
    # ****************************************************************
    # Plan Add Form
    # ****************************************************************
    url(r'^planform/$', views.planFormView, name="planform"),
    
    
    # ****************************************************************
    # Plan Edit Form
    # ****************************************************************
    url(r'^planeditform/(?P<id>\d+)/$', views.planEditFormView, name="planeditform"),
    
    # ****************************************************************
    # Plan Delete Form
    # ****************************************************************
    url(r'^delete/(?P<id>\d+)/$', views.delete_view,name='delete' ), 

    # ****************************************************************
    # Calculator Page
    # ****************************************************************
    path('calculator', views.CalculatorView, name="Calculator"),
    
    # ****************************************************************
    # Plan Join Page
    # ****************************************************************
    path('join-plan/<int:category_id>/<int:plan_id>/', views.Join_A_Plan, name="Join"),

    # ****************************************************************
    # Cancel a plan
    # ****************************************************************
    path('cancel-a-plan/<int:plan_id>', views.DeletePlan, name="DeletePlan"),
    
    # ****************************************************************
    # Cancel plan Request
    # ****************************************************************
    path("cancel-request/<int:cat_id>/<int:plan_id>", views.leaveFamily, name="leaveFamily" ),
    
    
    # ****************************************************************
    # Subscription Cancel Request
    # ****************************************************************
    path('cancel-subscription/<int:plan_id>/<int:sub_id>/', views.Cancel_A_Plan, name="cancel"),
    
    # ****************************************************************
    # Accept Subsription Cancel Request
    # ****************************************************************
    path('delete-subscription/<int:plan_id>/<int:sub_id>', views.Delete_Subscription, name="Delete"),
    
    # ****************************************************************
    # User plans
    # ****************************************************************
    path('user-plans', views.Plans, name="Plans"),
    
    # ****************************************************************
    # Approve a subscription for a user
    # ****************************************************************
    path('approve-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.ApproveSubscription, name="Approve"),

    # ****************************************************************
    # Disapprove a subscription for a user
    # ****************************************************************
    path('disapprove-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.DisapproveSubscription, name="Disapprove"),

    # ****************************************************************
    # Edit a subscription
    # ****************************************************************
    path("edit-a-subscription/<int:plan_id>/<int:sub_id>/", views.EditSubscription, name="EditSubscription"),
    
    # ****************************************************************
    # Subscription Detail View
    # ****************************************************************
    path('detail-view-subscription/<int:plan_id>/<int:sub_id>', views.Detail, name="Details"),

    # ****************************************************************
    # Device Campatibility
    # ****************************************************************
    path('confirm-reservation', views.deviceCompatibility, name="Reservation"),
    
    # ****************************************************************
    # About Us
    # ****************************************************************
    path('about-us', views.About, name="About"),
    
    # ****************************************************************
    # FAQ
    # ****************************************************************
    path('FAQ', views.FAQ, name="FAQ"),
    
    # ****************************************************************
    # Plan Comment View
    # ****************************************************************
    path('plan-comment/<int:plan_id>/', views.planCommentView, name="comment_plan"),
    
    # ********************************************************************
    
    # ****************************************************************
    # Payment Method Goes Here
    # ****************************************************************
    path('misc', views.misc, name="misc"),
    url(r'^edit_card/(?P<id>\w+)/$', views.edit_card, name="edit_card"),
    url(r'^delete_payment/(?P<id>\w+)/$', views.delete_payment, name="delete_payment"),
    url(r'^make_default/(?P<id>\w+)/$', views.make_default, name="make_default"),
    path('add_card', views.add_card, name="add_card"),
    path('list_card', views.list_card, name="list_card"),
    path('charge', views.charge, name="charge"),

    # ****************************************************************
    # Terms of use Page
    # ****************************************************************
    path("terms-of-use", views.TermsConditions, name="TermsConditions"),

    # ****************************************************************
    # Privacy Policy
    # ****************************************************************
    path("privacy-policy", views.PrivacyPolicy, name="PrivacyPolicy"),
    
   
]
