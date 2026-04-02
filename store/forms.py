from django import forms
from django.contrib.auth.models import User
from .models import Profile


# store/forms.py
class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new user with a linked Profile role.
    """
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        # Link this form to the built-in Django User model
        model = User
        # Specify the order of fields to appear in the form
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        """
        Save the User instance and create the linked Profile object.
        """
        # Get the user instance from the parent save method without saving
        user = super().save(commit=False)
        # Securely hash the provided password
        user.set_password(self.cleaned_data["password"])

        if commit:
            # Save the User to the database
            user.save()
            # Create a Profile for the user and assign the chosen role
            # Line break used to stay under the 79-character limit
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )

        return user

