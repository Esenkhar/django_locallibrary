from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
import datetime

from .models import Author, Book, BookInstance, Genre
from .forms import RenewBookForm, RenewBookModelForm, MyForm


# Create your views here.
class MainPage(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = Book.objects.all().count()
        context['num_instances'] = BookInstance.objects.all().count()
        context['num_instances_available'] = BookInstance.objects.filter(status__exact='a').count()
        context['num_authors'] = Author.objects.all().count()
        context['num_genres'] = Genre.objects.all().count()
        context['num_books_with_dun'] = Book.objects.filter(title__icontains="дюн").count()
        num_visits = self.request.session.get('num_visits', 0)
        context['num_visits'] = num_visits
        self.request.session['num_visits'] = num_visits + 1
        return context


# def index(request):
#     num_books = Book.objects.all().count()
#     num_instances = BookInstance.objects.all().count()
#     num_instances_available = BookInstance.objects.filter(status__exact='a').count()
#     num_authors = Author.objects.all().count()
#     num_genres = Genre.objects.all().count()
#     num_books_with_dun = Book.objects.filter(title__icontains="дюн").count()
#     num_visits=request.session.get('num_visits', 0)
#     request.session['num_visits']=num_visits+1
#     return render(
#         request,
#         'index.html',
#         context={'num_books': num_books, 'num_instances': num_instances,
#                  'num_instances_available': num_instances_available, 'num_authors': num_authors,
#                  'num_genres': num_genres, 'num_books_with_dun': num_books_with_dun, 'num_visits': num_visits}
#     )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    context_object_name = 'book_list'
    template_name = 'book_list.html'
    # queryset = Book.objects.all()

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5
    template_name = 'author_list.html'
    context_object_name = 'author_list'
    # queryset = Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class LoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    # model = BookInstance
    template_name = 'bookinstance_list_borrowed.html'
    paginate_by = 5
    permission_required = 'catalog.staff_member_required'
    queryset = BookInstance.objects.filter(status__exact='o').order_by('due_back')


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    # model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').filter(borrower=self.request.user).order_by('due_back')


# @permission_required('catalog.can_mark_returned')
# def renew_book_librarian(request, pk):
#     book_inst = get_object_or_404(BookInstance, pk=pk)
#     if request.method == 'POST':
#         form = RenewBookModelForm(request.POST)
#         if form.is_valid():
#             book_inst.due_back = form.cleaned_data['due_back']
#             book_inst.save()
#             return HttpResponseRedirect(reverse('all-borrowed'))
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
#     return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class RenewBookLibrarian(PermissionRequiredMixin, UpdateView):
    form_class = RenewBookModelForm
    model = BookInstance
    initial = {'due_back': datetime.date.today() + datetime.timedelta(weeks=3)}
    template_name = 'book_renew_librarian.html'
    permission_required = 'catalog.can_mark_returned'
    # redirect_field_name = reverse_lazy('all-borrowed')
    # success_url = reverse_lazy('all-borrowed')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not 'catalog.can_mark_returned' in request.user.get_all_permissions():
                return HttpResponseRedirect(reverse('index'))
        return super(RenewBookLibrarian, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('all-borrowed'))

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         if not request.user.user_permissions in permission_required:
    #             return HttpResponseRedirect(reverse('login'))
    #     super(RenewBookLibrarian, self).dispatch(request, *args, **kwargs)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    template_name = 'author_form.html'
    permission_required = 'catalog.staff_member_required'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'author_form.html'
    permission_required = 'catalog.staff_member_required'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'author_confirm_delete.html'
    permission_required = 'catalog.staff_member_required'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'
    permission_required = 'catalog.staff_member_required'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    template_name = 'book_form.html'
    permission_required = 'catalog.staff_member_required'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'book_confirm_delete.html'
    permission_required = 'catalog.staff_member_required'


class MyFormView(FormView):
    form_class = MyForm
    template_name = 'my_form.html'
    success_url = reverse_lazy('index')
    initial = {'field1': 'Поле 1', 'field2': 'Поле 2'}
