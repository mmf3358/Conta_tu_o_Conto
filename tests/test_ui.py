import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

AVAILABLE = importlib.util.find_spec('streamlit') is not None
APP = Path(__file__).resolve().parents[1] / 'app.py'


@unittest.skipUnless(AVAILABLE, 'Install Streamlit for interface tests')
class InterfaceTests(unittest.TestCase):
    def test_form_rejects_empty_fields(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(APP)).run()
        self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertTrue(app.error)

    def test_choice_is_persistent_and_story_can_restart(self):
        from streamlit.testing.v1 import AppTest
        engine = Mock()
        engine.generate.return_value = ['A new path.', 'A hidden door.', 'A distant light.']
        with patch('project.ui.get_engine', return_value=engine):
            app = AppTest.from_file(str(APP)).run()
            app.text_input[0].set_value('The castle')
            app.text_input[1].set_value('Ana')
            app.text_input[2].set_value('artist')
            app.selectbox[0].select('English')
            app.button[0].click().run(timeout=10)
            self.assertFalse(app.exception)
            self.assertEqual(engine.generate.call_count, 1)
            app.run()
            self.assertEqual(engine.generate.call_count, 1)
            app.button(key='choice_0_1').click().run(timeout=10)
            self.assertIn('A hidden door.', app.session_state['story'].text)
            self.assertEqual(engine.generate.call_count, 2)
            app.button(key='new_story').click().run()
            self.assertFalse(app.exception)
            self.assertTrue(app.text_input)

    def test_generated_markdown_is_plain_text_in_bounded_cards(self):
        from streamlit.testing.v1 import AppTest
        from project.story import StoryState
        choices = ['- - - A list that must stay text.', 'A very long paragraph. ' * 120,
                   '________________________\n_First blog post_ <script>never run</script>']
        story = StoryState('Title', 'Opening', 'en', alternatives=choices, round=1)
        engine = Mock()
        with patch('project.ui.get_engine', return_value=engine):
            app = AppTest.from_file(str(APP))
            app.session_state['story'] = story
            app.run()
            self.assertFalse(app.exception)
            text = [element.value for element in app.text]
            for choice in choices:
                self.assertIn(choice, text)
            # Generated text is never sent to Markdown, including button labels.
            markdown = '\n'.join(element.value for element in app.markdown)
            self.assertNotIn('First blog post', markdown)
            for i in range(3):
                self.assertEqual(app.button(key=f'choice_1_{i}').label, f'Escolher opção {i + 1}')
            engine.generate.assert_not_called()
