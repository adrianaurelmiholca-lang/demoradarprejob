import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('comparator', ROOT / 'scripts' / 'compare_esco_runs.py')
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)
OCC = compare.OCCUPATION


def payload(ess, opt):
    def rel(u, label='skill'):
        return {'uri': u, 'title': label, 'skillType': 'http://data.europa.eu/esco/skill-type/skill'}
    return {'uri': OCC, '_links': {'hasEssentialSkill': [rel(u) for u in ess],
                                    'hasOptionalSkill': [rel(u) for u in opt]}}


class CompareEscoTest(unittest.TestCase):
    def test_added_removed_changed(self):
        before = {'a': {'relationship': 'essential', 'title': 'Old', 'skill_type': 'skill'},
                  'b': {'relationship': 'optional', 'title': 'Same', 'skill_type': 'skill'}}
        after = {'b': {'relationship': 'essential', 'title': 'Same', 'skill_type': 'skill'},
                 'c': {'relationship': 'essential', 'title': 'New', 'skill_type': 'skill'}}
        result = compare.compare(after, before)
        self.assertEqual([x['uri'] for x in result['new_relations']], ['c'])
        self.assertEqual([x['uri'] for x in result['removed_relations']], ['a'])
        self.assertEqual([x['uri'] for x in result['modified_relations']], ['b'])

    def test_unpacked_relations(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = pathlib.Path(tmp) / 'payload.json'
            file.write_text(json.dumps(payload(['s1'], ['s2'])), encoding='utf-8')
            result, sha = compare.unpack(file)
            self.assertEqual(result['s1']['relationship'], 'essential')
            self.assertEqual(result['s2']['relationship'], 'optional')
            self.assertEqual(len(sha), 64)

    def test_duplicate_uri_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = pathlib.Path(tmp) / 'payload.json'
            file.write_text(json.dumps(payload(['s1'], ['s1'])), encoding='utf-8')
            with self.assertRaises(ValueError):
                compare.unpack(file)

    def test_wrong_occupation_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = pathlib.Path(tmp) / 'payload.json'
            data = payload([], [])
            data['uri'] = 'wrong'
            file.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaises(ValueError):
                compare.unpack(file)


if __name__ == '__main__':
    unittest.main()
