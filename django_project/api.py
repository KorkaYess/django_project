from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, status

from django_project.email import send_email
from .models import Post, Profile
from .serializers import \
    ProfileSerializer, ProfileDetailSerializer, PostDetailSerializer,\
    ProfileRegistrationSerializer


class CreateRegisterToken(APIView):

    def post(self, request):
        profile = ProfileRegistrationSerializer().create(validated_data=request.data)  # noqa
        if profile is not None:
            profile.save()
            activation_token = PasswordResetTokenGenerator().make_token(profile)  # noqa
            send_email(profile, activation_token)
            return Response(status=status.HTTP_201_CREATED)
        else:  # pragma: no cover
            return Response({
                'Passwords do not match or this data already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):

    def post(self, request):
        serializer = super().serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id
        })


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):  # pragma: no cover
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()  # noqa


class PostViewSet(ModelViewSet):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    read_only = True


class ProfileViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    serializer_action_classes = {
        'list': ProfileSerializer,
        'retrieve': ProfileDetailSerializer,
    }
    read_only = True


router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register('profiles', ProfileViewSet)
api_urls = router.urls
