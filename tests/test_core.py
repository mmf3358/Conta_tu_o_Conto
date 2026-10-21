import unittest
from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import Mock, patch

from project.settings import Settings
from project.story import StoryState, choice_label, make_context
from project.engine import ModelUnavailable, StoryEngine, get_engine


class StoryTests(unittest.TestCase):
    def test_all_required_fields_are_checked(self):
        for name, job in [('', 'artist'), ('Ana', ''), ('Ana', '  ')]:
            with self.subTest(name=name, job=job), self.assertRaises(ValueError):
                make_context(name, 20, job, 'Castelo')

    def test_context_languages(self):
        self.assertIn('Era uma vez', make_context('Ana', 20, 'artista', 'Castelo'))
        self.assertIn('enchanted forest', make_context('Ana', 20, 'artist', 'Floresta', 'en'))

    def test_invalid_language(self):
        with self.assertRaises(ValueError):
            make_context('Ana', 20, 'artist', 'Castelo', 'fr')

    def test_reruns_do_not_regenerate(self):
        generator = Mock(return_value=['First.', 'Second.', 'Third.'])
        state = StoryState('Title', 'Opening', 'en')
        state.ensure_choices(generator)
        state.ensure_choices(generator)
        generator.assert_called_once_with('Opening', 'en')

    def test_selection_uses_displayed_choice_once(self):
        state = StoryState('Title', 'Opening', alternatives=['A', 'B', 'C'])
        state.choose(1)
        self.assertEqual(state.text, 'Opening\n\nB')
        self.assertEqual(state.round, 1)
        self.assertEqual(state.alternatives, [])
        with self.assertRaises(ValueError):
            state.choose(1)

    def test_next_round_uses_updated_story(self):
        state = StoryState('Title', 'Opening', 'en', alternatives=['A', 'B', 'C'])
        state.choose(2)
        generator = Mock(return_value=['D', 'E', 'F'])
        state.ensure_choices(generator)
        generator.assert_called_once_with('Opening\n\nC', 'en')

    def test_failed_generation_does_not_destroy_story(self):
        state = StoryState('Title', 'Opening')
        for candidates in [[], ['A', '', 'C'], ['A', 'B']]:
            with self.assertRaises(ValueError):
                state.ensure_choices(Mock(return_value=candidates))
            self.assertEqual(state.text, 'Opening')
            self.assertEqual(state.alternatives, [])

    def test_prompt_bounded_but_export_complete(self):
        state = StoryState('Title', 'A' * 22000, paragraphs=['Latest event'])
        self.assertLessEqual(len(state.prompt), 20000)
        self.assertTrue(state.prompt.endswith('Latest event'))
        self.assertIn('A' * 22000, state.export())

    def test_export_preserves_plain_text(self):
        state = StoryState('<Title>', '<script>text</script>')
        self.assertEqual(state.export(), '<Title>\n\n<script>text</script>\n')

    def test_extract_preview(self):
        self.assertEqual(choice_label('First sentence. Another sentence.'), 'First sentence.')
        self.assertLessEqual(len(choice_label('word ' * 100)), 110)


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = StoryEngine(Settings())

    def test_construction_needs_no_models(self):
        self.assertEqual(self.engine.status(), {'generator_loaded': False, 'translation_models_loaded': 0})

    def test_cached_engine_reused(self):
        get_engine.cache_clear()
        self.assertIs(get_engine(), get_engine())
        get_engine.cache_clear()

    def test_english_skips_translation(self):
        self.engine._translate = Mock(side_effect=AssertionError('Unexpected translation'))
        self.engine._generate_english = Mock(return_value=['A', 'B', 'C'])
        self.assertEqual(self.engine.generate('Opening', 'en'), ['A', 'B', 'C'])
        self.engine._translate.assert_not_called()

    def test_portuguese_translates_context_once_and_three_choices(self):
        self.engine._translate = Mock(side_effect=[['English context'], ['Um', 'Dois', 'Três']])
        self.engine._generate_english = Mock(return_value=['A', 'B', 'C'])
        self.assertEqual(self.engine.generate('Contexto', 'pt'), ['Um', 'Dois', 'Três'])
        self.assertEqual(self.engine._translate.call_args_list[0].args, (['Contexto'], 'pt_en'))
        self.assertEqual(self.engine._translate.call_args_list[1].args, (['A', 'B', 'C'], 'en_pt'))

    def test_bad_input_never_loads_models(self):
        self.engine._load = Mock()
        for text, lang in [('', 'en'), (' ', 'pt'), ('text', 'fr')]:
            with self.assertRaises(ValueError):
                self.engine.generate(text, lang)
        self.engine._load.assert_not_called()

    def test_model_failure_is_not_disguised_as_a_story(self):
        self.engine._generate_english = Mock(side_effect=OSError('Missing weights'))
        with self.assertLogs('project.engine', level='ERROR'), self.assertRaises(ModelUnavailable):
            self.engine.generate('Opening', 'en')

    def test_empty_output_rejected(self):
        self.engine._generate_english = Mock(return_value=['A', '', 'C'])
        with self.assertLogs('project.engine', level='ERROR'), self.assertRaises(ModelUnavailable):
            self.engine.generate('Opening', 'en')

    def test_token_slicing_and_model_cache(self):
        class Tensor:
            shape = (1, 3)
            def to(self, device):
                return self

        tokenizer = Mock()
        tokenizer.eos_token_id = 99
        tokenizer.return_value = {'input_ids': Tensor(), 'attention_mask': Tensor()}
        tokenizer.decode.side_effect = lambda row, **kw: ' '.join(map(str, row))
        model = Mock()
        model.config = SimpleNamespace(max_position_embeddings=1024)
        model.generate.return_value = [[1, 2, 3, 10], [1, 2, 3, 20], [1, 2, 3, 30]]
        self.engine._load = Mock(return_value=(tokenizer, model))
        self.engine._libraries = Mock(return_value=(SimpleNamespace(inference_mode=nullcontext), None, None, None))
        self.assertEqual(self.engine._generate_english('Opening'), ['10', '20', '30'])
        self.engine._generate_english('Next')
        self.engine._load.assert_called_once()
        self.assertEqual(model.generate.call_args.kwargs['num_return_sequences'], 3)
        self.assertEqual(tokenizer.call_args.kwargs['max_length'], 384)
        self.assertEqual(tokenizer.truncation_side, 'left')


class SettingsTests(unittest.TestCase):
    def test_defaults_do_not_point_to_lost_model(self):
        with patch.dict('os.environ', {}, clear=True):
            self.assertEqual(Settings.from_env().model, 'openai-community/gpt2')

    def test_invalid_limits_rejected(self):
        for key, value in [('MAX_NEW_TOKENS', '0'), ('TEMPERATURE', '0'), ('CONTEXT_TOKENS', '1000')]:
            with patch.dict('os.environ', {key: value}, clear=True), self.assertRaises(ValueError):
                Settings.from_env()


if __name__ == '__main__':
    unittest.main()
