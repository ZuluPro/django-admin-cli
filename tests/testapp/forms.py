from django import forms
from testapp import models


class TestModelAddForm(forms.ModelForm):
    form_field = forms.CharField(required=20)

    class Meta:
        model = models.TestModel
        fields = ('form_field',)

    def clean_form_field(self):
        form_field = self.cleaned_data.get("form_field")
        if not form_field:
            forms.ValidationError('Error')
        return form_field

    def save(self, commit=True):
        obj = super(TestModelAddForm, self).save(commit=False)
        form_field = self.cleaned_data["form_field"]
        obj.field1 = form_field
        obj.field2 = len(form_field)
        obj.no_verbose = len(form_field) / 2
        if commit:
            obj.save()
        return obj
