# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import pytest

from nextpy.backend.vars import Var
from nextpy.frontend.components.framer.motion import (
    MotionA,
    MotionArticle,
    MotionAside,
    MotionButton,
    MotionDiv,
    MotionFieldset,
    MotionFooter,
    MotionForm,
    MotionH1,
    MotionH2,
    MotionH3,
    MotionH4,
)


class TestCodeUnderTest:
    """Class to test various components of Framer Motion in Nextpy."""

    # def test_motion_base_instantiation(self):
    #     """Test that MotionBase can be instantiated with no arguments."""
    #     motion_base = MotionBase()
    #     assert isinstance(motion_base, MotionBase)

    def test_motion_a_instantiation(self):
        """Test that MotionA can be instantiated with no arguments."""
        motion_a = MotionA()
        assert isinstance(motion_a, MotionA)

    def test_motion_article_instantiation(self):
        """Test that MotionArticle can be instantiated with no arguments."""
        motion_article = MotionArticle()
        assert isinstance(motion_article, MotionArticle)

    # def test_motion_input_animate_property(self):
    #     """Test MotionInput's animate property with x, y, z values."""
    #     motion_input = MotionInput()
    #     motion_input.x = 1
    #     motion_input.y = 2
    #     motion_input.z = 3
    #     assert motion_input.animate == {"x": 1, "y": 2, "z": 3}

    def test_var_create_type_error(self):
        """Ensure Var.create raises TypeError for JSON-unserializable values."""
        with pytest.raises(TypeError):
            Var.create({"key": lambda x: x})

    def test_motion_aside_instantiation(self):
        """Test that MotionAside can be instantiated with no arguments."""
        motion_aside = MotionAside()
        assert isinstance(motion_aside, MotionAside)

    def test_motion_button_instantiation(self):
        """Test that MotionButton can be instantiated with no arguments."""
        motion_button = MotionButton()
        assert isinstance(motion_button, MotionButton)

    def test_motion_div_instantiation(self):
        """Test that MotionDiv can be instantiated with no arguments."""
        motion_div = MotionDiv()
        assert isinstance(motion_div, MotionDiv)

    def test_motion_fieldset_instantiation(self):
        """Test that MotionFieldset can be instantiated with no arguments."""
        motion_fieldset = MotionFieldset()
        assert isinstance(motion_fieldset, MotionFieldset)

    def test_motion_footer_instantiation(self):
        """Test that MotionFooter can be instantiated with no arguments."""
        motion_footer = MotionFooter()
        assert isinstance(motion_footer, MotionFooter)

    def test_motion_form_instantiation(self):
        """Test that MotionForm can be instantiated with no arguments."""
        motion_form = MotionForm()
        assert isinstance(motion_form, MotionForm)

    def test_motion_h1_instantiation(self):
        """Test that MotionH1 can be instantiated with no arguments."""
        motion_h1 = MotionH1()
        assert isinstance(motion_h1, MotionH1)

    def test_motion_h2_instantiation(self):
        """Test that MotionH2 can be instantiated with no arguments."""
        motion_h2 = MotionH2()
        assert isinstance(motion_h2, MotionH2)

    def test_motion_h3_instantiation(self):
        """Test that MotionH3 can be instantiated with no arguments."""
        motion_h3 = MotionH3()
        assert isinstance(motion_h3, MotionH3)

    def test_motion_h4_instantiation(self):
        """Test that MotionH4 can be instantiated with no arguments."""
        motion_h4 = MotionH4()
        assert isinstance(motion_h4, MotionH4)
