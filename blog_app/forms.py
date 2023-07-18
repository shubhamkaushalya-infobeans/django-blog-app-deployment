from django import forms
from .models import Blog, Comment

class AddBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('author','title','text')

        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Post Title'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea form-control','placeholder':'Enter Post Description'}),
        }

class AddComment(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'author': forms.TextInput(attrs = {'class': 'form-control' ,'placeholder':'Author Name'}),
            'text': forms.Textarea(attrs = {'class': 'form-control mb-3','placeholder':'Enter comment'}),
        }