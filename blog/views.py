from django.shortcuts import redirect
from django.urls import reverse

def redirect_to_posts(request):
    return redirect('posts_list_url', permanent=True)