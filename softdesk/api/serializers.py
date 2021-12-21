from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Project, Contributor, Issue, Comment


User = get_user_model()


class UserSignupSerializer(ModelSerializer):

    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'tokens']

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError("User already exists")
        return value

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise ValidationError("Password is empty")

    def get_tokens(self, user: User) -> dict:
        tokens = RefreshToken.for_user(user)
        data = {
            "refresh": str(tokens),
            "access": str(tokens.access_token)
        }
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'author_user_id']


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'issues']

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'title', 'priority', 'tag', 'status', 'project_id']


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'title', 'description', 'priority', 'tag', 'status', 'author_user_id', 'assignee_user_id', 'project_id', 'comments']

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        return CommentListSerializer(queryset, many=True).data


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_time', 'description', 'author_user_id', 'issue_id']



