from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Movie, Comment
from .serializers import CommentSerializer, ChildSerializer, CommentLikeDislikeSerializer
from rest_framework.response import Response
from rest_framework import status


class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Movie.objects.all()


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_id = self.kwargs['id']
        return Comment.objects.filter(id=comment_id)


class CommentReplyListCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        comment_id = self.kwargs['id']
        return Comment.objects.filter(parent_id=comment_id)

    def perform_create(self, serializer):
        comment_id = self.kwargs['id']
        parent_comment = Comment.objects.get(id=comment_id)
        serializer.save(parent=parent_comment)


class ParentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['show_children'] = True
        return context


class CommentLikeDislikeView(CreateAPIView):
    serializer_class = CommentLikeDislikeSerializer
    def create(self, request, *args, **kwargs):
        comment_id = kwargs.get('id')
        action = request.data.get('action')

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Fucking comment 404"}, status=status.HTTP_404_NOT_FOUND)

        if action == "like":
            comment.likes += 1
        elif action == "dislike":
            comment.dislikes += 1
        else:
            return Response({"error": "Fucking bad request"}, status=status.HTTP_400_BAD_REQUEST)

        comment.save()

        return Response({"success": f"Fucking {action} added"}, status=status.HTTP_201_CREATED)
