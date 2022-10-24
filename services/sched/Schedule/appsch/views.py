from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .models import Userinfo, LessonDate, Status
from .someform import LoginForm, UserinfoForm
from django.contrib.auth.models import User


class HomePage(View):
    template_name = 'appsch/home.html'

    def get(self, response):
        return render(response, template_name=self.template_name)


class Mypage(ListView):
    template_name = 'appsch/userpage.html'
    model = Userinfo

    def get(self, response):
        a = self.model.objects.all().filter(Account=User.objects.all().get(username=response.user))
        ctx = {'usernamae': a}

        if a.count() > 0:
            return render(response, template_name=self.template_name, context=ctx)
        raise Http404


class UserPage(ListView):
    template_name = 'appsch/userpage.html'
    model = Userinfo

    def get(self, response, account):
        a = self.model.objects.all().filter(Account=User.objects.all().get(username=account))
        ctx = {'usernamae': a}

        if a.count() > 0:
            if a[0].Account == response.user:
                return redirect('appsch:mypage')
            return render(response, template_name=self.template_name, context=ctx)
        raise Http404


class UserPageEdit(ListView):
    template_name = 'appsch/editmypage.html'
    model = Userinfo

    def get(self, response):
        a = self.model.objects.all().filter(Account=User.objects.all().get(username=response.user))
        form = UserinfoForm()
        form.Meta.textet = 'sfafsa'

        ctx = {'myaccount': a, 'form': form}

        if a.count() > 0:
            return render(response, template_name=self.template_name, context=ctx)
        raise Http404

    def post(self, response):
        a = self.model.objects.all().filter(Account=User.objects.all().get(username=response.user))
        n = a[0]
        som = UserinfoForm(response.POST, response.FILES)
        n.First_name = som.data['firstname']
        n.Last_name = som.data['lastname']
        n.About_me = som.data['aboutme']
        if 'picture' in som.files.keys():
            n.picture = som.files['picture']
        n.save()
        return redirect('appsch:mypage')


class MyLessons(ListView):
    template_name = 'appsch/lessonslist.html'
    model = Userinfo

    def get(self, response):
        a = self.model.objects.all().filter(Account=User.objects.all().get(username=response.user))
        lessons = LessonDate.objects.all().filter(instructor=a[0])
        print(lessons)
        ctx = {'myaccount': a, 'lessons': lessons}

        if a.count() > 0:
            return render(response, template_name=self.template_name, context=ctx)
        raise Http404

    def post(self, response):
        a = self.model.objects.all().filter(Account=User.objects.all().get(username=response.user))
        n = a[0]
        som = UserinfoForm(response.POST, response.FILES)
        n.First_name = som.data['firstname']
        n.Last_name = som.data['lastname']
        n.About_me = som.data['aboutme']
        if 'picture' in som.files.keys():
            n.picture = som.files['picture']
        n.save()
        return redirect('appsch:mypage')


class AuthPage(View):
    template_name = 'appsch/login.html'

    def get(self, response):
        return render(response, template_name=self.template_name)

    def post(self, response):
        som = LoginForm(response.POST)
        user = authenticate(response, username=som.data['username'], password=som.data['password'])
        if user is not None:
            login(response, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(response, f"You are now logged in as {som.data['username']}")
            return redirect('/')
        else:
            messages.error(response, "Invalid username or password.")

        return render(response, template_name=self.template_name)


class RegisterPage(View):
    template_name = 'appsch/register.html'

    def get(self, response):
        return render(response, template_name=self.template_name)

    def post(self, response):
        som = LoginForm(response.POST)
        if User.objects.all().filter(email=som.data['email']).count() > 0 or User.objects.all().filter(
                username=som.data['username']).count() > 0:
            return redirect('appsch:register')
        user = User.objects.create_user(username=som.data['username'], password=som.data['password'],
                                        email=som.data['email'])

        a = Status(status="student")
        a.save()
        if Status.objects.all().get(status="student") == []:
            a = Status(status="student")
            a.save()
        n = Userinfo(Account=user, stat=Status.objects.all().get(status="student")).save()
        if user is not None:
            login(response, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('appsch:edit_profile')

        return render(response, template_name='appsch/register.html')
