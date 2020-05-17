import sys
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import stripe

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone

#################################################################################
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(
    api_key='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')
from_email = Email("futuresoftcode@gmail.com")
from .models import *
stripe.api_key = settings.STRIPE_SECRET_KEY
##################################################################################


def handler404(request):
    return render(request, '404.html', status=404)


# ****************************************************************
# Home Page View
# ****************************************************************
def home(request):
    form = planForm()
    error = None
    if request.method == "POST":
        form = planForm(request.POST)
        try:
            if form.is_valid():
                new = form.save(commit=False)
                new.user = request.user
                new.number_of_open_slots = new.total_slots
                new.save()
                form.save()
                current_site = get_current_site(request)
                build_link = str(request.scheme) + "://" + str(current_site.domain) + \
                    str(reverse("plandetail", args=[new.id]))
                subject = 'New Plan [Alert]'
                content = f"Details of the new plan as follows:\n"
                content += f"Plan Creator Name : {new.user.username}\n"
                content += f"Plan Name : {new.plan_name}\n"
                content += f"Plan Family Name : {new.family_name}\n"
                content += f"Plan Category : {new.category}\n"
                content += f"Plan Creation Timestamp : {new.created}\n"
                content += f"Plan Details Link\n"
                content += str(build_link)
                email = EmailMessage(subject, content, to=[
                                     "support@circledin.io"])
                email.send()
                messages.success(
                    request, "Plan has been created successfully and has been sent to the Admin for revisions.")
                return redirect("Plans")
            else:
                error = True
        except Exception as e:
            print(e)
    value = plan.objects.all().filter(status="Active")
    if request.GET.get("category"):
        if request.GET.get("category") == "All":
            categories = category.objects.all()
        else:
            categories = category.objects.filter(Name=request.GET['category'])
    else:
        categories = category.objects.all()
    # print(categories)
    return render(request, 'music/home.html', {'value': value, 'categories': categories,  'form': form, 'error': error, 'filters': category.objects.all()})

# ****************************************************************
# User Dashboard
# ****************************************************************
@login_required()
def dashboard(request):
    obj = subscription.objects.filter(
        user=User.objects.get(username=request.user.username)
    ).order_by('-number_of_slots')
    context = {
        'obj': obj,
        'dashboard_section': True
    }
    return render(request, 'music/dashboard.html', context)


