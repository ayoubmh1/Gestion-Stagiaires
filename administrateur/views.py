from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if request.user.user_type != 0:
        return redirect('login')  # Redirect if not administrateur
    return render(request, 'administrateur/dashboard.html')
