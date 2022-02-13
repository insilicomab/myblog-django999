from django.db import models
from django.contrib.sites.models import Site


class SiteConfig(models.Model):
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    meta_title = models.CharField(verbose_name='meta_title', max_length=100)
    meta_description = models.CharField(verbose_name='meta_description', max_length=300)
    meta_keywords = models.CharField(verbose_name='SEOキーワード', max_length=300)
    author = models.CharField(verbose_name='管理者', max_length=30)
    top_title = models.CharField(verbose_name='Topページタイトル', max_length=100)
    top_subtitle = models.CharField(verbose_name='Topページサブタイトル', max_length=200)

    def __str__(self):
        return self.meta_title