# ****************************************************************
# Login User View
# ****************************************************************
def login_user(request):
    if request.method != 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        valuenext = request.POST.get('next')
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if len(valuenext) != 0 and valuenext is not None:
                    return redirect(valuenext)
                else:
                    return redirect('home')
            else:
                messages.warning(
                    request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    return render(request, 'music/login.html', {'form': form})

# ****************************************************************
# Logout User View
# ****************************************************************


def logout_user(request):
    logout(request)
    return redirect('home')

# ****************************************************************
# User Profie View
# ****************************************************************
@login_required
def profile_user(request):
    try:
        profile = profileModel.objects.get(
            user=User.objects.get(username=request.user.username))
        contactNumber = profile.contactNumber
        
    except profileModel.DoesNotExist:
        profile = None
        contactNumber = None
    customer = Api_key.objects.get(user=request.user)
    invoice = stripe.Invoice.list(limit=10, customer=customer.customer_Id)
    invoices = (invoice.data)
    upcoming = stripe.Invoice.upcoming(customer="cus_HHJ0khDpoO5BpB")
    print(customer)
    context = {
        'contactNumber': contactNumber,
        'section_profile': True,
        'upcoming': upcoming, 
        'invoices': invoices, 
        'customer': customer
    }
    return render(request, 'music/profile.html', context)


# ****************************************************************
# User Registration View
# ****************************************************************
def register_user(request):
    if request.method != 'POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.save()
            profile = profileModel.objects.create(user=user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.save()
            current_site = get_current_site(request)
            valuenext = request.POST.get('next')
            if len(valuenext) == 0 or valuenext is None:
                valuenext = None
            content = render_to_string('music/acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'valuenext': valuenext
            })
            subject = 'Activate your account.'
            to_email = (form.cleaned_data.get('email'))
            ################################
            # to_email = To(form.cleaned_data.get('email').lower())
            subject = 'Activate your account.'
            # mail = Mail(from_email, to_email, subject, content)
            # sg.client.mail.send.post(request_body=mail.get())
            email = EmailMessage(subject, content, to=[to_email])
            email.send()
            return render(request, 'music/acc_active_email_confirm.html', {'email': to_email})
    return render(request, 'music/register.html', {'form': form, 'form_2': form_2})


# ****************************************************************
# User Email Vrefication View
# ****************************************************************
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        current_site = get_current_site(request)
        subject = 'A new User has been registered'
        u = User.objects.filter(is_superuser=True)
        content = f'A new user has been registerd\nDetails of the newly registered as follows:\nName:{user.username}\nEmail Address:{user.email}'
        email = EmailMessage(subject, content, to=["support@circledin.io"])
        email.send()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # print(request.GET)
        try:
            n = request.GET.get("next", None)
            if n is not None:
                return redirect(n)
            else:
                return redirect('home')
        except:
            return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

# ****************************************************************
# Edit Profile View
# ****************************************************************
@login_required()
def edit_profile(request):
    customer = None
    invoice  = None
    invoices  = None
    upcoming = None
    try:
        profile = profileModel.objects.get(user=request.user)
    except profileModel.DoesNotExist:
        profile = profileModel.objects.create(user=request.user)
        profile.save()
    if request.method != 'POST':
        form = EditProfileForm(instance=request.user)
        form_2 = EditprofileInformForm(instance=profile)
        try:
            customer = Api_key.objects.filter(user=request.user)
            if len(customer) != 0:
                customer = customer[0]
                invoice = stripe.Invoice.list(limit=10, customer=customer.customer_Id)
                invoices = (invoice.data)
                upcoming = stripe.Invoice.upcoming(customer=customer.customer_Id)
        except:
            customer = None
            invoice  = None
            invoices  = None
            upcoming = None
        
    else:
        # print(request.POST)
        form_2 = EditprofileInformForm(request.POST, instance=profile)
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid() and form_2.is_valid():
            form.save()
            form_2.save()
            messages.success(request, "Profile has been updated successfully.")
            return HttpResponseRedirect(reverse('edit_profile'))
    # print(form_2.errors)
    return render(request, 'music/edit_profile.html', {'form': form, 'profile': profile, 'form_2': form_2, 'edit_profile': True, 'upcoming': upcoming, 
        'invoices': invoices, 
        'customer': customer})

# ****************************************************************
# Change Password View
# ****************************************************************
@login_required()
def change_password(request):
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, "Password has been updated successfully.")
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'music/change_password.html', {'form': form, 'change_password_section': True})

# ****************************************************************
# Contact Form
# ****************************************************************


def contact(request):
    if request.method != 'POST':
        form = contactForm()
    else:
        form = contactForm(request.POST)
        if form.is_valid():
            mail_subject = 'Contact -- By -- ' + \
                form.cleaned_data.get('userName')
            email = form.cleaned_data.get('email')
            message = f"\nMessage\n"
            body = form.cleaned_data.get('body')
            message += f"{body}"
            message += f"\nUser's email address: {email}"
            email = EmailMessage(mail_subject, message, to=[
                                 "support@circledin.io"])
            email.send()
            context = {
                'form': contactForm(),
                'send_successfull_contact': True
            }
            try:
                if request.GET.get("next", None):
                    messages.error(request, "Email Send")
                    return redirect(request.GET.get("next"))
                else:
                    return render(request, 'music/contact.html', context)
            except Exception as e:
                # print(e)
                return render(request, 'music/contact.html', context)
    context = {'form': form}
    return render(request, 'music/contact.html', context)


def search(request):

    query = request.GET.get('query', None)
    search_user = profileModel.objects.all()
    if query is not None:
        search_user = search_user.filter(
            Q(user__username__icontains=query) |
            Q(contactNumber__icontains=query)


        )
    # print(query)
    # for i in search_user:
    #     print(i.user.email)
    context = {

        'search_user': search_user,
        'query': query

    }

    return render(request, 'music/search.html', context)


