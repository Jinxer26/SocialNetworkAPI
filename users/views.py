from django.contrib.auth import authenticate
from rest_framework import authentication,generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .authentication import TokenAuthentication
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

class UserSignupView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        firstname = data.get('first_name')
        lastname = data.get('last_name')
        if not email or not password:
            return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchView(generics.ListAPIView):

    authentication_classes = [authentication.SessionAuthentication,TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '').lower()
        return User.objects.filter(
            Q(email__iexact=keyword) |
            Q(username__icontains=keyword) |
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword)
        )

class FriendRequestView(APIView):
    authentication_classes = [authentication.SessionAuthentication,TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        from_user = request.user
        if from_user == to_user:
            return Response({"error": "You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        recent_requests = FriendRequest.objects.filter(from_user=from_user, created_at__gte=timezone.now()-timedelta(minutes=1))
        if recent_requests.count() >= 3:
            return Response({"error": "You can only send 3 friend requests per minute"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(id=pk, to_user=request.user)
            stat = request.data.get('status')
        except:
            return Response({"error": "Friend Request Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if stat not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        friend_request.status = stat
        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.SessionAuthentication,TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user.username)
        friends1 = FriendRequest.objects.filter(Q(from_user=user) & Q(status='accepted')).values_list('to_user', flat=True)
        friends2 = FriendRequest.objects.filter(Q(to_user=user) & Q(status='accepted')).values_list('from_user', flat=True)
        return User.objects.filter(id__in=friends2) | User.objects.filter(id__in=friends1)

class PendingFriendRequestsView(generics.ListAPIView):

    serializer_class = FriendRequestSerializer
    authentication_classes = [authentication.SessionAuthentication,TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = FriendRequest.objects.filter(to_user=self.request.user, status='pending')
        return queryset