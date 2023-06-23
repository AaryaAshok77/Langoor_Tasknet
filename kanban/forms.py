from django import forms
from django.contrib.auth import get_user_model
from core.models import CustomUser
from django.db.models import Q

from .models import Project, Task


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'assigned_users', 'start_date', 'end_date', 'status')

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Project Name',
        'class': 'py-4 px-6 rounded-xl'
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Project Description',
        'class': 'w-2/3 py-4 px-6 rounded-xl'
    }))

    assigned_users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.exclude(Q(username__iexact='admin') | Q(role__iexact='product_owner')),
        widget=forms.SelectMultiple(attrs={
            'class': 'multi-select-tag',
        }),
    )

    start_date = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={
        'class': 'py-4 px-6 rounded-xl',
    }))

    end_date = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={
        'class': 'py-4 px-6 rounded-xl',
    }))

    status = forms.ChoiceField(
        choices=(('ONGOING', 'Ongoing'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')),
        widget=forms.Select(attrs={'class': 'py-4 rounded-xl text-center'}),
    )

    def __init__(self, *args, **kwargs):
        is_edit_form = kwargs.pop('is_edit_form', False)
        super().__init__(*args, **kwargs)
        if not is_edit_form:
            self.fields['status'].required = True
        else:
            self.fields['status'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'End date should be after the start date.')

        return cleaned_data




class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('project', 'title', 'description', 'status', 'assigned_to', 'due_date')

    project = forms.ModelChoiceField(
        queryset=Project.objects.none(),  # Empty queryset initially
        widget=forms.Select(attrs={
            'class': 'py-4 px-6 rounded-xl',
            'onchange': 'loadAssignedUsers(this.value)',
        })
    )

    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Task Title',
        'class': 'py-4 px-6 rounded-xl'
    }))

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Task Description',
            'class': 'w-2/3 py-4 px-6 rounded-xl'
        })
    )

    status = forms.ChoiceField(
        choices=(('TODO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Done')),
        widget=forms.Select(attrs={'class': 'py-4 rounded-xl text-center'}),
    )

    due_date = forms.DateTimeField(
        widget=forms.SelectDateWidget(attrs={'class': 'py-4 px-6 rounded-xl'}),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.role == 'director':
            self.fields['project'].queryset = Project.objects.all()
        else:
            self.fields['project'].queryset = Project.objects.filter(Q(assigned_users=user) | Q(creator=user)).distinct()
        self.fields['assigned_to'].queryset = CustomUser.objects.none()  # Empty queryset initially

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                project = Project.objects.get(id=project_id)
                self.fields['assigned_to'].queryset = project.assigned_users.all()
            except (ValueError, Project.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['assigned_to'].queryset = self.instance.project.assigned_users.all()
