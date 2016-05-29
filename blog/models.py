from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):

	def get_queryset(self):
		
		return super(PublishedManager,
						self).get_queryset()\
								.filter(status='published')


class Post(models.Model):

	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title = models.CharField(max_length=250) #This is the field for the post title
	slug = models.SlugField(max_length=250, 
							unique_for_date='publish') #This is a field intended to be used in URLs
	author = models.ForeignKey(User,
								related_name='blog_posts') #This field defines a many-to-one relationship
	body = models.TextField() #This is the body of the post
	publish = models.DateTimeField(default=timezone.now) #This datetime indicates when the post was published
	created = models.DateTimeField(auto_now_add=True) #This datetime indicates when the post was created
	updated = models.DateTimeField(auto_now=True) #This datetime indicates the last time the post has been updated
	status = models.CharField(max_length=10,
								choices=STATUS_CHOICES,
								default='draft') #This is a field to show the status of a post
	objects = models.Manager() # The default manager.
	published = PublishedManager() # Our custom manager.

	def get_absolute_url(self):
		return reverse('blog:post_detail',
						args=[self.publish.year,
								self.publish.strftime('%m'),
								self.publish.strftime('%d'),
								self.slug])


	class Meta:
		"""
		Sorting results by the publish field in descending order by default when we query the
		database.
		"""
		ordering = ('-publish',)
	
	def __str__(self):
		
		return self.title