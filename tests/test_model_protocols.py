"""Protocol invariants; torch tests are optional and do not download weights."""
import unittest,importlib.util
from experiments.public_model_diagnostics import strict_letter
from experiments.standard_transformer_study import build_model,grammar

class AnswerProtocol(unittest.TestCase):
    def test_format_is_not_semantic_choice(self):
        self.assertEqual(strict_letter(' \nB\t'),'B')
        for s in ['B: 6','The answer is B.','AB','','A\nB','b']:
            self.assertIsNone(strict_letter(s))

@unittest.skipUnless(importlib.util.find_spec('torch'),'optional CPU torch not installed')
class CausalDecoder(unittest.TestCase):
    def test_future_has_no_forward_or_gradient_effect(self):
        import torch
        torch.manual_seed(144);model=build_model();model.eval()
        original=torch.tensor([[0,1,3,4,2,6,7]])
        changed=original.clone();changed[:,4:]=torch.tensor([[1,2,8]])
        with torch.no_grad():
            self.assertTrue(torch.equal(model(original)[:,:4],model(changed)[:,:4]))
        captured=[]
        def capture(_m,_i,o):o.retain_grad();captured.append(o)
        handle=model.tokens.register_forward_hook(capture)
        model(original)[0,2,1].backward();handle.remove()
        grad=captured[0].grad
        self.assertEqual(float(grad[:,3:].abs().max()),0.)
        self.assertGreater(float(grad[:,:3].abs().max()),0.)
    def test_grammar_rule_and_intervention_labels(self):
        words,docs=grammar();self.assertEqual(len(docs),8)
        for row in docs:
            self.assertEqual(words[row[6]],'meow' if words[row[1]]=='cat' else 'woof')
        # Holding the distractor fixed must not redefine the true label.
        self.assertNotEqual(docs[3][1],docs[4][1])
        self.assertNotEqual(docs[3][6],docs[4][6])
