from django import forms
from ckeditor.widgets import CKEditorWidget
from api.models import Blog
class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Blog
        fields = '__all__'
