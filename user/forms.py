from django import forms

from user.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'id',
            'dating_sex','location','min_distance','max_distance','min_dating_age',
            'max_dating_age', 'vibration','only_matche','auto_play',
        ]

    def clean_max_dating_age(self):
        clean_data = super().clean()#数据清洗
        min_dating_age = clean_data.get('min_dating_age')
        max_dating_age = clean_data.get('max_dating_age')
        if min_dating_age > max_dating_age:
            raise forms.ValidationError('min_dating_age > max_dating_age')


class UploadForm(forms.Form):
    avatar = forms.fields.FileField()