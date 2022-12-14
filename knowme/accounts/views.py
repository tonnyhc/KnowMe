from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, get_user_model, login
from django.urls import reverse_lazy
from django.views import generic as views

from knowme.accounts.forms import CustomAuthForm, UserCreateForm, CustomPasswordChangeForm, ReportProfileForm, \
    AccountEditForm, ProfileEditForm
from knowme.accounts.models import Profile
from knowme.common.forms import SearchBarForm
from knowme.common.models import Followers

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    form_class = CustomAuthForm
    template_name = 'accounts/login-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchBarForm()
        return context

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is
            self.request.session.modified = True
        return super(SignInView, self).form_valid(form)


class SignUpView(views.CreateView):
    template_name = 'accounts/register-page.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchBarForm()
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class PasswordChangeView(auth_views.PasswordChangeView, LoginRequiredMixin):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/partials/change-password.html'
    success_url = reverse_lazy('sign out')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchBarForm()
        return context


class SignOutView(auth_views.LogoutView, LoginRequiredMixin):
    next_page = reverse_lazy('index')


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followers = Followers.objects.filter(following_profile_id=self.object.pk)
        following = Followers.objects.filter(profile_id=self.object.pk)
        is_following = []
        print(len(is_following))

        if self.request.user.is_authenticated:
            context['request_user_followings'] = [follow.profile.pk for follow in Followers.objects.filter(
                profile_id=self.request.user.profile.pk).all()]
            context['is_owner'] = self.request.user.profile == self.object
            is_following = Followers.objects.filter(following_profile_id=self.object.pk,
                                                    profile_id=self.request.user.profile.pk).all()
        if len(is_following) == 0:
            is_following = False
        else:
            is_following = True

        context['posts'] = self.object.post_set.all()
        context['posts_count'] = len(self.object.post_set.all())
        context['followers'] = followers
        context['followings'] = following
        context['followers_count'] = len(followers)
        context['followings_count'] = len(following)
        context['is_following'] = is_following
        context['search_form'] = SearchBarForm()
        context['report_form'] = ReportProfileForm()
        return context


class AccountEditView(views.UpdateView, LoginRequiredMixin):
    model = UserModel
    form_class = AccountEditForm
    template_name = 'accounts/partials/account_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchBarForm()
        return context

    def get_success_url(self):
        return reverse_lazy('profile edit', kwargs={'pk': self.request.user.profile.pk})


@login_required
def account_delete_view(request, pk):
    if request.user.pk != pk:
        return redirect('account edit', pk)
    account = UserModel.objects.filter(pk=pk).get()
    profile = Profile.objects.filter(pk=account.profile.pk).get()
    account.delete()
    profile.delete()
    return redirect('index')


@login_required
def profile_edit_view(request, pk):
    profile = Profile.objects.get(pk=pk)
    context = {}
    if request.user.profile.pk != profile.pk:
        return redirect(reverse_lazy('profile edit', kwargs={'pk': request.user.profile.pk}))
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('profile details', kwargs={'pk': pk}))
    else:
        form = ProfileEditForm(instance=profile)
        context = {
            'form': form,
            'profile': profile,
            'search_form': SearchBarForm()
        }

    return render(request, 'accounts/partials/edit_profile.html', context)


@login_required
def report_profile(request, username):
    if request.user.username == username:
        return redirect(request.META['HTTP_REFERER'])
    if request.method == "POST":
        form = ReportProfileForm(request.POST)
        profile_to_report = Profile.objects.filter(user__username=username).first()
        if form.is_valid():
            report = form.save(commit=False)
            report.to_profile = profile_to_report
            report.from_profile = request.user.profile
            report.save()

    return redirect(request.META['HTTP_REFERER'])
