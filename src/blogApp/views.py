from django.http import HttpResponse
from django.shortcuts import render, redirect
from blogApp.models import *
from blogApp.forms import *
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

import sys
sys.path.append("..")
from recommend_post import give_rec

error = {
'401' : "You're not authorized to browse this page!",
'form' : "Form is not valid!"
}
error_template = 'errors/error.html'

def index(request):
    context = {}

    context['recent'] = Post.objects.filter(visible = True).order_by('-published')[:12]
    return render(request, "head.html", context=context)

class createArticleView(View):
    form_class = PostForm
    template_name = 'article/create.html'

    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, error_template , {'error': error['401']}, status=401)

    def post(self, request, *args, **kwargs):
        if(request.user.is_authenticated and request.user.profile.author):
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                article = form.save(commit = False)
                article.author = User.objects.get(username = request.user)
                new_article = article.save()
                form.save_m2m()
                return redirect('article_preview', post_id = article.pk)
            else:
                return render(request, error_template , {'error': error['form']})
        else:
            return render(request, error_template , {'error': error['401']}, status=401)

def previewArticle(request, post_id): # zamienić do view?
    pk = post_id
    if(request.user.is_authenticated):
        if Post.objects.filter(id = pk).count():
            if Post.objects.get(id = pk).author == request.user:
                context = {}
                context['article'] = Post.objects.get(id = pk)
                return render(request, 'article/preview.html', context)
            else:
                return HttpResponse("You're not post owner")
        else:
            return HttpResponse("Post doesn't exist")
    else:
        return HttpResponse("You're not logged in")



class profileView(View):
    def get(self, request, user, *args, **kwargs):
        context = {}
        context['respond'] = User.objects.get(username = user)
        return render(request, 'userProfile.html', context=context)

class ArticleView(View):
    form_class = CommentForm
    template_name = 'article/view.html'

    def get(self, request, post_id, *args, **kwargs):
        context = {}
        context['article'] = Post.objects.get(id = post_id)
        context['userProf'] = User.objects.get(username = context['article'].author)
        context['otherUserPosts'] = Post.objects.filter(author = context['article'].author).exclude(id = post_id)[:5]
        context['commentsPost'] = Comment.objects.filter(article = post_id).order_by('published')
        context['form'] = self.form_class()
        result = give_rec(int(post_id))
        rec_list = []
        for i in result:
            rec_list.append(Post.objects.get(id=i))
        context['recPosts'] = rec_list
        return render(request, self.template_name, context=context)

    def post(self, request, post_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.author = User.objects.get(username = request.user)
            comment.article = Post.objects.get(id = post_id)
            comment.save()
            form.save_m2m()
            return redirect('article_view', post_id = post_id)

class CategoriesView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['categories'] = Category.objects.all()
        return render(request, 'article/category.html', context=context)

# Sign Up View from https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django###########################################
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your codeStation account.'

            message = render_to_string('registration/activate_form.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/email_sent.html')

        return render(request, self.template_name, {'form': form})



class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            auth_login(request, user)
            return render(request, 'registration/activate.html')
        else:
            return render(request, error_template , {'error': 'Your token is invalid!'})
#####################################################


def error_404(request, exception):
        return render(request,'error/error_404.html')

def error_500(request):
        data = {}
        return render(request,'error/error_500.html', data)
