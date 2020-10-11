""" Reports module """

import os
from io import BytesIO
import base64

import easydev
import matplotlib.pyplot as plt
from jinja2 import Template
from markdown import markdown
from bs4 import BeautifulSoup


def read_template(uri):
    """ Loads a jinja2 template """

    with open(uri, "r") as file:
        return Template(file.read())


def transform_markdown(text):
    """ auxiliar function to transform markdown to html """

    return markdown(text, extensions=["fenced_code", "codehilite"])


class Report:
    """ html report class """

    def __init__(self, title="Report", scripts=[], raw_scripts=[], styles={}):

        # Main arguments
        self.args = {"title": title}

        # Script resources
        self.scripts = scripts
        self.raw_scripts = raw_scripts

        # Style resources
        self.styles = styles

        # Body
        self.body = []

        # Figures
        self.figures = {}

    def add_script(self, script, raw=False):
        """ Adds a script resource """
        if raw:
            self.raw_scripts.append(script)

        else:
            self.script.append(script)

    def add_style(self, style):
        """ Add a style resource """

        self.styles.append(style)

    def add_markdown(self, text):
        """ Adds raw markdown """

        self.body.append(transform_markdown(text))

    def add_title(self, title, level=1):
        """ Adds a title """

        # Create a title using markdown
        self.add_markdown(f"{'#'*level} {title}")

    def add_figure(self, figurename=None, options=None, thumb_fmt="png", link_fmt="pdf"):
        """ 
            Adds the latest displayed matplotlib figure. 
            
            Can create a file in a dedicated directory and link it to the thumbnail
            shown in the html page. 
      
            Args:
                figurename: name of the file, if None no figure file is created
                options:    string of html attributes of the IMG tag, default: "width = 49%"
                thumb_fmt:  file format for the thumbnail (default png)
                link_fmt:   file format of the linked file (default pdf) 
        """

        options = options or "width = 49%"

        tmpfile = BytesIO()
        plt.savefig(tmpfile, format=thumb_fmt)
        encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")

        if figurename is None:
            self.body.append(f"<img src='data:image/{thumb_fmt};base64,{encoded}' {options}>")

        else:
            tmpfile = BytesIO()
            plt.savefig(tmpfile, format=link_fmt)
            encoded_pdf = tmpfile
            self.figures[figurename + "." + link_fmt] = encoded_pdf.getbuffer()

            self.body.append(
                """
                    <a href = \'img/{figurename}.{link_fmt}\'>
                      <img src=\'data:image/{thumb_fmt};base64,{encoded}\' {options}>
                    </a>
                """
            )

    def write_report(
        self, template_name="simple", template_path=None, filename="report.html", prettify=True
    ):
        """
            Writes the html report.

            Args:
                template_name:  name of the template to use (only used if template_path is None)
                template_path:  path of the custom template to use
                filename:       output file to write
                prettify:       bool to prettify the output html

            Available templates are:
            * simple
        """

        # If no custom path, use one of the predefined templates
        if template_path is None:
            relative_uri = f"html_reports/templates/{template_name}.html"

            template_uri = os.sep.join(
                [easydev.get_package_location("html_reports")] + relative_uri.split("/")
            )

        # Else, use user template
        else:
            template_uri = template_path

        # Load jinja2 template
        template = read_template(template_uri)

        # Render jinja2 template
        output = template.render(
            body="\n".join(self.body),
            scripts=self.scripts,
            raw_scripts=self.raw_scripts,
            styles=self.styles,
            **self.args,
        )

        # Prettify html file
        if prettify:
            output = BeautifulSoup(output, "html.parser").prettify()

        # Write html file
        with open(filename, "w") as file:
            file.write(output)

        # Add figures if needed
        if len(self.figures):
            figure_path = os.path.join(os.path.dirname(os.path.abspath(filename)), "img")

            if not os.path.exists(figure_path):
                os.mkdir(figure_path)

            for figurename, figuredata in self.figures.items():
                with open(os.path.join(figure_path, figurename), "wb") as file:
                    file.write(figuredata)
