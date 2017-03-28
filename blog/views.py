from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from blog.models import Article
from navigation.models import Category, MenuItem
from blog.form import SendMassageForm, ArticleForm
from comment.forms import CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from loginsys.models import Profile
from django.contrib import messages
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
import logging
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import JsonResponse


def bootstrap_query(array, num):
    new_list = []
    length = int(len(array)//num)
    rest = len(array) % num
    b = 0
    for i in range(length):
        new_list.append(array[b:b+num])
        b += num
    if rest:
        new_list.append(array[len(array)-rest:])
    return new_list

# @cache_control(must_revalidate=True, max_age=3600)
# @vary_on_headers("User-Agent", "Cookie", "Accept-language")
# def start_page(request):
#     form = SendMassageForm()
#     users = Profile.objects.exclude(pk=request.user.pk).order_by('-user__date_joined')
#     current_page = Paginator(users, 6)
#     page_number = request.GET.get('page', 1)
#     # if request.user:
#     #     logger = logging.getLogger(__name__)
#     #     logger.error('\nSomething went wrong!\n')
#     users_list = current_page.page(page_number)
#     if request.POST and 'pause' not in request.session:
#         form = SendMassageForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             massage = form.cleaned_data['massage']
#             from_email = settings.EMAIL_HOST_USER
#             to_email = [settings.EMAIL_HOST_USER, 'mishaelitzem1@rambler.ru']
#             send_mail(email, massage, from_email, to_email, fail_silently=False)
#             request.session.set_expiry(60)
#             request.session['pause'] = True
#             return redirect('/')
#     context = {
#         'form': form,
#         'users': users_list,
#         }
#     return render(request, 'content_start_page.html', context)


def start_page(request):
    form = SendMassageForm()
    users = Profile.objects.exclude(pk=request.user.pk).order_by('-user__date_joined')
    current_page = Paginator(users, 6)
    page_number = request.GET.get('page', 1)
    users_list = current_page.page(page_number)

    request.session['color'] = 'blue'

    context = {
        'form': form,
        'users': users_list,
        }
    return render(request, 'content_start_page.html', context)


def send_mail_ajax(request):
    data = dict()
    form = SendMassageForm()
    import time
    now = time.time()

    if request.session.get('send', False) and request.session.get('start_time', False) > now:
        messages.error(request, _('Ви вже відправили повідомлення, зачекайте хвилину.'), extra_tags='error')

    else:
        if request.is_ajax() and request.POST:
            form = SendMassageForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                massage = form.cleaned_data['massage']
                from_email = settings.EMAIL_HOST_USER
                to_email = [settings.EMAIL_HOST_USER, 'mishaelitzem2@rambler.ru']
                send_mail(email, massage, from_email, to_email, fail_silently=False)

                form = SendMassageForm()

                messages.success(request, _('Повідомлення відправлено успішно!'), extra_tags='success')

                request.session['send'] = True
                request.session['start_time'] = time.time() + 20

    message = messages.get_messages(request)
    if message:
        data['html_messages'] = render_to_string('messages.html',
                                                 {'messages': message},
                                                 request=request)

    context = {'form': form}
    data['html_form'] = render_to_string('partial_mail_form.html',
                                         context,
                                         request=request)
    return JsonResponse(data)

def article_list_ajax(request, item_slug, category_slug):
    category = get_object_or_404(Category,  menu_category__menu_name=item_slug, category_name=category_slug)
    article = Article.objects.filter(article_category__category_name=category_slug,
                                     article_category__menu_category__menu_name=item_slug).order_by('-article_date')

    context = dict()
    article_with_image = article.exclude(article_image__exact='')
    if article_with_image.exists():
        articles_carousel = article_with_image.order_by('-article_likes')[0:3]
        context['articles_carousel'] = articles_carousel

    data = dict()
    query = request.GET.get('q')
    if query:
        article = article.filter(
            Q(article_title__icontains=query) |
            Q(article_text__icontains=query)).distinct()

        data['json_query'] = list(article.values_list('article_title', flat=True))

    # suite all articles adding class = "row"
    articles_list = bootstrap_query(article, 3)
    paginator = Paginator(articles_list, 2)
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
        # print(articles.page_range)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    context.update({
        'articles': articles,
        'paginator': paginator,
        'category': category
    })

    if request.is_ajax():
        # articles_json = list(Article.objects.values_list('article_title', flat=True))
        # data['json_query'] = list(article.values_list('article_title', flat=True))
        data['html_articles'] = render_to_string('partial_articles_list.html',
                                                 {'articles': articles,
                                                  },
                                                 request=request)

        data['html_page'] = render_to_string('partial_articles_pages.html',
                                             {'articles': articles,
                                              'paginator': paginator},
                                             request=request)
        return JsonResponse(data)

    return render(request, 'gallery_works.html', context)