# ****************************************************************
# Add a New Plan Form
# ****************************************************************
@login_required
def planFormView(request):
    form = planForm()
    if request.method == 'POST':
        form = planForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.number_of_open_slots = new.total_slots
            new.save()
            form.save()
            current_site = get_current_site(request)
            build_link = str(request.scheme) + "://" + str(current_site.domain) + \
                str(reverse("admin:apps_plan_change", args=[new.id]))
            subject = 'New Plan [Alert]'
            content = f"Details of the new plan as follows:\n"
            content += f"Plan Creator Name : {new.user.username}\n"
            content += f"Plan Name : {new.plan_name}\n"
            content += f"Plan Family Name : {new.family_name}\n"
            content += f"Plan Category : {new.category}\n"
            content += f"Plan Creation Timestamp : {new.created}\n"
            content += f"Plan Details Link\n"
            content += str(build_link)
            email = EmailMessage(subject, content, to=["support@circledin.io"])
            email.send()
            messages.success(
                request, "Plan has been added to your plan list and has been sent to the Admin for revisions.")
            return redirect('plan')
    context = {
        'form': form,
        'categories': category.objects.all(),
        'section_add_a_new_plan': True
    }
    return render(request, 'app/form_plan.html', context)


@login_required
def planEditFormView(request, id):
    try:
        obj = plan.objects.get(id=id)
        if obj.user == User.objects.get(username=request.user.username):
            form = planForm(instance=obj)
            if request.method == 'POST':
                form = planForm(request.POST, instance=obj)
                if form.is_valid():
                    new = form.save(commit=False)
                    new.user = request.user
                    new.save()
                    form.save()
                    current_site = get_current_site(request)
                    build_link = str(request.scheme) + "://" + str(current_site.domain) + \
                        str(reverse("admin:apps_plan_change", args=[new.id]))
                    build_link_2 = str(request.scheme) + "://" + str(current_site.domain) + str(
                        reverse("admin:apps_plan_history", args=[new.id]))
                    subject = 'Edit Existing Plan [Alert]'
                    content = f"Details of the Edit plan as follows:\n"
                    content += f"Plan Editor Name : {new.user.username}\n"
                    content += f"Plan Name : {new.plan_name}\n"
                    content += f"Plan Family Name : {new.family_name}\n"
                    content += f"Plan Category : {new.category}\n"
                    content += f"Plan Updated Timestamp : {timezone.now()}\n"
                    content += f"Plan Details Link\n"
                    content += f"{str(build_link)}\n"
                    email = EmailMessage(subject, content, to=[
                                         "support@circledin.io"])
                    email.send()
                    messages.success(
                        request, "Plan has been edited successfully.")
                    return redirect('Plans')
            context = {
                'form': form,
                'object': obj,
                'list_plans_section': True
            }
            return render(request, 'app/form_edit_plan.html', context)
        else:
            messages.success(request, "Does Not have access.")
            return render(request, 'app/error.html')
    except:
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


@login_required
def planList(request):
    plans = plan.objects.filter(
        user=request.user).order_by('number_of_open_slots')

    context = {
        'plans': plans,
        'list_plans_section': True
    }

    return render(request, 'app/list_plan.html', context)


@login_required
def plandetail(request, id):
    obj = plan.objects.get(id=id)

    context = {
        'obj': obj,
    }
    return render(request, 'app/plan_detail.html', context)


@login_required
def delete_view(request, id):
    context = {}
    obj = plan.objects.get(id=id)

    if request.method == "POST":
        obj.delete()
        return redirect("dashboard")

    return render(request, "app/delete_view.html", context)


# ****************************************************************
# Calculator
# ****************************************************************
@login_required
def CalculatorView(request):
    if request.method == "POST":
        print(request.POST)
    template_name = "app/calculator.html"
    return render(request, template_name, context={})


