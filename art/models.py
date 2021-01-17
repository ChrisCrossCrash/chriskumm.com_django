from django.db import models
from ckeditor.fields import RichTextField


class Artist(models.Model):
    name = models.CharField(max_length=100)
    biography = RichTextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    web_site_url = models.URLField(blank=True)
    description = RichTextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Piece(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT)
    styles = models.ManyToManyField(Style, blank=True)
    description = RichTextField(blank=True, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    wiki_url = models.URLField(blank=True)
    # ImageFields require 'Pillow' to be installed
    # A media url is also required in urlpatterns for serving files in development
    image = models.ImageField(upload_to='art/piece_images/')

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title
