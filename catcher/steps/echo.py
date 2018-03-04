from os.path import join
from jinja2 import Template
from catcher.steps.step import Step
from catcher.utils.logger import info


class Echo(Step):
    def __init__(self, path: str, body: dict) -> None:
        super().__init__(body)
        self._export_from = body['from']
        self._export_to = body.get('to', None)
        self._path = path

    @property
    def source(self) -> str:
        return self._export_from

    @property
    def dst(self) -> str or None:
        return self._export_to

    @property
    def path(self):
        return self._path

    def action(self, includes: dict, variables: dict) -> dict:
        template = Template(self.source)
        out = template.render(variables)
        if self.dst is None:
            info(out)
        else:
            template = Template(self.dst)
            dst = template.render(variables)
            with open(join(self.path, dst), 'w') as f:
                f.write(out)
        return self.process_register(variables)
