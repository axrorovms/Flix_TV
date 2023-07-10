from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Movie, Comment
from .serializers import CommentSerializer, ChildSerializer


class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Movie.objects.all()


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(id=comment_id)


class CommentReplyListCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(parent_id=comment_id)

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        parent_comment = Comment.objects.get(id=comment_id)
        serializer.save(parent=parent_comment)


class ParentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['show_children'] = True
        return context
