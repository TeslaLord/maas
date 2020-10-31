from django import forms


class SentimentForm(forms.Form):
    sentiment_text = forms.CharField(label='Enter the text', max_length=100)


class CategoryForm(forms.Form):
    category_text = forms.CharField(label='Enter the text', max_length=100)


class SpeechForm(forms.Form):
    speech_text = forms.CharField(label='Enter the text', max_length=100)


class TextForm(forms.Form):
    audio_file = forms.FileField()


class ImageForm(forms.Form):
    image_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    CHOICES = [('original', 'Original'),
               ('bw', 'Black and white')]

    type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
