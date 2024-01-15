# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Compiler for the nextpy apps."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Optional, Type

from nextpy import constants
from nextpy.build.compiler import templates, utils
from nextpy.frontend.components.component import (
    BaseComponent,
    Component,
    ComponentStyle,
    CustomComponent,
    StatefulComponent,
)
from nextpy.build.config import get_config
from nextpy.backend.state import BaseState
from nextpy.frontend.imports import ImportDict, ReactImportVar


def _compile_document_root(root: Component) -> str:
    """Compile the document root.

    Args:
        root: The document root to compile.

    Returns:
        The compiled document root.
    """
    return templates.DOCUMENT_ROOT.render(
        imports=utils.compile_imports(root.get_imports()),
        document=root.render(),
    )


def _compile_app(app_root: Component) -> str:
    """Compile the app template component.

    Args:
        app_root: The app root to compile.

    Returns:
        The compiled app.
    """
    return templates.APP_ROOT.render(
        imports=utils.compile_imports(app_root.get_imports()),
        custom_codes=app_root.get_custom_code(),
        hooks=app_root.get_hooks(),
        render=app_root.render(),
    )


def _compile_theme(theme: dict) -> str:
    """Compile the theme.

    Args:
        theme: The theme to compile.

    Returns:
        The compiled theme.
    """
    return templates.THEME.render(theme=theme)


def _compile_contexts(state: Optional[Type[BaseState]]) -> str:
    """Compile the initial state and contexts.

    Args:
        state: The app state.

    Returns:
        The compiled context file.
    """
    is_dev_mode = os.environ.get("NEXTPY_ENV_MODE", "dev") == "dev"
    return (
        templates.CONTEXT.render(
            initial_state=utils.compile_state(state),
            state_name=state.get_name(),
            client_storage=utils.compile_client_storage(state),
            is_dev_mode=is_dev_mode,
        )
        if state
        else templates.CONTEXT.render(is_dev_mode=is_dev_mode)
    )


def _compile_page(
    component: Component,
    state: Type[BaseState],
) -> str:
    """Compile the component given the app state.

    Args:
        component: The component to compile.
        state: The app state.

    Returns:
        The compiled component.
    """
    imports = component.get_imports()
    imports = utils.compile_imports(imports)

    # Compile the code to render the component.
    kwargs = {"state_name": state.get_name()} if state else {}

    return templates.PAGE.render(
        imports=imports,
        dynamic_imports=component.get_dynamic_imports(),
        custom_codes=component.get_custom_code(),
        hooks=component.get_hooks(),
        render=component.render(),
        **kwargs,
    )


def compile_root_stylesheet(stylesheets: list[str]) -> tuple[str, str]:
    """Compile the root stylesheet.

    Args:
        stylesheets: The stylesheets to include in the root stylesheet.

    Returns:
        The path and code of the compiled root stylesheet.
    """
    output_path = utils.get_root_stylesheet_path()

    code = _compile_root_stylesheet(stylesheets)

    return output_path, code


def _compile_root_stylesheet(stylesheets: list[str]) -> str:
    """Compile the root stylesheet.

    Args:
        stylesheets: The stylesheets to include in the root stylesheet.

    Returns:
        The compiled root stylesheet.

    Raises:
        FileNotFoundError: If a specified stylesheet in assets directory does not exist.
    """
    # Add tailwind css if enabled.
    sheets = (
        [constants.Tailwind.ROOT_STYLE_PATH]
        if get_config().tailwind is not None
        else []
    )
    for stylesheet in stylesheets:
        if not utils.is_valid_url(stylesheet):
            # check if stylesheet provided exists.
            stylesheet_full_path = (
                Path.cwd() / constants.Dirs.APP_ASSETS / stylesheet.strip("/")
            )
            if not os.path.exists(stylesheet_full_path):
                raise FileNotFoundError(
                    f"The stylesheet file {stylesheet_full_path} does not exist."
                )
            stylesheet = f"@/{stylesheet.strip('/')}"
        sheets.append(stylesheet) if stylesheet not in sheets else None
    return templates.STYLE.render(stylesheets=sheets)


def _compile_component(component: Component) -> str:
    """Compile a single component.

    Args:
        component: The component to compile.

    Returns:
        The compiled component.
    """
    return templates.COMPONENT.render(component=component)


def _compile_components(components: set[CustomComponent]) -> str:
    """Compile the components.

    Args:
        components: The components to compile.

    Returns:
        The compiled components.
    """
    imports = {
        "react": [ReactImportVar(tag="memo")],
        f"/{constants.Dirs.STATE_PATH}": [ReactImportVar(tag="E"), ReactImportVar(tag="isTrue")],
    }
    component_renders = []

    # Compile each component.
    for component in components:
        component_render, component_imports = utils.compile_custom_component(component)
        component_renders.append(component_render)
        imports = utils.merge_imports(imports, component_imports)

    # Compile the components page.
    return templates.COMPONENTS.render(
        imports=utils.compile_imports(imports),
        components=component_renders,
    )


