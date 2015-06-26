from mock import MagicMock

from pytest import fixture

from impaf.application import Application

from ..application import Jinja2Application


class MockedApplication(Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags = {}
        self.config = MagicMock()

    def _create_config(self):
        self.flags['_create_config'] = True

    def _generate_registry(self, registry):
        self.flags['_generate_registry'] = True


class ExampleJinja2Application(Jinja2Application, MockedApplication):
    pass


class TestJinja2Application(object):

    @fixture
    def application(self):
        return ExampleJinja2Application('module')

    def test_create_config(self, application):
        application._create_config()

        assert application.flags['_create_config'] is True
        application.config.include.assert_called_once_with('pyramid_jinja2')

    def test_generate_registry(self, application):
        registry = {}
        application._generate_registry(registry)

        assert application.flags['_generate_registry'] is True
        assert registry == {
            'jinja2': application.config.get_jinja2_environment.return_value
        }