# ****************************************************************
# Join A Subscription (Join Plan)
# ****************************************************************
def Join_A_Plan(request, category_id, plan_id):
    try:
        c = category.objects.get(id=category_id)
        p = plan.objects.get(id=plan_id, category=c)
        if request.method == "POST":
            if request.user.is_authenticated:
                try:
                    obj, status = subscription.objects.get_or_create(
                        user=User.objects.get(
                            username=request.user.username
                        ),
                        plan=p
                    )
                    if status:
                        obj.number_of_slots = request.POST['number_of_slots']
                        obj.TotalAmount = int(
                            p.currently_monthly_payment_per_line) * int(request.POST['number_of_slots'])
                        obj.save()
                        # Reduced the plan available slots for subscription
                        p.number_of_open_slots = int(
                            p.number_of_open_slots) - int(request.POST['number_of_slots'])
                        p.save()
                        # ****************************************************************
                        # Email Settings
                        # mail = Mail(from_email, to_email, subject, content)
                        # sg.client.mail.send.post(request_body=mail.get())
                        # ****************************************************************
                        current_site = get_current_site(request)
                        link_build = str(request.scheme) + "://" + str(
                            current_site.domain) + str(reverse("Details", args=[plan_id, obj.id]))
                        to_email = (p.user.email)
                        subject = 'Subscription Alert'
                        content = f"A Subscription has been added to your plan.Kindly visit the following link to see details.\n\t{link_build}"
                        email = EmailMessage(subject, content, to=[
                                             to_email, "support@circledin.io"])
                        email.send()
                        messages.success(
                            request, "Account Owner has been notified about your subscription to this plan. Thanks")
                        return redirect(reverse("Join", args=[category_id, plan_id]))
                    else:
                        messages.success(
                            request, "You have already been subscribed to this plan. Thanks")
                        return redirect(reverse("Join", args=[category_id, plan_id]))
                except Exception as e:
                    print(e)
                    messages.success(
                        request, "Due to some technical reasons, subscription can not be done right now. Sorry")
                    return redirect(reverse("Join", args=[category_id, plan_id]))
            else:
                return redirect("login")
        template_name = "app/join.html"
        p = plan.objects.get(id=plan_id)
        slots = p.number_of_open_slots
        slots = [i for i in range(1, (slots) + 1)]
        context = {
            'slots': slots,
            'plan': p,
            'total': len(slots)
        }
        return render(request, template_name, context)
    except (plan.DoesNotExist, category.DoesNotExist, subscription.DoesNotExist):
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


# ****************************************************************
# Calcel A Subscription (Joined Plan) Request
# ****************************************************************
@login_required
def Cancel_A_Plan(request,  plan_id, sub_id):
    if request.method != "POST":
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(
            id=sub_id, plan=p, user=User.objects.get(username=request.user.username))
        current_site = get_current_site(request)
        link_build = str(request.scheme) + "://" + str(current_site.domain) + \
            str(reverse("Details", args=[plan_id, s.id]))
        try:
            subject = 'Subscription Alert [Request to Cancel]'
            content = f"""A request has been to cancel a subscription.\n
                    Following are the subscription details\n
                    Subscription user: {s.user}\n
                    Subscription user email : {s.user.email}\n
                    Subscription Plan: {s.plan.plan_name}\n
                    Subscription Number of Slots: {s.number_of_slots}\n
                    Subscription Total Amount: {s.TotalAmount}\n 
                    Subscription Timestamp: {s.created_at}\n
                    Reason/Feedback:\n
                    {request.POST['feedback']}\n
                    Link to see the details of the subscription\n
                    {link_build}"""
            to_email = (p.user.email)
            email = EmailMessage(subject, content, to=[
                                 to_email, "support@circledin.io"])
            # p.number_of_open_slots  = int(p.number_of_open_slots) + int(s.number_of_slots)
            p.save()
            s.leaveRequest = True
            s.save()
            email.send()
            messages.success(
                request, "CI has been informed. Please be aware that you’ll need to pay for any outstanding cost that you have on your mobile bill before we can transfer you out of the family plan")
            return redirect("dashboard")
        except:
            messages.success(
                request, "Due to some technical reasons, subscription can not be cancel right now. Sorry.")
            return redirect("dashboard")
    except (subscription.DoesNotExist, plan.DoesNotExist) as e:
        # print(e)/
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    except Exception as e:
        # print(e)
        messages.success(
            request, "Due to some technical reasons, subscription can not be done right now. Sorry.")
        return redirect("dashboard")


