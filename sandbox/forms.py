from django import forms

choices = [
    ("Happy", "Happy"),
    ("Neutral", "Neutral"),
    ("Bad", "Bad"),
]

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    feedback = forms.CharField()
    satisfaction = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@gmail.com" not in email:
            raise forms.ValidationError("Email has to be a gmail")
        
        return email