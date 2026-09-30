"""Fictional evidence catalogs, metadata safety, and guarded regeneration."""
import json
from pathlib import Path
import re
import shutil
import struct
import sys
import tempfile
import unittest
from urllib.parse import unquote
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
import brain
import intake
import source_catalog


class SourceCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='brain fictional catalog ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'toolkit'
        self.root.mkdir()
        (self.root / '.brain').write_text('brain:2\n')
        shutil.copytree(REPO / 'templates', self.root / 'templates')
        brain.new_project(self.root, 'alpha')
        brain.new_project(self.root, 'beta')
        self.source = self.base / 'Fictional Source (draft).md'
        self.source.write_text('A fictional observation; authority remains unsettled.\n')
        self.source_id = 'local:fictional:source-001'
        self.catalog = self.root / 'Projects/alpha/SOURCES.md'

    def capture(self, projects=('alpha',), source_id=None, **kwargs):
        return intake.capture(self.root, self.source, source_id or self.source_id, projects, **kwargs)

    def describe(self, record, **changes):
        description = {'title': 'Fictional research interview', 'source_type': 'primary_evidence',
                       'known_gaps': ['The sample may not represent all readers.'], 'evidence_links': []}
        description.update(changes)
        return source_catalog.describe(self.root, record['source_id'], record['sha256'], description)

    def synthesis(self, record, project='alpha', name='interview.md'):
        path = self.root / 'Projects' / project / 'Ingestion' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Fictional source-linked interpretation.\n')
        intake.mark_complete(self.root, record['source_id'], record['sha256'], project, f'Ingestion/{name}')
        return path

    def generated(self):
        result = source_catalog.generate(self.root, 'alpha')
        return result, self.catalog.read_text()

    def assert_links_resolve(self, content):
        for href in re.findall(r'\]\(([^)]+)\)', content):
            self.assertTrue((self.catalog.parent / unquote(href)).is_file(), href)

    def test_catalog_answers_inventory_uncertainty_and_links(self):
        record = self.capture(revision='revision one')
        report = self.root / 'maintenance/fictional-review.md'
        report.write_text('Fictional evidence for the recorded uncertainty.\n')
        self.describe(record, evidence_links=[{'label': 'Review evidence', 'path': 'maintenance/fictional-review.md'}])
        self.synthesis(record)
        result, content = self.generated()
        self.assertEqual(result['sources'], 1)
        self.assertEqual(result['recorded_gaps'], 1)
        self.assertEqual(result['pending_interpretations'], 0)
        for phrase in ('What remains uncertain', 'Primary evidence', source_catalog.text(self.source.name), self.source_id,
                       record['sha256'], 'UTC capture time', 'revision one', 'may not represent',
                       'Captured original', 'Read workspace interpretation', 'Review evidence'):
            self.assertIn(phrase, content)
        self.assert_links_resolve(content)

    def test_same_identity_versions_group_without_losing_revision_history(self):
        first = self.capture(revision='provider-v1')
        self.describe(first, source_type='imported_summary')
        self.capture(revision='provider-v1-renamed')
        self.source.write_text('A fictional changed-content version.\n')
        second = self.capture(revision='provider-v2')
        self.describe(second, title='Updated fictional interview')
        result, content = self.generated()
        self.assertEqual(result['sources'], 1)
        self.assertEqual(result['content_versions'], 2)
        self.assertIn(first['sha256'], content)
        self.assertIn(second['sha256'], content)
        self.assertIn('provider-v1-renamed', content)
        self.assertIn('Imported wiki summary (secondary evidence)', content)
        self.assertIn('follow its cited primary evidence', content)
        self.assert_links_resolve(content)

    def test_multi_workspace_scope_and_paused_workspace(self):
        shared = self.capture(('alpha', 'beta'))
        self.describe(shared)
        self.synthesis(shared, 'beta')
        self.capture(('beta',), source_id='local:fictional:beta-only')
        registry_path = self.root / 'registry.json'
        registry = json.loads(registry_path.read_text())
        registry['workspaces'][0].update(status='paused', planning=False, review=False)
        registry_path.write_text(json.dumps(registry))
        before = registry_path.read_bytes()
        result, content = self.generated()
        self.assertEqual(result['sources'], 1)
        self.assertEqual(result['pending_interpretations'], 1)
        self.assertNotIn('beta-only', content)
        self.assertNotIn('Projects/beta', content)
        self.assertEqual(registry_path.read_bytes(), before)

    def test_unknown_metadata_is_explicit_and_incomplete_is_not_verified(self):
        self.capture()
        _, content = self.generated()
        self.assertIn('Unknown — source type has not been established', content)
        self.assertIn('No completed interpretation is recorded.', content)
        self.assertIn('does not establish', content)
        self.assertIn('Known gaps: none recorded', content)

    def test_missing_synthesis_is_reported_pending_without_mutating_receipt(self):
        record = self.capture()
        path = self.synthesis(record)
        before = Path(record['receipt']).read_bytes()
        path.unlink()
        result, content = self.generated()
        self.assertEqual(result['pending_interpretations'], 1)
        self.assertIn('Recorded synthesis is missing or empty.', content)
        self.assertNotIn('Interpretation: complete', content)
        self.assertEqual(Path(record['receipt']).read_bytes(), before)
        self.assert_links_resolve(content)

    def test_description_preserves_other_metadata_identity_paths_and_bytes(self):
        record = self.capture()
        receipt = Path(record['receipt'])
        data = json.loads(receipt.read_text())
        data['custom_future_field'] = {'nested': ['preserve this']}
        receipt.write_text(json.dumps(data))
        raw = Path(record['raw_path'])
        raw_before = raw.read_bytes()
        self.describe(record)
        changed = json.loads(receipt.read_text())
        for field in ('source_id', 'sha256', 'raw_path', 'captured_at', 'original_name', 'custom_future_field'):
            self.assertEqual(changed[field], data[field])
        self.assertEqual(raw.read_bytes(), raw_before)
        self.describe(record, title='A later display title', known_gaps=[])
        changed_again = json.loads(receipt.read_text())
        self.assertEqual(changed_again['description']['title'], 'A later display title')
        self.assertEqual(changed_again['description']['known_gaps'], [])
        self.assertEqual(changed_again['raw_path'], data['raw_path'])

    def test_repeat_generation_preserves_mtime_and_refuses_human_edits(self):
        self.capture()
        first, _ = self.generated()
        self.assertTrue(first['changed'])
        before = self.catalog.stat().st_mtime_ns
        second, _ = self.generated()
        self.assertFalse(second['changed'])
        self.assertEqual(self.catalog.stat().st_mtime_ns, before)
        self.catalog.write_text(self.catalog.read_text() + '\nMy human note.\n')
        modified = self.catalog.read_bytes()
        with self.assertRaisesRegex(brain.BrainError, 'unmanaged or edited'):
            self.generated()
        self.assertEqual(self.catalog.read_bytes(), modified)

    def test_unmanaged_catalog_is_never_overwritten(self):
        self.catalog.write_text('# My own catalog\nKeep my notes.\n')
        before = self.catalog.read_bytes()
        with self.assertRaisesRegex(brain.BrainError, 'unmanaged or edited'):
            self.generated()
        self.assertEqual(self.catalog.read_bytes(), before)

    def test_edited_generation_state_is_rejected(self):
        self.capture()
        self.generated()
        state = self.root / 'maintenance/source-catalogs/alpha.json'
        state.write_text('{"unexpected":true}')
        with self.assertRaisesRegex(brain.BrainError, 'Invalid catalog generation state'):
            self.generated()

    def test_interrupted_state_write_recovers_exact_generated_content(self):
        self.capture()
        real_write = brain.atomic_write
        def interrupted(path, data):
            if path.name == 'alpha.json' and path.parent.name == 'source-catalogs':
                raise OSError('Fictional interrupted state write')
            return real_write(path, data)
        with patch.object(brain, 'atomic_write', side_effect=interrupted), self.assertRaises(OSError):
            self.generated()
        result, _ = self.generated()
        self.assertFalse(result['changed'])
        self.assertTrue((self.root / 'maintenance/source-catalogs/alpha.json').is_file())

    def test_legacy_receipt_paths_and_missing_date_are_supported(self):
        source_id, key = intake.identity('legacy:fictional:notes')
        content = b'Fictional legacy captured content.\n'
        digest = brain.digest(content)
        raw_path = f'raw/{key}/{digest}/source.md'
        raw = self.root / raw_path
        raw.parent.mkdir(parents=True)
        raw.write_bytes(content)
        receipt = intake.receipt_path(self.root, key, digest)
        receipt.parent.mkdir(parents=True)
        receipt.write_text(json.dumps({'schema_version': 1, 'source_id': source_id, 'sha256': digest,
            'raw_path': raw_path, 'original_name': 'Original legacy filename.md', 'revisions': [],
            'targets': {'alpha': {'status': 'pending', 'synthesis': None}}, 'status': 'pending'}))
        _, catalog = self.generated()
        self.assertIn('Original legacy filename.md', catalog)
        self.assertIn('Unknown (missing or invalid capture timestamp)', catalog)
        self.assertIn('capture time is missing or invalid', catalog)
        self.assert_links_resolve(catalog)

    def test_html_markdown_and_path_characters_are_escaped(self):
        record = self.capture(revision='revision [x](javascript:bad)')
        report = self.root / 'maintenance' / 'Review (draft) #1.md'
        report.write_text('Fictional report.\n')
        self.describe(record, title='<script>alert("x")</script> [x](javascript:bad)',
                      known_gaps=['<img src=x> *uncertainty* [x](bad)'],
                      evidence_links=[{'label': '<b>Review</b>', 'path': 'maintenance/Review (draft) #1.md'}])
        _, content = self.generated()
        self.assertNotIn('<script>', content)
        self.assertNotIn('<img', content)
        self.assertNotIn('[x](javascript:', content)
        self.assertIn('&lt;script&gt;', content)
        self.assertIn('%28draft%29%20%231.md', content)
        self.assert_links_resolve(content)

    def test_invalid_descriptions_and_unsafe_or_missing_links_change_nothing(self):
        record = self.capture()
        receipt = Path(record['receipt'])
        before = receipt.read_bytes()
        invalid = [
            {'title': 'bad\nheading'}, {'source_type': 'guessed'}, {'source_type': []},
            {'known_gaps': ['bad\nline']}, {'known_gaps': 'not a list'},
            {'evidence_links': [{'label': 'escape', 'path': '../outside.md'}]},
            {'evidence_links': [{'label': 'public', 'path': 'README.md'}]},
            {'evidence_links': [{'label': 'missing', 'path': 'maintenance/missing.md'}]},
            {'evidence_links': [{'label': 'web', 'path': 'https://example.test'}]},
        ]
        for change in invalid:
            with self.subTest(change=change), self.assertRaises(brain.BrainError):
                self.describe(record, **change)
            self.assertEqual(receipt.read_bytes(), before)

    def test_symlink_evidence_and_catalog_destinations_are_rejected(self):
        record = self.capture()
        outside = self.base / 'outside.md'
        outside.write_text('Outside the permitted catalog boundary.\n')
        linked = self.root / 'maintenance/linked.md'
        linked.symlink_to(outside)
        with self.assertRaises(brain.BrainError):
            self.describe(record, evidence_links=[{'label': 'escape', 'path': 'maintenance/linked.md'}])
        self.catalog.unlink(missing_ok=True)
        self.catalog.symlink_to(outside)
        with self.assertRaises(brain.BrainError):
            self.generated()
        self.assertEqual(outside.read_text(), 'Outside the permitted catalog boundary.\n')

    def test_finder_metadata_and_allocation_state_are_not_receipts(self):
        record = self.capture()
        folder = Path(record['receipt']).parent
        finder = b'\x00\x00\x00\x01Bud1' + b'\x00' * 24
        appledouble = struct.pack('>II16sHIII', 0x00051607, 0x00020000, b'', 1, 9, 38, 0)
        (folder / '.DS_Store').write_bytes(finder)
        (folder / '._receipt.json').write_bytes(appledouble)
        (folder.parent / '.DS_Store').write_bytes(finder)
        (folder.parent / 'unrelated.lock').write_text('Fictional lock')
        self.assertTrue((folder.parent / 'storage.json').is_file())
        result, _ = self.generated()
        self.assertEqual(result['sources'], 1)

    def test_malformed_unrelated_receipt_reports_coverage_failure(self):
        first = self.capture()
        other = self.capture(('beta',), source_id='local:fictional:other-source')
        Path(other['receipt']).write_text('{"targets":"unknown"}')
        with self.assertRaisesRegex(brain.BrainError, 'coverage is incomplete'):
            self.generated()
        self.assertTrue(Path(first['raw_path']).is_file())

    def test_arbitrary_underscore_files_are_not_silently_hidden(self):
        record = self.capture()
        folder = Path(record['receipt']).parent
        (folder / '._important-note.md').write_text('Fictional human note, not Finder metadata.\n')
        with self.assertRaisesRegex(brain.BrainError, 'coverage is incomplete'):
            self.generated()

    def test_changed_original_fails_without_replacing_catalog(self):
        record = self.capture()
        self.generated()
        before = self.catalog.read_bytes()
        Path(record['raw_path']).write_text('Unexpected fictional change.')
        with self.assertRaisesRegex(brain.BrainError, 'missing or changed'):
            self.generated()
        self.assertEqual(self.catalog.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
