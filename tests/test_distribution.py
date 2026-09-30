"""Exercise the shipped files and CLI in a fresh extracted release, with fictional data."""
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid
import zipfile

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
import brain


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='brain distribution ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / 'source toolkit'
        # Use the actual reviewed release files, including the current templates.
        for relative, content in brain.release_files(REPO):
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        for relative in ('skills/.DS_Store', 'optional-skills/.DS_Store'):
            (self.source / relative).write_bytes(b'Fictional Finder metadata')

    def run_cli(self, root, *arguments, expected=0, cwd=None):
        result = subprocess.run(
            [sys.executable, '-B', str(root / 'scripts/brain.py'), *arguments],
            cwd=cwd or root, text=True, capture_output=True, timeout=30,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def run_intake(self, root, *arguments, expected=0):
        result = subprocess.run(
            [sys.executable, '-B', str(root / 'scripts/intake.py'), *arguments],
            cwd=root, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout) if expected == 0 else result

    def test_git_ignore_excludes_private_root_content_but_keeps_public_templates(self):
        private = ['Projects/example/wiki/note.md','raw/source.md','inbox/item.json',
                   'maintenance/runs/review.md','context/goals.md','outputs/plan.md',
                   'INDEX.md','registry.json','integrations.json','brain/raw/legacy.md']
        public = ['AGENTS.md','scripts/brain.py','templates/root/INDEX.md',
                  'templates/root/context/goals.md','templates/root/Projects/.gitkeep',
                  'templates/project/wiki/INDEX.md']
        subprocess.run(['git','init','--quiet',str(self.source)],check=True,capture_output=True,timeout=30)
        result=subprocess.run(['git','check-ignore','--no-index','--stdin'],
                              input='\n'.join(private+public)+'\n',cwd=self.source,
                              text=True,capture_output=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(set(result.stdout.splitlines()),set(private))

    def test_optional_coordination_installs_portably_and_keeps_runtime_records_private(self):
        self.run_cli(self.source, 'new-project', 'example', '--type', 'general')
        sentinel = 'FICTIONAL_COORDINATION_PRIVATE_' + uuid.uuid4().hex
        private_paths = [
            'Projects/example/coordination/work-card.md',
            'maintenance/runs/example-run/plan.md',
            'maintenance/runs/example-run/handoff.md',
            'maintenance/runs/example-run/workers/worker-one.md',
        ]
        for relative in private_paths:
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(sentinel)
        release = json.loads(self.run_cli(self.source, 'build-release').stdout)
        extracted = self.base / 'portable install'
        resources = {'docs/COORDINATION.md', 'templates/coordination/work-card.md',
                     'templates/coordination/handoff.md'}
        with zipfile.ZipFile(release['archive']) as archive:
            names = set(archive.namelist())
            self.assertTrue({'Brain/' + path for path in resources}.issubset(names))
            self.assertIn('Brain/optional-skills/coordinate/SKILL.md', names)
            self.assertFalse({'Brain/' + path for path in private_paths} & names)
            self.assertNotIn(sentinel.encode(), b'\n'.join(archive.read(name) for name in names))
            archive.extractall(extracted)
        root = extracted / 'Brain'
        self.run_cli(root, 'setup')
        for host in brain.HOSTS:
            self.assertFalse((root / host / 'coordinate').exists())
        result = json.loads(self.run_cli(root, 'setup', '--with-optional').stdout)
        self.assertEqual(result['skills'], len(list((root / 'skills').glob('*/SKILL.md'))) +
                         len(list((root / 'optional-skills').glob('*/SKILL.md'))))
        canonical = (root / 'optional-skills/coordinate/SKILL.md').read_bytes()
        for host in brain.HOSTS:
            installed = root / host / 'coordinate/SKILL.md'
            self.assertEqual(installed.read_bytes(), canonical)
            # Resolve actual referenced resources from the enclosing marker, not
            # from a hardcoded number of parents in a generated skill directory.
            toolkit = next(parent for parent in installed.parents if (parent / '.brain').is_file())
            self.assertEqual(toolkit, root)
            references = set(re.findall(r'(?:docs|templates)/[^`\s)\]]+\.md', installed.read_text()))
            self.assertTrue(resources.issubset(references))
            for relative in references:
                self.assertTrue(brain.safe_under(toolkit, relative).is_file(), relative)
        self.run_cli(root, 'setup')
        self.run_cli(root, 'verify', '--installed')
        for host in brain.HOSTS:
            self.assertEqual((root / host / 'coordinate/SKILL.md').read_bytes(), canonical)
        self.run_cli(root, 'uninstall')
        self.run_cli(root, 'setup', '--with-visuals')
        for host in brain.HOSTS:
            self.assertEqual((root / host / 'coordinate/SKILL.md').read_bytes(), canonical)
        self.run_cli(root, 'verify', '--installed')
        for relative in private_paths:
            self.assertEqual((self.source / relative).read_text(), sentinel)

    def test_release_review_scope_defaults_and_opt_out_survive_setup(self):
        archive_path = json.loads(self.run_cli(self.source, 'build-release').stdout)['archive']
        extracted = self.base / 'review scope install'
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(extracted)
        root = extracted / 'Brain'
        self.run_cli(root, 'setup')
        self.run_cli(root, 'init-brain')
        empty = self.run_cli(root, 'list-projects', '--scope', 'review',
                             '--require-nonempty', expected=2)
        self.assertIn('No workspaces match scope', empty.stderr)
        self.assertEqual(empty.stdout, '')
        for slug in ('example-one', 'example-two'):
            self.run_cli(root, 'new-project', slug)
        args = ('list-projects', '--scope', 'review', '--require-nonempty')
        self.assertEqual([item['slug'] for item in json.loads(self.run_cli(root, *args).stdout)],
                         ['example-one', 'example-two'])
        registry_path = root / 'registry.json'
        registry = json.loads(registry_path.read_text())
        registry['workspaces'][0]['review'] = False
        registry['workspaces'][1]['status'] = 'paused'
        registry_path.write_text(json.dumps(registry))
        before = registry_path.read_bytes()
        self.run_cli(root, 'setup')
        self.run_cli(root, 'init-brain')
        self.assertEqual(registry_path.read_bytes(), before)
        self.assertEqual(json.loads(self.run_cli(root, 'list-projects', '--scope', 'review').stdout), [])
        self.run_cli(root, *args, expected=2)
        self.assertEqual(registry_path.read_bytes(), before)
        registry['workspaces'][1]['status'] = 'active'
        registry_path.write_text(json.dumps(registry))
        self.assertEqual([item['slug'] for item in json.loads(self.run_cli(root, *args).stdout)],
                         ['example-two'])
        # Eligibility is distinct from availability: keep missing entries visible.
        (root / 'Projects/example-two/PROJECT.md').unlink()
        listed = json.loads(self.run_cli(root, *args).stdout)
        self.assertFalse(listed[0]['available'])

    def test_shared_intake_registry_and_nested_application_in_fresh_toolkit(self):
        root = self.source
        self.run_cli(root, 'init-brain')
        self.run_cli(root, 'new-project', 'example-one', '--type', 'business')
        self.run_cli(root, 'new-project', 'example-two', '--type', 'personal')
        one = root / 'Projects/example-one'
        app = one / 'app'
        app.mkdir()
        (app / 'main.py').write_text('print("fictional app runs")\n')
        self.assertEqual(Path(self.run_cli(root, 'resolve', cwd=app).stdout.strip()), one)
        execution = subprocess.run([sys.executable, str(app / 'main.py')], cwd=app,
                                   capture_output=True, text=True, timeout=30)
        self.assertEqual(execution.returncode, 0, execution.stderr)
        self.assertEqual(execution.stdout.strip(), 'fictional app runs')

        registry_path = root / 'registry.json'
        registry = json.loads(registry_path.read_text())
        registry['workspaces'][0]['application'] = {'kind': 'internal', 'path': 'app'}
        registry['workspaces'][1]['planning'] = False
        registry_path.write_text(json.dumps(registry))
        planning = json.loads(self.run_cli(root, 'list-projects', '--scope', 'planning').stdout)
        self.assertEqual([item['slug'] for item in planning], ['example-one'])
        self.assertEqual(len(json.loads(self.run_cli(root, 'list-projects', '--scope', 'review').stdout)), 2)

        source = self.base / 'fictional Monday meeting.md'
        source.write_text('Fictional source about a proposal for two workspaces.\n')
        source_id = 'local:fixture:monday-meeting'
        args = ('capture', '--file', str(source), '--source-id', source_id)
        queued = self.run_intake(root, *args)
        self.assertEqual(queued['status'], 'unassigned')
        routed = self.run_intake(root, *args, '--project', 'example-one', '--project', 'example-two')
        self.assertEqual(queued['raw_path'], routed['raw_path'])
        self.assertEqual(routed['pending_projects'], ['example-one', 'example-two'])
        for slug in ('example-one', 'example-two'):
            synthesis = root / 'Projects' / slug / 'Ingestion/meeting.md'
            synthesis.write_text('Fictional scoped proposal. Source: '+routed['raw_path']+'\n')
            done = self.run_intake(root, 'mark-complete', '--source-id', source_id,
                                   '--digest', routed['sha256'], '--project', slug,
                                   '--synthesis', 'Ingestion/meeting.md')
        self.assertEqual(done['status'], 'complete')
        self.assertEqual(self.run_intake(root, *args)['status'], 'complete')
        self.assertEqual(Path(routed['raw_path']).name, source.name)
        self.assertEqual(Path(routed['raw_path']).parent.relative_to(root).as_posix(), 'raw/unassigned')
        descriptor = self.base / 'source-description.json'
        descriptor.write_text(json.dumps({'title': 'Fictional Monday meeting',
                                         'source_type': 'primary_evidence',
                                         'known_gaps': ['Outcome is not yet confirmed.'],
                                         'evidence_links': []}))
        for arguments in [('describe', '--source-id', source_id, '--digest', routed['sha256'],
                           '--metadata-json', str(descriptor)),
                          ('generate', '--project', 'example-one')]:
            run = subprocess.run([sys.executable, '-B', str(root/'scripts/source_catalog.py'), *arguments],
                                 cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stderr)
        catalog = (root/'Projects/example-one/SOURCES.md').read_text()
        self.assertIn('Fictional Monday meeting', catalog)
        self.assertIn('Outcome is not yet confirmed.', catalog)
        self.assertIn('Ingestion/meeting.md', catalog)
        self.assertIn('[sources', (root/'Projects/example-one/PROJECT.md').read_text())

    def test_extracted_release_creates_generic_workspaces_and_preserves_private_data(self):
        fresh = json.loads(self.run_cli(self.source, 'verify').stdout)
        self.assertFalse(fresh['installed'])
        archive_path = json.loads(self.run_cli(self.source, 'build-release').stdout)['archive']
        self.assertEqual(Path(archive_path).name, f'Brain-{brain.VERSION}.zip')
        extracted = self.base / 'fresh install with spaces'
        with zipfile.ZipFile(archive_path) as archive:
            self.assertIn('Brain/docs/GETTING_STARTED.md', archive.namelist())
            self.assertFalse(any('.DS_Store' in name for name in archive.namelist()))
            self.assertFalse(any(Path(name).parts[1] in (brain.PRIVATE_DIRECTORIES | brain.PRIVATE_FILES | {'brain'}) for name in archive.namelist()))
            archive.extractall(extracted)
        root = extracted / 'Brain'
        self.assertEqual((root / '.brain').read_text().strip(), 'brain:2')
        setup = json.loads(self.run_cli(root, 'setup').stdout)
        self.assertEqual(setup['skills'], len(list((root / 'skills').glob('*/SKILL.md'))))
        self.assertFalse(setup['global_changes'])
        installation = json.loads((root / '.local/installation.json').read_text())
        self.assertEqual(installation['toolkit'], 'brain')
        self.assertEqual(installation['version'], brain.VERSION)
        self.assertTrue(json.loads(self.run_cli(root, 'verify', '--installed').stdout)['installed'])

        cases = [
            ('example-career', 'career', 'Explore a fictional career change.'),
            ('example-personal', 'personal', 'Organize fictional household records.'),
            ('example-business', 'business', 'Plan a fictional craft shop.'),
        ]
        for slug, kind, purpose in cases:
            with self.subTest(kind=kind):
                self.run_cli(root, 'new-project', slug, '--name', 'Example '+kind,
                             '--type', kind, '--purpose', purpose)
                workspace = root / 'Projects' / slug
                result = self.run_cli(root, 'resolve', '--project', slug)
                self.assertEqual(Path(result.stdout.strip()), workspace)
                for relative in ('PROJECT.md', 'context/profile.md'):
                    content = (workspace / relative).read_text()
                    self.assertIn(kind, content)
                    self.assertIn(purpose, content)
                    self.assertNotIn('{{', content)
                self.assertEqual(json.loads((root / 'integrations.json').read_text())['connections'], [])
                self.assertFalse((workspace / 'raw').exists())
                self.assertFalse((workspace / 'maintenance').exists())
                self.assertFalse((workspace / 'Stakeholders').exists())
                self.assertFalse((workspace / 'Hypotheses').exists())

        self.assertEqual(Path(self.run_cli(root, 'resolve-brain').stdout.strip()), root)
        self.assertEqual(len(json.loads(self.run_cli(root, 'list-projects', '--scope', 'planning').stdout)), 3)
        self.run_cli(root, 'resolve', expected=2)
        self.run_cli(root, 'resolve', '--project', cases[0][0],
                     cwd=root / 'Projects' / cases[1][0], expected=2)
        project = root / 'Projects' / cases[0][0]
        profile = project / 'context/profile.md'
        sentinel = 'FICTIONAL_PRIVATE_' + uuid.uuid4().hex
        profile.write_text(profile.read_text()+'\n'+sentinel+'\n')
        before = profile.read_bytes()
        shared = root / 'context/goals.md'
        shared.write_text(shared.read_text()+'\n'+sentinel+'\n')
        shared_before = shared.read_bytes()
        self.run_cli(root, 'init-brain')
        self.assertEqual(shared.read_bytes(), shared_before)
        self.run_cli(root, 'new-project', cases[0][0], expected=2)
        self.run_cli(root, 'setup')
        self.assertEqual(profile.read_bytes(), before)
        upgraded = json.loads(self.run_cli(root, 'setup', '--with-visuals').stdout)
        self.assertEqual(upgraded['skills'], len(list((root / 'skills').glob('*/SKILL.md'))) + len(list((root / 'optional-skills').glob('*/SKILL.md'))))
        self.run_cli(root, 'verify', '--installed')
        self.run_cli(root, 'uninstall')
        self.assertEqual(profile.read_bytes(), before)
        self.run_cli(root, 'setup')
        release = json.loads(self.run_cli(root, 'build-release').stdout)
        with zipfile.ZipFile(release['archive']) as archive:
            contents = b'\n'.join(archive.read(name) for name in archive.namelist())
            self.assertFalse(sentinel.encode() in contents, 'Private workspace content entered the release')
            self.assertFalse(any(Path(name).parts[1] in (brain.PRIVATE_DIRECTORIES | brain.PRIVATE_FILES | {'brain'}) for name in archive.namelist()))
        self.assertEqual(profile.read_bytes(), before)
        self.assertEqual(shared.read_bytes(), shared_before)


if __name__ == '__main__':
    unittest.main()