# ****************************************************************
# Accept Subscription Cancel Request
# ****************************************************************
@login_required
def Delete_Subscription(request, plan_id, sub_id):
    if request.method != "GET":
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')
    else:
        try:
            p = plan.objects.get(id=plan_id, user=User.objects.get(
                username=request.user.username))
            s = subscription.objects.get(id=sub_id, plan=p)
            subject = 'Subscription Alert [Subscription Cancel Request Approved]'
            content = f"""A request to cancel a subscription has been approved.\n
                    Following are the subscription details\n
                    Subscription user: {s.user}\n
                    Subscription Plan: {s.plan.plan_name}\n
                    Subscription Number of Slots: {s.number_of_slots}\n
                    Subscription Total Amount: {s.TotalAmount}\n 
                    Subscription Timestamp: {s.created_at}\n
                    Reason/Feedback:\n
                    {s.feedback}\n"""
            to_email = (s.user.email, p.user.email)
            email = EmailMessage(subject, content, to=[
                                 to_email, "support@circledin.io"])
            s.delete()  # Delete Subscription
            email.send()
            messages.success(request, "A Sunscription has been deleted.")
            return redirect("Plans")
        except Exception as e:
            # print(e)
            messages.success(
                request, "Due to some technical reasons, subscription can not be done right now. Sorry.")
            return redirect("Plans")



# ****************************************************************
# User Added Plans
# ****************************************************************
@login_required
def Plans(request):
    obj = plan.objects.filter(
        user=User.objects.get(username=request.user.username))

    categories = category.objects.all()
    A = []
    C = {}

    for i in obj:
        if str(i.category.Name) in C.keys():
            C[str(i.category.Name)].append(i)
        else:
            C[str(i.category.Name)] = [i]

    return render(request, 'app/plans.html', {'obj': obj, 'categories': categories, 'C': C, 'our_plans_section': True})

# ****************************************************************
# Approve a subscription
# ****************************************************************
@login_required
def ApproveSubscription(request, user_id, plan_id, sub_id):
    try:
        p = plan.objects.get(user=User.objects.get(
            username=request.user.username), id=plan_id)
        s = subscription.objects.get(
            user=User.objects.get(id=user_id), id=sub_id, plan=p)
        s.status = "Active"
        s.save()
        messages.success(
            request, "Subscription has been approved succcessfully")
        # ****************************************************************
        # Email Settings
        # ****************************************************************
        subject = 'Subscription Alert'
        current_site = get_current_site(request)
        link_build = str(request.scheme) + "://" + str(current_site.domain) + \
            str(reverse("Details", args=[plan_id, s.id]))
        to_email = (s.user.email)
        content = f"A Subscription has been approved.Kindly visit the following link to see details.\n\t{link_build}"
        email = EmailMessage(subject, content, to=[
                             to_email, "support@circledin.io"])
        email.send()
        return redirect("Plans")
    except Exception as e:
        print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


# ****************************************************************
# Disapprove a subscription
# ****************************************************************
@login_required
def DisapproveSubscription(request, user_id, plan_id, sub_id):
    try:
        p = plan.objects.get(user=User.objects.get(
            username=request.user.username), id=plan_id)
        s = subscription.objects.get(
            user=User.objects.get(id=user_id), id=sub_id, plan=p)
        s.status = "Inactive"
        s.save()
        messages.success(request, "Subscription has been disapproved")
        # ****************************************************************
        # Email Settings
        # ****************************************************************
        subject = 'Subscription Alert'
        current_site = get_current_site(request)
        link_build = str(request.scheme) + "://" + str(current_site.domain) + \
            str(reverse("Details", args=[plan_id, s.id]))
        to_email = (s.user.email)
        content = f"A Subscription has been disapproved.Kindly visit the following link to see details.\n\t{link_build}"
        email = EmailMessage(subject, content, to=[
                             to_email, "support@circledin.io"])
        email.send()
        return redirect("Plans")
    except Exception as e:
        # print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


