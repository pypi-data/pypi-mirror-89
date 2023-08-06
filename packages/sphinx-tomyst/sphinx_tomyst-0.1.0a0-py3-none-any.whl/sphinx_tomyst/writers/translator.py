"""
Translator for RST to MYST Conversion

TODO:
1. Given the way SphinxTranslator works we should remove all unecessary methods
https://github.com/sphinx-doc/sphinx/blob/275d93b5068a4b6af4c912d5bebb2df928416060/sphinx/util/docutils.py#L438

"""

from __future__ import unicode_literals
import re
from docutils import nodes

from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .myst import MystSyntax
from .accumulators import List
from .accumulators import TableBuilder

logger = logging.getLogger(__name__)


class MystTranslator(SphinxTranslator):
    """Myst Translator

    docutils:
        1. https://docutils.sourceforge.io/docs/ref/doctree.html
        2. https://docutils.sourceforge.io/docs/ref/doctree.html#element-reference
    sphinx:
        1. https://www.sphinx-doc.org/en/master/extdev/nodes.html
        2. https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html

    .. todo::
        1. review NotImplementedError to see if visit methods in base classes
           are suitable
    """

    indentation = " " * 2

    # Boolean(State Tracking)
    admonition = False
    attribution = False
    attention = False
    caption = False
    caution = False
    citation = False
    danger = False
    download_reference = False
    error = False
    hint = False
    important = False
    literal = False
    literal_block = False
    math = False
    note = False
    inpage_reference = False
    reference = False
    tip = False
    toctree = False
    topic = False
    warning = False

    # Dict(State Tracking)
    # Block Quote
    block_quote = dict()
    block_quote["in"] = False
    block_quote["type"] = None
    block_quote["collect"] = []
    # Definition
    definition = dict()
    definition["in"] = False
    # Figure
    figure = dict()
    figure["in"] = False
    figure["figure-options"] = None
    # Footnotes
    footnote = {}
    footnote["in"] = False
    footnote_reference = dict()
    footnote_reference["in"] = False
    footnote_reference["autoid"] = []
    # Bullet List
    bullet_list = dict()
    bullet_list["in"] = True
    bullet_list["marker"] = "*"
    bullet_list["level"] = -1
    # Image
    image = dict()
    image["in"] = False
    image["skip-reference"] = False
    # Index
    index = dict()
    index["in"] = False
    index["type"] = None
    # Math
    math_block = dict()
    math_block["in"] = False
    math_block["options"] = []

    # Accumulators
    List = None
    Table = None

    # sphinx.ext.todo
    todo = False

    def __init__(self, document, builder):
        """
        A Myst(Markdown) Translator
        """
        super().__init__(document, builder)
        # Config
        self.target_mystnb = self.builder.config["tomyst_target_mystnb"]
        self.default_ext = ".myst"
        self.default_language = self.builder.config["tomyst_default_language"]
        self.language_synonyms = self.builder.config["tomyst_language_synonyms"]
        self.language_synonyms.append(self.default_language)
        self.debug = self.builder.config["tomyst_debug"]
        self.messages = set()
        # Document Settings
        self.syntax = MystSyntax()
        self.images = []
        self.section_level = 0
        # Support for sphinxcontrib-bibtex data
        if "sphinxcontrib.bibtex" in self.builder.config.extensions:
            self.bibtex_cache = self.builder.env.bibtex_cache

    # ----------#
    # -Document-#
    # ----------#

    def visit_document(self, node):
        self.output = []
        if self.target_mystnb:
            self.output.append(self.builder.config["tomyst_jupytext_header"].lstrip())
            self.add_newline()

    def depart_document(self, node):
        self.body = "".join(self.output)
        if self.messages:
            for msg in self.messages:
                logger.info(msg)

    def unknown_visit(self, node):
        raise NotImplementedError("Unknown node: " + node.__class__.__name__)

    def unknown_departure(self, node):
        pass

    # -------#
    # -Nodes-#
    # -------#

    # -- Text -- #

    def visit_Text(self, node):
        text = node.astext()

        if self.caption:
            raise nodes.SkipNode
        if self.math_block["in"]:
            text = text.strip()
        if self.index["in"] and self.index["type"] == "role":
            presyntax, postsyntax = self.index["role_syntax"]
            text = presyntax + text + postsyntax
            # Switch off index and role
            self.index["in"] = False
            self.index["type"] = None

        self.text = text

    def depart_Text(self, node):
        # Accumulators
        if self.definition["in"]:
            self.definition["text"] += self.text
            return
        if self.List:
            self.List.addto_list_item(self.text)
            return
        if self.Table:
            self.Table.add_item(self.text)
            return
        if self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(self.text)
            return
        # Adjust Spacing
        if self.math_block["in"]:
            self.text = self.text
        if self.literal_block:
            self.text = self.text + "\n"
        if self.caption and self.toctree:  # TODO: Check this condition
            self.text = "# {}".format(self.text)
        self.output.append(self.text)

    # -- Elements --- #

    # docutils.elements.abbreviation
    # https://docutils.sourceforge.io/docs/ref/doctree.html#abbreviation

    # docutils.elements.acroynm
    # https://docutils.sourceforge.io/docs/ref/doctree.html#acronym

    # docutils.elements.address
    # https://docutils.sourceforge.io/docs/ref/doctree.html#address

    # docutils.elements.admonition
    # types: attention, caution, danger, error, hint, important, note, tip, warning
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions

    def visit_admonition(self, node):
        self.admonition = True
        title = self.infer_admonition_attrs(node)
        if title is None:
            raise SyntaxWarning("title attribute cannot be None")
        syntax = self.syntax.visit_admonition(title)
        self.output.append(syntax)
        self.add_newline()

    def infer_admonition_attrs(self, node):
        title = None
        for child in node.children:
            if type(child) is nodes.title:
                title = child.astext()
        return title

    def depart_admonition(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_admonition())
        self.add_newparagraph()
        self.admonition = False

    # docutils.elements.attention
    # https://docutils.sourceforge.io/docs/ref/doctree.html#attention

    def visit_attention(self, node):
        self.attention = True
        self.output.append(self.syntax.visit_directive("attention"))
        self.add_newline()

    def depart_attention(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.attention = False

    # docutils.elements.attribution
    # https://docutils.sourceforge.io/docs/ref/doctree.html#attribution

    def visit_attribution(self, node):
        self.attribution = True
        self.add_newline()
        self.output.append(self.syntax.visit_attribution())

    def depart_attribution(self, node):
        self.attribution = False
        self.add_newline()

    # docutils.elements.author
    # https://docutils.sourceforge.io/docs/ref/doctree.html#author
    # https://docutils.sourceforge.io/docs/ref/doctree.html#authors

    # sphinxcontrib-bibtex
    # https://sphinxcontrib-bibtex.readthedocs.io/en/latest/index.html

    def visit_bibliography(self, node):
        """
        TODO: add support for directive options :cited:, :notcited:, :all:
        and :filter:
        https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html#filtering
        """
        docname = self.builder.current_docname
        bib_id = node.attributes["ids"][0]
        bib_cache = self.bibtex_cache.get_bibliography_cache(docname, bib_id)
        srcdir = self.builder.srcdir
        # Extract Directive Info
        files = [x.replace(srcdir + "/", "") for x in bib_cache.bibfiles]
        options = {}
        if bib_cache.style != "alpha":
            options["style"] = bib_cache.style
        if bib_cache.encoding != "utf-8-sig":
            options["encoding"] = bib_cache.encoding
        if bib_cache.enumtype != "arabic":
            options["enumtype"] = bib_cache.enumtype
        if bib_cache.start != 1:
            options["start"] = bib_cache.start
        if bib_cache.labelprefix != "":
            options["labelprefix"] = bib_cache.labelprefix
        if bib_cache.keyprefix != "":
            options["keyprefix"] = bib_cache.keyprefix
        options = self.myst_options(options)
        directive = self.syntax.visit_directive(
            "bibliography", argument=" ".join(files), options=options
        )
        self.output.append(directive)
        self.add_newline()

    def depart_bibliography(self, node):
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()

    # docutils.element.block_quote
    # class types: epigraph
    # https://docutils.sourceforge.io/docs/ref/doctree.html#block-quote

    def visit_block_quote(self, node):
        self.block_quote["in"] = True
        # Determine class type
        if "epigraph" in node.attributes["classes"]:
            self.block_quote["type"] = "epigraph"
            self.output.append(self.syntax.visit_directive("epigraph"))
            self.add_newline()
        elif "highlights" in node.attributes["classes"]:
            self.block_quote["type"] = "highlights"
            self.output.append(self.syntax.visit_directive("highlights"))
            self.add_newline()
        elif "pull-quote" in node.attributes["classes"]:
            self.block_quote["type"] = "pull-quote"
            self.output.append(self.syntax.visit_directive("pull-quote"))
            self.add_newline()
        else:
            self.block_quote["type"] = "block_quote"
            self.block_quote["collect"] = ["> "]

    def depart_block_quote(self, node):
        if self.block_quote["type"] != "block_quote":
            self.output.append(self.syntax.depart_directive())
            self.add_newparagraph()
        else:
            # Add block_quote lines to output
            linemarker = self.syntax.visit_block_quote()
            if (
                self.block_quote["collect"]
                and self.block_quote["collect"][-1] == "\n\n"
            ):
                self.block_quote["collect"].pop()
            block = "".join(self.block_quote["collect"])
            block = block.replace("\n", "\n{}".format(linemarker))
            self.output.append(block)
            self.add_newparagraph()
            self.block_quote["collect"] = []
        self.block_quote["in"] = False

    # docutils.elements.bullet_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#bullet-list

    def visit_bullet_list(self, node):
        marker = None
        if node.hasattr("bullet"):
            marker = node.attributes["bullet"]
        if not self.List:
            self.List = List(marker=marker)
        else:
            # Finalise any open List Item
            if self.List.list_item:
                self.List.add_list_item()
            self.List = List(marker=marker, parent=self.List)

    def depart_bullet_list(self, node):
        if self.List.parent == "base":
            self.output.append(self.List.to_markdown())
            self.add_newparagraph()
            self.List = None
        else:
            self.List = self.List.add_to_parent()

    # docutils.elements.caption
    # https://docutils.sourceforge.io/docs/ref/doctree.html#caption

    def visit_caption(self, node):
        self.caption = True
        if self.literal_block:
            raise nodes.SkipNode

    def depart_caption(self, node):
        self.caption = False
        if self.toctree:
            self.output.append("\n")

    # docutils.elements.caution
    # https://docutils.sourceforge.io/docs/ref/doctree.html#caution

    def visit_caution(self, node):
        self.caution = True
        self.output.append(self.syntax.visit_directive("caution"))
        self.add_newline()

    def depart_caution(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.caution = False

    # docutils.citations
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#citations

    def visit_citation(self, node):
        self.citation = True
        if "ids" in node.attributes:
            id_text = ""
            for id_ in node.attributes["ids"]:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
        self.output.append(self.syntax.visit_citation(id_text))

    def depart_citation(self, node):
        self.citation = False

    # docutils.elements.citation_reference
    # https://docutils.sourceforge.io/docs/ref/doctree.html#citation-reference

    def visit_citation_reference(self, node):
        citation = node.astext()
        syntax = self.syntax.visit_role("cite", citation)
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        else:
            self.output.append(syntax)
        raise nodes.SkipChildren

    def depart_citation_reference(self, node):
        syntax = self.syntax.depart_role()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        else:
            self.output.append(syntax)

    # docutils.elements.classifier
    # https://docutils.sourceforge.io/docs/ref/doctree.html#classifier

    # docutils.elements.colspec
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#colspec

    def visit_colspec(self, node):
        self.Table.add_column_width(node["colwidth"])

    # docutils.elements.comment
    # https://docutils.sourceforge.io/docs/ref/doctree.html#comment

    def visit_comment(self, node):
        raise nodes.SkipNode

    # sphinx.nodes.compact_paragraph
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html?highlight=compact_paragraph#sphinx.addnodes.compact_paragraph

    def visit_compact_paragraph(self, node):
        pass  # TODO: review

    def depart_compact_paragraph(self, node):
        pass

    # docutils.elements.compound
    # https://docutils.sourceforge.io/docs/ref/doctree.html#compound

    def visit_compound(self, node):
        pass
        # if "toctree-wrapper" in node['classes']:
        #     self.toctree = True

    def depart_compound(self, node):
        pass
        # if "toctree-wrapper" in node['classes']:
        #     self.toctree = False

    # docutils.elements.contact
    # https://docutils.sourceforge.io/docs/ref/doctree.html#contact

    # docutils.elements.container
    # https://docutils.sourceforge.io/docs/ref/doctree.html#container

    def visit_container(self, node):
        pass

    def depart_container(self, node):
        pass

    # docutils.elements.copyright
    # https://docutils.sourceforge.io/docs/ref/doctree.html#copyright

    # docutils.elements.danger
    # https://docutils.sourceforge.io/docs/ref/doctree.html#danger

    def visit_danger(self, node):
        self.danger = True
        self.output.append(self.syntax.visit_directive("danger"))
        self.add_newline()

    def depart_danger(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.danger = False

    # docutils.elements.date
    # https://docutils.sourceforge.io/docs/ref/doctree.html#date

    # docutils.elements.decoration
    # https://docutils.sourceforge.io/docs/ref/doctree.html#decoration

    # docutils.elements.definition
    # https://docutils.sourceforge.io/docs/ref/doctree.html#definition

    def visit_definition(self, node):
        self.definition["in"] = True
        self.definition["text"] = ""

    def depart_definition(self, node):
        syntax = self.syntax.visit_definition(self.definition["text"].rstrip())
        self.output.append(syntax)
        self.definition["text"] = ""
        self.definition["in"] = False

    # docutils.elements.definition_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#definition-list

    def visit_definition_list(self, node):
        msg = """
        CONFIG [definition_list] support for definition list in myst requires:
            myst_deflist_enable = True
        to be specified in the conf.py
        """.strip()
        self.messages.add(msg)

    def depart_definition_list(self, node):
        pass

    # docutils.elements.definition_list_item
    # https://docutils.sourceforge.io/docs/ref/doctree.html#definition-list-item

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        self.add_newparagraph()

    # docutils.elements.description
    # https://docutils.sourceforge.io/docs/ref/doctree.html#description

    # docutils.elements.docinfo
    # https://docutils.sourceforge.io/docs/ref/doctree.html#docinfo

    # docutils.elements.doctest-block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#doctest-block

    # docutils.elements.document
    # https://docutils.sourceforge.io/docs/ref/doctree.html#document

    # sphinx.nodes.download_reference
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#new-inline-nodes

    def visit_download_reference(self, node):
        self.download_reference = True
        html = "<a href={} download>".format(node["reftarget"])
        self.output.append(html)

    def depart_download_reference(self, node):
        self.download_reference = False
        self.output.append("</a>")

    # docutils.elements.emphasis
    # uses: Text
    # https://docutils.sourceforge.io/docs/ref/doctree.html#emphasis

    def visit_emphasis(self, node):
        syntax = self.syntax.visit_italic()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    def depart_emphasis(self, node):
        syntax = self.syntax.depart_italic()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    # docutils.elements.entry
    # uses: table?
    # https://docutils.sourceforge.io/docs/ref/doctree.html#entry

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass

    # docutils.elements.enumerated_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#enumerated-list

    def visit_enumerated_list(self, node):
        """
        .. TODO: should use item_count to make a more readable
        list in markdown output

        .. TODO: add support for different styles of enumerated
        lists. This currently is nested numbered lists
        """
        marker = "1."
        if not self.List:
            self.List = List(marker=marker)
        else:
            # Finalise any open List Item
            if self.List.list_item:
                self.List.add_list_item()
            self.List = List(marker=marker, parent=self.List)

    def depart_enumerated_list(self, node):
        if self.List.parent == "base":
            self.output.append(self.List.to_markdown())
            self.add_newparagraph()
            self.List = None
        else:
            self.List = self.List.add_to_parent()

    # docutils.elements.error
    # https://docutils.sourceforge.io/docs/ref/doctree.html#error

    def visit_error(self, node):
        self.error = True
        self.output.append(self.syntax.visit_directive("error"))
        self.add_newline()

    def depart_error(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.error = False

    # docutils.elements.field
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field

    # TODO: Implement Support for Fields

    def visit_field(self, node):
        # for child in node.children:
        #     if type(child) is nodes.field_name:
        #         field_name = child.astext()
        #     elif type(child) is nodes.field_body:
        #         field_body = child.astext()
        raise nodes.SkipChildren

    # docutils.elements.field_body
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field-body

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

    # docutils.elements.field_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field-list

    def visit_field_list(self, node):
        pass

    def depart_field_list(self, node):
        pass

    # docutils.element.field_name
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field-name

    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    # docutils.figure
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure

    def visit_figure(self, node):
        """
        Note: additional options need parsing in image node
        """
        self.figure["in"] = True
        self.figure["figure-options"] = self.infer_figure_attrs(node)

    def infer_figure_attrs(self, node):
        """
        :align: -> align
        :figwidth: -> width
        :figclass: -> classes
        """
        options = {}
        if node.hasattr("align"):
            align = node.attributes["align"]
            if align not in ["default"]:  # if not set may have default value = default
                options["align"] = align
        if node.hasattr("width"):
            options["figwidth"] = node.attributes["width"]
        if len(node.attributes["classes"]) > 0:
            classes = str(node.attributes["classes"]).strip("[]").strip("'")
            options["figclass"] = classes
        return options

    def depart_figure(self, node):
        self.figure["in"] = False
        self.figure["figure-options"] = None

    # docutils.elements.footer
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footer

    # docutils.elements.footnote
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footnote

    def visit_footnote(self, node):
        self.footnote["in"] = True
        try:
            refname = node.attributes["names"][0]
        except IndexError:
            refname = self.footnote_reference["autoid"].pop(0)
        self.output.append(self.syntax.visit_footnote(refname))

    def depart_footnote(self, node):
        self.footnote["in"] = False

    # docutils.elements.footnote_reference
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footnote-reference

    def visit_footnote_reference(self, node):
        self.footnote_reference["in"] = True
        if node.hasattr("refname"):
            refname = node.attributes["refname"]
        else:
            count = len(self.footnote_reference["autoid"])
            autoid = "autoid_{}".format(count)
            self.footnote_reference["autoid"].append(autoid)
            refname = autoid
        syntax = self.syntax.visit_footnote_reference(refname)
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        else:
            self.output.append(syntax)

    def depart_footnote_reference(self, node):
        self.footnote_reference["in"] = False

    # docutils.elements.generated
    # https://docutils.sourceforge.io/docs/ref/doctree.html#generated

    # docutils.elements.header
    # https://docutils.sourceforge.io/docs/ref/doctree.html#header

    # sphinx.elements.highlightlang
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#sphinx.addnodes.highlightlang

    def visit_highlightlang(self, node):
        if self.debug:
            msg = "[highlightang] typically handeled by transform/post-transform"
            logger.info(msg)

    def depart_highlightlang(self, node):
        pass

    # docutils.elements.hint
    # https://docutils.sourceforge.io/docs/ref/doctree.html#hint

    def visit_hint(self, node):
        self.hint = True
        self.output.append(self.syntax.visit_directive("hint"))
        self.add_newline()

    def depart_hint(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.hint = False

    # docutils.elements.image
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#images

    def visit_image(self, node):
        """
        1. the scale, height and width properties are not combined in this
        as in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image
        """
        self.image["in"] = True
        # Image wrapped within a reference
        if self.reference:
            if self.output[-1] == self.syntax.visit_reference():
                self.output.pop()
                self.image["skip-reference"] = True
        options = self.infer_image_attrs(node)
        if self.figure["in"]:
            figure_options = self.figure["figure-options"]
            options = {**options, **figure_options}  # Figure options take precedence
        options = self.myst_options(options)
        uri = node.attributes["uri"]
        self.images.append(uri)
        if self.figure["in"]:
            syntax = self.syntax.visit_figure(uri, options)
        else:
            syntax = self.syntax.visit_image(uri, options)
        self.output.append(syntax)

    def infer_image_attrs(self, node):
        """
        https://docutils.sourceforge.io/docs/ref/rst/directives.html#image-options
        :alt: -> alt
        :height: -> height
        :width: -> width
        :scale: -> scale
        :align: -> align
        :target: -> node.parent = docutils.nodes.reference
        """
        options = {}
        for option in ["alt", "height", "width", "scale", "align"]:
            if node.hasattr(option):
                options[option] = node.attributes[option]
        if type(node.parent) is nodes.reference:
            if node.parent.hasattr("refuri"):
                options["target"] = node.parent.attributes["refuri"]
        return options

    def depart_image(self, node):
        self.add_newline()
        self.output.append(self.syntax.depart_figure())
        self.add_newparagraph()
        self.image["in"] = False

    # docutils.elements.important
    # https://docutils.sourceforge.io/docs/ref/doctree.html#important

    def visit_important(self, node):
        self.important = True
        self.output.append(self.syntax.visit_directive("important"))
        self.add_newline()

    def depart_important(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.important = False

    # sphinx.nodes.index
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#new-inline-nodes
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#index-generating-markup

    def visit_index(self, node):
        self.index["in"] = True
        inline = True  # default value
        if node.hasattr("inline"):
            inline = node.attributes["inline"]
        if inline:
            self.parse_index_as_role(node)  # Syntax is parsed at Text Node
        else:
            syntax = self.parse_index_as_directive(node)
            self.output.append(syntax)
            self.add_newparagraph()

    def parse_index_as_role(self, node):
        self.index["type"] = "role"
        if len(node.attributes["entries"]) != 1:
            # Issue Warning
            docname = self.builder.current_docname
            line = node.line
            msg = """
            [{}:{}] contains an inline :index: role that cannot be converted.
            """.format(
                docname, line
            ).strip()
            logger.warning(msg)
            raise nodes.SkipNode
        else:
            entry = node.attributes["entries"][0]
            entrytype, entryname, target, ignored, key = entry
            presyntax = "{" + "index" + "}`"
            postsyntax = " <{}: {}>`".format(entrytype, entryname)
            # Save info for parsing at first Text node
            self.index["role_syntax"] = (presyntax, postsyntax)

    def parse_index_as_directive(self, node):
        self.index["type"] = "directive"
        entries = []
        options = []
        for entry in node.attributes["entries"]:
            entrytype, entryname, target, ignored, key = entry
            entries.append("{}: {}".format(entrytype, entryname))
            # Sphinx > 3.0
            if not re.match("index-", target) and target != "":
                option = ":name: {}".format(target)
                if option not in options:
                    options.append(option)
        # -Construct Syntax
        syntax = []
        if len(entries) == 1:
            syntax.append(self.syntax.visit_directive("index", argument=entries[0]))
        else:
            syntax.append(self.syntax.visit_directive("index"))
            syntax += entries
        syntax += options
        syntax.append(self.syntax.depart_directive())
        return "\n".join(syntax)

    def depart_index(self, node):
        if self.index["type"] == "role":
            # Delay state change until parsed by visit_Text
            pass
        else:
            self.index["in"] = False
            self.index["type"] = None

    # docutils.elements.inline
    # uses: container?
    # https://docutils.sourceforge.io/docs/ref/doctree.html#inline

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    # docutils.container.label
    # https://docutils.sourceforge.io/docs/ref/doctree.html#label

    def visit_label(self, node):
        if self.citation:
            self.output.append(self.syntax.visit_label())

    def depart_label(self, node):
        if self.citation:
            self.output.append(self.syntax.depart_label())
            self.add_space()

    # docutils.elements.legend
    # https://docutils.sourceforge.io/docs/ref/doctree.html#legend

    # docutils.elements.line
    # https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#line-blocks

    def visit_line(self, node):
        pass  # TODO: remove? use SphinxTranslator version

    def depart_line(self, node):
        pass

    # docutils.elements.line_block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#line-block

    def visit_line_block(self, node):
        pass  # TODO: remove? use SphinxTranslator version

    def depart_line_block(self, node):
        pass

    # docutils.elements.list_item
    # https://docutils.sourceforge.io/docs/ref/doctree.html#list-item

    def visit_list_item(self, node):
        self.List.start_list_item()

    def depart_list_item(self, node):
        if self.List.list_item:
            self.List.add_list_item()

    # docutils.element.literal
    # https://docutils.sourceforge.io/docs/ref/doctree.html#literal

    def visit_literal(self, node):
        self.literal = True
        if self.download_reference:
            return  # TODO: can we just raise SkipNode?
        syntax = self.syntax.visit_literal()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    def depart_literal(self, node):
        if self.download_reference:
            return
        syntax = self.syntax.depart_literal()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)
        self.literal = False

    # docutils.element.literal_block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#literal-block
    #

    def visit_literal_block(self, node):
        self.literal_block = True
        options = self.infer_literal_block_attrs(node)
        # Check for literalinclude::
        if node.hasattr("source"):
            fl = node.attributes["source"]
            srcdir = self.builder.srcdir + "/"
            fl = fl.replace(srcdir, "")
            syntax = self.syntax.visit_directive("literalinclude", argument=fl)
        # Check for code-block::
        elif node.hasattr("language"):
            self.nodelang = node.attributes["language"].strip()
            if self.nodelang == "default":
                self.nodelang = self.default_language
            # A code-block that isn't the same as the kernel
            if self.nodelang not in self.language_synonyms:
                # code-block (no execution via myst_nb)
                syntax = self.syntax.visit_literal_block(
                    language=self.nodelang, target_mystnb=False
                )
            elif "no-execute" in node.attributes["classes"]:
                # code-block (no execution via myst_nb)
                syntax = self.syntax.visit_literal_block(
                    language=self.nodelang, target_mystnb=False
                )
            else:
                # code-cell (execution code blocks)
                syntax = self.syntax.visit_literal_block(
                    language=self.nodelang, target_mystnb=self.target_mystnb
                )
        else:
            syntax = self.syntax.visit_literal_block(target_mystnb=self.target_mystnb)
        # option block parsing
        if options != []:
            options = "\n".join(options)
            syntax = syntax + "\n" + options
        if self.List:
            self.List.addto_list_item(syntax)
            self.List.addto_list_item("\n")
        else:
            self.output.append(syntax)
            self.add_newline()
        if node.hasattr("source"):
            raise nodes.SkipChildren  # Skip contents for .. literalinclude::

    def infer_literal_block_attrs(self, node):
        """
        :dedent: option cannot be inferred as text is already altered
        but could be a PR upstream in
        sphinx/directives/code.py -> literal['dedent'] = self.options['dedent']

        # TODO: Rework this function to be dict(options)
        """
        attributes = node.attributes
        options = []
        options.append("---")
        if node.hasattr("linenos") and attributes["linenos"]:
            options.append("linenos:")
        if node.hasattr("highlight_args"):
            if "linenostart" in attributes["highlight_args"]:
                if attributes["highlight_args"]["linenostart"] > 1:
                    options.append(
                        "lineno-start: {}".format(
                            attributes["highlight_args"]["linenostart"]
                        )
                    )
            if "hl_lines" in attributes["highlight_args"]:
                vals = str(attributes["highlight_args"]["hl_lines"]).strip("[]")
                options.append("emphasize-lines: {}".format(vals))
        if type(node.parent) is nodes.container:
            if node.parent.hasattr("names"):
                vals = str(node.parent.attributes["names"]).strip("[]").strip("'")
                options.append("name: {}".format(vals))
            # Check children for caption
            for child in node.parent.children:
                if type(child) is nodes.caption:
                    caption = child.astext()
                    options.append("caption: {}".format(caption))
        if node.hasattr("force") and attributes["force"]:
            options.append("force:")
        # Parse `code-cell` options
        if self.target_mystnb:
            tags = []
            if "skip-test" in node.attributes["classes"]:
                tags.append("raises-exception")
            if "hide-output" in node.attributes["classes"]:
                tags.append("hide-output")
            if "collapse" in node.attributes["classes"]:
                tags.append("output_scroll")
            if tags:
                options.append("tags: [" + ", ".join(tags) + "]")
        # Parse `literalinclude` options
        # Note: Not all options are current supported
        # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html?highlight=literalinclude#directive-literalinclude
        if node.hasattr("source"):
            if node.hasattr("language"):
                options.append("language: {}".format(node.attributes["language"]))
        options.append("---")
        if len(options) == 2:
            options = []
        return options

    def depart_literal_block(self, node):
        syntax = self.syntax.depart_literal_block()
        if self.List:
            self.List.addto_list_item("\n")
            self.List.addto_list_item(syntax)
            self.List.addto_list_item("\n")
        else:
            self.output.append(syntax)
            self.add_newparagraph()
        self.literal_block = False

    # docutils.element.math
    # https://docutils.sourceforge.io/docs/ref/doctree.html#math

    def visit_math(self, node):
        """Inline Math"""
        self.math = True
        syntax = self.syntax.visit_math()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    def depart_math(self, node):
        syntax = self.syntax.depart_math()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)
        self.math = False

    # docutils.element.math_block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#math-block

    def visit_math_block(self, node):
        self.math_block["in"] = True
        self.math_block["options"] = self.infer_math_block_attrs(node)
        math_block = []
        if self.math_block["options"]:
            math_block.append(self.syntax.visit_directive("math"))
            math_block.append(self.math_block["options"] + "\n")
        else:
            math_block.append(self.syntax.visit_math_block())
        syntax = "\n".join(math_block) + "\n"
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    def infer_math_block_attrs(self, node):
        options = []
        if node["label"]:
            options.append(":label: {}".format(node["label"]))
        if node.hasattr("nowrap"):
            if node["nowrap"]:
                options.append(":nowrap:")
        return "\n".join(options)

    def depart_math_block(self, node):
        math_block = ["\n"]
        if self.math_block["options"]:
            math_block.append(self.syntax.depart_directive())
        else:
            math_block.append(self.syntax.depart_math_block())
        syntax = "".join(math_block)
        if self.List:
            self.List.addto_list_item(syntax + "\n")
        elif self.Table:
            self.Table.add_item(syntax + "\n\n")
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax + "\n\n")
        elif self.definition["in"]:
            self.definition["text"] += syntax + "\n\n"
        else:
            self.output.append(syntax + "\n\n")
        self.math_block["in"] = False

    # docutils.elements.paragraph
    # https://docutils.sourceforge.io/docs/ref/doctree.html#paragraph

    # docutils.elements.note
    # https://docutils.sourceforge.io/docs/ref/doctree.html#note

    def visit_note(self, node):
        self.note = True
        self.output.append(self.syntax.visit_directive("note"))
        self.add_newline()

    def depart_note(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.note = False

    # sphinx.nodes.only
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#special-nodes
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-only

    def visit_only(self, node):
        target = node.attributes["expr"]
        self.output.append(self.syntax.visit_directive("only", argument=target))
        self.add_newline()

    def depart_only(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()

    # docutils.elements.option
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-argument
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-group
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-list-item
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-string

    # docutils.elements.organization
    # https://docutils.sourceforge.io/docs/ref/doctree.html#organization

    # docutils.elements.paragraph
    # https://docutils.sourceforge.io/docs/ref/doctree.html#paragraph

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self.List:
            if self.List.list_item:
                self.List.addto_list_item("<\\paragraph>")  # Used for Formating
            return
        if self.block_quote["in"] and self.block_quote["type"] != "block_quote":
            self.add_newline()
            return
        if self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append("\n\n")
            return
        if self.definition["in"]:
            self.definition["text"] += "\n\n"
            return
        self.add_newparagraph()

    # docutils.elements.pending
    # https://docutils.sourceforge.io/docs/ref/doctree.html#pending

    def visit_pending(self, node):
        if self.debug:
            msg = "[pending] typically handeled by transform/post-transform"
            logger.info(msg)

    def depart_pending(self, node):
        pass

    # sphinx.pending_xref
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#sphinx.addnodes.pending_xref
    # TODO: should visit_citation_references be implemented here?

    def visit_pending_xref(self, node):
        reftype = node.attributes["reftype"]
        target = node.attributes["reftarget"]
        linktext = node.astext()
        if reftype == "eq":
            content = "{}".format(target)
        else:
            # doc, ref style links
            content = "{} <{}>".format(linktext, target)
        syntax = self.syntax.visit_role(reftype, content)
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        else:
            self.output.append(syntax)
        raise nodes.SkipChildren

    def depart_pending_xref(self, node):
        syntax = self.syntax.depart_role()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        else:
            self.output.append(syntax)

    # docutils.elements.problematic
    # https://docutils.sourceforge.io/docs/ref/doctree.html#problematic

    def visit_problematic(self, node):
        pass

    def depart_problematic(self, node):
        pass

    # docutils.elements.raw
    # https://docutils.sourceforge.io/docs/ref/doctree.html#raw

    def visit_raw(self, node):
        self.raw = True
        rawformat = node.attributes["format"]
        # options = self.infer_raw_attrs(node)
        self.output.append(self.syntax.visit_raw(rawformat))
        self.add_newline()

    def infer_raw_attrs(self, node):
        # options = {}
        if node.hasattr("source") and self.debug:
            fn = self.builder.current_docname
            line = node.line
            msg = "[{}:{}] raw directive specifies a source file. The contents of this \
file will be included in the myst directive".format(
                fn, line
            )
            logger.info(msg)
        # TODO: add support for :url and :encoding:

    def depart_raw(self, node):
        self.add_newline()
        self.output.append(self.syntax.depart_raw())
        self.add_newparagraph()
        self.raw = False

    # docutils.elements.references
    # https://docutils.sourceforge.io/docs/ref/doctree.html#reference

    # TODO: rework visit_reference, depart_reference
    # TODO: update to include syntax from self.syntax

    def visit_reference(self, node):
        self.reference = True
        syntax = self.syntax.visit_reference()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.figure["in"] or self.image["in"]:
            pass
        else:
            self.output.append(syntax)

    def depart_reference(self, node):
        # subdirectory = False
        formatted_text = ""

        if self.image["skip-reference"]:
            self.image["skip-reference"] = False
            self.reference = False
            return

        if self.topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = node.astext().replace(" ", "-")
            formatted_text = "](#{})".format(uri_text)
            # self.output.append(formatted_text)
        else:
            # if refuri exists, then it includes id reference
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if (
                    "internal" in node.attributes
                    and node.attributes["internal"] is True
                ):
                    refuri = self.add_extension_to_inline_link(refuri, self.default_ext)
            else:
                # in-page link
                if "refid" in node:
                    refid = node["refid"]
                    self.inpage_reference = True
                    # markdown doesn't handle closing brackets very well replace with %28 and %29 # noqa: E501
                    refid = refid.replace("(", "%28")
                    refid = refid.replace(")", "%29")
                    # markdown target
                    refuri = "#{}".format(refid)
                # error
                else:
                    self.error("Invalid reference")
                    refuri = ""

            # TODO: review if both %28 replacements necessary in this function?
            #      Propose delete above in-link refuri
            # ignore adjustment when targeting pdf as pandoc doesn't parse %28 correctly
            refuri = refuri.replace(
                "(", "%28"
            )  # Special case to handle markdown issue with reading first )
            refuri = refuri.replace(")", "%29")
            formatted_text = self.syntax.depart_reference(refuri)

        # if there is a list add to it, else add it to the output
        if self.List:
            self.List.addto_list_item(formatted_text)
        elif self.figure["in"] or self.image["in"]:
            pass
        else:
            self.output.append(formatted_text)
        self.reference = False

    # docutils.elements.revision
    # https://docutils.sourceforge.io/docs/ref/doctree.html#revision

    # docutils.elements.row
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#row

    def visit_row(self, node):
        self.Table.start_row()

    def depart_row(self, node):
        self.Table.end_row()

    # docutil.elements.rubric
    # https://docutils.sourceforge.io/docs/ref/doctree.html#rubric

    def visit_rubric(self, node):
        if len(node.children) != 0 and node.children[0].astext() in ["Footnotes"]:
            raise nodes.SkipNode

    def depart_rubric(self, node):
        pass

    # docutils.elements.section
    # https://docutils.sourceforge.io/docs/ref/doctree.html#section

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    # docutils.elements.sidebar
    # https://docutils.sourceforge.io/docs/ref/doctree.html#sidebar

    # docutils.elements.status
    # https://docutils.sourceforge.io/docs/ref/doctree.html#status

    # docutils.elements.strong
    # https://docutils.sourceforge.io/docs/ref/doctree.html#strong

    def visit_strong(self, node):
        syntax = self.syntax.visit_bold()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    def depart_strong(self, node):
        syntax = self.syntax.depart_bold()
        if self.List:
            self.List.addto_list_item(syntax)
        elif self.Table:
            self.Table.add_item(syntax)
        elif self.block_quote["in"] and self.block_quote["type"] == "block_quote":
            self.block_quote["collect"].append(syntax)
        elif self.definition["in"]:
            self.definition["text"] += syntax
        else:
            self.output.append(syntax)

    # docutils.elements.subscript
    # https://docutils.sourceforge.io/docs/ref/doctree.html#subscript
    # https://docutils.sourceforge.io/docs/ref/doctree.html#substitution-definition
    # https://docutils.sourceforge.io/docs/ref/doctree.html#substitution-reference

    # docutils.elements.subtitle
    # https://docutils.sourceforge.io/docs/ref/doctree.html#subtitle

    # docutils.elements.superscript
    # https://docutils.sourceforge.io/docs/ref/doctree.html#superscript

    # docutils.elements.system_message
    # https://docutils.sourceforge.io/docs/ref/doctree.html#system-message

    def visit_system_message(self, node):
        if self.debug:
            msg = "[system_mesage] typically handeled by transform/post-transform\n\n{}".format(  # noqa: E501
                node.astext()
            )
            logger.info(msg)
        raise nodes.SkipNode

    def depart_system_message(self, node):
        pass

    # docutils.elements.table
    # Category: Compound
    # https://docutils.sourceforge.io/docs/ref/doctree.html#table

    def visit_table(self, node):
        self.Table = TableBuilder(node)

    def depart_table(self, node):
        markdown = self.Table.to_markdown()
        self.output.append(markdown)
        self.Table = None
        self.add_newline()

    # docutils.elements.target
    # https://docutils.sourceforge.io/docs/ref/doctree.html#target

    def visit_target(self, node):
        if "refid" in node.attributes:
            targetname = node.attributes["refid"]
        elif "refuri" in node.attributes:
            # refuri handled in visit_reference
            raise nodes.SkipNode
        elif len(node.attributes["names"]) == 1:
            targetname = node.attributes["names"][0]
        else:
            raise nodes.SkipNode
        self.output.append(self.syntax.visit_target(targetname))
        self.add_newline()

    def depart_target(self, node):
        pass

    # docutils.elements.tbody
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#tbody

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    # docutils.element.term
    # https://docutils.sourceforge.io/docs/ref/doctree.html#term

    def visit_term(self, node):
        self.output.append(node.astext())
        self.add_newline()
        raise nodes.SkipChildren

    def depart_term(self, node):
        pass

    # docutils.element.tgroup
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#tgroup

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    # docutils.element.thead
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#thead

    def visit_thead(self, node):
        pass

    def depart_thead(self, node):
        """ create the header line which contains the alignment for each column """
        self.Table.add_header_line("|")

    # docutils.element.tip
    # https://docutils.sourceforge.io/docs/ref/doctree.html#tip

    def visit_tip(self, node):
        self.tip = True
        self.output.append(self.syntax.visit_directive("tip"))
        self.add_newline()

    def depart_tip(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.tip = False

    # docutils.element.title
    # https://docutils.sourceforge.io/docs/ref/doctree.html#title

    def visit_title(self, node):
        if self.admonition:
            raise nodes.SkipNode
        elif self.topic:
            # this prevents from making it a subsection from section
            self.output.append(self.syntax.visit_title(self.section_level + 1))
            self.add_space()
        elif self.Table:
            self.Table.add_title(node)
        else:
            self.output.append(self.syntax.visit_title(self.section_level))
            self.add_space()

    def depart_title(self, node):
        if not self.Table:
            self.add_newparagraph()

    # docutils.element.title_reference
    # https://docutils.sourceforge.io/docs/ref/doctree.html#title-reference

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    # sphinx.nodes.toctree
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#sphinx.addnodes.toctree

    def visit_toctree(self, node):
        self.toctree = True
        listing, options = self.infer_toctree_attrs(node)
        options = self.myst_options(options)
        self.output.append(self.syntax.visit_directive("toctree", options=options))
        self.add_newparagraph()
        self.output.append("\n".join(listing))
        self.add_newline()

    def infer_toctree_attrs(self, node):
        """
        https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree
        """
        # Parse File Listing
        listing = []
        if node.hasattr("entries"):
            for entry in node.attributes["entries"]:
                title, fn = entry
                listing.append(fn)
        # Parse Options
        options = {}
        if node.hasattr("hidden"):
            if node.attributes["hidden"]:
                options["hidden"] = ""
        if node.hasattr("numbered"):
            if node.attributes["numbered"] == 999:  # top level default value
                options["numbered"] = ""
        if node.hasattr("caption"):
            if node.attributes["caption"] is not None:
                options["caption"] = node.attributes["caption"]
        # TODO: implement :name: option
        if node.hasattr("titlesonly"):
            if node.attributes["titlesonly"]:
                options["titlesonly"] = ""
        if node.hasattr("glob"):
            if node.attributes["glob"]:
                options["glob"] = ""
        if node.hasattr("reversed"):
            if node.attributes["reversed"]:
                options["reversed"] = ""
        if node.hasattr("includehidden"):
            if node.attributes["includehidden"]:
                options["includehidden"] = ""
        if node.hasattr("maxdepth"):
            if node.attributes["maxdepth"] != -1:  # default value -1
                options["maxdepth"] = node.attributes["maxdepth"]
        return listing, options

    def depart_toctree(self, node):
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.toctree = False

    # docutils.elements.topic
    # https://docutils.sourceforge.io/docs/ref/doctree.html#topic

    def visit_topic(self, node):
        # docutils.contents (https://docutils.sourceforge.io/docs/ref/rst/directives.html#table-of-contents) # noqa: E501
        if "contents" in node.attributes["classes"]:
            title, options = self.infer_contents_attrs(node)
            options = self.myst_options(options)
            self.output.append(self.syntax.visit_directive("contents", title, options))
            self.add_newline()
            raise nodes.SkipChildren
        self.topic = True

    def infer_contents_attrs(self, node):
        title, options = None, {}
        for child in node.children:
            if type(child) is nodes.title:
                title = (
                    child.astext()
                )  # This will add default "Contents" to myst output
            if type(child) is nodes.pending:
                if "depth" in child.details:
                    options["depth"] = child.details["depth"]
                if "local" in child.details:
                    options["local"] = ""
                if "backlinks" in child.details:
                    options["backlinks"] = child.details["backlinks"]
                if "class" in child.details:
                    options["class"] = ", ".join(child.details["class"])
        return title, options

    def depart_topic(self, node):
        if "contents" in node.attributes["classes"]:
            self.output.append(self.syntax.depart_directive())
            self.add_newparagraph()
        self.topic = False

    # docutils.elements.transition
    # https://docutils.sourceforge.io/docs/ref/doctree.html#transition

    def visit_transition(self, node):
        docname = self.builder.current_docname
        msg = """
        SKIP {} [transition] objects are not supported by sphinx-tomyst
        """.format(
            docname
        ).strip()
        logger.warning(msg)
        pass

    def depart_transition(self, node):
        pass

    # docutils.elements.version
    # https://docutils.sourceforge.io/docs/ref/doctree.html#version

    # docutils.elements.warning
    # https://docutils.sourceforge.io/docs/ref/doctree.html#warning

    def visit_warning(self, node):
        self.warning = True
        self.output.append(self.syntax.visit_directive("warning"))
        self.add_newline()

    def depart_warning(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.warning = False

    # -Extension Support-#

    def visit_todo_node(self, node):
        """ Support for sphinx.ext.todo """
        self.todo = True
        self.output.append(self.syntax.visit_directive("todo"))
        self.add_newline()

    def depart_todo_node(self, node):
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.todo = False

    # -----------#
    # -Utilities-#
    # -----------#

    def strip_whitespace(self, text):
        text = text.split("\n")
        text = [item.strip() for item in text]
        return "\n".join(text)

    def add_space(self, n=1):
        self.output.append(" " * n)

    def add_newline(self, n=1):
        self.output.append("\n" * n)

    def remove_newline(self):
        if self.output[-1] == "\n\n":
            self.output[-1] = "\n"
        elif self.output[-1] == "\n":
            self.output.pop()

    def add_newparagraph(self):
        self.output.append("\n\n")

    # TODO: Review Utilities below

    @classmethod
    def split_uri_id(cls, uri):
        regex = re.compile(r"([^\#]*)\#?(.*)")
        return re.search(regex, uri).groups()

    @classmethod
    def add_extension_to_inline_link(cls, uri, ext):
        """
        Removes an extension such as `html` and replaces with `ipynb`

        .. todo::

            improve implementation for references (looks hardcoded)
        """
        if "." not in uri:
            if len(uri) > 0 and uri[0] == "#":
                return uri
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)
        # adjust relative references
        elif "../" in uri:
            # uri = uri.replace("../", "")
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)

        return uri

    @staticmethod
    def strip_blank_lines_in_end_of_block(line_text):
        lines = line_text.split("\n")

        for line in range(len(lines)):
            if len(lines[-1].strip()) == 0:
                lines = lines[:-1]
            else:
                break

        return "\n".join(lines)

    # Myst Support
    @staticmethod
    def myst_options(options):
        """return myst options block"""
        num_options = len(options.keys())
        myst_options = []
        if num_options == 0:
            return myst_options
        elif num_options < 2:  # TODO parameterise this in conf.py
            for option, option_val in options.items():
                myst_options.append(":{}: {}".format(option, option_val).rstrip())
            return myst_options
        else:
            myst_options.append("---")
            for item in sorted(options.keys()):
                myst_options.append("{}: {}".format(item, options[item]))
            myst_options.append("---")
            return myst_options
