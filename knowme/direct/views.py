from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from knowme.accounts.models import Profile
from knowme.common.forms import SearchBarForm
from knowme.direct.forms import DirectForm
from knowme.direct.models import Message


@login_required
def inbox(request):
    profile = request.user.profile
    profiles = {}

    for query in Message.objects.filter(recipient_id=profile.pk).all():
        if query.sender not in profiles:
            profiles[query.sender] = {
                "text": query.text,
                "date": query.date,
                "is_read": query.is_read
            }

    context = {
        'profiles': profiles,
        'search_form': SearchBarForm()
    }

    return render(request, 'direct/inbox.html', context)


@login_required
def direct(request, username):
    profile = request.user.profile
    profiles = {}

    for query in Message.objects.filter(recipient_id=profile.pk).all():
        if query.sender not in profiles:
            profiles[query.sender] = {
                "text": query.text,
                "date": query.date,
                "is_read": query.is_read
            }

    direct_profile = Profile.objects.filter(user__username=username).get()
    conversation_messages = Message.objects.filter(sender_id=direct_profile.pk,
                                                   recipient_id=profile.pk).all() | Message.objects.filter(
        recipient_id=direct_profile.pk, sender_id=profile.pk)
    context = {
        'profiles': profiles,
        'active_direct': username,
        'direct_profile': direct_profile,
        'conversation_messages': conversation_messages,
        'direct_form': DirectForm,
        'search_form': SearchBarForm()
    }

    return render(request, 'direct/direct.html', context)


@login_required
def send_direct(request, username, pk):
    if request.method == "POST":
        form = DirectForm(request.POST)
        if form.is_valid():
            direct = form.save(commit=False)
            direct.sender_id = request.user.profile.pk
            direct.recipient_id = pk
            direct.save()
            return redirect(reverse_lazy('direct', kwargs={'username': username}))
