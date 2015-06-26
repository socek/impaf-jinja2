from mock import MagicMock
from mock import sentinel
from mock import patch

from pytest import fixture
from pytest import yield_fixture
from jinja2 import Template

from impaf.widget import Widget

from ..widget import BaseWidget
from ..widget import SingleWidget
from ..widget import MultiWidget


class MockedWidget(Widget):

    def feed_request(self, request):
        self.flags = {}
        self.request = MagicMock()
        self.request.registry = {
            'jinja2': sentinel.jinja2,
        }
        assert request == sentinel.request


class ExampleBaseWidget(BaseWidget, MockedWidget):
    pass


class TestBaseWidget(object):

    @fixture
    def widget(self):
        return ExampleBaseWidget()

    def test_feed_request(self, widget):
        """
        .feed_request should assign registry['jinja2'] to self.env
        """
        widget.feed_request(sentinel.request)

        assert widget.flags == {}
        assert widget.env == sentinel.jinja2

    def test_render(self, widget):
        """
        .render should render template from template link
        """
        template = 'url.to.module:template.jinja2'
        widget.env = MagicMock()
        widget.env.get_template.return_value = Template('hello {{me}}')
        widget.context = {
            'me': 'Felix',
        }

        markup = widget.render(template)
        widget.env.get_template.assert_called_once_with(template)
        assert str(markup) == 'hello Felix'


class ExampleSingleWidget(SingleWidget):
    template = 'link to template'

    def make(self, arg, kw):
        super().make()
        self.context = {
            'arg': arg,
            'kw': kw,
        }


class TestSingleWidget(object):

    @fixture
    def widget(self):
        return ExampleSingleWidget()

    @yield_fixture
    def mrender(self, widget):
        patcher = patch.object(widget, 'render')
        with patcher as mock:
            yield mock

    def test_simple(self, widget, mrender):
        widget('arg', kw='kwarg')

        assert widget.context == {
            'arg': 'arg',
            'kw': 'kwarg',
        }
        mrender.assert_called_once_with(widget.template)


class TestMultiWidget(object):

    @fixture
    def widget(self):
        return MultiWidget()

    @yield_fixture
    def mrender(self, widget):
        patcher = patch.object(widget, 'render')
        with patcher as mock:
            yield mock

    def test_get_template_when_no_self_prefix(self, widget):
        assert widget.get_template('myname', 'p1') == 'p1/myname'

    def test_get_template_when_self_prefix(self, widget):
        widget.prefix = 'p2'
        assert widget.get_template('myname') == 'p2/myname'

    def test_render_for(self, widget, mrender):
        widget.request = sentinel.request
        widget.context = {'old': sentinel.old}
        widget.render_for('mytemplate', {'mycontext': sentinel.new})

        assert widget.context == {
            'request': sentinel.request,
            'mycontext': sentinel.new,
            'self': widget,
        }
        mrender.assert_called_once_with('mytemplate')
