import hashlib
import html
import logging
import textwrap
import traceback
import warnings
from typing import Any, Dict, List, Union

import ipyvuetify as v
import pymdownx.emoji
import pymdownx.highlight
import pymdownx.superfences

import nextpy.interfaces.jupyter as widget
# import nextpy.interfaces.jupyter.components.applayout

try:
    import pygments

    has_pygments = True
except ModuleNotFoundError:
    has_pygments = False
else:
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

logger = logging.getLogger(__name__)

html_no_execute_enabled = "<div><i>Solara execution is not enabled</i></div>"


@widget.component
def ExceptionGuard(children=[]):
    exception, clear_exception = widget.use_exception()
    if exception:
        widget.Error(f"Oops, an error occurred: {str(exception)}")
        with widget.Details("Exception details"):
            error = "".join(traceback.format_exception(None, exception, exception.__traceback__))
            widget.pre(error)
    else:
        if len(children) == 1:
            return children[0]
        else:
            widget.column(children=children)


def _run_solara(code):
    ast = compile(code, "markdown", "exec")
    local_scope: Dict[Any, Any] = {}
    exec(ast, local_scope)
    app = None
    if "app" in local_scope:
        app = local_scope["app"]
    elif "Page" in local_scope:
        Page = local_scope["Page"]
        app = widget.components.applayout._AppLayoutEmbed(children=[ExceptionGuard(children=[Page()])])
    else:
        raise NameError("No Page of app defined")
    box = v.Html(tag="div")
    box, rc = widget.render(app, container=box)
    widget_id = box._model_id
    return (
        '<div class="widget-markdown-output v-card v-sheet elevation-7">'
        f'<jupyter-widget widget="IPY_MODEL_{widget_id}">loading widget...</jupyter-widget>'
        '<div class="v-messages">Live output</div></div>'
    )


def _markdown_template(html, style=""):
    return (
        """
<template>
    <div class="widget-markdown rendered_html jp-RenderedHTMLCommon" style=\""""
        + style
        + """\">"""
        + html
        + """</div>
</template>

<script>
module.exports = {
    mounted() {
        if(window.mermaid)
            mermaid.init()
        if(window.MathJax && MathJax.Hub) {
            MathJax.Hub.Queue(['Typeset', MathJax.Hub, this.$el]);
        }
        this.$el.querySelectorAll("a").forEach(a => this.setupRouter(a))
        window.md = this.$el
    },
    methods: {
        setupRouter(a) {
            let href = a.attributes['href'].value;
            if(href.startsWith("./")) {
                // TODO: should we really do this?
                href = location.pathname + href.substr(1);
                a.attributes['href'].href = href;
                // console.log("change href to", href);
            }
            if(href.startsWith("./") || href.startsWith("/")) {
                // console.log("connect link with href=", href, "to router")
                a.onclick = e => {
                    console.log("clicked", href)
                    if(href.startsWith("./")) {
                        widget.router.push(href);
                    } else {
                        widget.router.push(href);
                    }
                    e.preventDefault()
                }
            } else if(href.startsWith("#")) {
                // console.log("connect anchor with href=", href, "to custom javascript due to using <base>")
                href = location.pathname + href;
                a.attributes['href'].value = href;
            } else {
                console.log("href", href, "is not a local link")
            }
        }
    },
    updated() {
        // if the html gets update, re-run mermaid
        if(window.mermaid)
            mermaid.init()
        if(window.MathJax && MathJax.Hub) {
            MathJax.Hub.Queue(['Typeset', MathJax.Hub, this.$el]);
        }
    }
}
</script>
    """
    )


def _highlight(src, language, unsafe_solara_execute, extra, *args, **kwargs):
    """Highlight a block of code"""

    if not has_pygments:
        warnings.warn("Pygments is not installed, code highlighting will not work, use pip install pygments to install it.")
        src_safe = html.escape(src)
        return f"<pre><code>{src_safe}</code></pre>"

    run_src_with_solara = False
    if language == "widget":
        run_src_with_solara = True
        language = "python"

    lexer = get_lexer_by_name(language)
    formatter = HtmlFormatter()
    src_html = pygments.highlight(src, lexer, formatter)

    if run_src_with_solara:
        if unsafe_solara_execute:
            html_widget = _run_solara(src)
            return src_html + html_widget
        else:
            return src_html + html_no_execute_enabled
    else:
        return src_html


