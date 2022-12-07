from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views import View
from django.contrib.auth import get_user_model


User = get_user_model()


def password_reset_form(request):
    return render(request, 'magazine/index.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class Profile(View):

    def get(self, request, *args, **kwargs):
        template = 'users/profile.html'
        user = User.objects.filter(username=request.user)

        context = {
            'user': user,
        }
        return render(request, template, context)

@login_required
@transaction.atomic
def update_profile(request, slug):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            post = profile_form.save(commit=False)
            post.save()
            return redirect('magazine:home')

    else:
        profile_form = ProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {
        'profile_form': profile_form
    })

