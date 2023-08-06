from typing import Any, Dict

from sphinx.application import Sphinx

from .builders import MystBuilder
from .transform import InterceptAST

DEFAULT_JUPYTEXT_HEADER = """
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
"""


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_builder(MystBuilder)

    app.add_transform(InterceptAST)
    app.add_config_value("tomyst_parser", "myst_nb", "tomyst")
    app.add_config_value("tomyst_static_file_path", ["_static"], "tomyst")
    app.add_config_value("tomyst_debug", False, "tomyst")

    # myst_nb options
    app.add_config_value(
        "tomyst_jupytext_header", DEFAULT_JUPYTEXT_HEADER, "tomyst"
    )  # noqa: E501
    if app.config["tomyst_parser"] == "myst_nb":
        app.add_config_value("tomyst_target_mystnb", True, "tomyst")
    else:
        app.add_config_value("tomyst_target_mystnb", False, "tomyst")

    # Code Block/Cell Languages
    app.add_config_value("tomyst_default_language", "python", "tomyst")
    app.add_config_value(
        "tomyst_language_synonyms",
        ["ipython", "ipython3", "python2", "python3"],
        "tomyst",
    )

    # Adjust generated conf.py based on block tags {{ tomyst-remove-start }}
    # and {{tomyst-remove-finish}}
    app.add_config_value("tomyst_conf_removeblocks", False, "tomyst")
    app.add_config_value("tomyst_conf_dropcontaining", [], "tomyst")

    return {
        "version": "builtin",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