# # @cache_page(60 * 15, key_prefix='articles')
# def article_list(request, item_slug, category_slug):
#     category = get_object_or_404(Category,  menu_category__menu_name=item_slug, category_name=category_slug)
#     article = Article.objects.filter(article_category__category_name=category_slug,
#                                      article_category__menu_category__menu_name=item_slug).order_by('-article_date')
#     # suite all articles adding class = "row"
#     articles_list = bootstrap_query(article, 3)
#     articles_carousel = article.order_by('-article_likes')[0:3]
#     query = request.GET.get('q')
#     if query:
#         articles_list = Article.objects.filter(
#             Q(article_title__icontains=query) |
#             Q(article_text__icontains=query)).distinct()
#     paginator = Paginator(articles_list, 3)
#     page = request.GET.get('page')
#     try:
#         # it`s for pagination in bootstrap part 1
#         page_before = int(page) - 3
#         page_after = int(page) + 3
#         list_pagination = []
#         for p in paginator.page_range:
#             if p == page or p == paginator.page_range[0] or p == paginator.page_range[-1]:
#                 list_pagination.append(p)
#             elif p < page_before or p > page_after:
#                 if page_before == paginator.page_range[0]:
#                     page_before += 1
#                 elif page_after == paginator.page_range[-1]:
#                     page_after += 1
#                 else:
#                     continue
#             else:
#                 list_pagination.append(p)
#         #
#         articles = paginator.page(page)
#     except PageNotAnInteger:
#         article = paginator.page(1)
#     except EmptyPage:
#         articles = paginator.page(paginator.num_pages)
#
#     # it`s for pagination in bootstrap: catch except TypeError part 2
#     except TypeError:
#         list_pagination = []
#         for s in paginator.page_range:
#             if s in paginator.page_range[:8] or s in paginator.page_range[-1:]:
#                 list_pagination.append(s)
#                 page_after = 8
#             else:
#                 continue
#         articles = paginator.page(1)
#     return render(request, 'gallery_works.html', locals())


def articles_list_update(request, item_slug, category_slug=None):
    if not request.user.is_superuser:
        raise Http404
    ArticleFormSet = inlineformset_factory(Category, Article, form=ArticleForm, extra=1, can_delete=True)
    category = get_object_or_404(Category, menu_category__menu_name=item_slug, category_name=category_slug)
    if request.POST:
        forms = ArticleFormSet(request.POST, request.FILES, instance=category)
        if forms.is_valid():
            instances = forms.save(commit=False)
            for form in forms.deleted_objects:
                form.delete()
            for instance in instances:
                instance.article_user = get_object_or_404(Profile, user=request.user)
                instance.article_category = get_object_or_404(Category,  menu_category__menu_name=item_slug,
                                                              category_name=category_slug)
                instance.save()
            forms.save_m2m()
            messages.success(request, _("Список категорії \'") + category.category_title + _("\' змінений успішно!"),
                             extra_tags='success')
            return HttpResponseRedirect(category.get_absolute_url())               # you can use return redirect(instance)
    else:
        forms = ArticleFormSet(instance=category)

    title = _('Форма для зміни списку статей')
    button_create = _('змінити список')
    button_cancel = _('відміна')
    return_path = category.get_absolute_url()
    context = {
        'title': title,
        'button_create': button_create,
        'button_cancel': button_cancel,
        'forms': forms,
        'return_path': return_path,
        }
    return render(request, 'articles_list_update.html', context)


def article_detail_ajax(request, item_slug, category_slug, article_slug):
    category = get_object_or_404(Category, menu_category__menu_name=item_slug, category_name=category_slug)
    article = category.articles.get(article_slug=article_slug)
    comments = article.comments.all().order_by('-comments_create')
    current_page = Paginator(comments, 4)
    page_number = request.GET.get('page', 1)
    form = CommentForm(auto_id='id_for_%s', label_suffix=' -> -> -> ->')

    context = {
        'comments': current_page.page(page_number),
        'article': article,
        'form': form,
        }
    return render(request, 'gallery_work.html', context)


# def article_detail(request, item_slug, category_slug, article_slug):
#     category = get_object_or_404(Category, menu_category__menu_name=item_slug, category_name=category_slug)
#     article = category.articles.get(article_slug=article_slug)
#     comments = article.comments.all().order_by('-comments_create')
#     current_page = Paginator(comments, 4)
#     page_number = request.GET.get('page', 1)
#     form = CommentForm(auto_id='id_for_%s', label_suffix=' -> -> -> ->')
#
#     # if not request.user.is_authenticated():
#     #     return redirect('/auth/login/?next=%s' % request.path)
#
#     if request.POST and 'pause' in request.session:
#         messages.error(request, _('Ви вже залишили коментар, зачекайте хвилину.'), extra_tags='error')
#     elif request.POST and 'pause' not in request.session:
#         form = CommentForm(request.POST)
#         if form.is_valid() and request.user.is_authenticated():
#             comment = form.save(commit=False)
#             comment.comments_article = Article.objects.get(article_slug=article_slug)
#             comment.comments_user = Profile.objects.get(pk=request.user.pk)                            # АБО comment.comments_from = auth.get_user(request)  АБО comment.comments_from_id = auth.get_user(request).id
#             comment.save()
#             request.session.set_expiry(60)
#             request.session['pause'] = True
#             messages.success(request, _('Коментар добавлений успішно!'), extra_tags='success')
#             return redirect(article.get_absolute_url())
#     context = {
#         'comments': current_page.page(page_number),
#         'article': article,
#         'form': form,
#         }
#     return render(request, 'gallery_work.html', context)
#

