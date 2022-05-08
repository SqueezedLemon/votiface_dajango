from django.urls import path

from .views import CheckCitizenship, UserRecordView, UserDataView, SetProfileImage

app_name='accounts_api'
urlpatterns = [
    path('user/get_token/', UserRecordView.as_view(), name='user'),
    path('user/get_user_info/', UserDataView.as_view(), name='info'),
    path('user/set_profile_image/', SetProfileImage.as_view(), name='image'),
    path('user/check_citizenship/', CheckCitizenship.as_view(), name='citizenship'),
]