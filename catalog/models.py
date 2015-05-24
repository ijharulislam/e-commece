
from __future__ import unicode_literals
from django.db import models
from django.db import models
from django.db.models import Q
#from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from financial.models import Tax
# Create your models here.



"""-------------Author------------------------"""



class Author(models.Model):
	name = models.CharField(max_length=255)
	slug_name = models.SlugField(max_length=255)
	description = models.TextField(null=True, blank=True)
	short_introduction = models.CharField(max_length=1024, blank=True, default='')
	email = models.EmailField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return '/author/' + self.slug_name

	def save(self, force_insert=False, force_update=False):
		if Author.objects.filter(slug_name=self.slug_name).exclude(pk=self.id).count() != 0:
			 raise Exception('Duplicate slug title !!!')
		return super(Author, self).save(force_insert=force_insert, force_update=force_update)


"""-------------Publisher------------------------"""
	

class Publisher (models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	description = models.TextField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	updated_by = models.CharField(max_length=100)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.CharField(max_length=100)

	class Meta:
		 ordering = ('name',)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_publisher', (self.slug,))

	def get_breadcrumbs(self):

		return ({'name': self.name, 'url': self.get_absolute_url()},)

	@classmethod
	def get_publishers(cls):
		return list(cls.objects.filter(is_active=True))



"""-------------categories------------------------"""

class Category(models.Model): 
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	description = models.TextField(null=True, blank=True)
	pic = models.ImageField(upload_to='images/catalog/categories', null=True, blank=True)
	parent = models.ForeignKey('self', related_name='sub_categories', null=True, blank=True)
	tags = models.CharField(max_length=100, null=True, blank=True,
                            help_text='Comma-delimited set of SEO keywords for meta tag')
	display_order = models.IntegerField(default=0)
	is_active = models.BooleanField(default=True)
	updated_by = models.CharField(max_length=100)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.CharField(max_length=100)

	class Meta:
		ordering = ('display_order', 'id',)
		verbose_name_plural = 'Categories'

	def __init__(self, *args, **kwargs):
		super(Category, self).__init__(*args, **kwargs)
		self.sub_categories_list = None

	def __unicode__(self):
		if self.parent:
			return '%s > %s' % (self.parent, self.name)
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_category', (self.slug,))

	def get_breadcrumbs(self):
		breadcrumbs = ({'name': self.name, 'url': self.get_absolute_url()},)

		if self.parent:
			return self.parent.get_breadcrumbs() + breadcrumbs

		return breadcrumbs

	def get_all_sub_categories(self):
		for sub_category in self.sub_categories_list:
			yield sub_category

			for sub_category2 in sub_category.get_all_sub_categories():
				yield sub_category2

	def get_sub_categories(self, categories):
		sub_categories = []
		for sub_category in categories:
			if sub_category.parent_id == self.id:
				sub_category.parent = self
				sub_categories.append(sub_category)

		return sub_categories

	@classmethod
	def get_category(cls, slug):
		categories = list(cls.get_categories())

		for category in categories:
			if category.slug == slug:
				return category

	@classmethod
	def get_categories(cls):
		categories = list(
			cls.objects.filter(is_active=True).order_by('display_order'))
		
		for category in categories:
			category.sub_categories_list = category.get_sub_categories(
				categories)

		return categories





"""-------------Book------------------------"""



class Book(models.Model):
	name = models.CharField(max_length=100, unique=True)
	authors = models.ManyToManyField(Author, blank=True, related_name='book_set')
	author_name = models.CharField(max_length=256, blank=True, default='')
	content = RichTextField()
	slug = models.SlugField(max_length=100, unique=True)
	book_publisher = models.ForeignKey(Publisher, help_text='Publisher')
	sku = models.CharField(max_length=50, verbose_name='SKU', null=True, blank=True)
	gtin = models.CharField(max_length=50, verbose_name='GTIN', null=True, blank=True,
                            help_text='Global Trade Item Number (GTIN)')
	category = models.ForeignKey(Category)
	gist = models.CharField(
        max_length=500, null=True, blank=True, help_text='Short description of the product')
	description = models.TextField(
        null=True, blank=True, help_text='Full description displayed on the product page')
	price = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Per unit price')
	old_price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0)
	cost = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0, help_text='Per unit cost')
	shipping_cost = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0, help_text='Shipping cost per unit')
	quantity = models.IntegerField(help_text='Stock quantity')

	is_active = models.BooleanField(
        default=True, help_text='Product is available for listing and sale')

	is_bestseller = models.BooleanField(
        default=False, help_text='It has been best seller')
	is_featured = models.BooleanField(
        default=False, help_text='Promote this product on main pages')
	is_free_shipping = models.BooleanField(
        default=False, help_text='No shipping charges')
	tax = models.ForeignKey(
        Tax, null=True, blank=True,  help_text='Tax applied on this product, if tax exempt select none')
	tags = models.CharField(max_length=250, null=True, blank=True,
                            help_text='Comma-delimited set of SEO keywords for meta tag')
	updated_by = models.CharField(max_length=100)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.CharField(max_length=100)
	isbn = models.CharField(max_length=32, verbose_name="ISBN", blank=True,
		help_text='Add ISBN of the book') # A-B-C-D

	class Meta:
		ordering = ('id',)

	def __unicode__(self):
		return self.name

	def get_discount(self):
		if self.old_price:
			return int(((self.old_price - self.price) / self.old_price) * 100)

		return 0

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_book', (self.id, self.slug,),)

	def get_breadcrumbs(self, categories):
		breadcrumbs = ({'name': self.name, 'url': self.get_absolute_url()},)

		if self.category_id:
			self.category = [
				category for category in categories if category.id == self.category_id][0]
			return self.category.get_breadcrumbs() + breadcrumbs

		return breadcrumbs

	@classmethod
	def get_detail(cls, book_id):
		return cls.objects.prefetch_related('pics', 'book_publisher').get(id=book_id)

	@classmethod
	def get_active(cls):
		return cls.objects.prefetch_related('pics').filter(is_active=True)

	@classmethod
	def get_search(cls, q):
		return cls.get_active().filter(Q(name__icontains=q) |
                                       Q(category__name__icontains=q) |
                                       Q(book_publisher__name__icontains=q) |
                                       Q(gist__icontains=q) |
                                       Q(tags__icontains=q))

	@classmethod
	def featured_books(cls):
		return list(cls.get_active().filter(is_featured=True))

	@classmethod
	def recent_books(cls, max_books):
		return list(cls.get_active().filter(is_active=True).order_by('-id')[:max_books])

	@classmethod
	def category_books(cls, category):
		sub_categories_ids = [
            sub_category.id for sub_category in category.get_all_sub_categories()]
		sub_categories_ids.append(category.id)
		return cls.get_active().filter(category_id__in=sub_categories_ids)

	@classmethod
	def publisher_books(cls, publisher):
		return cls.get_active().filter(book_publisher=publisher)

	@classmethod
	def search_books(cls, q):
		return cls.get_search(q)

	@classmethod
	def search_advance_books(cls, keyword, category, publisher, price_from, price_to, categories):
		query = cls.get_search(keyword)

		if category:
			category = next(category2 for category2 in categories if category2.id == category.id)
			sub_categories_ids = [category.id]
			sub_categories_ids += (sub_category.id for sub_category in category.get_all_sub_categories())

			query = query.filter(category_id__in=sub_categories_ids)

		if publisher:
			query = query.filter(book_publisher=publisher)
		if price_from:
			query = query.filter(price__gte=price_from)
		if price_to:
			query = query.filter(price__lte=price_to)

		return query

	def get_authors(self):
		link = ''
		if self.authors.count() > 1:
			for author in self.authors.all():
				link = link + '<span><a href="' + author.get_absolute_url() + '">' + author.name + '</a></span>'
		else:
			for author in self.authors.all():
				link = link + '<span><a href="' + author.get_absolute_url() + '">' + author.name + '</a></span>'
		if not link:
			link = u'<span>%s</span>' % self.author_name
		return link


class BookPic(models.Model):
	book = models.ForeignKey(Book, related_name='pics')
	url = models.ImageField(upload_to="images/catalog/books")
	display_order = models.IntegerField(default=0)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.CharField(max_length=100)

	class Meta:
		db_table = 'catalog_book_pic'
		ordering = ('display_order', 'id')
		verbose_name_plural = 'Book Pics'

	def __unicode__(self):
		return '%s [Pic #id %s]' % (self.book, self.id)