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

    target_blank = models.BooleanField(
        default=False,
        verbose_name=_('Open gallery links new tab?'),
    )

    hidden_xs = models.BooleanField(
        default=True,
        verbose_name=_('Hide on small screens?'),
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
    mobile_first = models.BooleanField(
        default=False,
        verbose_name=_('Mobile First'),
        help_text=_('Responsive settings use mobile first calculation')
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

    thumbnail_size = models.CharField(
        max_length=15,
        default='99999x600',
        verbose_name=_('Thumbnail size'),
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
        output.update(
            self.responsive_to_json()
        )
        return json.dumps(output)

    def responsive_to_json(self):
        # breakpoints:
        # xs:  480px [  0; 768-1]
        # sm:  768px [768; 992-1]
        # md:  992px [992; 1200-1]
        # lg: 1200px [1200; inf+]

        def slide_decr(x): return max(x-1, 1)

        def slide_incr(x): return max(x+1, 1)

        def media(breakpoint, slidesToShow=1, slidesToScroll=1, **kwargs):
            settings = {
                'slidesToShow': slidesToShow,
                'slidesToScroll': slidesToScroll,
            }
            settings.update(**kwargs)

            media_dict = {
                'breakpoint': breakpoint,
                'settings': settings,
            }
            return media_dict

        slides = self.slides_to_show
        if self.mobile_first:
            # default settings are xs

            # mobile-first, thus means:
            # 'from this breakpoint and above, do this'

            slides = slide_incr(slides)
            sm = media(768, slidesToShow=slides, slidesToScroll=1)

            slides = slide_incr(slides)
            md = media(992, slidesToShow=slides, slidesToScroll=1)

            responsive = [sm, md]

        else:
            # default settings are lg+

            # not mobile-first, thus means:
            # 'from this breakpoint and below, do this'
            md = media(1200-1, slidesToShow=slides, slidesToScroll=1)

            slides = slide_decr(slides)
            sm = media(992-1, slidesToShow=slides, slidesToScroll=1)

            slides = slide_decr(slides)
            xs = media(768-1, slidesToShow=slides, slidesToScroll=1)

            responsive = [sm, xs]

        output = {
            'responsive': responsive
        }
        return output

    class Meta:
        abstract = True
        verbose_name = _('Slider')
        verbose_name_plural = _('Slider')
