from django import forms
from django.core.exceptions import ValidationError

from .models import *

class TagForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # slug = forms.CharField(max_length=50)

    # # for specific properties changing attributes of rendering form input
    # title.widget.attrs.update({'class': 'form-control'})
    # slug.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tag
        # which properties of model we need
        fields = ['title', 'slug']
        # overriding property widget methods
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError("Slug cannot be 'create'")
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('This slug already exists')
        return new_slug

    # DON'T NEED THIS METHOD IF WE INHERIT FROM MODELFORM
    # def save(self):
    #     # cleaned data is validated and checked data
    #     new_tag = Tag.objects.create(title=self.cleaned_data['title'], slug=self.cleaned_data['slug'])
    #     return new_tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError("Slug cannot be 'create'")
        if Post.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('This slug already exists')
        return new_slug