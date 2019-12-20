from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from accounts.forms import LoginForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            messages.success(request, '가입이 완료되었습니다. 다시 로그인 해주세요.')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup-page.html', {
        'form': form,
    })


class Loginviews(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_invalid(self, form):
        messages.warning(self.request, '아이디 또는 비밀번호를 잘못 입력 하셨습니다.')
        return redirect('login')


loginview = Loginviews.as_view()


class LogoutViews(LogoutView):
    next_page = settings.LOGIN_URL


logoutview = LogoutViews.as_view()