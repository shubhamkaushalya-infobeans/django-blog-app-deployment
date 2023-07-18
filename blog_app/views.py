from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect,get_object_or_404, HttpResponse,HttpResponseRedirect
from .forms import AddBlog, AddComment, SignupUser
from .models import Blog, Comment
from django.views.generic import (TemplateView, CreateView, ListView, DeleteView, UpdateView, DetailView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

class IndexPage(TemplateView):
    template_name = 'home.html'


class CreateBlog(LoginRequiredMixin,CreateView):

    login_url = 'blog_app_name:login'
    redirect_field_name = 'blog/post_detail.html'
    model = Blog
    form_class = AddBlog
    template_name = 'add_blog.html'
    success_message = 'Blog added successfully'

class BlogList(ListView):
    context_object_name = 'blog_data'
    model = Blog
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        return Blog.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class BlogDetails(DetailView):
     model = Blog
     template_name = 'blog_details.html'

     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
         context = super().get_context_data(**kwargs)
         context['blog_data']   = Blog.objects.get(id__exact=self.get_object().pk)
         context['latest_blogs'] = Blog.objects.filter(published_date__isnull = False).order_by('-published_date')[0:5]
         context['comments'] = Comment.objects.filter(post_id__exact=self.get_object().pk, approve_commet = True)
         if(self.request.user.is_superuser):
              context['approval_pending_comments'] = Comment.objects.filter(post_id__exact=self.get_object().pk, approve_commet = False)
         else:
              context['approval_pending_comments'] = Comment.objects.filter(post_id__exact=self.get_object().pk, approve_commet = False, created_by=self.request.user.id)

         context['comment_form'] = AddComment()
         return context

    
class DraftBlogList(ListView):
     model = Blog
     context_object_name = 'blog_data'
     template_name = 'blog_draft_list.html'
     paginate_by = 5

     def get_queryset(self) -> QuerySet[Any]:
        return Blog.objects.filter(published_date__isnull = True)
     
@login_required
def blog_publish(request,pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.publish_blog()
    return redirect('/blog_app/blog-list')

@login_required
def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
           comment = form.save(commit=False)
           comment.post = blog
           comment.created_by = request.user
           comment.save()
           return HttpResponseRedirect(reverse('blog_app_name:blog-details', args=[pk]))
        else:
            return HttpResponseRedirect(reverse('blog_app_name:blog-details', args=[pk]))
    else:
        return HttpResponse('Not allowed')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = authenticate(username=username, password=password)
        # print(password)
        if user_obj:
            if user_obj.is_active:
                 user_login = login(request,user_obj)
                 return redirect('/blog_app/blog-list')
        else:
            messages.error(request, "Please enter correct username and password.")
            return redirect('blog_app_name:login')
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def approve_comment(request):
    if is_ajax(request=request):
        comment_id = request.POST['id']
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.approve_comments()
        return JsonResponse({'success':'true'},safe=False)
    
@login_required
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def remove_comment(request, pk):
    comment_details = get_object_or_404(Comment, pk=pk)
    associated_post = comment_details.post.id
    comment_details.delete()
    return redirect('blog_app_name:blog-details',pk=associated_post)

class SignupUser(CreateView,SuccessMessageMixin):
    model = User
    form_class = SignupUser
    template_name = 'blog_app/signup.html'
    success_message = 'Thank you for registering'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_url(self):
          return reverse('blog_app_name:signup-user')
    
    # def get_success_message(self, cleaned_data):
    #     return "%(id)s was created successfully" % {'id': self.object.id}
    
    # def form_valid(self, form):
    #   messages.success(self.request, "This is my success message")
    #   super().form_valid(form)
    #   return HttpResponseRedirect(self.get_success_url())
    
    # signup_form = SignupUser()
    # if request.method == 'POST':
    #     form = SignupUser(request.POST)
    #     if  form.is_valid():
    #         return HttpResponse('ok')
    #     else:
    #         err = form.errors
    #         return reverse('blog_app_name:signup-user',{'err':err})
    # return  render(request,'blog_app/signup.html',{'signup_form':signup_form })