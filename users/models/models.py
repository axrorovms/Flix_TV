from users.models.base import BaseAbstractUser


class User(BaseAbstractUser):
    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def reviews(self):
        return self.review_set.all()


