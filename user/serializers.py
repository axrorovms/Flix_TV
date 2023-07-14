from django.db import models
from django.template.defaultfilters import slugify

import datetime
import uuid
from django.core.validators import RegexValidator, ValidationError
from rest_framework import serializers

from movie.models import Movie
from user.models import Wishlist

MEDIA_TYPES = {
    r'^(jpg|jpeg|png|JPG)$': 'image',
    r'^(mp4)$': 'videos'
}

FILE_TYPES = {
    r'^(jpg|jpeg|png|JPG)$': 'images',
    r'^(pdf)$': 'documents',
    r'^(mp4)$': 'videos'
}


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self, )
            while self.__class__.objects.filter(slug=self.slug).exists():
                slug = self.__class__.objects.filter(slug=self.slug).first().slug
                if '-' in slug:
                    try:
                        if slug.split('-')[-1] in self:
                            self.slug += '-1'
                        else:
                            self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                    except:
                        self.slug = slug + '-1'
                else:
                    self.slug += '-1'
        return super().save(*args, **kwargs)


def upload_name(instance, filename):
    file_type = filename.split('.')[-1]
    date = datetime.datetime.now().strftime('%Y/%m/%d')

    for regex, folder in FILE_TYPES.items():
        try:
            RegexValidator(regex).__call__(file_type)
            instance.type = folder
            return '%s/%s/%s/%s.%s' % (folder, instance._meta.model_name, date, uuid.uuid4(), file_type)
        except ValidationError:
            pass
    raise ValidationError('File type is unacceptable')


class WishlistCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('movie', 'user')


class WishlistListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('movie',)

    def to_representation(self, instance: Wishlist):
        rep = super().to_representation(instance)
        rep["photo"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('photo')).get('photo')
        rep["title"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('title')).get('title')
        rep["release_year"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('release_year')).get('release_year')
        rep["status"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('status')).get('status')
        rep["genre"] = [i.title for i in instance.movie.genre.all()]
        if not instance.movie.review_set.all():
            rep['rating'] = float(0.0)
        else:
            rep[
                'rating'] = f'{sum([i.rating for i in instance.movie.review_set.all()]) / instance.movie.review_set.all().count():.1f}'

        return rep
