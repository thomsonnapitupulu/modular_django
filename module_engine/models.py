# module_engine/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class Module(models.Model):
    """Model representing an installed module."""
    name = models.CharField(_("Module name"), max_length=100)
    identifier = models.SlugField(_("Module identifier"), max_length=100, unique=True)
    version = models.CharField(_("Version"), max_length=20)
    installed = models.BooleanField(_("Installed"), default=False)
    active = models.BooleanField(_("Active"), default=False)
    install_date = models.DateTimeField(_("Install date"), auto_now_add=True)
    update_date = models.DateTimeField(_("Update date"), auto_now=True)
    
    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.version})"


class ModuleField(models.Model):
    """Model to track module fields for migrations."""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='fields')
    model_name = models.CharField(_("Model name"), max_length=100)
    field_name = models.CharField(_("Field name"), max_length=100)
    field_type = models.CharField(_("Field type"), max_length=100)
    field_params = models.JSONField(_("Field parameters"), default=dict)
    is_active = models.BooleanField(_("Active"), default=True)
    
    class Meta:
        unique_together = ['module', 'model_name', 'field_name']
        verbose_name = _("Module field")
        verbose_name_plural = _("Module fields")
    
    def __str__(self):
        return f"{self.module.name} - {self.model_name}.{self.field_name}"