from django import forms
from penntext.models import Subject, Sell, UserProfile, TicketSell, HouseholdSell, Term, SubletsSell, Other
from django.contrib.auth.models import User

class SubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=4, help_text="Please enter the subject name (Ex: FNCE).")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Subject
    def clean_name(self):
        if len(self.cleaned_data['name']) < 3:
            raise forms.ValidationError("Subject must have at least 3 letters")
        else:
            return self.cleaned_data['name'].upper()

class TermForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the term you are subletting for")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Term
    def clean_name(self):
        return self.cleaned_data['name'].upper()

class SellForm(forms.ModelForm):
    contact = forms.CharField(help_text="Please enter your phone number.(Optional).", required=False)
    book = forms.CharField(help_text="Please name your book")
    course = forms.CharField(help_text="Please enter course number")
    price = forms.IntegerField(help_text="Please enter the lowest price you would sell at")    
    picture = forms.ImageField(help_text="Please upload a picture (Optional)", required=False) 
    class Meta:
        model = Sell

        fields = ('contact', 'book', 'course', 'price', 'picture')


class TicketSellForm(forms.ModelForm):
    contact = forms.CharField(help_text="Please enter your phone number(Optional).", required=False)
    ticket = forms.CharField(help_text="Please name the ticket you are selling.")
    description = forms.CharField(widget=forms.Textarea, help_text="Please describe the ticket briefly.")
    price = forms.IntegerField(help_text="Please enter the lowest price you would sell at")
    picture = forms.ImageField(help_text="Please upload a picture (Optional)", required=False)
    class Meta:
        model = TicketSell
        fields = ('contact', 'ticket', 'description', 'price', 'picture')


class HouseholdSellForm(forms.ModelForm):
    contact = forms.CharField(help_text="Please enter your phone number(Optional).", required=False)
    item = forms.CharField(help_text="Please name the item you are selling.")
    description = forms.CharField(widget=forms.Textarea, help_text="Please describe the item you are selling.")
    price = forms.IntegerField(help_text="Please enter the lowest price you would sell at")
    picture = forms.ImageField(help_text="Please upload a picture (Optional)", required=False)
    class Meta:
        model = HouseholdSell
        fields = ('contact', 'item', 'description', 'price', 'picture')
        
class SubletsSellForm(forms.ModelForm):
    contact = forms.CharField(help_text="Please enter your phone number(Optional).", required=False)
    title = forms.CharField(help_text="Please give a title to place to your advertisement.")
    description = forms.CharField(widget=forms.Textarea, help_text="Please describe the place.")
    price = forms.IntegerField(help_text="Please enter an approximate rent")
    picture = forms.ImageField(help_text="Please upload a picture (Optional)", required=False)
    class Meta:
        model = SubletsSell
        fields = ('contact', 'title', 'description', 'price', 'picture')
        

class OtherForm(forms.ModelForm):
    contact = forms.CharField(help_text="Please enter your phone number (Optional).", required=False)
    title = forms.CharField(help_text="Please name the item you are selling.")
    description = forms.CharField(widget=forms.Textarea, help_text="Please describe the item you are selling.")
    price = forms.IntegerField(help_text="Please enter the lowest price you would sell at")
    picture = forms.ImageField(help_text="Please upload a picture (Optional)", required=False)
    class Meta:
        model = Other
        fields = ('contact', 'title', 'description', 'price', 'picture')
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="Alphanumeric Only.")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        User.email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(("This email address is already in use. Please supply a different email address."))

        User.username = self.cleaned_data["username"]
        if not User.username.isalnum():
            raise forms.ValidationError(("Contains non-alphanumberic characters."))
     #   if not User.email.endswith(".upenn.edu"):
      #    raise forms.ValidationError(("Not a valid Penn email"))
        
        return self.cleaned_data['email']

class UserProfileForm(forms.ModelForm):
    activation_key = forms.CharField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = UserProfile
        fields = ('activation_key',)
