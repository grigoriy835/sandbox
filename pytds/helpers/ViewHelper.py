from jinja2 import Environment, PackageLoader


agregatorsEnv = Environment(
    loader=PackageLoader('templates', package_path=''),
)


def view(path, data):
    template = agregatorsEnv.get_template(path)
    content = template.render(**data)
    return content