# ****************************************************************
# Edit a Subscription
# ****************************************************************
@login_required
def EditSubscription(request, plan_id, sub_id):
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(
            user=User.objects.get(
                username=request.user.username
            ),
            plan=p
        )
        if request.method == "POST":
            p.number_of_open_slots = int(
                p.number_of_open_slots) + int(s.number_of_slots)
            p.save()
            s.number_of_slots = request.POST['number_of_slots']
            s.TotalAmount = int(
                p.currently_monthly_payment_per_line) * int(request.POST['number_of_slots'])
            s.save()
            # Reduced the plan available slots for subscription
            p.number_of_open_slots = int(
                p.number_of_open_slots) - int(s.number_of_slots)
            p.save()
            # ****************************************************************
            # Email Settings
            # ****************************************************************
            subject = 'Subscription Alert'
            current_site = get_current_site(request)
            link_build = str(request.scheme) + "://" + str(current_site.domain) + \
                str(reverse("Details", args=[plan_id, s.id]))
            to_email = (p.user.email)
            content = f"A Subscription has been modified.Kindly visit the following link to see details.\n\t{link_build}"
            email = EmailMessage(subject, content, to=[
                                 to_email, "support@circledin.io"])
            email.send()
            messages.success(
                request, "Account Owner has been notified about your subscription to this plan. Thanks")
            return redirect("dashboard")
        else:
            # print(s)
            template_name = "app/edit_subscription.html"
            slots = int(s.number_of_slots) + int(p.number_of_open_slots)
            total = slots
            slots = [i for i in range(1, (slots) + 1)]
            context = {
                'slots': slots,
                'plan': p,
                'subs': s,
                'total': total
            }
            return render(request, template_name, context)

    except (plan.DoesNotExist, category.DoesNotExist) as e:
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')

    except Exception as e:
        print(e)
        messages.success(
            request, "Due to some technical reasons, subscription can not be edited right now. Sorry")
        return redirect("dashboard")

# ****************************************************************
# Subscription Detail View
# ****************************************************************
@login_required
def Detail(request, plan_id, sub_id):
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(plan=p, id=sub_id)
        if s.user == User.objects.get(username=request.user.username) or p.user == User.objects.get(username=request.user.username):
            template_name = "app/detail.html"
            context = {
                'plan': p,
                'subs': s,
            }
            return render(request, template_name, context)

    except (plan.DoesNotExist, category.DoesNotExist):
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')

    except Exception as e:
        print(e)
        messages.success(
            request, "Due to some technical reasons, subscription can not be edited right now. Sorry")
        return redirect("dashboard")


# ****************************************************************
# Device Camptibility Handler View
# ****************************************************************
def deviceCompatibility(request):
    if request.method == "POST":
        messages.success(
            request, "Your request has been sent to your Account Owner.")
    template_name = "app/device-campatibility.html"
    context = {

    }
    return render(request, template_name, context)


# ****************************************************************
# About Us
# ****************************************************************
def About(request):
    template_name = 'app/about_us.html'
    context = {

    }
    return render(request, template_name, context)

# ****************************************************************
# FAQ
# ****************************************************************


def FAQ(request):
    template_name = 'app/Circledin_FAQ.html'
    context = {

    }
    return render(request, template_name, context)


# ****************************************************************
# Delete A Plan
# ****************************************************************
@login_required
def DeletePlan(request, plan_id):
    try:
        p = plan.objects.get(id=plan_id, user=User.objects.get(
            username=request.user.username))
        try:
            content = f"A request has been to cancel a plan from a {request.user.username} with the following details\n"
            content += f"Plan Owner : {request.user.username}\n"
            content += f"Plan Name : {p.plan_name}\n"
            content += f"Plan category : {p.category}\n"
            # to_email = []
            # to_email.append(p.user.email)
            try:
                # ****************************************************************
                # Email Settings
                # ****************************************************************
                subject = 'Plan Alert [Cancel Request]'
                current_site = get_current_site(request)
                build_link = str(request.scheme) + "://" + str(current_site.domain) + \
                    str(reverse("admin:apps_plan_change", args=[p.id]))
                content += "\nDetails Following Link\n"
                content += f"{build_link}"
                email = EmailMessage(subject, content, to=[
                                     "support@circledin.io"])
                email.send()
                messages.success(
                    request, "A cancel request has been sent to the admins for revsions.")
                return redirect("plan")
            except Exception as e:
                messages.success(
                    request, "Due to some technical reasons, Plan can't be deleted right now.Sorry")
                return redirect("plan")
        except Exception as e:
            print(e)
            messages.success(
                request, "Due to some technical reasons, Plan can't be deleted right now.Sorry")
            return redirect("plan")
    except Exception as e:
        print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


