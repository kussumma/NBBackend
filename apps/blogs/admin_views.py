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
