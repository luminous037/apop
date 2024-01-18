import csv
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout
from django.views.generic import View, TemplateView, ListView, DetailView
from django.urls import reverse_lazy
from huami.forms import HuamiAccountCreationForm
from huami.models.healthdata import HealthData
from .forms import MyAuthenticationForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

# Create your views here.
class LoginView(Login):
    """로그인을 위한 클래스 기반 뷰
    """    
    template_name = 'accounts/login.html'
    redirect_field_name = 'redirect_to'
    next_page= reverse_lazy('home')

    
class LogoutView(Logout):
    """로그아웃을 위한 클래스 기반 뷰
    """    
    template_name = 'accounts/login.html'
    redirect_field_name = 'redirect_to'
    next_page = reverse_lazy('home')


class SignUpView(View):
    """회원가입 페이지를 제공하는 클래스 기반 뷰
    """    
    form_class = [HuamiAccountCreationForm, MyAuthenticationForm]
    template_name = 'accounts/signup.html'
    
    def get(self, request, *args, **kwargs):
        """회원가입 폼 입력 화면

        Args:
            request (HttpRequest): HttpRequest 정보

        Returns:
            HttpResponse: 렌더링 된 입력화면 HTML
        """        
        account_form = self.form_class[1]
        huami_account_form = self.form_class[0]
        return render(request, self.template_name, {'account_form': account_form,
                                                    'huami_account_form': huami_account_form})
    
    def post(self, request, *args, **kwargs):
        """회원가입 폼 제출 화면

        Args:
            request (HttpRequest): HttpRequest 정보

        Returns:
            HttpResponse: 입력에 따라 렌러딩 된 결과화면 HTML
        """        
        account_form = self.form_class[1](request.POST)
        huami_account_form = self.form_class[0](request.POST)
        
        #HuamiAccountCreationForm에서 계정 정보가 유효한지 검증
        if account_form.is_valid() and huami_account_form.is_valid():
            user = account_form.save()
            huami_account = huami_account_form.save(commit=False)
            huami_account.user = user
            huami_account.save()
            
            return redirect('accounts:successSignup')

        return render(request, self.template_name, {'account_form': account_form, 
                                                    'huami_account_form': huami_account_form})
        

class SuccessSignUpView(TemplateView):
    """회원가입 성공 화면 제공을 위한 클래스 기반 뷰
    """    
    template_name = 'accounts/successSignup.html'


class SuperuserRequiredMixin(UserPassesTestMixin):
    """관리자만 접근하도록 지정하는 믹스인
    """    
    def test_func(self):
        return self.request.user.is_superuser
    

class UserInfoView(DetailView, SuperuserRequiredMixin):
    """유저 정보를 제공하기 위한 클래스 기반 뷰
    """
    model = get_user_model()
    context_object_name = 'userInfo'
    template_name = 'accounts/userInfo.html'
    

class UserManageView(ListView, SuperuserRequiredMixin):
    """유저 정보들을 리스트로 제공하기 위한 클래스 기반 뷰
    """    
    template_name = 'accounts/userManage.html'
    model = settings.AUTH_USER_MODEL
    context_object_name = 'users'
    queryset = get_user_model().objects.filter(is_superuser=False)
    paginate_by = 5


class UserNoteUpdateView(View, SuperuserRequiredMixin):
    """유저에 대한 비고란을 수정하기 위한 클래스 기반 뷰
    post요청만 지원
    """
    def post(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.huami.note = request.POST['note']
        user.huami.save()
        return redirect(reverse_lazy('accounts:userInfo', kwargs={'pk': pk}))


class UserHealthNoteUpdateView(View, SuperuserRequiredMixin):
    """유저가 가진 건강 정보의 비고란을 수정하기 위한 클래스 기반 뷰
    post요청만 지원
    """    
    def post(self, request, pk):
        health_data = get_object_or_404(HealthData, pk=pk)
        health_data.note = request.POST['note']
        health_data.save()
        return redirect(reverse_lazy('accounts:userInfo', kwargs={'pk': health_data.huami_account.user.pk}))

class UserHealthDataSyncView(View, SuperuserRequiredMixin):
    """유저의 데이터 동기화를 위한 클래스 기반 뷰
    get요청만 지원
    """    
    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        try:
            health_data = HealthData.create_from_sync_data(user.huami)
            messages.success(request, f"{len(health_data)}일의 데이터가 추가되었습니다.")
        except Exception as e:
            messages.error(request, "동기화 과정 중 오류가 발생하였습니다.")
            
        return redirect(reverse_lazy('accounts:userInfo', kwargs={'pk': pk}))
    

class HealthDataCsvDownloadView(View, SuperuserRequiredMixin):
    """유저 데이터를 csv로 전달하는 클래스 기반 뷰
    get요청만 지원
    """    
    def _make_list(self, data):
        if data == None:
            return [None for i in range(1440)]
        return [int(i.strip()) for i in data[1:-1].split(",")]
    
    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        response = HttpResponse(headers={
            'Content-Type':'text/csv',
            'Content-Disposition': f'attachment; filename="{pk}.csv"'})
        
        writer = csv.writer(response)
        writer.writerow(['year', 'month', 'day', 'hour', 'minute', 
                         'age', 'height', 'weight', 'bmi', 
                         'heart', 'sleep', 'step', 'stress', 'spo2'])
        for health in user.huami.health.all():
            heart = self._make_list(health.heart_rate)
            sleep = self._make_list(health.sleep_quality)
            steps = self._make_list(health.step_count)
            stress = self._make_list(health.stress)
            spo2 = self._make_list(health.spo2)
            for minute in range(0, 1440):
                writer.writerow([health.date.year, health.date.month, health.date.day, minute // 60, minute % 60,
                                health.age, health.height, health.weight, health.bmi,
                                heart[minute], sleep[minute], steps[minute], stress[minute], spo2[minute]
                                ])
        
        return response
    

class HealthDataCsvDownloadAPIView(View):
    """데이터를 가져올 유저의 pk를 리스트로 받아서 해당하는 유저들의 데이터를 csv파일로 전달하는 API 클래스 기반 뷰
    get 요청만 지원
    """    
    
    def _make_list(self, data):
        if data == None:
            return [None for i in range(1440)]
        return [int(i.strip()) for i in data[1:-1].split(",")]
    
    def get(self, request: HttpRequest, pk):
        if request.headers.get('auth-key') != '1234':
            return HttpResponse({"Fuck you": "and you"})
        user = get_object_or_404(get_user_model(), pk=pk)
        response = HttpResponse(headers={
            'Content-Type':'text/csv',
            'Content-Disposition': f'attachment; filename="{pk}.csv"'})
        writer = csv.writer(response)
        writer.writerow(['year', 'month', 'day', 'hour', 'minute', 
                    'age', 'height', 'weight', 'bmi', 
                    'heart', 'sleep', 'step', 'stress', 'spo2'])
        for health in user.huami.health.all():
            heart = self._make_list(health.heart_rate)
            sleep = self._make_list(health.sleep_quality)
            steps = self._make_list(health.step_count)
            stress = self._make_list(health.stress)
            spo2 = self._make_list(health.spo2)
            for minute in range(0, 1440):
                writer.writerow([health.date.year, health.date.month, health.date.day, minute // 60, minute % 60,
                                health.age, health.height, health.weight, health.bmi,
                                heart[minute], sleep[minute], steps[minute], stress[minute], spo2[minute]
                                ])
        return response