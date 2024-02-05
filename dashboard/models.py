from django.db import models
# env/Scripts/activate 
# Create your models here.
class ShopType(models.Model):
    name=models.CharField(max_length=100)
    local_name=models.CharField(max_length=100)
    description=models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name=models.CharField(max_length=100)
    shoptype=models.ForeignKey(ShopType, on_delete=models.CASCADE)
    sort_order=models.IntegerField()
    
    def __str__(self):
        return self.name
    







class Shop(models.Model):
    shop_name = models.CharField(max_length=100, verbose_name="Shop Name")
    shop_name_local = models.CharField(max_length=100, verbose_name="Shop Name Local", blank=True, null=True)
    shoptype=models.ForeignKey(ShopType, on_delete=models.CASCADE,blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    shop_address = models.CharField(verbose_name="Shop Address",max_length=250,blank=True, null=True)
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number (Username)",blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, verbose_name="Whatsapp Number (With Country Code)", blank=True, null=True,default='91')
    shop_code = models.CharField(max_length=10, verbose_name="Shop Code",blank=True, null=True)
    shop_logo = models.ImageField(upload_to='shop_logos/', blank=True,verbose_name="Shop Logo (494x86)")
    shop_url = models.CharField(verbose_name="Shop URL",blank=True, null=True,max_length=50)
    expired_date = models.DateField(verbose_name="Expired Date")
    seo_title = models.CharField(max_length=100, verbose_name="Seo Title",blank=True, null=True)

    PAYMENT_CHOICES = [
        ('basic', 'Basic'),
        ('advanced', 'Advanced'),
        ('premium', 'Premium'), 
    ]
    pay_type = models.CharField(max_length=50, verbose_name="Pay Type", choices=PAYMENT_CHOICES,blank=True, null=True)
    seo_image = models.ImageField(upload_to='seo_images/', blank=True, verbose_name="Seo Image")
    background_sound = models.FileField(upload_to='background_sounds/', verbose_name="Background Sound", blank=True, null=True)
    shop_map_url = models.URLField(verbose_name="Shop Map URL", blank=True, null=True)
    seo_description = models.TextField(verbose_name="Seo Description",blank=True, null=True)
    city_names = models.TextField(verbose_name="City Names",blank=True, null=True)
    menu_brochure = models.FileField(upload_to='menu_brochures/', verbose_name="Menu / Brochure")
    publish_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name
    

s_choiches=[
    ('facebook','facebook'),
    ('instagram','instagram'),
    ('whatsapp','whatsapp')

]
class  Icon(models.Model):
    name=models.CharField(max_length=100,choices=s_choiches,blank=True, null=True)
    social_icons_url = models.URLField(verbose_name="Social Icons Url", blank=True, null=True)
    shop=models.ForeignKey(Shop, on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.name












    
    