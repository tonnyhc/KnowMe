from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from pyperclip import copy

from knowme.accounts.models import Profile
from knowme.common.forms import CommentForm, SearchBarForm, CommentReportForm
from knowme.common.models import Followers, Comment, Like, SavePost
from knowme.posts.forms import PostReportForm
from knowme.posts.models import Post


@login_required
def index(request):
    posts = Post.objects.all().order_by('-publish_date')

    comment_form = CommentForm()
    report_form = PostReportForm()
    all_liked_posts_by_request_user = [like.to_post.id for like in request.user.profile.like_set.all()]
    all_saved_posts_by_request_user = [post.to_post.id for post in request.user.profile.savepost_set.all()]
    request_user_followers = [follower.following_profile_id for follower in
                              Followers.objects.filter(profile_id=request.user.profile.pk)]

    context = {
        'posts': posts,
        'request_user_followers': request_user_followers,
        'comment_form': comment_form,
        'all_liked_posts_by_request_user': all_liked_posts_by_request_user,
        'all_saved_posts_by_request_user': all_saved_posts_by_request_user,
        'report_form': report_form,
        'search_form': SearchBarForm,
    }
    return render(request, 'common/index.html', context)


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(pk=post_id).get()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_post = post
            comment.profile = request.user.profile
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f"#{post_id}")


@login_required
def delete_comment(request):
    comment_id = request.path.split('/comments/delete/')[1]
    comment = Comment.objects.filter(pk=comment_id)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'] + f"#")


@login_required
def like_post(request, post_id):
    post = Post.objects.filter(pk=post_id).get()
    liked_object = Like.objects.filter(to_post_id=post_id, to_profile=request.user.profile)

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_post=post, to_profile=request.user.profile)
        like.save()

    redirect_path = request.META['HTTP_REFERER'] + f'#{post_id}'
    return redirect(redirect_path)


@login_required
def save_post(request, post_id):
    post = Post.objects.filter(pk=post_id).get()
    saved_object = SavePost.objects.filter(to_post_id=post_id, to_profile=request.user.profile.pk)

    if saved_object:
        saved_object.delete()
    else:
        save_post = SavePost(to_post_id=post.id, to_profile_id=request.user.profile.pk)
        save_post.save()

    redirect_path = request.META['HTTP_REFERER'] + f'#{post_id}'
    return redirect(redirect_path)


@login_required(login_url=reverse_lazy('sign in'))
def follow_profile(request, profile_id):
    profile = Profile.objects.filter(pk=profile_id).get()
    followed_object = Followers.objects.filter(following_profile_id=profile.pk)

    if profile.pk == request.user.profile.pk:
        redirect_path = request.META['HTTP_REFERER']
        return redirect(redirect_path)

    if followed_object:
        followed_object.delete()
    else:
        follower = Followers(following_profile_id=profile.pk, profile_id=request.user.profile.pk)
        follower.save()

    redirect_path = request.META['HTTP_REFERER']
    return redirect(redirect_path)


@login_required
def comment_report_view(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).get()
    if request.method == "POST":
        form = CommentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.to_comment = comment
            report.profile = request.user.profile
            report.save()
            return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])


def share_post(request, pk):
    copy(request.META['HTTP_HOST'] + resolve_url('post details', pk))
    return redirect(request.META['HTTP_REFERER'] + f'#{pk}')


@login_required
def notifications_view(request):
    follows = Followers.objects.filter(following_profile_id=request.user.profile.pk)
    likes = Like.objects.filter(to_post__profile__user=request.user)
    context = {
        'follows': follows,
        'likes': likes,
        'search_form': SearchBarForm()
    }
    return render(request, 'common/notifications.html', context)


def search_view(request):
    search_form = SearchBarForm(request.GET)
    search_pattern = None
    profiles = None
    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['profile_name']
    if search_pattern:
        profiles = Profile.objects.filter(user__username__icontains=search_pattern) | Profile.objects.filter(
            first_name__icontains=search_pattern) | Profile.objects.filter(
            last_name__icontains=search_pattern)
    context = {
        'profiles': profiles,
        'search_form': SearchBarForm()
    }
    return render(request, 'common/search.html', context)


def about_page(request):
    return render(request, 'common/about.html')