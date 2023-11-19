import marko
import argparse
import yaml
import pathlib
import shutil
import os
import jinja2 as jinja
from datetime import date

class StyledRendererMixin(object):
    def render_image(self, element):
        template = '<img src="{}" alt="{}" style="width: 80%; object-fit: cover;" class="rounded mx-auto d-block"{} />'
        title = f' title="{self.escape_html(element.title)}"' if element.title else ""
        url = self.escape_url(element.dest)
        render_func = self.render
        self.render = self.render_plain_text  # type: ignore
        body = self.render_children(element)
        self.render = render_func  # type: ignore
        return template.format(url, body, title)

today = date.today()
date = today.strftime("%B %d, %Y")
styledExtension = marko.helpers.MarkoExtension(renderer_mixins=[StyledRendererMixin])
markdown = marko.Markdown(extensions=[styledExtension])

def cli():
    parser = argparse.ArgumentParser(
        prog='process',
        description='Process markdown files for the Rowland Hall Robotics website.',
        epilog='This is an internal tool.'
    )

    parser.add_argument('-s', required=True, type=argparse.FileType('r'), dest="specification",
        help="website specification")

    return parser.parse_args()

def process_file(specification, input, output):
    # Reading
    input_source = ''
    with open(input, 'r') as f:
        input_source = f.read()

    input_sections = input_source.split('---')

    # Markdown and metadata
    metadata = yaml.load(input_sections[1], Loader=yaml.Loader)
    rendered_html = markdown.convert(input_sections[2])

    # Templating
    template_env = jinja.Environment(loader=jinja.FileSystemLoader(specification['templates']))
    template = template_env.get_template(metadata['layout'] + '.html')
    filled_html = template.render(
        title=metadata['title'],
        rendered=rendered_html,
        date=date
    )

    # Output
    with open(output, 'w+') as f:
        f.write(filled_html)

def main():
    # Prelude
    args = cli()
    specification_source = args.specification.read()
    specification = yaml.load(specification_source, Loader=yaml.Loader)

    # Walk
    for path in pathlib.Path(specification['content']).rglob('*.md'):
        input = str(path)
        output = specification['output'] + os.sep + input.replace(specification['content'], '').replace(".md", ".html")

        print('(content) ' + input + ' -> ' + output + '...')
        process_file(specification, input, output)

    for input in specification['runtime']:
        output = specification['output'] + os.sep + input.replace(specification['content'], '')

        print('(runtime) ' + input + ' -> ' + output + '...')

        try:
            shutil.copytree(input, output)
        except FileExistsError as e:
            shutil.rmtree(output)
            shutil.copytree(input, output)

    favicon_input = specification['favicon']
    favicon_output = specification['output'] + os.sep + favicon_input.split(os.sep)[-1]
    print('(runtime) ' + favicon_input + ' -> ' + favicon_output)
    shutil.copy(favicon_input, favicon_output)

if __name__ == '__main__':
    main()