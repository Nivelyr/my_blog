from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import Post, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, View
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html', {'section': 'dashboard'})
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
        instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

        
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
                                                                   cd['email'],
                                                                   post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                                                                     post_url,
                                                                     cd['name'],
                                                                     cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request, 'blog/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})

#authorization
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:dashboard')
                else:
                    form = LoginForm()
                    return render(request, 'registration/login.html', locals())
            else:
                form = LoginForm()
                return render(request, 'registration/login.html', locals())
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render_to_response('registration/logout.html')

def logout_then_login_view():
    return redirect('/login/')

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'registration/password_change_form.html',  {'form': form})
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        return render(request, 'registration/password_change_form.html',  {'form': form})

def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

def password_reset(request):
    return password_reset(request, template_name='registration/password_reset_form.html',
                          email_template_name='registration/password_reset_email.html',) 