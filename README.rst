=====================
feincms_simplegallery
=====================

feincms_simplegallery is a simple implementation of gallery for feincms

Quick start
-----------

1. Add "feincms_simplegallery" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'feincms_simplegallery',
    )

2. If you intend to use it as feincms content type, register GalleryContent 
   for your Page model (or any other Base-derived model) like this::

    from feincms_simplegallery.models import GalleryContent
    # ...
    Page.create_content_type(GalleryContent)

3. (optional) It is possible to define TYPE_CHOICES for GalleryContent if you want to 
   render galleries using different templates::

    from feincms_simplegallery.models import GalleryContent
    # ...
    Page.create_content_type(GalleryContent, TYPE_CHOICES=(
            ('default', 'default template'),
            ('other', 'some other template'),
            # ... (other types)
        )
    )
    
    # galleries will be rendered as either of these, depending on admin choice:
    # templates/content/feincms_simplegallery/default.html
    # templates/content/feincms_simplegallery/other.html
    # ...

    Some of the templates (grid and lightbox) are bundled with the plugin

4. Migrate your models
