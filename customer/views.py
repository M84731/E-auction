from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
import uuid
from product.models import Product


# Create your views here.
class Home(View):
    def get(self, request):
        product = Product.objects.all()
        return render(request, 'home.html', {'products': product})


def send_email_after_registration(email, token):
    subject = 'Verify Email'
    message = f'Hi, Click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)


# account verification
def acount_verify(request, token):
    pf = Profile.objects.filter(token=token).first()
    pf.verify = True
    pf.save()
    print(token)
    messages.success(request, "Your account has been verified,you can login")
    return redirect('/sign-up/')


# sign_up view
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            new_user = form.save()
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            uid = uuid.uuid4()
            data = Profile(user=new_user, name=name, email=email, phone=phone, token=uid)
            data.save()
            send_email_after_registration(new_user.email, uid)
            messages.success(request, "Your Account created Successfully,To verify your Account,Check your email")
        return redirect('/sign-up/')



# login view

class LoginView(View):
    def get(self, request):
        fm = LoginForm()
        return render(request, 'login.html', {'form': fm})

    def post(self, request):
        fm = LoginForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            pro = Profile.objects.get(user=user)
            if pro.verify:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Your Account is not verified,please check your mail and verify your Account")
                return redirect('/login')


class MyAccountView(LoginRequiredMixin, TemplateView):
    user_form = SignUpForm
    template_name = 'my_account_detail.html'


class ProfileUpdateView(View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'profile_update.html', {'u_form': u_form, 'p_form': p_form})

    def post(self, request):
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        username = request.POST['username']
        User.objects.filter(id=request.user.id).update(username=username, email=email)
        print(phone)
        up = Profile.objects.get(user_id=request.user.id)
        up.name = name
        up.email = email
        up.phone = phone
        up.save()
        return redirect('/')
