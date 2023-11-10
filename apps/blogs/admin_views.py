from django.forms import ModelForm
from tools.fileupload_helper import FileUploadHelper

from .models import (
    BlogCategory,
    Blog,
    BlogImage,
)


class BlogCategoryFormAdmin(ModelForm):
    class Meta:
        model = BlogCategory
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


class BlogFormAdmin(ModelForm):
    class Meta:
        model = Blog
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
        if (
            self.cleaned_data.get("cover_homepage_mobile")
            == self.instance.cover_homepage_mobile
        ):
            pass
        else:
            new_cover_homepage_mobile = self.cleaned_data.get("cover_homepage_mobile")
            self.cleaned_data["cover_homepage_mobile"] = FileUploadHelper(
                new_cover_homepage_mobile, webp=True
            ).validate()
        if (
            self.cleaned_data.get("cover_homepage_headline")
            == self.instance.cover_homepage_headline
        ):
            pass
        else:
            new_cover_homepage_headline = self.cleaned_data.get(
                "cover_homepage_headline"
            )
            self.cleaned_data["cover_homepage_headline"] = FileUploadHelper(
                new_cover_homepage_headline, webp=True
            ).validate()


class BlogImageFormAdmin(ModelForm):
    class Meta:
        model = BlogImage
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("image") == self.instance.image:
            pass
        else:
            new_image = self.cleaned_data.get("image")
            self.cleaned_data["image"] = FileUploadHelper(
                new_image, webp=True
            ).validate()
