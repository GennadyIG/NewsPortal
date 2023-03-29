from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView, DetailView
from NPbd.models import Category, Subscription

from .forms import UserForm


class ShowProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'


class ProfileEdit(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'edit_profile.html'

    def get_success_url(self):
        return reverse('profile', args=[str(self.request.user.id)])


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
