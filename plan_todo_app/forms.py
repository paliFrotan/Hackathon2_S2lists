from django import forms
from .models import Todo


class TodoCreateForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta: 
        model = Todo
        fields = ["title", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Clean room"}),
        }


class TodoUpdateForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Todo
        fields = ["title", "due_date", "is_done"]