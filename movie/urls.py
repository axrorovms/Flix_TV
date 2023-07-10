from django.urls import path
from movie.views import CreateCommentAPIView, CommentListAPIView, CommentReplyListCreateAPIView, ParentListAPIView

urlpatterns = [
    path('comments', CreateCommentAPIView.as_view(), name='comments'),
    path('comment', ParentListAPIView.as_view(), name='parent_list'),
    path('comments/<int:comment_id>', CommentListAPIView.as_view(), name='comments_list'),
    path('comment_replay/<int:comment_id>', CommentReplyListCreateAPIView.as_view(), name='comments_replay'),
]
