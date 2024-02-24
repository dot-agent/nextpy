import ipyvue
import traitlets

import nextpy.interfaces.jupyter as widget


class SpinnerSolaraWidget(ipyvue.VueTemplate):
    template_file = (__file__, "spinner-widget.vue")

    size = traitlets.Unicode("64px").tag(sync=True)


@widget.component
def spinner(size="64px"):
    """Spinner component with the Solara logo to indicate the app is busy.

    ### Basic example

    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        widget.SpinnerSolara(size="100px")
    ```

    ## Arguments
     * `size`: Size of the spinner.
    """
    return SpinnerSolaraWidget.element(size=size)
