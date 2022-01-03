from datetime import date

from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Button
from crispy_forms.bootstrap import FormActions

from .models import BookModel

class BookForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100, required=True)
    author = forms.CharField(max_length=100, required=True)
    date = forms.DateField(
        required=True,
        widget=DatePickerInput(
            attrs={'placeholder':'yyyy-mm-dd'},
            format="%Y-%m-%d"
        )
    )
    isbn = forms.CharField(required=False, min_length=13, max_length=13)
    pages = forms.IntegerField(required=True, min_value=0)
    cover = forms.URLField(required=True)
    language = forms.CharField(max_length=25, required=True)

    class Meta:
        model = BookModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('author')
            ),
            Row(
                Column('date'),
                Column('isbn')
            ),
            Row(
                Column('pages'),
                Column('cover')
            ),
            'language',
            FormActions(
                Submit('post', 'Add')
            )
        )

    def clean_title(self):
        data = self.cleaned_data.get('title')
        return data
    def clean_author(self):
        data = self.cleaned_data.get('author')
        return data
    def clean_date(self):
        data = self.cleaned_data.get('date')
        if data > date.today():
            print("date invalid")
            raise forms.ValidationError("Can't set date in the future")
        return data
    def clean_isbn(self):
        data = self.cleaned_data.get('isbn')
        if data and not data.isdigit():
            raise forms.ValidationError("ISBN must be a number")
        if data and len(data) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digit long")
        return data
    def clean_pages(self):
        data = self.cleaned_data.get('pages')
        return data
    def clean_cover(self):
        data = self.cleaned_data.get('cover')
        return data
    def clean_language(self):
        data = self.cleaned_data.get('language')
        return data

class SearchBookForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=False)
    author = forms.CharField(max_length=100, required=False)
    datefrom = forms.DateField(
        label="Date from",
        required=False,
        widget=DatePickerInput(
            attrs={'placeholder':'yyyy-mm-dd'},
            format="%Y-%m-%d"
        )
    )
    dateto = forms.DateField(
        label="Date to",
        required=False,
        widget=DatePickerInput(
            attrs={'placeholder':'yyyy-mm-dd'},
            format="%Y-%m-%d"
        )
    )
    language = forms.CharField(max_length=25, required=False)

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('author')
            ),
            Row(
                Column('datefrom'),
                Column('dateto')
            ),
            'language',
            FormActions(
                Submit('get', 'Search'),
                Submit('get', 'Search Rest', css_class="ml-4 btn-secondary"),
                Button(
                    'clear',
                    'clear',
                    css_class="ml-4 btn-danger",
                    onclick='window.location.href="/"'
                )
            )
        )
    def clean_datefrom(self):
        clean_date = self.cleaned_data.get('datefrom')
        return clean_date
    def clean_dateto(self):
        return self.clean_date()
    def clean_date(self):
        dates = []
        dates.append(self.cleaned_data.get('datefrom'))
        dates.append(self.cleaned_data.get('dateto'))
        if None not in dates and dates[0] > dates[1]:
            raise forms.ValidationError("Inappropriate date. Must be older than date from")
        return dates[1]

class ImportForm(forms.Form):
    q = forms.CharField(label='Keywords', max_length=75, required=False)
    intitle = forms.CharField(label='Title', max_length=100, required=False)
    inauthor = forms.CharField(label='Author', max_length=100, required=False)
    isbn = forms.CharField(label='ISBN number', max_length=13, required=False)
    subject = forms.CharField(label='Subject', max_length=50, required=False)

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            'q',
            Row(
                Column('intitle'),
                Column('inauthor')
            ),
            Row(
                Column('isbn'),
                Column('subject')
            ),
            FormActions(
                Submit('get', 'Import'),
            )
        )
    def clean_isbn(self):
        data = self.cleaned_data.get('isbn')
        if not data:
            return data
        if not data.isdigit():
            raise forms.ValidationError("ISBN must be a number")
        if len(data) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10/13 - digit long")
        return data
