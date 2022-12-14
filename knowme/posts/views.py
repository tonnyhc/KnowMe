from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from knowme.common.forms import CommentForm, CommentReportForm, SearchBarForm
from knowme.common.models import Like, Followers, SavePost
from knowme.posts.forms import PostReportForm, PostEditForm, PostAddForm
from knowme.posts.models import Post


class PostDetailsView(views.DetailView):
    template_name = 'posts/post_details.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes = Like.objects.filter(to_post=self.object)
        if self.request.user.is_authenticated:
            context['request_user_followings'] = [follower.following_profile_id for follower in
                                                  Followers.objects.filter(profile_id=self.request.user.profile.pk)]
            context['is_creator'] = self.request.user.profile == self.object.profile
            context['is_user_saved_post'] = SavePost.objects.filter(to_profile_id=self.request.user.profile.pk,
                                                                    to_post_id=self.object.pk)
            context['is_user_liked'] = Like.objects.filter(to_profile_id=self.request.user.profile.pk,
                                                           to_post_id=self.object.pk)
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm
        context['comment_report_form'] = CommentReportForm()
        context['search_form'] = SearchBarForm()
        context['report_form'] = PostReportForm()
        context['likes_count'] = len(likes)
        return context


@login_required
def post_edit_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.profile.pk != post.profile.pk:
        return redirect(reverse_lazy('index'))

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('post details', args=(pk,)))
    else:
        form = PostEditForm(instance=post)
        context = {
            'form': form,
            'post': post,
            'pk': pk,
            'search_form': SearchBarForm(),
        }
        return render(request, 'posts/post-edit.html', context)


class PostDeleteView(views.DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('index')


@login_required
def add_post_view(request):
    form = PostAddForm()
    if request.method == "POST":
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = request.user.profile
            post.save()
            return redirect(reverse_lazy('index'))
    else:
        context = {
            'form': form,
            'search_form': SearchBarForm()
        }
        return render(request, 'posts/post_add.html', context)
    context = {"form": form}
    return render(request, 'posts/post_add.html', context)


@login_required
def post_report_view(request, pk):
    post = Post.objects.filter(pk=pk).get()
    if request.method == "POST":
        form = PostReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.to_post = post
            report.profile = request.user.profile
            report.save()
            return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])
