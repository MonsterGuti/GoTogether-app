from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(5, 0, -1)],
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        label="Оценка"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control rounded-3',
            'rows': 4,
            'placeholder': 'Споделете впечатленията си от пътуването и шофьора...'
        }),
        required=False,
        label="Коментар"
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']