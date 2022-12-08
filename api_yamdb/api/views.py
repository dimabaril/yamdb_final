from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdministratorOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    ForAdminSerializer,
    ForUserSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    TokenSerializer
)
from users.models import User
from reviews.models import Review, Title, Category, Genre


class APISignUp(APIView):
    """User auth."""

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ForUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.create_confirmation_code_and_send_email(
                serializer.data['username'])

            return Response(
                {'email': serializer.data['email'],
                 'username': serializer.data['username']},
                status=status.HTTP_200_OK)

    @staticmethod
    def create_confirmation_code_and_send_email(username):
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=f'{user.username} Confirmation code',
            message=f'Your confirmation code {confirmation_code}',
            from_email=None,
            recipient_list=[user.email, ])


class APIToken(APIView):
    """Get token."""

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])

            if default_token_generator.check_token(
                    user, serializer.data['confirmation_code']):
                token = AccessToken.for_user(user)

                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK)

            return Response({
                'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """Работа с пользователями."""

    permission_classes = (IsAdmin, )
    queryset = User.objects.all()
    serializer_class = ForAdminSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = ForUserSerializer(request.user)

        if request.method == 'PATCH':

            if request.user.is_admin:
                serializer = ForAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)

            else:
                serializer = ForUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data)


class CustomMixin(ListModelMixin,
                  CreateModelMixin,
                  DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Prebuild ViewSet for GET, POST and DEL methods."""

    pass


class CategoryViewSet(CustomMixin):
    """API для работы с моделью категорий."""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    """API для работы с моделью жанров."""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """API для работы с моделью произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):

        if self.action in ('create', 'partial_update'):

            return TitleCreateSerializer

        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Title.objects.filter(pk=self.kwargs.get('title_id')).exists():

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        if Review.objects.filter(
            author=self.request.user,
            title=self.kwargs.get('title_id')
        ).exists():

            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        title = Title.objects.get(pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for comments model."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not (
            Title.objects.filter(pk=self.kwargs.get('title_id')).exists()
            or Review.objects.filter(pk=self.kwargs.get('review_id')).exists()
        ):

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
