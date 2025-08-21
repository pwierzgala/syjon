from django.http import HttpResponse
from django.template import Context, loader
# from weasyprint import HTML, default_url_fetcher

from apps.syjon.lib.functions import escape_invalid_xml_chars


def render_to_pdf(request, template_path, template_context, file_name, is_attachment=False):
    template = loader.get_template(template_path)
    rendered_html = template.render(template_context)
    rendered_html = escape_invalid_xml_chars(rendered_html, '?')
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'filename="{0}.pdf"'.format(file_name)
    if is_attachment:
        response['Content-Disposition'] += '; attachment'
    HTML(
        string=rendered_html,
        base_url=request.build_absolute_uri(),
        url_fetcher=default_url_fetcher
    ).write_pdf(response)
    return response


def create_pdf(template_path, template_context, output_path):
    template = loader.get_template(template_path)
    rendered_html = template.render(Context(template_context))
    HTML(
        string=rendered_html,
        base_url='http://127.0.0.1:8000/static/',
        url_fetcher=default_url_fetcher
    ).write_pdf(output_path)
