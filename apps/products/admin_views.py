from .models import Wishlist
from django.shortcuts import redirect
from django.contrib import messages
from django.forms import ModelForm
from tools.fileupload_helper import FileUploadHelper

from .models import (
    Category,
    Subcategory,
    Subsubcategory,
    Product,
    Stock,
    Brand,
    ExtraProductImage,
    ExtraProductVideo,
    Rating,
)


def delete_wishlist_by_product(request, product_id):
    try:
        Wishlist.objects.filter(product__id=product_id).delete()
        messages.success(request, "Wishlist deleted successfully.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("admin:products_wishlist_changelist")


class CategoryFormAdmin(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()
        if self.cleaned_data.get("cover_mobile") == self.instance.cover_mobile:
            pass
        else:
            new_cover_mobile = self.cleaned_data.get("cover_mobile")
            self.cleaned_data["cover_mobile"] = FileUploadHelper(
                new_cover_mobile, webp=True
            ).validate()
        if self.cleaned_data.get("cover_homepage") == self.instance.cover_homepage:
            pass
        else:
            new_cover_homepage = self.cleaned_data.get("cover_homepage")
            self.cleaned_data["cover_homepage"] = FileUploadHelper(
                new_cover_homepage, webp=True
            ).validate()


class SubcategoryFormAdmin(ModelForm):
    class Meta:
        model = Subcategory
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()
        if self.cleaned_data.get("cover_mobile") == self.instance.cover_mobile:
            pass
        else:
            new_cover_mobile = self.cleaned_data.get("cover_mobile")
            self.cleaned_data["cover_mobile"] = FileUploadHelper(
                new_cover_mobile, webp=True
            ).validate()
        if self.cleaned_data.get("cover_homepage") == self.instance.cover_homepage:
            pass
        else:
            new_cover_homepage = self.cleaned_data.get("cover_homepage")
            self.cleaned_data["cover_homepage"] = FileUploadHelper(
                new_cover_homepage, webp=True
            ).validate()


class SubsubcategoryFormAdmin(ModelForm):
    class Meta:
        model = Subsubcategory
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()
        if self.cleaned_data.get("cover_mobile") == self.instance.cover_mobile:
            pass
        else:
            new_cover_mobile = self.cleaned_data.get("cover_mobile")
            self.cleaned_data["cover_mobile"] = FileUploadHelper(
                new_cover_mobile, webp=True
            ).validate()
        if self.cleaned_data.get("cover_homepage") == self.instance.cover_homepage:
            pass
        else:
            new_cover_homepage = self.cleaned_data.get("cover_homepage")
            self.cleaned_data["cover_homepage"] = FileUploadHelper(
                new_cover_homepage, webp=True
            ).validate()


class BrandFormAdmin(ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("logo") == self.instance.logo:
            pass
        else:
            new_logo = self.cleaned_data.get("logo")
            self.cleaned_data["logo"] = FileUploadHelper(new_logo, webp=True).validate()

        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()
        if self.cleaned_data.get("cover_mobile") == self.instance.cover_mobile:
            pass
        else:
            new_cover_mobile = self.cleaned_data.get("cover_mobile")
            self.cleaned_data["cover_mobile"] = FileUploadHelper(
                new_cover_mobile, webp=True
            ).validate()
        if self.cleaned_data.get("cover_homepage") == self.instance.cover_homepage:
            pass
        else:
            new_cover_homepage = self.cleaned_data.get("cover_homepage")
            self.cleaned_data["cover_homepage"] = FileUploadHelper(
                new_cover_homepage, webp=True
            ).validate()


class ProductFormAdmin(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()


class StockFormAdmin(ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("variant_image") == self.instance.variant_image:
            pass
        else:
            new_variant_image = self.cleaned_data.get("variant_image")
            self.cleaned_data["variant_image"] = FileUploadHelper(
                new_variant_image, webp=True
            ).validate()


class ExtraProductImageFormAdmin(ModelForm):
    class Meta:
        model = ExtraProductImage
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("image") == self.instance.image:
            pass
        else:
            new_image = self.cleaned_data.get("image")
            self.cleaned_data["image"] = FileUploadHelper(
                new_image, webp=True
            ).validate()


class ExtraProductVideoFormAdmin(ModelForm):
    class Meta:
        model = ExtraProductVideo
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("video") == self.instance.video:
            pass
        else:
            new_video = self.cleaned_data.get("video")
            self.cleaned_data["video"] = FileUploadHelper(
                new_video, type="video"
            ).validate()


class RatingFormAdmin(ModelForm):
    class Meta:
        model = Rating
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("image") == self.instance.image:
            pass
        else:
            new_image = self.cleaned_data.get("image")
            self.cleaned_data["image"] = FileUploadHelper(
                new_image, webp=True
            ).validate()

        if self.cleaned_data.get("video") == self.instance.video:
            pass
        else:
            new_video = self.cleaned_data.get("video")
            self.cleaned_data["video"] = FileUploadHelper(
                new_video, type="video"
            ).validate()
