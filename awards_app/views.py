from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

# app imports
from awards_app.forms import CreateUserForm, UserForm
from awards_app.models import  Profile
from api.models import Project
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.views import View


# Create your views here.
# DJANGO MONOLITH APPLICATION VIEW CLASSES
class HomeView(View):
    def get(self, request):
        # trending = Project.objects.all()
        # for site in trending:
        # get site with average rating > 6 == trending site
        # trending_site = site.avg_ratings()
        # if trending_site > 6:
        #     return trending_site

        projects = Project.objects.all().order_by('-created_at')[:12]
        ctx = {
            # 'trend': trending_site,
            'projects': projects
        }
        return render(request, 'awards/index.html', ctx)


# todo: register view
class UserRegisterView(View):
    """this class renders the registration form and executes the logic for registering a user"""
    form = CreateUserForm()
    ctx = {
        'title': 'Register',
        'form': form,
    }

    def get(self, request):
        return render(request, 'awards/register.html', self.ctx)

    def post(self, request):
        form = CreateUserForm(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            print(form)
            form = CreateUserForm()  # reset form
            messages.success(request, 'Registered successfully.')
            return redirect(reverse('awards:login'))
        messages.error(request, 'Registration failed.')
        context = {
            form: form,
        }
        return render(request, 'awards/register.html', context)


# todo: login view
class UserLoginView(View):
    context = {
        'title': 'Login'
    }

    def get(self, request):
        return render(request, 'awards/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('awards:home'))
        else:
            messages.error(request, 'Invalid username or password.')

        return render(request, 'awards/login.html', self.context)


class ProjectView(View):
    """this class renders a single project by its id and executes the rate functionality"""

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        context = {
            'project': project
        }
        return render(request, 'awards/project.html', context)


# !userprofile create method
@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)

    # prepolate the form with the user's data
    user_form = UserForm(instance=user)

    ProfileInlineFormSet = inlineformset_factory(
        User, Profile, fields=('photo', 'bio', 'phone', 'street', 'neighborhood'))
    formset = ProfileInlineFormSet(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(
                request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormSet(
                request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormSet(
                    request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/profile/')

        return render(request, 'awards/edit_profile.html', {
            "pk": pk,
            "user_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied

# logout


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('awards:home')
