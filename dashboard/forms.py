from .models import ShopType,Category,Shop
from django import forms

class ShopTypeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    local_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(required=False)
    class Meta:
        model = ShopType
        fields = ['name', 'local_name', 'description', 'is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shoptype'].label_from_instance = lambda obj: obj.name


from django import forms
from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'  
        widgets = {
            'expired_date': forms.DateInput(attrs={'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'style': 'width: 20px; height: 20px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shoptype'].label_from_instance = lambda obj: obj.name
        # self.fields['social_icons'].label_from_instance = lambda obj: obj.name
        self.fields['category'].label_from_instance = lambda obj: obj.name
        # self.fields['category'].queryset = Category.objects.none()

        if 'shoptype' in self.data:
            try:
                shoptype_id = int(self.data.get('shoptype'))
                self.fields['category'].queryset = Category.objects.filter(shoptype_id=shoptype_id).all()
            except (ValueError, TypeError):
                pass 

     
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  

from .models import Icon
from django.forms import inlineformset_factory

class IconForm(forms.ModelForm):
    class Meta:
        model= Icon
        fields = ['name','social_icons_url','shop']
    

        

    def __init__(self, *args, **kwargs):
        super(IconForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.all()
        self.fields['name'].widget.attrs.update({'style': 'width: 330px;'})  
        self.fields['social_icons_url'].widget.attrs.update({'style': 'width: 330px;'}) 
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    

        

ModelBFormSet = inlineformset_factory(Shop, Icon, form=IconForm, extra=2, can_delete=True)



from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','is_staff','is_active']







