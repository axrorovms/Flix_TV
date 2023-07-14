from django.urls import path
from movie.views import CreateCommentAPIView, CommentListAPIView, CommentReplyListCreateAPIView, ParentListAPIView, CommentLikeDislikeView
app_name='movie'
urlpatterns = [
    path('comments', CreateCommentAPIView.as_view(), name='comments'),
    path('comment', ParentListAPIView.as_view(), name='parent_list'),
    path('comments/<int:id>', CommentListAPIView.as_view(), name='comments_list'),
    path('comment_replay/<int:id>', CommentReplyListCreateAPIView.as_view(), name='comments_replay'),
    path('comment_likes/<int:id>', CommentLikeDislikeView.as_view(), name='comments_likes_and_dislikes'),
]
