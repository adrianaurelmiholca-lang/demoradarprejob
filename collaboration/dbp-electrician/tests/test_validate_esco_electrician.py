import copy
import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('esco_checker', ROOT / 'scripts' / 'validate_esco_electrician.py')
esco = importlib.util.module_from_spec(spec)
spec.loader.exec_module(esco)


class EscoCheckerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = esco.candidates(ROOT / 'data' / 'electrician_candidate_skills.csv')
        cls.fixture = json.loads((ROOT / 'tests' / 'fixture_esco_synthetic.json').read_text(encoding='utf-8'))

    def test_21_unique_candidates(self):
        self.assertEqual(len(self.rows), 21)
        self.assertEqual(len({x['skill_uri'] for x in self.rows}), 21)

    def test_hypermedia_path(self):
        found = esco.extraction(self.fixture)
        self.assertEqual(len(found), 2)
        self.assertEqual(found[self.rows[0]['skill_uri']][0], 'essential')

    def test_not_under_root(self):
        broken = copy.deepcopy(self.fixture)
        broken['hasEssentialSkill'] = broken['_links'].pop('hasEssentialSkill')
        with self.assertRaises(ValueError):
            esco.extraction(broken)

    def test_fixture_never_validated_official(self):
        results, _ = esco.verify(self.rows, self.fixture, 'fixture', 'dummyhash', '')
        self.assertIn('FIXTURE_MATCH_NOT_OFFICIAL', {r['validation_status'] for r in results})
        self.assertNotIn('VERIFIED_OFFICIAL', {r['validation_status'] for r in results})

    def test_relation_mismatch_is_flagged(self):
        rows = [dict(self.rows[0])]
        rows[0]['relationship_in_attachment'] = 'optional'
        result, _ = esco.verify(rows, self.fixture, 'live', 'sha', 'https://example.invalid')
        self.assertEqual(result[0]['validation_status'], 'API_RELATION_REQUIRES_REVIEW')
        self.assertIn('RELATION_TYPE_MISMATCH', result[0]['quality_flags'])

    def test_matching_live_is_not_promoted_without_version(self):
        rows = [dict(self.rows[0])]
        rows[0]['skill_label_en_in_attachment'] = 'synthetic label'
        result, _ = esco.verify(rows, self.fixture, 'live', 'sha', 'https://example.invalid')
        self.assertEqual(result[0]['validation_status'], 'API_RELATION_CONFIRMED_VERSION_UNVERIFIED')

    def test_skill_type_mismatch_is_flagged(self):
        rows = [dict(self.rows[0])]
        rows[0]['skill_type_in_attachment'] = 'knowledge'
        result, _ = esco.verify(rows, self.fixture, 'live', 'sha', 'https://example.invalid')
        self.assertIn('SKILL_TYPE_MISMATCH', result[0]['quality_flags'])

    def test_invalid_occupation(self):
        broken = copy.deepcopy(self.fixture)
        broken['uri'] = 'unexpected'
        with self.assertRaises(ValueError):
            esco.extraction(broken)

    def test_offline_fixture_cli(self):
        with tempfile.TemporaryDirectory() as temp:
            rc = esco.main(['--candidates', str(ROOT / 'data/electrician_candidate_skills.csv'),
                            '--fixture', str(ROOT / 'tests/fixture_esco_synthetic.json'), '--out', temp])
            self.assertEqual(rc, 0)
            meta = json.loads((pathlib.Path(temp) / 'esco_electrician_manifest.json').read_text())
            self.assertEqual(meta['mode'], 'fixture')
            self.assertEqual(meta['candidate_count'], 21)
            self.assertFalse((pathlib.Path(temp) / 'esco_electrician_http200_raw.json').exists())


if __name__ == '__main__':
    unittest.main()
