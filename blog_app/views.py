from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DetailView,
								CreateView, UpdateView, DeleteView)
from blog_app.forms import PostForm, CommentForm
from blog_app.models import PostModel, CommentModel

# Create your views here.
class AboutView(TemplateView):
	template_name = 'about.html'


class PostListView(ListView):
	model = PostModel

	def get_queryset(self):
		return PostModel.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')


class PostDetailView(DetailView):
	model = PostModel


class PostCreateView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	redirect_field_name = 'blog_app/postmodel_detail.html'
	form_class = PostForm
	model = PostModel


class PostUpdateView(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	redirect_field_name = 'blog_app/postmodel_detail.html'
	form_class = PostForm
	model = PostModel


class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = PostModel
	success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
	model = PostModel
	login_url = '/login/'
	redirect_field_name = 'blog_app/postmodel_list.html'

	def get_queryset(self):
		return PostModel.objects.filter(publish_date__isnull=True).order_by('-create_date')

@login_required
def add_comment_to_post(request, pk):
	post = get_object_or_404(PostModel, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog_app/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(CommentModel, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(CommentModel, pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('post_detail', pk=post_pk)

@login_required
def post_publish(request, pk):
	post = get_object_or_404(PostModel, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