def _compile_stateful_components(
    page_components: list[BaseComponent],
) -> str:
    """Walk the page components and extract shared stateful components.

    Any StatefulComponent that is shared by more than one page will be rendered
    to a separate module and marked rendered_as_shared so subsequent
    renderings will import the component from the shared module instead of
    directly including the code for it.

    Args:
        page_components: The Components or StatefulComponents to compile.

    Returns:
        The rendered stateful components code.
    """
    all_import_dicts = []
    rendered_components = {}

    def get_shared_components_recursive(component: BaseComponent):
        """Get the shared components for a component and its children.

        A shared component is a StatefulComponent that appears in 2 or more
        pages and is a candidate for writing to a common file and importing
        into each page where it is used.

        Args:
            component: The component to collect shared StatefulComponents for.
        """
        for child in component.children:
            # Depth-first traversal.
            get_shared_components_recursive(child)

        # When the component is referenced by more than one page, render it
        # to be included in the STATEFUL_COMPONENTS module.
        if isinstance(component, StatefulComponent) and component.references > 1:
            # Reset this flag to render the actual component.
            component.rendered_as_shared = False

            rendered_components.update(
                {code: None for code in component.get_custom_code()},
            )
            all_import_dicts.append(component.get_imports())

            # Indicate that this component now imports from the shared file.
            component.rendered_as_shared = True

    for page_component in page_components:
        get_shared_components_recursive(page_component)

    # Don't import from the file that we're about to create.
    all_imports = utils.merge_imports(*all_import_dicts)
    all_imports.pop(
        f"/{constants.Dirs.UTILS}/{constants.PageNames.STATEFUL_COMPONENTS}", None
    )

    return templates.STATEFUL_COMPONENTS.render(
        imports=utils.compile_imports(all_imports),
        memoized_code="\n".join(rendered_components),
    )


def _compile_tailwind(
    config: dict,
) -> str:
    """Compile the Tailwind config.

    Args:
        config: The Tailwind config.

    Returns:
        The compiled Tailwind config.
    """
    return templates.TAILWIND_CONFIG.render(
        **config,
    )


def compile_document_root(head_components: list[Component]) -> tuple[str, str]:
    """Compile the document root.

    Args:
        head_components: The components to include in the head.

    Returns:
        The path and code of the compiled document root.
    """
    # Get the path for the output file.
    output_path = utils.get_page_path(constants.PageNames.DOCUMENT_ROOT)

    # Create the document root.
    document_root = utils.create_document_root(head_components)

    # Compile the document root.
    code = _compile_document_root(document_root)
    return output_path, code


def compile_app(app_root: Component) -> tuple[str, str]:
    """Compile the app root.

    Args:
        app_root: The app root component to compile.

    Returns:
        The path and code of the compiled app wrapper.
    """
    # Get the path for the output file.
    output_path = utils.get_page_path(constants.PageNames.APP_ROOT)

    # Compile the document root.
    code = _compile_app(app_root)
    return output_path, code


def compile_theme(style: ComponentStyle) -> tuple[str, str]:
    """Compile the theme.

    Args:
        style: The style to compile.

    Returns:
        The path and code of the compiled theme.
    """
    output_path = utils.get_theme_path()

    # Create the theme.
    theme = utils.create_theme(style)

    # Compile the theme.
    code = _compile_theme(theme)
    return output_path, code


def compile_contexts(state: Optional[Type[BaseState]]) -> tuple[str, str]:
    """Compile the initial state / context.

    Args:
        state: The app state.

    Returns:
        The path and code of the compiled context.
    """
    # Get the path for the output file.
    output_path = utils.get_context_path()

    return output_path, _compile_contexts(state)


def compile_page(
    path: str, component: Component, state: Type[BaseState]
) -> tuple[str, str]:
    """Compile a single page.

    Args:
        path: The path to compile the page to.
        component: The component to compile.
        state: The app state.

    Returns:
        The path and code of the compiled page.
    """
    # Get the path for the output file.
    output_path = utils.get_page_path(path)

    # Add the style to the component.
    code = _compile_page(component, state)
    return output_path, code


def compile_components(components: set[CustomComponent]):
    """Compile the custom components.

    Args:
        components: The custom components to compile.

    Returns:
        The path and code of the compiled components.
    """
    # Get the path for the output file.
    output_path = utils.get_components_path()

    # Compile the components.
    code = _compile_components(components)
    return output_path, code


