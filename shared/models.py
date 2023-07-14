from django.template.defaultfilters import slugify
from django.db import models

from django.core.validators import RegexValidator, ValidationError
import datetime
import uuid

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
    slug = models.SlugField(max_length=100, blank=True)

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


