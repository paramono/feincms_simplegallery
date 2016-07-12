# from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile

from feincms_simplegallery.util.mixins import OrderableMixin

try:
    from feincms.admin.item_editor import FeinCMSInline
except ImportError:  # pragma: no cover, FeinCMS not available.
    # Does not do anything sane, but does not hurt either
    from django.contrib.admin import StackedInline as FeinCMSInline


class GalleryContainer(OrderableMixin):
    """
    Container of Elements to be rendered.
    """

    title = models.CharField(_('Title'), max_length=300)

    def __str__(self):
        return self.title

    def render(self, **kwargs):
        # return
        return render_to_string(
            # 'content/containers/%s/container.html' % self.type,
            'content/simplegallery/gallery/default/container.html',
            {
                'elements': self.container_elements.all(),
                'container_title': self.title,
                'container_id': id(self)
            },
            context_instance=kwargs.get('context'))

    class Meta:
        ordering = ['_order', 'title']
        verbose_name = _('Simple Gallery')
        verbose_name_plural = _('Simple Galleries')


class GalleryElement(OrderableMixin, models.Model):
    """
    Element to be rendered.
    """
    title = models.CharField(
        _('Title'),
        max_length=100,
        blank=True,
        null=True,
    )
    subtitle = models.CharField(
        _('Subtitle'),
        max_length=200,
        blank=True,
        null=True,
    )
    alt = models.CharField(
        _('alt attribute'),
        max_length=200,
        blank=True,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )
    page = models.ForeignKey(
        Page,
        verbose_name=_("Page"),
        blank=True,
        null=True,
    )
    url = models.CharField(
        _('URL'),
        max_length=2048,
        blank=True,
        null=True,
    )
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.page:
            url = self.page.get_absolute_url()
        else:
            url = self.url
        return url

    def render(self, **kwargs):
        return render_to_string(
            'content/containers/%s/elem.html' %
            self.__class__.__name__.lower(),
            {
                'elem': self,
                'elem_id': id(self)
            },
            context_instance=kwargs.get('context'))

    class Meta:
        ordering = ['_order', 'title']
        verbose_name = _('Gallery Element')
        verbose_name_plural = _('Gallery Elements')


class GalleryContentInline(FeinCMSInline):
    raw_id_fields = ('container',)


class GalleryContent(models.Model):
    feincms_item_editor_inline = GalleryContentInline
    container_type = 'gallery'

    container = models.ForeignKey(
        'GalleryContainer',
        verbose_name=_('Link to Gallery'),
        related_name='%(app_label)s_%(class)s_related',
        blank=True,
        null=True,
    )

    def __str__(self):
        return _('Base Content') + "#{}".format(self.pk)

    @classmethod
    def initialize_type(cls, TYPE_CHOICES=None, cleanse=None):

        if TYPE_CHOICES is None:
            raise ImproperlyConfigured(
                'You need to set TYPE_CHOICES when creating a'
                ' %s' % cls.__name__
                )

        cls.add_to_class(
            'type',
            models.CharField(
                _('type'),
                max_length=20, choices=TYPE_CHOICES,
                default=TYPE_CHOICES[0][0]
            )
        )

        if cleanse:
            cls.cleanse = cleanse

    def render(self, **kwargs):
        # return
        template_dir = 'content/simplegallery/%s/%s/' % (
            self.container_type,
            self.type,
            )
        template_container = template_dir + 'container.html'
        template_element = template_dir + 'element.html'
        return render_to_string(
            template_container,
            {
                'elements': self.container.container_elements.all(),
                'container': self,
                'container_title': self.container.title,
                'container_id': id(self),
                'template_dir': template_dir,
                'template_element': template_element,
            },
            context_instance=kwargs.get('context'))

    @property
    def media(self):
        """
        this should be overridden, because you may want to use your own
        styles and scripts depending on type selected from TYPE_CHOICES
        """

    class Meta:
        abstract = True
        verbose_name = _('Simple Gallery')
        verbose_name_plural = _('Simple Gallery')
