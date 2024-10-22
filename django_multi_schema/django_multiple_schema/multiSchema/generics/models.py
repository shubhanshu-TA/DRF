from django.db import models


class TimeStampModel(models.Model):
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    #tenant_identifier can be group id in azure ad token or any unique id to tenant
    tenant_identifier = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.upper()

    class Meta:
        db_table = "tenant"
        app_label = "common"

class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    class Meta:
        abstract = True

