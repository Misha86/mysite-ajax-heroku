from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from comment.forms import CommentForm
from blog.models import Article
from loginsys.models import Profile
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.translation import gettext as _
import time


def comment_create(request, id=None):
    data = dict()
    article = Article.objects.get(id=id)
    form = CommentForm()
    now = time.time()

    if request.session.get('pause', False) and request.session.get('start_time', False) > now:
        messages.error(request, _('Ви вже залишили коментар, зачекайте хвилину.'), extra_tags='error')

    else:
        if request.is_ajax() and request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid() and request.user.is_authenticated():
                comment = form.save(commit=False)
                comment.comments_article = article
                comment.comments_user = Profile.objects.get(pk=request.user.pk)                            # АБО comment.comments_from = auth.get_user(request)  АБО comment.comments_from_id = auth.get_user(request).id
                comment.save()

                form = CommentForm()

                messages.success(request, _('Коментар добавлений успішно!'), extra_tags='success')

                request.session['pause'] = True
                request.session['start_time'] = time.time() + 20

                comments = article.comments.all().order_by('-comments_create')
                current_page = Paginator(comments, 4)
                page_number = request.GET.get('page', 1)
                data['html_comments'] = render_to_string('partial_comments_list.html',
                                                         {"comments": current_page.page(page_number)},
                                                         request=request)

                data['form_is_valid'] = True

            else:
                data['form_is_valid'] = False

    message = messages.get_messages(request)
    if message:
        data['html_messages'] = render_to_string('messages.html',
                                                 {'messages': message},
                                                 request=request)

    context = {'form': form,
               'article': article}
    data['html_form'] = render_to_string('partial_comment_form.html',
                                         context,
                                         request=request)
    return JsonResponse(data)
