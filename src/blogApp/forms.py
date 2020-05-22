from django import forms
from ckeditor.fields import RichTextField
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):

    title = forms.CharField(label='title',
                            widget=forms.TextInput(attrs={'placeholder': 'Article title'}))
    class Meta:
        model = Post
        fields = ('title',
                  'image_on_view',
                  'text',
                  'category',
                  'tags'
                  )
        exclude = ["author"]


# Sign Up Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already in use.')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
            ]
