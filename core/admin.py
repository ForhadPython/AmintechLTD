from django.contrib import admin
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Images, HeadSlider, SingleProduct, ContactMessage, Comment
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
from django.conf import settings

# for local computer only
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

    def __init__(self):
        super(ProductResource, self).__init__()
        # Introduce a class variable to pass dry_run into methods that do not get it
        self.in_dry_run = True

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Set helper class method to dry_run value
        self.in_dry_run = dry_run

    def before_import_row(self, row, row_number=None, **kwargs):
        if not self.in_dry_run:
            print("Downloading....")
            # Get URL and split image name from import file
            image_url = row['image']
            image_name = image_url.split('/')[-1]

            # Generate temporary file and download image from provided URL
            try:
                tmp_file = NamedTemporaryFile(delete=True, dir=f'{settings.MEDIA_ROOT}')
                tmp_file.write(urllib.request.urlopen(image_url).read())
                tmp_file.flush()
                row['image'] = File(tmp_file, image_name)
            except Exception as e:
                pass
        return row


class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 1


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['sku', 'name', 'qty', 'price', 'image_tag']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]


class HeadSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount']


class SingleProductAdmin(admin.ModelAdmin):
    list_display = ['title']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'create_at']
    readonly_fields = ('subject', 'comment', 'user', 'product', 'rate', 'id')


admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(HeadSlider, HeadSliderAdmin)
admin.site.register(SingleProduct, SingleProductAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Comment, CommentAdmin)
