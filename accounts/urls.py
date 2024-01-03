from django.urls import path
from .views import HealthDataCsvDownloadView, LoginView, LogoutView, SignUpView, SuccessSignUpView, UserHealthDataSyncView, UserInfoView, UserManageView, UserNoteUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('successSignup/', SuccessSignUpView.as_view(), name='successSignup'),
    path('manage/', UserManageView.as_view(), name='userManage'),
    path('info/<int:pk>/', UserInfoView.as_view(), name='userInfo'),
    path('<int:pk>/updateNote/', UserNoteUpdateView.as_view(), name='updateNote'),
    path('<int:pk>/syncData/', UserHealthDataSyncView.as_view(), name='syncHealth'),
    path('<int:pk>/csvData/', HealthDataCsvDownloadView.as_view(), name='csvDownload')
]
