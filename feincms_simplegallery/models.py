from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile

from feincms_simplegallery.util.mixins import OrderableMixin
from feincms_simplegallery.util.base import (
    BaseContainer,
    BaseElement,
    BaseContent,
    )


class GalleryContainer(BaseContainer):

    class Meta:
        ordering = ['_order', 'title']
        verbose_name = _('Simple Gallery')
        verbose_name_plural = _('Simple Galleries')


class GalleryElement(BaseElement):

    container = models.ForeignKey(
        'GalleryContainer',
        verbose_name=_('Gallery'),
        related_name='container_elements',
        blank=True,
        null=True,
        )
    
    mediafile = MediaFileForeignKey(
        MediaFile,
        related_name='+',
        help_text=_('Image'), 
        limit_choices_to={'type': 'image'},
        blank=True,
        null=True,
        )

    class Meta:
        ordering = ['_order', 'title']
        verbose_name = _('Gallery Element')
        verbose_name_plural = _('Gallery Elements')


class GalleryContent(BaseContent):
    container = models.ForeignKey(
        'GalleryContainer', 
        verbose_name=_('Link to Gallery'), 
        related_name='%(app_label)s_%(class)s_related',
        blank=True,
        null=True,
        )
    container_type = 'gallery'

    @property
    def media(self):
        """ 
        this should be overridden, because you may want to use your own
        styles and scripts depending on type selected from TYPE_CHOICES
        """
        # if self.type == 'slider':
        # return forms.Media(
        #     css={
        #         'all': (
        #             'gallery/css/jssor_skin.css',
        #         ),
        #     },
        #     js=(
        #         'gallery/js/jssor.js', 
        #         'gallery/js/jssor.slider.mini.js', 
        #         'gallery/js/jssor_load.js',
        #         ),
        # )

    class Meta:
        abstract = True
        verbose_name = _('Simple Gallery')
        verbose_name_plural = _('Simple Gallery')
