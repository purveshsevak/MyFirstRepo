from django.conf.urls import url
from django.urls import path
from catalog import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
)

app_name = 'catalog'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'catalog/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'catalog/logout.html'}, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)/$', views.book_detail_view, name='book-detail'),
    url(r'^authors/$', views.author_list_view, name='authors'),
    url(r'^author/(?P<pk>\d+)/$', views.author_detail_view, name='author-detail'),
    url('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/$', views.renew_book_librarian, name='renew_book_librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

    url(r'^reset-password/$', password_reset, {'template_name': 'catalog/reset_password.html',
        'post_reset_redirect': 'catalog:password_reset_done',
        'email_template_name': 'accounts/reset_password_email.html'},
        name='password_reset'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'catalog/reset_password_done.html'},
        name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {'template_name': 'catalog/reset_password_confirm.html',
        'post_reset_redirect': 'catalog:password_reset_complete'},
        name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,
        {'template_name': 'catalog/reset_password_complete.html'},
        name='password_reset_complete'),
]
