from impaf.application import Application


class Jinja2Application(Application):

    def _create_config(self):
        super()._create_config()
        self.config.include('pyramid_jinja2')

    def _generate_registry(self, registry):
        super()._generate_registry(registry)
        registry['jinja2'] = self.config.get_jinja2_environment()
