from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from pedidos.models import Pedido 

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
            messages.success(request, f'¡Tu cuenta ha sido actualizada!')
            return redirect('user_panel')
        else:
            print("--- Form Error Debug ---")
            print(f"FILES: {request.FILES}")
            print(f"User Form Errors: {u_form.errors}")
            print(f"Profile Form Errors: {p_form.errors}")
            messages.error(request, 'Hubo un error al actualizar tu perfil.')

    else:
        u_form = UserUpdateForm(instance=request.user)
        # Ensure profile exists for GET request too
        if not hasattr(request.user, 'profile'):
            from .models import Profile
            Profile.objects.create(user=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Fetch orders for the current user using the new Pedido model
    orders = Pedido.objects.filter(comprador=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders
    }

    return render(request, 'panel_usuario/dashboard.html', context)