# ****************************************************************
# Plan Comment Add View
# ****************************************************************
@login_required
def planCommentView(request, plan_id):
    try:
        p = plan.objects.get(id=plan_id)
        if request.method != "POST":
            return redirect(reverse("Join", args=[
                p.category.id,
                p.id
            ]))
        else:
            form = planCommentForm(request.POST)
            if form.is_valid():
                try:
                    new = form.save(commit=False)
                    new.user = request.user
                    new.plan = p
                    new.save()
                    form.save()
                    messages.success(
                        request, "Comment has been added successfully.")
                    return redirect(reverse("Join", args=[
                        p.category.id,
                        p.id
                    ]))
                except Exception as e:
                    # print(e)
                    messages.success(
                        request, "Due to some technical reasons, comment can't be added right now.Sorry")
                    return redirect(reverse("Join", args=[
                        p.category.id,
                        p.id
                    ]))
            else:
                messages.success(request, str(form.errors))
                return redirect(reverse("Join", args=[
                    p.category.id,
                    p.id
                ]))
    except Exception as e:
        # print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


# ****************************************************************
# Terms and Conditions
# ****************************************************************
def TermsConditions(request):
    template_name = 'app/terms.html'
    context = {

    }
    return render(request, template_name, context)


# ****************************************************************
# Privacy Policy
# ****************************************************************
def PrivacyPolicy(request):
    template_name = 'app/privacy.html'
    context = {

    }
    return render(request, template_name, context)


# ****************************************************************
# Leave Plan Family by plan owner
# ****************************************************************
@login_required
def leaveFamily(request,  cat_id, plan_id):
    try:
        c = category.objects.get(id=cat_id)
        p = plan.objects.get(id=plan_id, user=User.objects.get(
            username=request.user.username))
        # ****************************************************************
        # Email Settings
        # ****************************************************************
        subject = 'Plan Alert [Request to Cancel]'
        current_site = get_current_site(request)
        build_link = str(request.scheme) + "://" + str(current_site.domain) + \
            str(reverse("admin:apps_plan_change", args=[p.id]))
        content = "\nDetails Following Link\n"
        content += f"{build_link}"
        email = EmailMessage(subject, content, to=["support@circledin.io"])
        email.send()
        p.leaveRequest = True
        p.save()
        messages.success(
            request, "A cancel request has been sent to the admins for revsions.")
        return redirect("plan")
    except Exception as e:
        print(e)
        messages.success(request, "Requested Page Does Not Exists")
        return render(request, 'app/error.html')


# Payment ###########################3

@csrf_exempt
def charge(request):
    if request.method == 'POST':
        # print("*********************************")
        # print(request.method)
        # print("*********************************")
        try:
            if request.body:
                data = json.loads(request.body)
                paymentMethod = data['payment_method']
                card = data['card']
                details = data['details']

                customer = stripe.Customer.create(
                    payment_method=stripe.PaymentMethod.retrieve(
                        paymentMethod),
                    email=request.user.email,
                    description='About Payment Plan',
                    invoice_settings={
                        'default_payment_method': paymentMethod
                    }
                )
                stripe.PaymentMethod.attach(
                paymentMethod,
                customer=customer.id,
                )
                Payment_key.objects.create(user=request.user,name=details['name'],phone=details['phone'],email=details['email'],last4=card['last4'],exp_month=card['exp_month'],exp_year=card['exp_year'],payment_id=paymentMethod,default=True)
                subscription = stripe.Subscription.create(
                    customer=customer.id,
                    items=[
                        {
                            'plan': 'plan_HFv9CmBmgpSKED',
                        },
                    ],
                    expand=['latest_invoice.payment_intent'],
                    # billing_cycle_anchor=datetime.now(),

                )

                # creating user object to be saved in database
                Api_key.objects.create(user=request.user, paymentMenthod=paymentMethod, customer_Id=customer.id,
                                       subscription_ID=subscription.id)
                
        except Exception as e:
            # print("***********************************")
            # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            # print("***********************************")
            pass

    return render(request, 'payment/payment.html')


def misc(request):
    try:
        customer = Api_key.objects.filter(user=request.user)
        if len(customer) != 0:
            customer = customer[0]
    except:
        pass
    # customer = Api_key.objects.get(user=request.user)
    invoice = stripe.Invoice.list(limit=10, customer=customer.customer_Id)
    invoices = (invoice.data)
    upcoming = stripe.Invoice.upcoming(customer="cus_HHJ0khDpoO5BpB")
    return render(request, 'payment/misc.html', {'upcoming': upcoming, 'invoices': invoices, 'customer': customer})


