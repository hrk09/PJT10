from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    # aritcle = forms.ModelChoiceField(
    #     queryset=Article.objects.all(),
    # )

    content = forms.CharField(
        label='리뷰',
    )

    class Meta:
        model = Review
        fields = ['content', 'score']
