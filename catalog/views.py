from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from config.views import BaseView
from catalog.forms import AdvancedSearchForm
from catalog.models import Publisher, Category, Book
from financial.models import Currency




class CatalogBaseView(BaseView):
    style_name = 'catalog'
    catalog_template_name = 'catalog_base.html'

    def __init__(self, *args, **kwargs):
        super(CatalogBaseView, self).__init__(*args, **kwargs)

        self.categories = Category.get_categories()
        self.publishers = Publisher.get_publishers()
        self.currencies = Currency.get_currencies()
        self.primary_currency = next((currency for currency in self.currencies if currency.is_primary), None)

        if self.primary_currency is None:
          raise ImproperlyConfigured('No primary currency is defined for ideapub.'
                                       ' You should defined primary currency for the system with exchange rate of 1.'
                                       ' All prices & costs should be defined in primary currency value.')

        if self.primary_currency.exchange_rate != 1:
          raise ImproperlyConfigured('Primary currency should have exchange rate of 1.'
                                       ' All prices & costs should be defined in primary currency value.')


    def get_context_data(self, **kwargs):

        context = super(CatalogBaseView, self).get_context_data(**kwargs)

        breadcrumbs = ({'name': 'Home', 'url': reverse('catalog_index')},)
        if 'breadcrumbs' in context:
            breadcrumbs += context['breadcrumbs']

        default_currency = self.request.session.get('default_currency', self.primary_currency.code)



        default_currency = next(
            (currency for currency in self.currencies if currency.code == default_currency), self.primary_currency)

        context['breadcrumbs'] = breadcrumbs
        context['categories'] = (category for category in self.categories if category.parent is None)
        context['publishers'] = self.publishers
        context['currencies'] = self.currencies
        context['primary_currency'] = self.primary_currency
        context['default_currency'] = default_currency
        context['catalog_template_name'] = self.catalog_template_name

        return context

    @classmethod
    def get_page_size(cls):
        """
        Returns page size for products listing
        """
        return int(cls.get_config('PAGE_SIZE'))




class IndexView(CatalogBaseView):
    """
    Displays list of featured and recently added books
    """
    template_name = 'catalog_index.html'

    def get(self, request):
        featured_books = Book.featured_books()
        recent_books = Book.recent_books(self.get_max_recent_arrivals())

        return super(IndexView, self).get(request,
                                          featured_books=featured_books,
                                          recent_books=recent_books)

    @classmethod
    def get_max_recent_arrivals(cls):
        return int(cls.get_config('MAX_RECENT_ARRIVALS'))


class CategoryBooksView(CatalogBaseView):
    """
    Displays books list from the Category
    """
    template_name = 'category_books.html'

    def get(self, request, slug, page_num):
        category = next((category for category in self.categories if category.slug == slug), None)

        if category is None:
            raise Http404()

        breadcrumbs = category.get_breadcrumbs()
        books = paginate(Book.category_books(category), self.get_page_size(),
                            page_num, 'catalog_category', [slug])

        return super(CategoryBooksView, self).get(request,
                                                     category=category,
                                                     books=books,
                                                     breadcrumbs=breadcrumbs,
                                                     page_title=category.name)


class PublishersBooksView(CatalogBaseView):

	template_name = 'publisher_books.html'

	def get(self, request, slug, page_num):
		publisher = next(
				(publisher for publisher in self.publishers if publisher.slug == slug), None)

		if publisher is None:
			raise Http404()

		breadcrumbs = publisher.get_breadcrumbs()
		books = paginate(Book.publisher_books(publisher), self.get_page_size(),
                            page_num, 'catalog_publisher', [slug])

		return super(PublishersBooksView, self).get(request,
                                                         publisher=publisher,
                                                         books=books,
                                                         breadcrumbs=breadcrumbs,
                                                         page_title=publisher.name)


class SearchBooksView(CatalogBaseView):
    template_name = 'search_books.html'

    def get(self, request, page_num):
        form = AdvancedSearchForm(request.GET)
        query = '?' + request.GET.urlencode()
        books = None
        keyword = request.GET.get('keyword', None)
        page_title = 'Search: ' + keyword
        breadcrumbs = ({'name': 'Search: ' + keyword, 'url': reverse('catalog_search') + query},)

        if form.is_valid():
            data = form.cleaned_data

            books = paginate(Book.search_advance_books(
                data['keyword'], data['category'], data['publisher'],
                data['price_from'], data['price_to'], self.categories),
                self.get_page_size(), page_num, 'catalog_search', qs=query)

        return super(SearchBooksView, self).get(request,form=form,keyword=keyword,books=books,page_title=page_title,breadcrumbs=breadcrumbs)




class BookDetailView(CatalogBaseView):
	template_name = 'book_detail.html'

	def get(self, request, book_id, slug):
		try:
			book = Book.get_detail(int(book_id))
		except Book.DoesNotExist:
			raise Http404()

		return super(BookDetailView, self).get(request,
                                                  book=book,
                                                  breadcrumbs=book.get_breadcrumbs(
                                                      self.categories),
                                                  page_title=book.name)


class ChangeCurrencyView(View):

  def post(self, request):
		next_url = request.POST['next'] or reverse('catalog_index')
		default_currency = request.POST['default_currency']
		request.session['default_currency'] = default_currency

		return HttpResponseRedirect(next_url)




def get_default_currency(request):
  if 'default_currency' in request.session:
        try:
            return Currency.objects.get(code=request.session['default_currency'])
        except Currency.DoesNotExist:
            return Currency.get_primary()

  return Currency.get_primary()



def paginate(query_set, page_size, page_num, url_name, url_args=[], qs=None):
	paginator = Paginator(query_set, page_size)
	try:
		page = paginator.page(page_num)
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)

    # Generating paginated previous and next urls
    # if page 1 than suppressing page number in url
	if page.has_previous():
		previous_page_num = page.previous_page_number()
		if previous_page_num == 1:
			page.previous_url = reverse(url_name, args=url_args) + (qs or '')
		else:
			page.previous_url = reverse(url_name, args=(url_args + [previous_page_num])) + (qs or '')

	if page.has_next():
		next_page_num = page.next_page_number()
		page.next_url = reverse(url_name, args=(url_args + [next_page_num])) + (qs or '')

	return page
