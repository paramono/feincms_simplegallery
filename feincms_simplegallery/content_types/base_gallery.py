from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

try:
    from feincms.admin.item_editor import FeinCMSInline
except ImportError:  # pragma: no cover, FeinCMS not available.
    # Does not do anything sane, but does not hurt either
    from django.contrib.admin import StackedInline as FeinCMSInline


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
        return _('Gallery Content') + "#{}".format(self.pk)

    @classmethod
    def initialize_type(cls, TYPE_CHOICES=None, cleanse=None):

        if TYPE_CHOICES:
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

        try:
            # TYPE_CHOICES is defined
            template_dir = 'content/simplegallery/%s/%s/' % (
                self.container_type,
                self.type,
            )
        except AttributeError:
            # TYPE_CHOICES is not defined
            template_dir = 'content/simplegallery/%s/' % (
                self.container_type,
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
            context_instance=kwargs.get('context')
        )

    @property
    def media(self):
        """
        this should be overridden, because you may want to use your own
        styles and scripts depending on type selected from TYPE_CHOICES
        """
        pass

    class Meta:
        abstract = True
        verbose_name = _('Simple Gallery')
        verbose_name_plural = _('Simple Gallery')