def compile_stateful_components(
    pages: Iterable[Component],
) -> tuple[str, str, list[BaseComponent]]:
    """Separately compile components that depend on State vars.

    StatefulComponents are compiled as their own component functions with their own
    useContext declarations, which allows page components to be stateless and avoid
    re-rendering along with parts of the page that actually depend on state.

    Args:
        pages: The pages to extract stateful components from.

    Returns:
        The path and code of the compiled stateful components.
    """
    output_path = utils.get_stateful_components_path()

    # Compile the stateful components.
    page_components = [StatefulComponent.compile_from(page) or page for page in pages]
    code = _compile_stateful_components(page_components)
    return output_path, code, page_components


def compile_tailwind(
    config: dict,
):
    """Compile the Tailwind config.

    Args:
        config: The Tailwind config.

    Returns:
        The compiled Tailwind config.
    """
    # Get the path for the output file.
    output_path = constants.Tailwind.CONFIG

    # Compile the config.
    code = _compile_tailwind(config)
    return output_path, code


def purge_web_pages_dir():
    """Empty out .web directory."""
    utils.empty_dir(constants.Dirs.WEB_PAGES, keep_files=["_app.js"])


class ExecutorSafeFunctions:
    """A helper class designed for easier parallel processing during compilation tasks.

    Key Points:
    - This class is accessible globally, meaning it can be used anywhere in your code.
    - It's especially useful when you're working with multiple processes, like with a ProcessPoolExecutor.
    - Here's how it works:
      1. Before creating a new (child) process, we save any necessary input data in this class.
      2. When a new process starts (forks), it gets its own copy of this class, including the saved input data.
      3. The child process uses this copied data to know what it needs to work on.

    Why is this useful?
    - Sometimes, you can't directly send input data to a new process because it's not in a format that can be easily transferred (not 'picklable'). 
    - Our method bypasses this problem by storing the data in the class, so there's no need to transfer it in the traditional way.
    
    Attributes:
            COMPILE_PAGE_ARGS_BY_ROUTE (dict): A mapping of routes to their respective page compilation arguments.
            COMPILE_APP_APP_ROOT (Component | None): The root component of the app, used in app compilation.
            CUSTOM_COMPONENTS (set[CustomComponent] | None): A set of custom components used in the compilation process.
            HEAD_COMPONENTS (list[Component] | None): A list of components that form the document head.
            STYLE (ComponentStyle | None): The style configuration for components.
            STATE (type[BaseState] | None): The state type used in context compilation.

    Limitations:
    - It can't handle data that can't be transferred (unpicklable) as output.
    - Changes made in a child process won't affect the original data in the parent process.

    """

    COMPILE_PAGE_ARGS_BY_ROUTE = {}
    COMPILE_APP_APP_ROOT: Component | None = None
    CUSTOM_COMPONENTS: set[CustomComponent] | None = None
    HEAD_COMPONENTS: list[Component] | None = None
    STYLE: ComponentStyle | None = None
    STATE: type[BaseState] | None = None

    @classmethod
    def compile_page(cls, route: str):
        """Compile a page.

        Args:
            route: The route of the page to compile.

        Returns:
            The path and code of the compiled page.
        """
        return compile_page(*cls.COMPILE_PAGE_ARGS_BY_ROUTE[route])

    @classmethod
    def compile_app(cls):
        """Compile the app.

        Returns:
            The path and code of the compiled app.

        Raises:
            ValueError: If the app root is not set.
        """
        if cls.COMPILE_APP_APP_ROOT is None:
            raise ValueError("COMPILE_APP_APP_ROOT should be set")
        return compile_app(cls.COMPILE_APP_APP_ROOT)

    @classmethod
    def compile_custom_components(cls):
        """Compile the custom components.

        Returns:
            The path and code of the compiled custom components.

        Raises:
            ValueError: If the custom components are not set.
        """
        if cls.CUSTOM_COMPONENTS is None:
            raise ValueError("CUSTOM_COMPONENTS should be set")
        return compile_components(cls.CUSTOM_COMPONENTS)

    @classmethod
    def compile_document_root(cls):
        """Compile the document root.

        Returns:
            The path and code of the compiled document root.

        Raises:
            ValueError: If the head components are not set.
        """
        if cls.HEAD_COMPONENTS is None:
            raise ValueError("HEAD_COMPONENTS should be set")
        return compile_document_root(cls.HEAD_COMPONENTS)

    @classmethod
    def compile_theme(cls):
        """Compile the theme.

        Returns:
            The path and code of the compiled theme.

        Raises:
            ValueError: If the style is not set.
        """
        if cls.STYLE is None:
            raise ValueError("STYLE should be set")
        return compile_theme(cls.STYLE)

    @classmethod
    def compile_contexts(cls):
        """Compile the contexts.

        Returns:
            The path and code of the compiled contexts.
        """
        return compile_contexts(cls.STATE)