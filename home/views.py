from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUpdatePostForm, CreateCommentForm, ReplayCommentForm, SearchPostForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class Home(View):
    def get(self, request):
        posts = Post.objects.all()
        form = SearchPostForm
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': form})


class PostDetail(View):
    form_class = CreateCommentForm
    reply_form = ReplayCommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['word'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = self.post_instance.pcomment.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'home/detail.html', {'post': self.post_instance, 'comments': comment,
                                                    'form': self.form_class,  'reply_form': self.reply_form,
                                                    'can_like': can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post =self.post_instance
            new_comment.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDelete(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success('پست شما با موفقیت حذف شد', 'success')
        else:
            messages.error('شما به این بخش دسترسی ندارید', 'danger')
        return redirect('home:home')


class PostUpdate(LoginRequiredMixin, View):
    form_class = CreateUpdatePostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'شما اجازه دسترسی به این قسمت را ندارید', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post =self.post_instance
        form =self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30], allow_unicode=True)
            new_post.save()
            messages.success(request, 'پست شما با موفقیت به روز رسانی شد', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreate(LoginRequiredMixin, View):
    form_class = CreateUpdatePostForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30], allow_unicode=True)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'پست شما با موفقیت ایجاد شد', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class ReplyComment(LoginRequiredMixin, View):
    form_class = ReplayCommentForm

    def post(self, request, post_id, comment_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=post_id)
        reply = get_object_or_404(Comment, id=comment_id)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = reply
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'پاسخ شما با موفقیت ثبت شد', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class PostLike(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.warning(request, 'این پست قبلا لایک شد', 'danger')
        else:
            Vote.objects.create(user=request.user, post=post)
            messages.success(request, 'این پست لایک شد', 'success')
        return redirect('home:post_detail', post.id, post.slug)