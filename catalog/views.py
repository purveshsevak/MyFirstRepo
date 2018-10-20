from django.shortcuts import render, get_object_or_404
from catalog.models import Book, BookInstance, Author, Language, Genre
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm


'''class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'''


#@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_maintenance = BookInstance.objects.filter(status__exact='m').count()
    num_instances_on_loan = BookInstance.objects.filter(status__exact='o').count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_instances_reserved = BookInstance.objects.filter(status__exact='r').count()

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    return render(request, 'catalog/index.html', context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 2

    '''def get(self, request):
        books = Book.objects.all()
        context = {'books': books}
        return render(request, 'catalog/book_list.html', context)'''


'''def book_list_view(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'catalog/book_list.html', context)'''


#@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book}
    return render(request, 'catalog/book_detail.html', context)


#@login_required
def author_list_view(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'catalog/author_list.html', context)


#@login_required
def author_detail_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {'author': author}
    return render(request, 'catalog/author_detail.html', context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    bookinstance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        book_renewal_form = RenewBookForm(request.POST)

        if book_renewal_form.is_valid():
            bookinstance.due_back = book_renewal_form.cleaned_data['renewal_date']
            bookinstance.save()

            return HttpResponseRedirect(reverse('catalog:all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html',
                  {'form': book_renewal_form, 'bookinstance': bookinstance})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('catalog:authors')


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth']
    success_url = reverse_lazy('catalog:authors')


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')
