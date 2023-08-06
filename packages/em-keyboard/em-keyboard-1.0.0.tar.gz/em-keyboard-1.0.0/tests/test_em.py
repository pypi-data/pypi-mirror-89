from unittest import TestCase
from unittest.mock import call, patch

from em import cli


class TestCli(TestCase):
    @patch("em.docopt")
    @patch("em.sys.exit")
    @patch("em.xerox.copy")
    @patch("builtins.print")
    def test_star(self, mock_print, mock_xerox, mock_exit, mock_docopt):
        mock_docopt.return_value = {"<name>": ["star"], "--no-copy": None, "-s": None}

        cli()
        mock_xerox.assert_called_once_with("⭐")
        mock_print.assert_called_once_with("Copied! ⭐")

    @patch("em.docopt")
    @patch("em.sys.exit")
    @patch("em.xerox.copy")
    @patch("builtins.print")
    def test_no_copy(self, mock_print, mock_xerox, mock_exit, mock_docopt):
        mock_docopt.return_value = {"<name>": ["star"], "--no-copy": True, "-s": None}

        cli()
        mock_xerox.assert_not_called()
        mock_print.assert_called_once_with("⭐")

    @patch("em.docopt")
    @patch("em.sys.exit")
    @patch("em.xerox.copy")
    @patch("builtins.print")
    def test_search_star(self, mock_print, mock_xerox, mock_exit, mock_docopt):
        mock_docopt.return_value = {"<name>": ["star"], "--no-copy": None, "-s": True}
        expected = (
            "💫  dizzy",
            "⭐  star",
            "✳️  eight_spoked_asterisk",
        )

        cli()
        mock_xerox.assert_not_called()
        for arg in expected:
            self.assertIn(call(arg), mock_print.call_args_list)
