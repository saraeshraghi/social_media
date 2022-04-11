from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post, Relations
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

# Create your views here.


class UserRegister(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'شما به این صفحه دسترسی ندارید', 'warning')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'شما با موفقیت ثبت نام کردید', 'success')
            return render(request, 'home/index.html')
        return render(request, 'accounts/register.html', {'form': form})


class UserLogin(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'شما به این صفحه دسترسی ندارید', 'warning')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogout(LoginRequiredMixin, View):
    # login_url = '/accounts/login'
    def get(self, request):
        logout(request)
        messages.success(request, 'شما از پنل کاربری با موفقیت خارج شدید', 'success')
        return redirect('home:home')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, user_id):
        not_user = False
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        if not Relations.objects.filter(from_user=request.user, to_user=user).exists() and user.id != request.user.id:
            not_user = True
        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts, 'not_user': not_user})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserFollowing(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relations = Relations.objects.filter(from_user=request.user, to_user=user).exists()
        if relations:
            messages.error(request, 'شما قبلا این کاربر را دنبال کردید', 'dander')
        else:
            Relations(from_user=request.user, to_user=user).save()
            messages.success(request, 'شما این کاریبر را با موفقیت دنبال میکنید', 'success')
        return redirect('accounts:user_profile', user.id)


class UserUnfollow(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relations = Relations.objects.filter(from_user=request.user, to_user=user)
        if relations.exists():
            relations.delete()
            messages.success(request, 'این کاربر از دنبال کننده های شما حذف شد', 'success')
        else:
            messages.error(request, 'این کاربر در دنبال کننده های شما وجود ندارد', 'dander')
        return redirect('accounts:user_profile', user.id)


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.userprofile, initial={'email': request.user.email})
        return render(request, 'accounts/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'پروفایل شما با موفقیت تغییر یافت', 'success')
        return redirect('accounts:user_profile', request.user.id)
