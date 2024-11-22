from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Profile

def home(request):
    return render(request, 'core/home.html')

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def subscribe(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.is_subscribed = True
    profile.save()
    messages.success(request, 'You have successfully subscribed to the newsletter.')

    # Send subscription confirmation email
    send_mail(
        'Subscription Confirmation',
        f"Dear {request.user.username},\n\nThank you for subscribing to our newsletter!\n\nBest regards,\nThe Kitchen Garden Team",
        'kitchengardenci@gmail.com',
        [request.user.email],
        fail_silently=False,
    )

    return redirect('home')

@login_required
def unsubscribe(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.is_subscribed = False
    profile.save()
    messages.success(request, 'You have successfully unsubscribed from the newsletter.')

    # Send unsubscription confirmation email
    send_mail(
        'Unsubscription Confirmation',
        f"Dear {request.user.username},\n\nYou have successfully unsubscribed from our newsletter.\n\nBest regards,\nThe Kitchen Garden Team",
        'kitchengardenci@gmail.com',
        [request.user.email],
        fail_silently=False,
    )

    return redirect('home')
