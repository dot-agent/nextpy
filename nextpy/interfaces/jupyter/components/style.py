import asyncio
import hashlib
import logging
from pathlib import Path
from typing import Optional, Union, cast

import ipyvuetify as v

try:
    import watchfiles
except ModuleNotFoundError:
    watchfiles = None  # type: ignore

import nextpy.interfaces.jupyter as widget
import nextpy.interfaces.jupyter.server.settings

logger = logging.getLogger("widget.style")


@widget.component
def style(value: Union[str, Path] = ""):
    """Add a custom piece of CSS.

    Note that this is considered an advanced feature, and should be used with caution.

    ## Example

    ```python
    from pathlib import Path
    import nextpy.interfaces.jupyter


    @widget.component
    def Page():
        widget.style(Path("style.css"))
        widget.button("Click me", classes=["company-style-button"])
    ```

    ## Arguments

    - `value`: The CSS string of CSS file to insert into the page. In development mode (the default)
        when a Path argument is passed, the file will be watched for changes, and the CSS will be reloaded when
        the file changes. In production mode, the CSS will be inserted once, and not reloaded.
    """
    css_content_reloaded, set_css_content_reloaded = widget.use_state(cast(Optional[str], None))

    def hot_reload():
        in_production = widget.server.settings.main.mode == "production"
        if not in_production and isinstance(value, Path):

            async def watch():
                try:
                    async for _ in watchfiles.awatch(value):
                        print(value, "changed, reloading css")  # noqa
                        set_css_content_reloaded(cast(Path, value).read_text())
                except RuntimeError:
                    pass  # swallow the RuntimeError: Already borrowed errors from watchfiles
                except Exception:
                    logger.exception("Error watching file")

            if watchfiles:
                future = asyncio.create_task(watch())
                return future.cancel
            else:
                logger.warning("watchfiles not installed, cannot watch file")

    widget.use_effect(hot_reload, [value])

    uuid = widget.use_unique_key()
    if css_content_reloaded is not None:
        css_content = css_content_reloaded
    else:
        css_content = value.read_text() if isinstance(value, Path) else value
    # del value
    hash = hashlib.sha256(css_content.encode("utf-8")).hexdigest()
    # the key is unique for this component + value
    # so that we create a new component if the value changes
    # but we do not remove the css of a component with the same value
    key = uuid + "-" + hash
    # ipyvue does not remove the css itself, so we need to do it manually
    script = (
        """
<script>
module.exports = {
  destroyed() {
    document.getElementById("ipyvue-%s").remove();
  },
};
</script>
    """
        % key
    )

    template = f"""
<template>
    <span style="display: none">
    </span>
</template>
{script}
<style id="{key}">
{css_content}
</style>
    """
    # using .key avoids re-using the template, which causes a flicker (due to ipyvue)
    return v.VuetifyTemplate.element(template=template).key(key)
