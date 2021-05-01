from django import forms
from blog_app.models import PostModel, CommentModel

class PostForm(forms.ModelForm):

	class Meta:
		model = PostModel
		fields = ('author', 'title', 'text')

	widgets = {
		'title': forms.TextInput(attrs={'class': 'textinputclass', }),
		'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
	}


class CommentForm(forms.ModelForm):

	class Meta:
		model = CommentModel
		fields = ('author', 'text')

	widgets = {
		'author': forms.TextInput(attrs={'class': 'textinputclass'}),
		'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}), 
	}