def article_create(request, item_slug, category_slug=None):
    if not request.user.is_superuser:
        raise Http404
    form = ArticleForm(request.POST or None, request.FILES or None)
    category = get_object_or_404(Category,  menu_category__menu_name=item_slug, category_name=category_slug)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.article_user = get_object_or_404(Profile, user=request.user)
        instance.article_category = category
        instance.save()
        messages.success(request, _("Ура, стаття сворена!"), extra_tags='success')
        return HttpResponseRedirect(instance.get_absolute_url())               # you can use return redirect(instance)
    title = _('Форма для створення статті')
    button_create = _('створити статтю')
    button_cancel = _('відміна')
    return_path = category.get_absolute_url()
    context = {
        'title': title,
        'button_create': button_create,
        'button_cancel': button_cancel,
        'form': form,
        'return_path': return_path,
        }
    return render(request, 'article_form.html', context)


def article_update(request, item_slug, category_slug, article_slug):
    if not request.user.is_staff or not request.user.is_superuser:
        # response = HttpResponse('<h1>Ти не маєш прав для оновлення статті!!!</h1')
        # response.status_code = 403
        # return response
        raise Http404
    title = _('Форма оновлення статті')
    button_create = _('змінити статтю')
    button_cancel = _('відміна')
    instance = get_object_or_404(Article, article_category__menu_category__menu_name=item_slug,
                                 article_category__category_name=category_slug, article_slug=article_slug)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, _("Ура, стаття оновлена!"), extra_tags='success')
        return redirect(instance)
    return_path = instance.get_absolute_url()
    context = {
        'title': title,
        'button_create': button_create,
        'button_cancel': button_cancel,
        'return_path': return_path,
        'form': form,
        'article': instance,
        }
    return render(request, 'article_form.html', context)


def article_delete(request, item_slug, category_slug, article_slug):
    title = _('Ви впевнені, що хочете видалити дану статтю?')
    button_delete = _('видалити статтю')
    button_cancel = _('відміна')
    instance = get_object_or_404(Article, article_category__menu_category__menu_name=item_slug,
                                 article_category__category_name=category_slug, article_slug=article_slug)
    return_path = instance.get_absolute_url()
    context = {
        'title': title,
        'button_delete': button_delete,
        'button_cancel': button_cancel,
        'return_path': return_path,
        }
    if request.POST:
        instance.delete()
        messages.error(request, _('Стаття \'') + instance.article_title + _('\' видалена!'), extra_tags='success')
        return redirect(instance.article_category.get_absolute_url())
    return render(request, 'article_delete_form.html', context)


# @login_required(redirect_field_name='my_redirect_field')
def add_like(request, id=None):
    # article = get_object_or_404(Article, id=id)
    article = Article.objects.filter(id=id)
    try:
        if id in request.COOKIES:
            return_path = request.META.get('HTTP_REFERER', '/')
            # messages.error(request, _("Ви вже оцінили картинку \'") + article.article_title + "\' !", extra_tags='error')
            messages.error(request, _("Ви вже оцінили картинку \'") + article[0].article_title + "\' !", extra_tags='error')
            return redirect(return_path)
        else:
            # article.article_likes += 1
            # article.save() or
            article.update(article_likes=F('article_likes') + 1)
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(id, 'test')
            # messages.error(request, _("Дякую за Вашу оцінку картинки \'") + article.article_title + "\' !",
            messages.error(request, _("Дякую за Вашу оцінку картинки \'") + article[0].article_title + "\' !",
                           extra_tags='success')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


import requests
import urllib.request
from bs4 import BeautifulSoup

url = 'https://vk.com/album90386736_237729907'


def make_soup(url):
    url_requests = b''
    try:
        url_requests += requests.get(url).content
    except Exception as e:
        print("Somethings bad: " + str(e))
        try:
            url_requests = urllib.request.urlopen(url)
        except Exception as e:
            print("Somethings bad: " + str(e))
    soup_data = BeautifulSoup(url_requests, "html.parser")   #.prettify()
    return soup_data


# def photo(request, item_slug):
#     my_data = ['aefasdf', ['sdfsdffsdfsfd']]
#     response = HttpResponse(my_data, content_type='application/vnd.ms-excel', status=200)
#     response['Content-Disposition'] = 'attachment; filename="foo.xls"'
#     return response

def photo(request, item_slug):
    menu_item = get_object_or_404(MenuItem,  menu_name=item_slug)
    photo_list = Article.objects.filter(article_category__menu_category__menu_name=item_slug).order_by('-article_date')
    soup = make_soup(url)
    vk_links = []
    links = soup.find_all('img', attrs={'class': 'ph_img'})
    for link in links:
        link_a = link.get('data-src_big')[:-8]
        vk_links.append(link_a)
    context = {
        'vk_links': vk_links
    }
    return render(request, 'photo_list.html', context)



def django_python(request):
    pass


def html_5(request):
    pass


def css_3(request):
    pass


def bootstrap(request):
    pass
