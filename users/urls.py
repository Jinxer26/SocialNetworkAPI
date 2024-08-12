from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, FriendRequestView, FriendListView, PendingFriendRequestsView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/',obtain_auth_token),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='respond_friend_request'),
    path('friends/', FriendListView.as_view(), name='friend_list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending_requests'),
]