# @widget.component
# def MarkdownIt(md_text: str, highlight: List[int] = [], unsafe_solara_execute: bool = False):
#     md_text = textwrap.dedent(md_text)

#     from markdown_it import MarkdownIt as MarkdownItMod
#     from mdit_py_plugins import container, deflist  # noqa: F401
#     from mdit_py_plugins.footnote import footnote_plugin  # noqa: F401
#     from mdit_py_plugins.front_matter import front_matter_plugin  # noqa: F401

#     def highlight_code(code, name, attrs):
#         return _highlight(code, name, unsafe_solara_execute, attrs)

#     md = MarkdownItMod(
#         "js-default",
#         {
#             "html": True,
#             "typographer": True,
#             "highlight": highlight_code,
#         },
#     )
#     md = md.use(container.container_plugin, name="note")
#     html = md.render(md_text)
#     hash = hashlib.sha256((html + str(unsafe_solara_execute) + repr(highlight)).encode("utf-8")).hexdigest()
#     return v.VuetifyTemplate.element(template=_markdown_template(html)).key(hash)


_index = pymdownx.emoji.emojione(None, None)


def _no_deep_copy_emojione(options, md):
    return _index


@widget.component
def markdown(md_text: str, unsafe_allow_html=False, style: Union[str, Dict, None] = None):
    """Renders markdown text

    Renders markdown using https://python-markdown.github.io/

    Math rendering is done using Latex syntax, using https://www.mathjax.org/.

    ## Examples

    ### Basic

    ```widget
    import nextpy.interfaces.jupyter


    @widget.component
    def Page():
        return widget.Markdown(r'''
        # This is a title

        ## This is a subtitle
        This is a markdown text, **bold** and *italic* text is supported.

        ## Math
        Also, $x^2$ is rendered as math.

        Or multiline math:
        $$
        \\int_0^1 x^2 dx = \\frac{1}{3}
        $$

        ''')
    ```

    ## Arguments

     * `md_text`: The markdown text to render
     * `unsafe_solara_execute`: If True, code marked with language "widget" will be executed. This is potentially unsafe
        if the markdown text can come from user input and should only be used for trusted markdown.
     * `style`: A string or dict of css styles to apply to the rendered markdown.

    """
    import markdown

    unsafe_solara_execute = unsafe_allow_html
    md_text = textwrap.dedent(md_text)
    style = widget.util._flatten_style(style)

    def make_markdown_object():
        def highlight(src, language, *args, **kwargs):
            try:
                return _highlight(src, language, unsafe_solara_execute, *args, **kwargs)
            except Exception as e:
                logger.exception("Error highlighting code: %s", src)
                return repr(e)

        return markdown.Markdown(  # type: ignore
            extensions=[
                "pymdownx.highlight",
                "pymdownx.superfences",
                "pymdownx.emoji",
                "toc",  # so we get anchors for h1 h2 etc
                "tables",
            ],
            extension_configs={
                "pymdownx.emoji": {
                    "emoji_index": _no_deep_copy_emojione,
                },
                "pymdownx.superfences": {
                    "custom_fences": [
                        {
                            "name": "mermaid",
                            "class": "mermaid",
                            "format": pymdownx.superfences.fence_div_format,
                        },
                        {
                            "name": "widget",
                            "class": "",
                            "format": highlight,
                        },
                    ],
                },
            },
        )

    md = widget.use_memo(make_markdown_object, dependencies=[unsafe_solara_execute])
    html = md.convert(md_text)
    # if we update the template value, the whole vue tree will rerender (ipvue/ipyvuetify issue)
    # however, using the hash we simply generate a new widget each time
    hash = hashlib.sha256((html + str(unsafe_solara_execute)).encode("utf-8")).hexdigest()
    return v.VuetifyTemplate.element(template=_markdown_template(html, style)).key(hash)
