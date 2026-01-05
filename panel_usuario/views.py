from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from store.models import Order 

@login_required
def dashboard(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Ensure profile exists before updating (though signal handles creation, migration might miss existing users)
        if not hasattr(request.user, 'profile'):
            from .models import Profile
            Profile.objects.create(user=request.user)
            
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_panel')

    else:
        u_form = UserUpdateForm(instance=request.user)
        # Ensure profile exists for GET request too
        if not hasattr(request.user, 'profile'):
            from .models import Profile
            Profile.objects.create(user=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Fetch orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders
    }

    return render(request, 'panel_usuario/dashboard.html', context)
