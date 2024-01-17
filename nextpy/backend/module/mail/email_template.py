from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import EmailConfig


class EmailTemplateManager:
    def __init__(self, config: EmailConfig):
        self.env = Environment(
            loader=FileSystemLoader(config.MAIL_TEMPLATE_FOLDER),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render_template(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)
        return template.render(context)
