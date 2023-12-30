# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import os
from typing import List

import pytest

from nextpy.build.compiler import compiler, utils
from nextpy.frontend import imports
from nextpy.frontend.imports import ReactImportVar


@pytest.mark.parametrize(
    "fields,test_default,test_rest",
    [
        (
            [ReactImportVar(tag="axios", is_default=True)],
            "axios",
            [],
        ),
        (
            [ReactImportVar(tag="foo"), ReactImportVar(tag="bar")],
            "",
            ["bar", "foo"],
        ),
        (
            [
                ReactImportVar(tag="axios", is_default=True),
                ReactImportVar(tag="foo"),
                ReactImportVar(tag="bar"),
            ],
            "axios",
            ["bar", "foo"],
        ),
    ],
)
def test_compile_import_statement(
    fields: List[ReactImportVar], test_default: str, test_rest: str
):
    """Test the compile_import_statement function.

    Args:
        fields: The fields to import.
        test_default: The expected output of default library.
        test_rest: The expected output rest libraries.
    """
    default, rest = utils.compile_import_statement(fields)
    assert default == test_default
    assert sorted(rest) == test_rest


@pytest.mark.parametrize(
    "import_dict,test_dicts",
    [
        ({}, []),
        (
            {"axios": [ReactImportVar(tag="axios", is_default=True)]},
            [{"lib": "axios", "default": "axios", "rest": []}],
        ),
        (
            {"axios": [ReactImportVar(tag="foo"), ReactImportVar(tag="bar")]},
            [{"lib": "axios", "default": "", "rest": ["bar", "foo"]}],
        ),
        (
            {
                "axios": [
                    ReactImportVar(tag="axios", is_default=True),
                    ReactImportVar(tag="foo"),
                    ReactImportVar(tag="bar"),
                ],
                "react": [ReactImportVar(tag="react", is_default=True)],
            },
            [
                {"lib": "axios", "default": "axios", "rest": ["bar", "foo"]},
                {"lib": "react", "default": "react", "rest": []},
            ],
        ),
        (
            {
                "": [
                    ReactImportVar(tag="lib1.js"),
                    ReactImportVar(tag="lib2.js"),
                ]
            },
            [
                {"lib": "lib1.js", "default": "", "rest": []},
                {"lib": "lib2.js", "default": "", "rest": []},
            ],
        ),
        (
            {
                "": [
                    ReactImportVar(tag="lib1.js"),
                    ReactImportVar(tag="lib2.js"),
                ],
                "axios": [ReactImportVar(tag="axios", is_default=True)],
            },
            [
                {"lib": "lib1.js", "default": "", "rest": []},
                {"lib": "lib2.js", "default": "", "rest": []},
                {"lib": "axios", "default": "axios", "rest": []},
            ],
        ),
    ],
)
def test_compile_imports(import_dict: imports.ImportDict, test_dicts: List[dict]):
    """Test the compile_imports function.

    Args:
        import_dict: The import dictionary.
        test_dicts: The expected output.
    """
    imports = utils.compile_imports(import_dict)
    for import_dict, test_dict in zip(imports, test_dicts):
        assert import_dict["lib"] == test_dict["lib"]
        assert import_dict["default"] == test_dict["default"]
        assert sorted(import_dict["rest"]) == test_dict["rest"]  # type: ignore


def test_compile_stylesheets(tmp_path, mocker):
    """Test that stylesheets compile correctly.

    Args:
        tmp_path: The test directory.
        mocker: Pytest mocker object.
    """
    project = tmp_path / "test_project"
    project.mkdir()

    assets_dir = project / "assets"
    assets_dir.mkdir()

    (assets_dir / "styles.css").touch()
    mocker.patch("nextpy.build.compiler.compiler.Path.cwd", return_value=project)

    stylesheets = [
        "https://fonts.googleapis.com/css?family=Sofia&effect=neon|outline|emboss|shadow-multiple",
        "https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css",
        "/styles.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css",
    ]

    assert compiler.compile_root_stylesheet(stylesheets) == (
        os.path.join(".web", "styles", "styles.css"),
        f"@import url('./tailwind.css'); \n"
        f"@import url('https://fonts.googleapis.com/css?family=Sofia&effect=neon|outline|emboss|shadow-multiple'); \n"
        f"@import url('https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css'); \n"
        f"@import url('@/styles.css'); \n"
        f"@import url('https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css'); \n",
    )


def test_compile_stylesheets_exclude_tailwind(tmp_path, mocker):
    """Test that Tailwind is excluded if tailwind config is explicitly set to None.

    Args:
        tmp_path: The test directory.
        mocker: Pytest mocker object.
    """
    project = tmp_path / "test_project"
    project.mkdir()

    assets_dir = project / "assets"
    assets_dir.mkdir()
    mock = mocker.Mock()

    mocker.patch.object(mock, "tailwind", None)
    mocker.patch("nextpy.build.compiler.compiler.get_config", return_value=mock)

    (assets_dir / "styles.css").touch()
    mocker.patch("nextpy.build.compiler.compiler.Path.cwd", return_value=project)

    stylesheets = [
        "/styles.css",
    ]

    assert compiler.compile_root_stylesheet(stylesheets) == (
        os.path.join(".web", "styles", "styles.css"),
        "@import url('@/styles.css'); \n",
    )


def test_compile_nonexistent_stylesheet(tmp_path, mocker):
    """Test that an error is thrown for non-existent stylesheets.

    Args:
        tmp_path: The test directory.
        mocker: Pytest mocker object.
    """
    project = tmp_path / "test_project"
    project.mkdir()

    assets_dir = project / "assets"
    assets_dir.mkdir()

    mocker.patch("nextpy.build.compiler.compiler.Path.cwd", return_value=project)

    stylesheets = ["/styles.css"]

    with pytest.raises(FileNotFoundError):
        compiler.compile_root_stylesheet(stylesheets)


def test_create_document_root():
    """Test that the document root is created correctly."""
    # Test with no components.
    root = utils.create_document_root()
    assert isinstance(root, utils.Html)
    assert isinstance(root.children[0], utils.DocumentHead)
    # No children in head.
    assert len(root.children[0].children) == 0

    # Test with components.
    comps = [
        utils.NextScript.create(src="foo.js"),
        utils.NextScript.create(src="bar.js"),
    ]
    root = utils.create_document_root(head_components=comps)  # type: ignore
    # Two children in head.
    assert len(root.children[0].children) == 2
