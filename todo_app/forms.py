from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priority', 'progress']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'progress': forms.NumberInput(attrs={'min': '0', 'max': '100'}),
        }

    def clean_progress(self):
        progress = self.cleaned_data.get('progress')
        if progress < 0 or progress > 100:
            raise forms.ValidationError('Progress must be between 0 and 100')
        return progress