@csrf_exempt
def add_card(request):
    customer = Api_key.objects.get(user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        paymentMethod = data['payment_method']
        card = data['card']
        details = data['details']
        print(details['name'], details['phone'])
        Payment_key.objects.create(user=request.user, name=details['name'], phone=details['phone'], email=details['email'],
                                   last4=card['last4'], exp_month=card['exp_month'], exp_year=card['exp_year'], payment_id=paymentMethod,)
        # attach payment to the customer
        stripe.PaymentMethod.attach(
            paymentMethod,
            customer=customer.customer_Id,
        )
    return render(request, 'payment/paymentupdate.html', {})


def edit_card(request, id):
    try:
        method = stripe.PaymentMethod.modify(
            id,
        )
        values = method.billing_details
        card = (method.card)

        if request.method == 'POST':
            method = stripe.PaymentMethod.modify(
                id,
                billing_details={'name': request.POST['username'], 'email': request.POST['useremail'],
                                    'phone': request.POST['phone'], 'address': {'city': request.POST['city'], 'state': request.POST['state'], 'country': request.POST['country']}},
                card={'exp_month': request.POST['exp_month'],
                        'exp_year': request.POST['exp_year']}
            )
            Payment_key.objects.filter(payment_id=id).update(name=request.POST['username'], phone=request.POST['phone'],
                                                                email=request.POST['useremail'], exp_month=request.POST['exp_month'], exp_year=request.POST['exp_year'],)
    except Exception as e:
        print(e)
        messages.success(request, "Technical Issues, Processing...")
        return redirect("list_card")
    return render(request, 'payment/retrieve.html', {'values': values, 'card': card , "p" : Payment_key})


def list_card(request):
    card = Payment_key.objects.filter(user=request.user)

    return render(request, 'payment/list.html', {'card': card})


def make_default(request, id):
    try:
        customer = Api_key.objects.filter(user=request.user)
        if len(customer) != 0:
            customer = customer[0]        
            card = Payment_key.objects.filter(user=request.user).update(default=False)
            stripe.Customer.modify(
                customer.customer_Id,
                invoice_settings={'default_payment_method': id}
                # billing_cycle_anchor=datetime.now(),

            )
            Payment_key.objects.filter(payment_id=id).update(default=True)
            card = Payment_key.objects.get(payment_id=id)
            print(card)
        else:
            customer  = None
            card =None
    except Exception as e:
        print(e)
        messages.success(request, "Can't make is as default right now." )
        return redirect("list_card")
        customer = None
        card  = None

    return render(request, 'payment/default.html', {'i': card})


def delete_payment(request, id):
    
    try:
        stripe.PaymentMethod.detach(id)
        if Payment_key.objects.filter(user  = request.user).count() == 1:
            messages.success(request, "That's only one payment method. you can't delete it." )
            return redirect("list_card")
        else:            
            Payment_key.objects.get(payment_id=id).delete()
            messages.success(request, "Successfully Deleted." )
            return redirect("list_card")
    except Exception as e:
        print(e)
        messages.success(request, "Technical Issues. Processing" )
        return redirect("list_card")
    return render(request, 'payment/delete.html')



# @csrf_exempt
# def chargeupdate(request):
#     customer = Api_key.objects.get(user=request.user)
#     if request.method == 'POST':

#         data = json.loads(request.body)
#         paymentMethod = data['payment_method']
#         stripe.PaymentMethod.detach(customer.paymentMenthod,
# )
#         Api_key.objects.update(user=request.user,paymentMenthod=paymentMethod)

#         stripe.PaymentMethod.attach(
#         paymentMethod,
#         customer="cus_HHRGotKA8ZVdQ7",
#         )
#         subscription = stripe.Subscription.modify(
#         customer.subscription_ID,

#         default_payment_method=paymentMethod
#         # billing_cycle_anchor=datetime.now(),

#         )

#         # creating user object to be saved in database
#         return redirect('home')
#     return render(request, 'app/paymentupdate.html')


def convert(time):
    return datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
