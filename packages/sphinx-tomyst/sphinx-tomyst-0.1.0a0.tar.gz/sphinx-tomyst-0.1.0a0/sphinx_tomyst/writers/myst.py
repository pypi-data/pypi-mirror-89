"""
Myst Syntax
"""

from .markdown import MarkdownSyntax


class MystSyntax(MarkdownSyntax):

    indentation = " " * 2
    target_mystnb = False

    # - Direct Syntax - #

    def visit_admonition(self, title):
        return "```{{admonition}} {}".format(title)

    def depart_admonition(self):
        return "```"

    def visit_attribution(self):
        return "-- "

    def visit_bullet_list_item(self, listobj):
        indent = self.indentation * listobj["level"]
        marker = listobj["marker"]
        return "{}{} ".format(indent, marker)

    def visit_definition(self, text):
        # Adjust \n and \n\n with indentation
        text = text.replace("\n", "\n  ")
        text = text.replace("\n  \n  ", "\n\n  ")
        return ": " + text

    def visit_epigraph(self):
        return "```{{epigraph}}"

    def visit_image(self, uri, options=None):
        if options is None:
            return "```{{image}} {}".format(uri)
        else:
            options = "\n".join(options)
            return "```{{image}} {}\n{}".format(uri, options)

    def visit_literal_block(self, language=None, target_mystnb=False):
        if language is None:
            return "```"
        else:
            if target_mystnb:
                return "```{{code-cell}} {0}".format(language)
            else:
                return "```{{code-block}} {0}".format(language)

    def visit_target(self, target):
        return "({})=".format(target)

    def visit_figure(self, uri, options=None):
        if options is None:
            return "```{{figure}} {}".format(uri)
        else:
            options = "\n".join(options)
            return "```{{figure}} {}\n{}".format(uri, options)

    def depart_figure(self):
        return "```"

    def visit_footnote(self, refname):
        return "[^{}]: ".format(refname)

    def depart_footnote(self):
        pass

    def visit_footnote_reference(self, refname):
        return "[^{}]".format(refname)

    def depart_footnote_reference(self):
        pass

    def visit_raw(self, rawformat):
        return "```{{raw}} {}".format(rawformat)

    def depart_raw(self):
        return "```"

    # - Syntax Methods - #

    def visit_directive(self, type, argument=None, options=None):
        directive = "```{" + "{}".format(type) + "}"
        if argument:
            directive += " {}".format(argument)
        if options:
            directive += "\n{}".format("\n".join(options))
        return directive

    def depart_directive(self):
        return "```"

    def visit_role(self, type, content):
        return "{" + str(type) + "}`" + "{}".format(content)

    def depart_role(self):
        return "`"
