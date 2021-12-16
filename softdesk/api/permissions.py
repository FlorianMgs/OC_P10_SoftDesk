from rest_framework.permissions import BasePermission
from api.models import Project, Contributor


def check_contributor(user, project):
    for contributor in Contributor.objects.filter(project_id=project.id):
        if user == contributor.user_id:
            return True
    return False


class ContributorViewsetPermission(BasePermission):

    """
    Contributors can List other contributors, Read details about them
    Authors can List, Read, Add, Update or Delete a contributor
    """

    message = 'You dont have permission to do that.'

    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, Project.objects.filter(id=view.kwargs['projects_pk']).first())

        elif view.action in ['update', 'partial_update', 'create', 'destroy']:
            return request.user == Project.objects.filter(id=view.kwargs['projects_pk']).first().author_user_id


class ProjectPermission(BasePermission):

    """
    Anyone can create a project.
    Authors can Create, Read, Update and Delete a project.
    Contributors can List theirs projects, Read a project
    """

    message = 'You dont have permissions to do that.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class IssuePermission(BasePermission):

    """
    Issue author can Update and Delete their issues.
    Project contributors can List all project issues, Read issue or Create issue.
    """

    message = 'You dont have permission to do that.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.project_id)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class CommentPermission(BasePermission):

    """
    Comment author can Update or Delete their comments.
    Project contributors can List all comments of an issue, Read a comment or Create a comment.
    """

    message = 'You dont have permission to do that.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.issue_id.project_id)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id
