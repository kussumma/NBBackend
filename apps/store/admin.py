from django.contrib import admin
from django.forms import ModelForm
from tools.fileupload_helper import FileUploadHelper

from .models import Contact, About, Partner, Investor, Policy, FAQ, CopyRight


class InvestorFormAdmin(ModelForm):
    class Meta:
        model = Investor
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("logo") == self.instance.logo:
            pass
        else:
            new_logo = self.cleaned_data.get("logo")
            self.cleaned_data["logo"] = FileUploadHelper(new_logo, webp=True).validate()


class PartnerFormAdmin(ModelForm):
    class Meta:
        model = Partner
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("logo") == self.instance.logo:
            pass
        else:
            new_logo = self.cleaned_data.get("logo")
            self.cleaned_data["logo"] = FileUploadHelper(new_logo, webp=True).validate()


class InvestorAdmin(admin.ModelAdmin):
    form = InvestorFormAdmin
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "description", "url")
    list_display = ("name", "description", "url", "logo", "is_active")


class PartnerAdmin(admin.ModelAdmin):
    form = PartnerFormAdmin
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "description", "url")
    list_display = ("name", "description", "url", "logo", "is_active")


admin.site.register(Contact)
admin.site.register(About)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(Policy)
admin.site.register(FAQ)
admin.site.register(CopyRight)
