from __future__ import unicode_literals

from django.views.generic import TemplateView

from .models import SysConfig




class BaseView(TemplateView):

    style_name = '/static/css/base.css'
    SITE_NAME = 'idea publications'
    SITE_TITLE = 'ideapub'
    COPYRIGHT = 'idea-2015'
    SUPPORT_EMAIL = 'ijharalkawsary@gmail.com'
    SITE_DESCRIPTION = 'islamic online books shop'
    

    # Base template to extend in drived views
    base_template_name = 'ideapub/base.html'

    # Decorators applied to generated view
    decorators = []

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        # Settings context data for base template
        context['request'] = self.request
        context['style_name'] = self.style_name
        context['base_template_name'] = self.base_template_name
        context['SITE_NAME'] = self.SITE_NAME
        context['SITE_TITLE'] = self.SITE_TITLE
        context['SITE_DESCRIPTION'] = self.SITE_DESCRIPTION
        context['COPYRIGHT'] = self.COPYRIGHT
        context['SUPPORT_EMAIL'] = self.SUPPORT_EMAIL

        if hasattr(self, 'page_title'):
            context['page_title'] = self.page_title

        return context

    @classmethod
    def get_decorators(cls):
        """
        Returns list of decorators defined as attribute of class

        Generic base views should override get_decorators method instead of defining decorators attribute
        """
        return cls.decorators

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Returns view function

        Decorators will be applied defined at class level
        """
        view = super(BaseView, cls).as_view(**initkwargs)

        # Applying decorators to generated view
        for decorator in cls.get_decorators():
            view = decorator(view)

        return view

    @staticmethod
    def get_config(name):
        return SysConfig.get_config(name)