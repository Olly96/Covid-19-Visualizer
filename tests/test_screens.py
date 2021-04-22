import unittest
from unittest.mock import Mock
from src import screens as screen

class TestStringMethods(unittest.TestCase):
    def test_draw_square(self):
        screens = screen.screen()
        draw_pen = Mock()
        screens.draw_square([25, 35], 20, draw_pen)
        draw_pen.penup.assert_called_once()
        draw_pen.setposition.assert_called_once_with(25, 35)
        draw_pen.pendown.assert_called_once()
        self.assert_(draw_pen.fd.callcount, 4)
        self.assert_(draw_pen.lt.callcount, 4)

    def test_set_default_config(self):
        screens = screen.screen()
        draw_pen = Mock()
        screens.draw_square([25, 35], 20, draw_pen)
        screens.set_default_config(draw_pen, "green", 2)
        draw_pen.speed.assert_called_once()
        draw_pen.speed.assert_any_call(0)
        draw_pen.color.assert_called_once()
        draw_pen.color.assert_any_call("green")
        draw_pen.pensize.assert_called_once()
        draw_pen.pensize.assert_any_call(2)

    def test_create_quarantine_location(self):
        screens = screen.screen()
        draw_pen = Mock()
        screens.set_default_config = Mock()
        screens.draw_square = Mock()
        screens.create_quarantine_location(draw_pen)
        screens.set_default_config.assert_called_once_with(draw_pen, "red", 5)
        screens.draw_square.assert_called_once_with([-50, -370], 50, draw_pen)

    def test_create_random_mov_screen(self):
        screens = screen.screen()
        draw_pen = Mock()
        screens.set_default_config = Mock()
        screens.draw_square = Mock()
        screens.create_random_mov_screen(draw_pen)
        screens.set_default_config.assert_called_once_with(draw_pen)
        screens.draw_square.assert_called_once_with([-250, -250], 500, draw_pen)

    def test_create_central_hub_screen(self):
        screens = screen.screen()
        draw_pen = Mock()
        screens.set_default_config = Mock()
        screens.draw_square = Mock()
        screens.create_central_hub_screen(draw_pen)
        screens.set_default_config.assert_called_once_with(draw_pen)
        screens.draw_square.assert_any_call([-250, -250], 500, draw_pen)
        screens.draw_square.assert_any_call([-20, -20], 20, draw_pen)

    def test_create_communities_screen(self):
        screens = screen.screen()
        draw_pen = Mock()
        screens.set_default_config = Mock()
        screens.draw_square = Mock()
        screens.create_communities_screen(draw_pen)
        screens.set_default_config.assert_called_once_with(draw_pen)
        screens.draw_square.assert_any_call([-300, -300], 620, draw_pen)
        screens.draw_square.assert_any_call([-280, 120], 180, draw_pen)
        screens.draw_square.assert_any_call([-80, 120], 180, draw_pen)
        screens.draw_square.assert_any_call([120, 120], 180, draw_pen)
        screens.draw_square.assert_any_call([-280, -80], 180, draw_pen)
        screens.draw_square.assert_any_call([-80, -80], 180, draw_pen)
        screens.draw_square.assert_any_call([120, -80], 180, draw_pen)
        screens.draw_square.assert_any_call([-280, -280], 180, draw_pen)
        screens.draw_square.assert_any_call([-80, -280], 180, draw_pen)
        screens.draw_square.assert_any_call([120, -280], 180, draw_pen)

