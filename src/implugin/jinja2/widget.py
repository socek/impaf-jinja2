from jinja2 import Markup

from impaf.widget import Widget


class BaseWidget(Widget):

    def feed_request(self, request):
        super().feed_request(request)
        self.env = self.registry['jinja2']

    def render(self, template):
        template = self.env.get_template(template)
        return Markup(template.render(**self.data))


class SingleWidget(Widget):

    def get_template(self):
        return self.template

    def __call__(self, *args, **kwargs):
        self.make(*args, **kwargs)
        return self.render(self.get_template())

    def make(self):
        pass


class MultiWidget(Widget):

    def get_template(self, name, prefix=None):
        prefix = prefix or self.prefix
        return '%s/%s' % (prefix, name)

    def render_for(self, name, data, prefix=None):
        self.generate_data()
        self.data.update(data)
        return self.render(self.get_template(name, prefix=prefix))
