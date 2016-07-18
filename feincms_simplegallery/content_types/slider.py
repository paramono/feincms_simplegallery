import json 

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base_gallery import GalleryContent


class SliderContent(GalleryContent):

    container_type = 'slider'

    LAZY_LOAD_ONDEMAND = 'ondemand'
    LAZY_LOAD_PROGRESSIVE = 'progressive'

    LAZY_LOAD_CHOICES = (
        (LAZY_LOAD_ONDEMAND, _('On Demand'),),
        (LAZY_LOAD_PROGRESSIVE, _('Progressive'),),
    )

    dots = models.BooleanField(
        default=True,
        verbose_name=_('Navigation dots'),
    )
    infinite = models.BooleanField(
        default=True,
        verbose_name=_('Infinite'),
        help_text=_('Shows first slide after the last one and vice versa'),
    )
    autoplay = models.BooleanField(
        default=False,
        verbose_name=_('Autoplay'),
    )
    adaptive_height = models.BooleanField(
        default=True,
        verbose_name=_('Adaptive Height'),
        help_text=_('Adapts slider height to the current slide'),
    )

    speed = models.PositiveIntegerField(
        default=500,
        verbose_name=_('Transition speed between slides'),
    )
    autoplay_speed = models.PositiveIntegerField(
        default=5000,
        verbose_name=_('Autoplay change interval'),
    )
    slides_to_show = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Number of slides to show at a time'),
    )
    slides_to_scroll = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Number of slides to scroll at a time'),
    )

    lazy_load = models.CharField(
        max_length=50,
        default=LAZY_LOAD_ONDEMAND,
        choices=LAZY_LOAD_CHOICES,
        verbose_name=_('Lazy Load'),
        help_text=_('Load images only when needed'),
    )

    def __str__(self):
        return _('Slider') + "#{}".format(self.pk)

    def to_json(self):
        output = {
            'dots': self.dots,
            'infinite': self.infinite,
            'autoplay': self.autoplay,
            'adaptiveHeight': self.adaptive_height,

            'speed': self.speed,
            'autoplaySpeed': self.autoplay_speed,
            'slidesToShow': self.slides_to_show,
            'slidesToScroll': self.slides_to_scroll,
            'lazyLoad': self.lazy_load,
        }
        return json.dumps(output)

    class Meta:
        abstract = True
        verbose_name = _('Slider')
        verbose_name_plural = _('Slider')
