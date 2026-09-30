"""Fictional shared-source capture and retry behavior; no connectors or user data."""
import json
import hashlib
import struct
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
import brain
import intake


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='brain intake ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'toolkit'
        self.root.mkdir()
        (self.root / '.brain').write_text('brain:2\n')
        shutil.copytree(REPO / 'templates', self.root / 'templates')
        brain.new_project(self.root, 'alpha')
        brain.new_project(self.root, 'beta')
        self.source = self.base / 'fictional meeting.md'
        self.source.write_text('Fictional meeting. A proposal needs review.\n')
        self.source_id = 'local:fictional:meeting-001'

    def raw_files(self):
        return [path for path in (self.root / 'raw').rglob('*') if path.is_file() and path != self.root / 'raw/.gitkeep' and not intake.is_finder_metadata(path)]

    def legacy(self, projects=('alpha',), receipt=True):
        source_id, key = intake.identity(self.source_id)
        digest = brain.digest(self.source.read_bytes())
        relative = f'raw/{key}/{digest}/source.md'
        raw = self.root / relative
        raw.parent.mkdir(parents=True)
        raw.write_bytes(self.source.read_bytes())
        data = {'schema_version': 1, 'source_id': source_id, 'sha256': digest,
                'raw_path': relative, 'original_name': self.source.name,
                'captured_at': '2024-02-03T04:05:06+00:00', 'revisions': ['fictional-revision'],
                'targets': {slug: {'status': 'pending', 'synthesis': None} for slug in projects},
                'custom_future_metadata': {'keep': True}}
        if receipt:
            intake.save_receipt(self.root, key, data)
        return data

    def finder_files(self, folder, filename):
        (folder / '.DS_Store').write_bytes(b'\x00\x00\x00\x01Bud1' + bytes(24))
        # Structurally valid AppleDouble with a Finder-info entry.
        (folder / ('._' + filename)).write_bytes(struct.pack('>II16sHIII', 0x00051607, 0x00020000,
                                                           bytes(16), 1, 9, 38, 32) + bytes(32))

    def capture(self, projects=(), **kwargs):
        return intake.capture(self.root, self.source, self.source_id, projects, **kwargs)

    def synthesize(self, project, record):
        path = self.root / 'Projects' / project / 'Ingestion/meeting.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Fictional sourced proposal; no decision made.\nSource: '+record['raw_path']+'\n')
        return intake.mark_complete(self.root, self.source_id, record['sha256'], project, 'Ingestion/meeting.md')

    def test_retry_preserves_one_original_and_completed_work(self):
        first = self.capture(['alpha'], revision='v1')
        raw = Path(first['raw_path'])
        original_time = raw.stat().st_mtime_ns
        self.assertEqual(first['status'], 'pending')
        complete = self.synthesize('alpha', first)
        self.assertEqual(complete['status'], 'complete')
        again = self.capture(['alpha'], revision='v2-same-content')
        self.assertFalse(again['created'])
        self.assertEqual(again['status'], 'complete')
        self.assertEqual(raw.stat().st_mtime_ns, original_time)
        self.assertEqual(raw.read_bytes(), self.source.read_bytes())
        self.assertEqual(len(self.raw_files()), 1)

    def test_changed_content_is_new_version_without_replacing_original(self):
        first = self.capture(['alpha'])
        before = Path(first['raw_path']).read_bytes()
        self.source.write_text('Fictional meeting revised with an explicit decision.\n')
        second = self.capture(['alpha'])
        self.assertNotEqual(first['sha256'], second['sha256'])
        self.assertEqual(Path(first['raw_path']).read_bytes(), before)
        self.assertEqual(second['status'], 'pending')

    def test_shared_meeting_tracks_each_workspace_independently(self):
        first = self.capture(['alpha', 'beta'])
        self.assertEqual(Path(first['raw_path']).parent, self.root / 'raw/shared')
        partially_done = self.synthesize('alpha', first)
        self.assertEqual(partially_done['pending_projects'], ['beta'])
        retry = self.capture(['beta', 'alpha'])
        self.assertEqual(retry['pending_projects'], ['beta'])
        self.assertEqual(self.synthesize('beta', first)['status'], 'complete')
        self.assertEqual(len(self.raw_files()), 1)

    def test_unassigned_source_queues_and_can_be_routed_on_retry(self):
        first = self.capture()
        self.assertEqual(first['status'], 'unassigned')
        self.assertEqual(Path(first['raw_path']).parent, self.root / 'raw/unassigned')
        queue = list((self.root / 'inbox').glob('*.json'))
        self.assertEqual(len(queue), 1)
        self.assertEqual(self.capture()['raw_path'], first['raw_path'])
        second = self.capture(['beta'])
        self.assertEqual(second['status'], 'pending')
        self.assertEqual(second['raw_path'], first['raw_path'])
        self.assertFalse(queue[0].exists())

    def test_bad_destination_captures_nothing(self):
        for slug in ('missing', '../escape'):
            with self.subTest(slug=slug), self.assertRaises(brain.BrainError):
                self.capture([slug])
        self.assertEqual(self.raw_files(), [])

    def test_completion_requires_assigned_project_and_existing_synthesis(self):
        first = self.capture(['alpha'])
        with self.assertRaises(brain.BrainError):
            intake.mark_complete(self.root, self.source_id, first['sha256'], 'alpha', 'Ingestion/missing.md')
        with self.assertRaises(brain.BrainError):
            self.synthesize('beta', first)
        self.assertEqual(self.capture(['alpha'])['status'], 'pending')

    def test_tampered_original_is_reported_not_silently_replaced(self):
        first = self.capture(['alpha'])
        Path(first['raw_path']).write_text('Unexpected modification')
        with self.assertRaisesRegex(brain.BrainError, 'missing or changed'):
            self.capture(['alpha'])
        self.assertEqual(Path(first['raw_path']).read_text(), 'Unexpected modification')

    def test_receipt_path_escape_is_rejected(self):
        first = self.capture(['alpha'])
        path = Path(first['receipt'])
        data = json.loads(path.read_text())
        data['raw_path'] = '../outside'
        path.write_text(json.dumps(data))
        with self.assertRaises(brain.BrainError):
            self.capture(['alpha'])

    def test_symlink_capture_destination_is_rejected(self):
        raw = self.root / 'raw'
        shutil.rmtree(raw)
        outside = self.base / 'outside'
        outside.mkdir()
        raw.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(brain.BrainError):
            self.capture(['alpha'])
        self.assertEqual(list(outside.iterdir()), [])

    def test_concurrent_source_run_fails_without_partial_capture(self):
        _, key = intake.identity(self.source_id)
        with intake.source_lock(self.root, key):
            with self.assertRaisesRegex(brain.BrainError, 'being processed'):
                self.capture(['alpha'])
        self.assertEqual(self.raw_files(), [])
        self.assertTrue(self.capture(['alpha'])['created'])

    def test_account_identity_separates_identical_document_ids(self):
        first = self.capture(['alpha'])
        second = intake.capture(self.root, self.source, 'local:another-account:meeting-001', ['beta'])
        self.assertNotEqual(first['raw_path'], second['raw_path'])

    def test_edited_inbox_pointer_is_preserved_before_status_change(self):
        first = self.capture()
        queue = next((self.root / 'inbox').glob('*.json'))
        queue.write_text('{"user_note":"Keep this for review"}')
        receipt_before = Path(first['receipt']).read_bytes()
        with self.assertRaisesRegex(brain.BrainError, 'Inbox pointer'):
            self.capture(['alpha'])
        self.assertEqual(Path(first['receipt']).read_bytes(), receipt_before)
        self.assertIn('Keep this', queue.read_text())

    def test_missing_completed_synthesis_is_pending_on_retry(self):
        first = self.capture(['alpha'])
        self.synthesize('alpha', first)
        (self.root / 'Projects/alpha/Ingestion/meeting.md').unlink()
        retry = self.capture(['alpha'])
        self.assertEqual(retry['status'], 'pending')
        self.assertEqual(retry['pending_projects'], ['alpha'])
        self.assertEqual(retry['raw_path'], first['raw_path'])

    def test_interrupted_capture_recovers_same_raw_after_input_rename(self):
        with patch.object(intake, 'save_receipt', side_effect=OSError('Fictional interrupted write')):
            with self.assertRaises(OSError):
                self.capture(['alpha'])
        raw = self.raw_files()
        self.assertEqual(len(raw), 1)
        renamed = self.source.with_suffix('.txt')
        self.source.rename(renamed)
        self.source = renamed
        result = self.capture(['alpha'])
        self.assertEqual(Path(result['raw_path']), raw[0])
        self.assertEqual(len(self.raw_files()), 1)

    def test_readable_paths_preserve_name_full_identity_and_utc_capture_date(self):
        first = self.capture(['alpha'], title='Fictional Workshop Notes')
        data = json.loads(Path(first['receipt']).read_text())
        _, key = intake.identity(self.source_id)
        raw = Path(first['raw_path'])
        self.assertEqual(raw.relative_to(self.root).as_posix(), 'raw/alpha/fictional meeting.md')
        self.assertEqual(raw.name, self.source.name)
        self.assertEqual(data['description']['title'], 'Fictional Workshop Notes')
        self.assertEqual(intake.read_storage(self.root)['schema_version'], 2)
        self.assertEqual(data['source_id'], self.source_id)
        self.assertEqual(len(data['sha256']), 64)
        self.assertEqual(intake.capture_date('2024-02-03T23:30:00-07:00'), '2024-02-04')

    def test_title_changes_and_renamed_files_keep_existing_source_directory(self):
        first = self.capture(['alpha'], title='First title')
        self.source.rename(self.source.with_name('Renamed input.md'))
        self.source = self.source.with_name('Renamed input.md')
        retry = self.capture(['alpha'], title='Second title')
        self.assertEqual(first['raw_path'], retry['raw_path'])
        data = json.loads(Path(retry['receipt']).read_text())
        self.assertEqual(data['original_name'], 'fictional meeting.md')
        self.source.write_text('A genuinely different fictional version.\n')
        new = self.capture(['alpha'], title='Third title')
        self.assertEqual(Path(first['raw_path']).parent, Path(new['raw_path']).parent)
        self.assertEqual(Path(new['raw_path']).name, 'Renamed input.md')

    def test_unsafe_and_unicode_original_names_have_safe_readable_paths(self):
        for name, expected in [('Résumé 日本語.md', 'Résumé 日本語.md'), ('.fictional.md', '.fictional.md'), ('CON.txt', '_CON.txt'),
                               ('Question: what?*.md', 'Question_ what__.md'),
                               ('line\nbreak.md', 'line_break.md'), ('trailing. ', 'trailing')]:
            with self.subTest(name=name):
                source = self.base / name
                source.write_text('Fictional safe filename case.\n')
                result = intake.capture(self.root, source, 'local:fictional:name-' + str(len(list(self.base.iterdir()))), ['alpha'])
                self.assertEqual(Path(result['raw_path']).name, expected)
                self.assertEqual(json.loads(Path(result['receipt']).read_text())['original_name'], name)
                self.assertLessEqual(len(Path(result['raw_path']).name.encode()), 180)
        self.assertLessEqual(len(intake.safe_original_name('日' * 200 + '.md').encode()), 180)

    def test_short_source_key_collision_extends_filename_without_overwrite(self):
        original_identity = intake.identity
        def collision_id(value):
            source_id, key = original_identity(value)
            return source_id, 'abcdef12' + key[8:]
        with patch.object(intake, 'identity', side_effect=collision_id):
            first = self.capture(['alpha'], title='Same title')
            second = intake.capture(self.root, self.source, 'local:fictional:other', ['alpha'], title='SAME TITLE')
            third = intake.capture(self.root, self.source, 'local:fictional:third', ['alpha'])
            self.assertEqual(Path(first['raw_path']).name, self.source.name)
            self.assertEqual(Path(second['raw_path']).name, 'fictional meeting--abcdef12.md')
            self.assertRegex(Path(third['raw_path']).name, r'^fictional meeting--abcdef12[a-f0-9]{4}\.md$')
            self.assertEqual(self.capture(['alpha'], title='Later label')['raw_path'], first['raw_path'])
            self.assertEqual(len(self.raw_files()), 3)

    def test_short_digest_collision_extends_version_without_overwrite(self):
        original_digest = brain.digest
        contents = [self.source.read_bytes(), b'Fictional second version.', b'Fictional third version.']
        def collision_digest(value):
            digest = original_digest(value)
            return '1234abcd' + digest[8:] if value in contents else digest
        with patch.object(brain, 'digest', side_effect=collision_digest):
            results = []
            for content in contents:
                self.source.write_bytes(content)
                results.append(self.capture(['alpha']))
            self.assertEqual(Path(results[0]['raw_path']).name, self.source.name)
            self.assertRegex(Path(results[1]['raw_path']).name, r'--\d{4}-\d{2}-\d{2}--1234abcd\.md$')
            self.assertRegex(Path(results[2]['raw_path']).name, r'--\d{4}-\d{2}-\d{2}--1234abcd[a-f0-9]{4}\.md$')
            for result, content in zip(results, contents):
                self.assertEqual(Path(result['raw_path']).read_bytes(), content)
            self.assertEqual(self.capture(['alpha'])['raw_path'], results[-1]['raw_path'])

    def test_case_insensitive_existing_filename_is_not_adopted(self):
        _, key = intake.identity(self.source_id)
        folder = self.root / 'raw/alpha'
        folder.mkdir()
        existing = folder / 'FICTIONAL MEETING.MD'
        existing.write_text('Unowned evidence')
        first = self.capture(['alpha'])
        self.assertEqual(Path(first['raw_path']).name, 'fictional meeting--' + key[:8] + '.md')
        self.assertEqual(existing.read_text(), 'Unowned evidence')

    def test_legacy_receipts_are_not_relocated_and_optional_metadata_survives(self):
        legacy = self.legacy()
        result = self.capture(['alpha', 'beta'], revision='later')
        self.assertEqual(Path(result['raw_path']), self.root / legacy['raw_path'])
        after = json.loads(Path(result['receipt']).read_text())
        self.assertEqual(after['custom_future_metadata'], {'keep': True})
        self.assertEqual(after['revisions'], ['fictional-revision', 'later'])
        self.assertEqual(set(after['targets']), {'alpha', 'beta'})
        self.assertFalse((self.root / intake.STORAGE_FILE).exists())

    def test_legacy_interrupted_capture_recovers_with_finder_metadata(self):
        legacy = self.legacy(receipt=False)
        raw = self.root / legacy['raw_path']
        self.finder_files(raw.parent, raw.name)
        renamed = self.source.with_name('renamed.txt')
        self.source.rename(renamed)
        self.source = renamed
        result = self.capture(['alpha'])
        self.assertEqual(Path(result['raw_path']), raw)
        self.assertEqual(len(self.raw_files()), 1)

    def test_friendly_interrupted_capture_recovers_name_time_and_finder_metadata(self):
        with patch.object(intake, 'save_receipt', side_effect=OSError('Fictional interrupted save')):
            with self.assertRaises(OSError):
                self.capture(['alpha'], title='Captured title')
        storage_before = intake.read_storage(self.root)
        raw = self.raw_files()[0]
        self.finder_files(raw.parent, raw.name)
        self.source.rename(self.source.with_name('different filename.txt'))
        self.source = self.source.with_name('different filename.txt')
        result = self.capture(['alpha'], title='New title')
        self.assertEqual(Path(result['raw_path']), raw)
        self.assertEqual(intake.read_storage(self.root), storage_before)
        self.assertEqual(json.loads(Path(result['receipt']).read_text())['original_name'], 'fictional meeting.md')

    def test_shared_folder_recovery_preserves_unrelated_files(self):
        with patch.object(intake, 'save_receipt', side_effect=OSError('Fictional interruption')):
            with self.assertRaises(OSError):
                self.capture(['alpha'])
        raw = self.raw_files()[0]
        extras = {'._notes.md': b'Genuine evidence', '.DS_Store': b'Genuine evidence',
                  'another source.txt': b'Unmanaged original'}
        for name, payload in extras.items():
            (raw.parent / name).write_bytes(payload)
        self.assertEqual(self.capture(['alpha'])['raw_path'], str(raw))
        for name, payload in extras.items():
            self.assertEqual((raw.parent / name).read_bytes(), payload)
            self.assertFalse(intake.is_finder_metadata(raw.parent / name))

    def test_finder_metadata_is_rejected_as_capture_input(self):
        self.finder_files(self.base, self.source.name)
        for name in ('.DS_Store', '._' + self.source.name):
            with self.subTest(name=name), self.assertRaisesRegex(brain.BrainError, 'Finder metadata'):
                intake.capture(self.root, self.base / name, 'fictional:metadata', ['alpha'])

    def test_relocation_plan_is_read_only_register_is_retryable_and_capture_stays_legacy(self):
        data = self.legacy()
        _, key = intake.identity(self.source_id)
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        plan = intake.plan_relocation(self.root, data, 'Human readable title')
        after = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(plan['raw_path'], 'raw/alpha/fictional meeting.md')
        self.assertEqual(plan['captured_at'], data['captured_at'])
        with intake.source_lock(self.root, key):
            intake.register_relocation(self.root, plan)
            intake.register_relocation(self.root, plan)
        self.assertEqual(self.capture(['alpha'])['raw_path'], str(self.root / data['raw_path']))
        self.assertEqual(intake.plan_relocation(self.root, data, 'Changed label')['raw_path'], plan['raw_path'])
        new = self.root / plan['raw_path']
        new.parent.mkdir(parents=True)
        new.write_bytes((self.root / data['raw_path']).read_bytes())
        data['raw_path'] = plan['raw_path']
        intake.save_receipt(self.root, key, data)
        relocated = self.capture(['alpha', 'beta'])
        self.assertEqual(relocated['raw_path'], str(new))
        self.assertEqual(relocated['sha256'], data['sha256'])
        self.assertFalse(relocated['created'])

    def test_tampered_or_stale_relocation_plan_does_not_register(self):
        data = self.legacy()
        _, key = intake.identity(self.source_id)
        plan = intake.plan_relocation(self.root, data)
        changed = dict(plan, raw_path='raw/other/version/elsewhere.md')
        with intake.source_lock(self.root, key), self.assertRaisesRegex(brain.BrainError, 'plan was altered'):
            intake.register_relocation(self.root, changed)
        (self.root / plan['directory']).mkdir()
        (self.root / plan['raw_path']).write_text('Unowned evidence')
        with intake.source_lock(self.root, key), self.assertRaisesRegex(brain.BrainError, 'plan was altered'):
            intake.register_relocation(self.root, plan)
        self.assertFalse((self.root / intake.STORAGE_FILE).exists())

    def test_friendly_receipt_requires_matching_full_identity_allocation(self):
        first = self.capture(['alpha'])
        data = json.loads(Path(first['receipt']).read_text())
        storage = intake.read_storage(self.root)
        _, key = intake.identity(self.source_id)
        del storage['sources'][key]
        (self.root / intake.STORAGE_FILE).write_text(json.dumps(storage))
        with self.assertRaisesRegex(brain.BrainError, 'unallocated'):
            self.capture(['alpha'])
        self.assertEqual(Path(first['raw_path']).read_bytes(), self.source.read_bytes())

    def test_storage_symlink_escape_is_rejected_before_raw_capture(self):
        storage = self.root / intake.STORAGE_FILE
        storage.parent.mkdir(parents=True, exist_ok=True)
        external = self.base / 'outside.json'
        external.write_text('{"keep": true}')
        storage.symlink_to(external)
        with self.assertRaisesRegex(brain.BrainError, 'Symlink'):
            self.capture(['alpha'])
        self.assertEqual(external.read_text(), '{"keep": true}')
        self.assertFalse(self.raw_files())

    def test_partial_allocation_is_retryable_before_bytes_are_written(self):
        original_save = intake.save_allocation
        def interrupted(root, plan, storage):
            original_save(root, plan, storage)
            raise OSError('Fictional interruption after allocation')
        with patch.object(intake, 'save_allocation', side_effect=interrupted):
            with self.assertRaises(OSError):
                self.capture(['alpha'])
        self.assertFalse(self.raw_files())
        storage = intake.read_storage(self.root)
        _, key = intake.identity(self.source_id)
        allocated = next(iter(storage['sources'][key]['versions'].values()))
        self.source.rename(self.source.with_name('Retry name.txt'))
        self.source = self.source.with_name('Retry name.txt')
        retry = self.capture(['alpha'])
        self.assertEqual(retry['raw_path'], str(self.root / allocated['raw_path']))
        data = json.loads(Path(retry['receipt']).read_text())
        self.assertEqual(data['captured_at'], allocated['captured_at'])
        self.assertEqual(data['original_name'], allocated['original_name'])

    def test_reserved_friendly_version_symlink_is_rejected(self):
        with patch.object(intake, 'save_receipt', side_effect=OSError('Fictional interrupted save')):
            with self.assertRaises(OSError):
                self.capture(['alpha'])
        raw = self.raw_files()[0]
        raw.unlink()
        raw.parent.rmdir()
        outside = self.base / 'outside-version'
        outside.mkdir()
        raw.parent.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(brain.BrainError, 'Symlink'):
            self.capture(['alpha'])
        self.assertFalse(list(outside.iterdir()))

    def test_optional_receipt_and_target_metadata_survive_completion_and_retries(self):
        first = self.capture(['alpha'])
        data = json.loads(Path(first['receipt']).read_text())
        data['custom_field'] = {'fictional': 'future-compatible'}
        data['targets']['alpha']['review_annotation'] = 'Keep this provenance.'
        data['description']['known_gaps'] = ['Fictional gap remains unresolved.']
        Path(first['receipt']).write_text(json.dumps(data))
        self.synthesize('alpha', first)
        self.capture(['alpha'])
        after = json.loads(Path(first['receipt']).read_text())
        self.assertEqual(after['custom_field'], data['custom_field'])
        self.assertEqual(after['targets']['alpha']['review_annotation'], 'Keep this provenance.')
        self.assertEqual(after['description'], data['description'])

    def test_exhausted_identifiers_fail_without_adopting_existing_files(self):
        _, key = intake.identity(self.source_id)
        folder = self.root / 'raw/alpha'
        folder.mkdir()
        names = [self.source.name] + ['fictional meeting--' + key[:length] + '.md' for length in range(8, 65, 4)]
        for name in names:
            (folder / name).write_text('Unmanaged evidence')
        with self.assertRaisesRegex(brain.BrainError, 'full identifier path is occupied'):
            self.capture(['alpha'])
        self.assertEqual({path.name for path in self.raw_files()}, set(names))
        self.assertTrue(all(path.read_text() == 'Unmanaged evidence' for path in self.raw_files()))
        self.assertFalse((self.root / intake.STORAGE_FILE).exists())

    def test_false_full_identity_in_allocations_is_rejected(self):
        first = self.capture(['alpha'])
        storage = intake.read_storage(self.root)
        _, key = intake.identity(self.source_id)
        storage['sources'][key]['source_id'] = 'fictional:another-identity'
        (self.root / intake.STORAGE_FILE).write_text(json.dumps(storage))
        with self.assertRaisesRegex(brain.BrainError, 'full source identity'):
            self.capture(['alpha'])
        self.assertEqual(Path(first['raw_path']).read_bytes(), self.source.read_bytes())

    def test_folder_and_filename_are_presentation_choices_not_routing(self):
        result = self.capture(folder='alpha/Research notes', filename='Readable report.md', title='Helpful title')
        self.assertEqual(result['raw_path'], str(self.root / 'raw/alpha/Research notes/Readable report.md'))
        self.assertEqual(result['status'], 'unassigned')
        data = json.loads(Path(result['receipt']).read_text())
        self.assertEqual(data['original_name'], self.source.name)
        self.assertEqual(data['targets'], {})
        self.assertEqual(Path(result['raw_path']).read_bytes(), self.source.read_bytes())
        retry = self.capture(['beta'], folder='beta/Another category', filename='Different title.txt')
        self.assertEqual(retry['raw_path'], result['raw_path'])
        self.assertEqual(retry['pending_projects'], ['beta'])
        self.assertFalse((self.root / 'raw/beta').exists())

    def test_capture_cli_accepts_folder_and_filename(self):
        import contextlib
        import io
        output = io.StringIO()
        with patch.object(intake, 'TOOLKIT_ROOT', self.root), contextlib.redirect_stdout(output):
            code = intake.main(['capture', '--file', str(self.source), '--source-id', self.source_id,
                                '--project', 'alpha', '--folder', 'alpha/Meetings', '--filename', 'Monday.md'])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())['raw_path'], str(self.root / 'raw/alpha/Meetings/Monday.md'))

    def test_invalid_categories_and_filename_paths_capture_nothing(self):
        for folder in ('', '/tmp', '../outside', 'a//b', 'a/../b', 'a\\b', 'CON', 'a.', '.hidden', 'a/:bad'):
            with self.subTest(folder=folder), self.assertRaises(brain.BrainError):
                self.capture(['alpha'], folder=folder)
        for filename in ('', '.', '..', '../outside', 'a/b.md', 'a\\b.md'):
            with self.subTest(filename=filename), self.assertRaises(brain.BrainError):
                self.capture(['alpha'], filename=filename)
        outside = self.base / 'outside-folder'
        outside.mkdir()
        (self.root / 'raw/category').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(brain.BrainError, 'Symlink'):
            self.capture(['alpha'], folder='category/nested')
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.root / intake.STORAGE_FILE).exists())

    def test_unicode_filename_collisions_preserve_both_identities(self):
        first = self.capture(['alpha'], filename='Résumé.md')
        second = intake.capture(self.root, self.source, 'local:fictional:another', ['alpha'], filename='Re\u0301sume\u0301.md')
        self.assertEqual(Path(first['raw_path']).name, 'Résumé.md')
        self.assertRegex(Path(second['raw_path']).name, r'^Résumé--[a-f0-9]{8}\.md$')
        self.assertNotEqual(first['raw_path'], second['raw_path'])
        self.assertEqual(Path(first['raw_path']).read_bytes(), self.source.read_bytes())

    def test_pending_reservations_protect_unwritten_filenames_and_folder_spelling(self):
        original_save = intake.save_allocation
        def interrupted(root, plan, storage):
            original_save(root, plan, storage)
            raise OSError('Fictional interruption before mkdir')
        with patch.object(intake, 'save_allocation', side_effect=interrupted), self.assertRaises(OSError):
            self.capture(['alpha'], folder='Reports', filename='first.md')
        self.assertFalse((self.root / 'raw/Reports').exists())
        with self.assertRaisesRegex(brain.BrainError, 'reserved folder'):
            intake.capture(self.root, self.source, 'local:fictional:other', ['alpha'], folder='reports', filename='different.md')
        second = intake.capture(self.root, self.source, 'local:fictional:other', ['alpha'], folder='Reports', filename='first.md')
        retry = self.capture(['alpha'], folder='changed')
        self.assertEqual(Path(retry['raw_path']).name, 'first.md')
        self.assertRegex(Path(second['raw_path']).name, r'^first--[a-f0-9]{8}\.md$')
        self.assertEqual(len(self.raw_files()), 2)

    def test_pending_file_and_directory_reservations_cannot_overlap(self):
        original_save = intake.save_allocation
        def interrupted(root, plan, storage):
            original_save(root, plan, storage)
            raise OSError('Fictional interruption before mkdir')
        with patch.object(intake, 'save_allocation', side_effect=interrupted), self.assertRaises(OSError):
            self.capture(['alpha'], folder='shared', filename='topic')
        with self.assertRaisesRegex(brain.BrainError, 'reserved as a source file'):
            intake.capture(self.root, self.source, 'local:fictional:nested', folder='shared/topic', filename='note.md')
        with patch.object(intake, 'save_allocation', side_effect=interrupted), self.assertRaises(OSError):
            intake.capture(self.root, self.source, 'local:fictional:deep', folder='shared/category', filename='note.md')
        result = intake.capture(self.root, self.source, 'local:fictional:category', folder='shared', filename='category')
        self.assertRegex(Path(result['raw_path']).name, r'^category--[a-f0-9]{8}$')
        self.assertTrue(self.capture(['alpha'])['created'])

    def test_global_allocation_lock_prevents_concurrent_reservations(self):
        with intake.source_lock(self.root, 'storage'):
            with self.assertRaisesRegex(brain.BrainError, 'being processed'):
                self.capture(['alpha'])
        self.assertFalse(self.raw_files())
        self.assertFalse((self.root / intake.STORAGE_FILE).exists())
        first = self.capture(['alpha'])
        second = intake.capture(self.root, self.source, 'local:fictional:second', ['alpha'])
        self.assertNotEqual(first['raw_path'], second['raw_path'])

    def test_schema_two_rejects_normalized_path_collision_and_parent_conflicts(self):
        first = self.capture(['alpha'])
        second = intake.capture(self.root, self.source, 'local:fictional:second', ['alpha'])
        _, first_key = intake.identity(self.source_id)
        _, second_key = intake.identity('local:fictional:second')
        original = intake.read_storage(self.root)
        for relative in ('raw/alpha/FICTIONAL MEETING.MD', 'raw/alpha/fictional meeting.md/child.md',
                         'raw/alpha//fictional meeting.md', 'raw/alpha/./fictional meeting.md'):
            storage = json.loads(json.dumps(original))
            storage['sources'][second_key]['versions'][second['sha256']]['raw_path'] = relative
            (self.root / intake.STORAGE_FILE).write_text(json.dumps(storage))
            with self.subTest(relative=relative), self.assertRaises(brain.BrainError):
                intake.read_storage(self.root)
        (self.root / intake.STORAGE_FILE).write_text(json.dumps(original))
        self.assertEqual(self.capture(['alpha'])['raw_path'], first['raw_path'])

    def test_v1_readable_allocation_is_preserved_then_explicitly_relocated(self):
        source_id, key = intake.identity(self.source_id)
        digest = brain.digest(self.source.read_bytes())
        directory = 'raw/old-title--' + key[:8]
        relative = directory + '/2024-02-03--' + digest[:8] + '/' + self.source.name
        raw = self.root / relative
        raw.parent.mkdir(parents=True)
        raw.write_bytes(self.source.read_bytes())
        version = {'raw_path': relative, 'original_name': self.source.name,
                   'captured_at': '2024-02-03T04:05:06+00:00', 'title': 'Old title'}
        storage = {'schema_version': 1, 'sources': {key: {'source_id': source_id, 'directory': directory,
                                                       'versions': {digest: version}}}}
        data = {'schema_version': 1, 'source_id': source_id, 'sha256': digest,
                **{field: version[field] for field in ('raw_path', 'original_name', 'captured_at')},
                'revisions': ['r1'], 'targets': {'alpha': {'status': 'pending', 'synthesis': None}},
                'custom_field': 'preserve'}
        intake.save_receipt(self.root, key, data)
        (self.root / intake.STORAGE_FILE).write_text(json.dumps(storage))
        self.assertEqual(self.capture(['alpha'], title='Changed title')['raw_path'], str(raw))
        self.assertEqual(intake.read_storage(self.root), storage)
        # A new source upgrades storage without altering or reallocating v1 originals.
        intake.capture(self.root, self.source, 'local:fictional:other', ['beta'])
        upgraded = intake.read_storage(self.root)
        self.assertEqual(upgraded['schema_version'], 2)
        self.assertEqual(upgraded['sources'][key], storage['sources'][key])
        plan = intake.plan_relocation(self.root, data, folder='alpha/Meetings', filename='Old meeting.md')
        self.assertEqual(plan['raw_path'], 'raw/alpha/Meetings/Old meeting.md')
        with intake.source_lock(self.root, key):
            intake.register_relocation(self.root, plan)
        self.assertEqual(self.capture(['alpha'])['raw_path'], str(raw))
        moved = self.root / plan['raw_path']
        moved.parent.mkdir(parents=True)
        moved.write_bytes(raw.read_bytes())
        data['raw_path'] = plan['raw_path']
        intake.save_receipt(self.root, key, data)
        with intake.source_lock(self.root, key):
            intake.register_relocation(self.root, plan)
        self.assertEqual(self.capture(['alpha'])['raw_path'], str(moved))
        after = json.loads(intake.receipt_path(self.root, key, digest).read_text())
        self.assertEqual(after['custom_field'], 'preserve')
        self.assertEqual(after['revisions'], ['r1'])
        self.assertEqual(raw.read_bytes(), moved.read_bytes())
        altered = dict(plan, previous_raw_path='raw/alpha/unmanaged.md')
        with intake.source_lock(self.root, key), self.assertRaisesRegex(brain.BrainError, 'unallocated prior path'):
            intake.register_relocation(self.root, altered)
        moved.write_text('Edited relocated original')
        with self.assertRaisesRegex(brain.BrainError, 'missing or changed'):
            self.capture(['alpha'])


if __name__ == '__main__':
    unittest.main()
