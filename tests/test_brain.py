"""Executable lifecycle, routing and release-boundary tests. All data is fictional."""
import importlib.util
from contextlib import redirect_stdout
from concurrent.futures import ThreadPoolExecutor
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import brain

class ToolkitTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='brain test with spaces ')
        self.base=Path(self.temp.name).resolve()
        self.root=self.base/'toolkit';self.root.mkdir()
        files={'.brain':'brain:2\n','README.md':'# Test toolkit\n','LICENSE':'Test license\n','AGENTS.md':'Read docs/OPERATING_GUIDE.md','CLAUDE.md':'Read docs/OPERATING_GUIDE.md','docs/OPERATING_GUIDE.md':'Select a workspace first.',
            'docs/GETTING_STARTED.md':'# Getting started\nSelect a fictional workspace before reading its context.\n',
            'templates/root/INDEX.md':'# Shared brain\n\nKeep this manual introduction.\n\n<!-- BEGIN WORKSPACES -->\nNo workspaces registered yet.\n<!-- END WORKSPACES -->\n\nKeep these manual notes.\n',
            'templates/root/registry.json':json.dumps({'schema_version':1,'workspaces':[]}),
            'templates/root/integrations.json':json.dumps({'schema_version':1,'connections':[],'sources':[],'routes':[]}),
            'templates/root/context/goals.md':'# Shared goals\nUnknown.\n',
            'templates/root/context/preferences.md':'# Shared preferences\nUnknown.\n',
            'templates/root/Projects/.gitkeep':'',
            'templates/project/PROJECT.md':'# {{PROJECT_NAME}}\nID {{PROJECT_SLUG}}\nType: {{WORKSPACE_TYPE}}\nPurpose: {{WORKSPACE_PURPOSE}}\n',
            'templates/project/wiki/INDEX.md':'# Empty knowledge\n',
            'scripts/brain.py':'# Fictional release fixture\n',
            'skills/brain-sample/SKILL.md':'---\nname: brain-sample\ndescription: Sample workflow for a test.\n---\nRead docs/OPERATING_GUIDE.md.\n',
            'optional-skills/brain-visual/SKILL.md':'---\nname: brain-visual\ndescription: Visual workflow for a test.\n---\nRead docs/OPERATING_GUIDE.md.\n'}
        for rel,text in files.items():
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
        (self.root/'capabilities.json').write_text(json.dumps([{'capability':'sample','skill':'brain-sample'},{'capability':'visual','skill':'brain-visual'}]))
        self.public=set(files)|{'capabilities.json','release-files.json'}
        self.write_allowlist()
        brain.new_project(self.root,'alpha')
        brain.new_project(self.root,'beta')
        self.alpha=self.root/'Projects/alpha';self.beta=self.root/'Projects/beta'
        (self.alpha/'private.md').write_text('ALPHA_ONLY_SENTINEL')
        (self.beta/'private.md').write_text('BETA_ONLY_SENTINEL')
    def tearDown(self):self.temp.cleanup()
    def write_allowlist(self):
        (self.root/'release-files.json').write_text(json.dumps(sorted(self.public)))
    def rename_fixture_skills(self):
        for folder,old,new in (('skills','brain-sample','sample'),('optional-skills','brain-visual','visual')):
            source=self.root/folder/old
            destination=self.root/folder/new
            source.rename(destination)
            skill=destination/'SKILL.md'
            skill.write_text(skill.read_text().replace('name: '+old,'name: '+new))
            self.public={relative.replace(folder+'/'+old+'/',folder+'/'+new+'/') for relative in self.public}
        (self.root/'capabilities.json').write_text(json.dumps([
            {'capability':'sample','skill':'sample'},{'capability':'visual','skill':'visual'}]))
        self.write_allowlist()
    def clear_private_fixture(self):
        # Remove only known private fixture paths, never the toolkit root/resources.
        for relative in brain.PRIVATE_DIRECTORIES | brain.PRIVATE_FILES:
            path=self.root/relative
            if path.is_dir():shutil.rmtree(path)
            elif path.exists():path.unlink()
    def snapshot(self):
        return {p.relative_to(self.root).as_posix():p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
    def update_registry(self,change):
        p=self.root/'registry.json'
        value=json.loads(p.read_text());change(value);p.write_text(json.dumps(value))
    def test_init_brain_preserves_edited_files_and_restores_only_missing_scaffold(self):
        goals=self.root/'context/goals.md';goals.write_text('User-authored shared goals.\n')
        private=self.root/'raw/source.md';private.write_text('Immutable fictional source.\n')
        before={p.relative_to(self.root).as_posix():p.read_bytes() for p in (self.root).rglob('*') if p.is_file()}
        result=brain.init_brain(self.root)
        self.assertEqual(result['created_files'],[])
        (self.root/'context/preferences.md').unlink()
        result=brain.init_brain(self.root)
        self.assertEqual(result['created_files'],['context/preferences.md'])
        for relative,data in before.items():self.assertEqual((self.root/relative).read_bytes(),data)
    def test_init_brain_preflights_all_destinations_before_writing(self):
        self.clear_private_fixture()
        collision=self.root/'context';collision.write_text('Keep this existing file.')
        with self.assertRaisesRegex(brain.BrainError,'Expected a directory'):brain.init_brain(self.root)
        self.assertFalse((self.root/'registry.json').exists())
        self.assertFalse((self.root/'Projects').exists())
        self.assertTrue((self.root/'templates/root/registry.json').exists())
        self.assertEqual(collision.read_text(),'Keep this existing file.')
    def test_init_brain_rejects_symlink_boundary(self):
        shutil.move(self.root/'context',self.base/'private-context')
        (self.root/'context').symlink_to(self.base/'private-context',target_is_directory=True)
        with self.assertRaisesRegex(brain.BrainError,'Symlink'):brain.init_brain(self.root)
        with self.assertRaisesRegex(brain.BrainError,'Symlink'):brain.resolve_brain(self.root)
    def test_new_project_auto_initializes_and_updates_only_generated_index_section(self):
        self.clear_private_fixture()
        result=brain.new_project(self.root,'career','Fictional career',workspace_type='career')
        self.assertEqual(Path(result['path']),self.root/'Projects/career')
        index=(self.root/'INDEX.md').read_text()
        self.assertIn('Keep this manual introduction.',index)
        self.assertIn('Keep these manual notes.',index)
        self.assertIn('[Fictional career](Projects/career/PROJECT.md)',index)
        self.assertEqual([item['slug'] for item in brain.load_registry(self.root)['workspaces']],['career'])
        self.assertFalse((self.root/'brain').exists())
    def test_new_project_preserves_index_when_markers_are_missing(self):
        index=self.root/'INDEX.md';index.write_text('Entirely user-written index.\n')
        registry=(self.root/'registry.json').read_bytes()
        with self.assertRaisesRegex(brain.BrainError,'marker pair'):brain.new_project(self.root,'gamma')
        self.assertFalse((self.root/'Projects/gamma').exists())
        self.assertEqual(index.read_text(),'Entirely user-written index.\n')
        self.assertEqual((self.root/'registry.json').read_bytes(),registry)
    def test_resolve_brain_requires_initialization_and_does_not_select_workspace(self):
        self.assertEqual(brain.resolve_brain(self.root),self.root)
        self.clear_private_fixture()
        with self.assertRaisesRegex(brain.BrainError,'init-brain'):brain.resolve_brain(self.root)
        self.assertTrue(self.root.is_dir())
        self.assertFalse((self.root/'registry.json').exists())
        self.assertFalse((self.root/'brain').exists())
    def test_nested_legacy_brain_requires_explicit_migration_without_any_writes(self):
        legacy=self.root/'brain';legacy.mkdir();(legacy/'keep.md').write_text('Legacy fictional material.')
        before=(self.root/'registry.json').read_bytes()
        actions=[lambda:brain.init_brain(self.root),lambda:brain.resolve_brain(self.root),
                 lambda:brain.resolve_project(self.root,'alpha',self.root),lambda:brain.list_projects(self.root),
                 lambda:brain.new_project(self.root,'gamma')]
        for action in actions:
            with self.assertRaisesRegex(brain.BrainError,'docs/MIGRATION.md'):action()
        self.assertEqual((legacy/'keep.md').read_text(),'Legacy fictional material.')
        self.assertEqual((self.root/'registry.json').read_bytes(),before)
        self.assertFalse((self.root/'Projects/gamma').exists())
    def test_legacy_marker_rejects_all_layout_mutations_without_writes(self):
        (self.root/'.brain').write_text('brain:1\n')
        before=self.snapshot()
        for action in (lambda:brain.init_brain(self.root),lambda:brain.new_project(self.root,'gamma'),
                       lambda:brain.setup(self.root),lambda:brain.build_release(self.root),
                       lambda:brain.resolve_brain(self.root)):
            with self.assertRaisesRegex(brain.BrainError,'docs/MIGRATION.md'):action()
            self.assertEqual(self.snapshot(),before)
    def test_missing_or_unknown_marker_requires_migration_without_adopting_files(self):
        marker=self.root/'.brain'
        for value in (None,'previous-toolkit:2\n'):
            with self.subTest(value=value):
                if value is None:marker.unlink()
                else:marker.write_text(value)
                before=self.snapshot()
                for action in (lambda:brain.init_brain(self.root),lambda:brain.setup(self.root)):
                    with self.assertRaisesRegex(brain.BrainError,'docs/MIGRATION.md'):action()
                    self.assertEqual(self.snapshot(),before)
    def test_prior_installation_identity_is_not_adopted_or_overwritten(self):
        brain.setup(self.root)
        manifest=self.root/brain.STATE
        state=json.loads(manifest.read_text())
        state['toolkit']='previous-toolkit'
        manifest.write_text(json.dumps(state))
        before=self.snapshot()
        for action in (lambda:brain.setup(self.root),lambda:brain.uninstall(self.root)):
            with self.assertRaisesRegex(brain.BrainError,'Unrecognized installation manifest'):action()
            self.assertEqual(self.snapshot(),before)
    def test_old_projects_without_registry_are_not_adopted_after_marker_change(self):
        # A user changing only the marker still cannot silently adopt legacy folders.
        (self.root/'registry.json').unlink()
        with self.assertRaisesRegex(brain.BrainError,'Restore it from backup'):
            brain.init_brain(self.root)
        self.assertFalse((self.root/'registry.json').exists())
        self.assertTrue((self.alpha/'private.md').is_file())
    def test_private_path_boundary_excludes_toolkit_and_unknown_paths(self):
        for relative in ('AGENTS.md','README.md','docs/OPERATING_GUIDE.md','scripts/brain.py','templates/root/INDEX.md',
                         'skills/brain-sample/SKILL.md','.local/installation.json','unknown/file.md',
                         'registry.json/child','INDEX.md/child','brain/raw/source.md'):
            with self.subTest(relative=relative),self.assertRaisesRegex(brain.BrainError,'Not a private Brain path'):
                brain.safe_brain_path(self.root,relative)
        for relative in ('INDEX.md','registry.json','integrations.json','context/goals.md',
                         'raw/source.md','inbox/item.json','outputs/plan.md','maintenance/runs/report.md',
                         'Projects/alpha/wiki/INDEX.md'):
            self.assertEqual(brain.safe_brain_path(self.root,relative),self.root/relative)
    def test_initializer_rejects_public_files_in_private_scaffold_before_writes(self):
        self.clear_private_fixture()
        (self.root/'templates/root/AGENTS.md').write_text('Must not replace public instructions.')
        before=self.snapshot()
        with self.assertRaisesRegex(brain.BrainError,'Not a private Brain path'):
            brain.init_brain(self.root)
        self.assertEqual(self.snapshot(),before)
    def test_list_projects_respects_active_planning_and_review_flags(self):
        brain.new_project(self.root,'gamma');brain.new_project(self.root,'delta')
        def configure(data):
            by_slug={entry['slug']:entry for entry in data['workspaces']}
            by_slug['alpha']['review']=False
            by_slug['beta']['status']='paused'
            by_slug['gamma']['status']='archived'
            by_slug['delta']['planning']=False
        self.update_registry(configure)
        expected={'active':['alpha','delta'],'planning':['alpha'],'review':['delta'],'all':['alpha','beta','gamma','delta']}
        for scope,slugs in expected.items():
            listed=brain.list_projects(self.root,scope)
            self.assertEqual([item['slug'] for item in listed],slugs)
            self.assertTrue(all(Path(item['path']).is_relative_to(self.root/'Projects') for item in listed))
        with self.assertRaisesRegex(brain.BrainError,'scope'):brain.list_projects(self.root,'unknown')
    def test_registry_metadata_commands_do_not_read_workspace_or_application_content(self):
        external=self.base/'external-code'
        self.update_registry(lambda data:data['workspaces'][0].update(application={'kind':'external','path':str(external)}))
        original_text=Path.read_text;original_bytes=Path.read_bytes
        def metadata_text(path,*args,**kwargs):
            self.assertFalse(path.is_relative_to(self.root/'Projects'))
            self.assertFalse(path.is_relative_to(external))
            return original_text(path,*args,**kwargs)
        def metadata_bytes(path,*args,**kwargs):
            self.assertFalse(path.is_relative_to(self.root/'Projects'))
            self.assertFalse(path.is_relative_to(external))
            return original_bytes(path,*args,**kwargs)
        with patch.object(Path,'read_text',metadata_text),patch.object(Path,'read_bytes',metadata_bytes):
            listed=brain.list_projects(self.root,'all')
            self.assertEqual(brain.resolve_project(self.root,'alpha',self.root),self.alpha)
        self.assertEqual(listed[0]['application']['path'],str(external))
        self.assertFalse(external.exists())
    def test_unavailable_workspace_is_reported_without_blocking_other_coverage(self):
        shutil.rmtree(self.beta)
        listed=brain.list_projects(self.root,'review')
        self.assertEqual([entry['slug'] for entry in listed],['alpha','beta'])
        self.assertTrue(listed[0]['available'])
        self.assertFalse(listed[1]['available'])
        self.assertIn('missing',listed[1]['error'])
        self.assertEqual(brain.resolve_project(self.root,'alpha',self.root),self.alpha)
        with self.assertRaisesRegex(brain.BrainError,'missing'):
            brain.resolve_project(self.root,'beta',self.root)
    def test_invalid_registry_is_rejected_without_repair_or_new_workspace(self):
        registry_path=self.root/'registry.json';original=json.loads(registry_path.read_text())
        cases=[{'schema_version':True,'workspaces':[]},{'schema_version':1,'workspaces':{}},
               {**original,'workspaces':original['workspaces']+[original['workspaces'][0]]}]
        for override in ({'slug':'../escape'},{'name':'two\nlines'},{'type':'unknown'},{'status':'deleted'},
                         {'planning':'true'},{'review':1},{'path':'../elsewhere'},
                         {'application':{'kind':'internal','path':'../beta'}},{'application':{'kind':'external','path':'relative/app'}}):
            clone=json.loads(json.dumps(original));clone['workspaces'][0].update(override);cases.append(clone)
        for data in cases:
            with self.subTest(data=data):
                text=json.dumps(data);registry_path.write_text(text)
                with self.assertRaises(brain.BrainError):brain.list_projects(self.root,'all')
                with self.assertRaises(brain.BrainError):brain.new_project(self.root,'gamma')
                self.assertEqual(registry_path.read_text(),text)
                self.assertFalse((self.root/'Projects/gamma').exists())
    def test_unregistered_workspace_is_not_discovered_or_selected(self):
        orphan=self.root/'Projects/orphan';orphan.mkdir();(orphan/'PROJECT.md').write_text('Not registered.')
        with self.assertRaisesRegex(brain.BrainError,'Unregistered workspace folders: orphan'):brain.list_projects(self.root,'all')
        with self.assertRaisesRegex(brain.BrainError,'registry'):brain.resolve_project(self.root,'orphan',self.root)
        with self.assertRaisesRegex(brain.BrainError,'Unregistered workspace folders: orphan'):brain.new_project(self.root,'orphan')
        self.assertEqual((orphan/'PROJECT.md').read_text(),'Not registered.')
    def test_missing_registry_with_existing_projects_is_not_recreated_empty(self):
        registry=self.root/'registry.json';registry.unlink()
        before={p.relative_to(self.root).as_posix():p.read_bytes() for p in (self.root).rglob('*') if p.is_file()}
        for action in (lambda:brain.init_brain(self.root),lambda:brain.new_project(self.root,'gamma')):
            with self.assertRaisesRegex(brain.BrainError,'Restore it from backup'):action()
            self.assertFalse(registry.exists())
        after={p.relative_to(self.root).as_posix():p.read_bytes() for p in (self.root).rglob('*') if p.is_file()}
        self.assertEqual(before,after)
        self.assertFalse((self.root/'.local/brain-metadata.lock').exists())
    def test_empty_registry_with_existing_projects_requires_explicit_repair(self):
        registry=self.root/'registry.json';registry.write_text(json.dumps({'schema_version':1,'workspaces':[]}))
        before=registry.read_bytes()
        for action in (lambda:brain.init_brain(self.root),lambda:brain.list_projects(self.root,'all')):
            with self.assertRaisesRegex(brain.BrainError,'Unregistered workspace folders: alpha, beta'):action()
        self.assertEqual(registry.read_bytes(),before)
        self.assertTrue(self.alpha.is_dir());self.assertTrue(self.beta.is_dir())
    def test_concurrent_workspace_creation_requires_retry_without_losing_registration(self):
        entered=threading.Event();release=threading.Event()
        original_plan=brain.plan_brain_init
        def held_plan(root):
            value=original_plan(root)
            entered.set()
            if not release.wait(timeout=10):raise AssertionError('Timed out waiting to release creation preflight.')
            return value
        with patch.object(brain,'plan_brain_init',held_plan),ThreadPoolExecutor(max_workers=1) as pool:
            first=pool.submit(brain.new_project,self.root,'gamma')
            try:
                self.assertTrue(entered.wait(timeout=10))
                with self.assertRaisesRegex(brain.BrainError,'metadata is being updated'):brain.new_project(self.root,'delta')
                with self.assertRaisesRegex(brain.BrainError,'metadata is being updated'):brain.init_brain(self.root)
                self.assertFalse((self.root/'Projects/delta').exists())
                self.assertTrue((self.root/'.local/brain-metadata.lock').exists())
            finally:release.set()
            self.assertEqual(first.result(timeout=10)['project'],'gamma')
        self.assertFalse((self.root/'.local/brain-metadata.lock').exists())
        brain.new_project(self.root,'delta')
        self.assertEqual([item['slug'] for item in brain.list_projects(self.root,'all')],['alpha','beta','gamma','delta'])
        index=(self.root/'INDEX.md').read_text()
        self.assertIn('Projects/gamma/PROJECT.md',index);self.assertIn('Projects/delta/PROJECT.md',index)
    def test_metadata_lock_is_released_after_failed_preflight(self):
        with self.assertRaises(brain.BrainError):brain.new_project(self.root,'alpha')
        self.assertFalse((self.root/'.local/brain-metadata.lock').exists())
        self.assertEqual(brain.new_project(self.root,'gamma')['project'],'gamma')
    def test_shared_paths_reject_traversal_and_symlink_escape(self):
        self.assertEqual(brain.safe_brain_path(self.root,'raw/source.md'),self.root/'raw/source.md')
        for relative in ('../README.md','/tmp/outside','raw/../../outside','raw\\..\\outside'):
            with self.assertRaises(brain.BrainError):brain.safe_brain_path(self.root,relative)
        (self.root/'raw/linked').symlink_to(self.base,target_is_directory=True)
        with self.assertRaisesRegex(brain.BrainError,'Symlink'):brain.safe_brain_path(self.root,'raw/linked/private.md')
    def test_registry_internal_application_symlink_is_rejected(self):
        (self.alpha/'app').symlink_to(self.beta,target_is_directory=True)
        self.update_registry(lambda data:data['workspaces'][0].update(application={'kind':'internal','path':'app'}))
        with self.assertRaisesRegex(brain.BrainError,'Symlink'):brain.list_projects(self.root,'all')
    def test_cli_whole_brain_commands_use_registry_scope(self):
        output=io.StringIO()
        with patch.object(brain,'TOOLKIT_ROOT',self.root),redirect_stdout(output):
            self.assertEqual(brain.main(['list-projects','--scope','planning']),0)
        self.assertEqual([item['slug'] for item in json.loads(output.getvalue())],['alpha','beta'])
        output=io.StringIO()
        with patch.object(brain,'TOOLKIT_ROOT',self.root),redirect_stdout(output):
            self.assertEqual(brain.main(['resolve-brain']),0)
        self.assertEqual(output.getvalue().strip(),str(self.root))
    def test_explicit_project(self):
        self.assertEqual(brain.resolve_project(self.root,'alpha',self.root),self.alpha)
    def test_infer_nested_project(self):
        self.assertEqual(brain.resolve_project(self.root,None,self.alpha/'wiki'),self.alpha)
    def test_root_asks_even_one_project(self):
        shutil.rmtree(self.beta)
        with self.assertRaisesRegex(brain.BrainError,'No workspace selected'):brain.resolve_project(self.root,None,self.root)
    def test_conflict_rejected(self):
        with self.assertRaisesRegex(brain.BrainError,'Project conflict'):brain.resolve_project(self.root,'alpha',self.beta)
    def test_unknown_business(self):
        with self.assertRaisesRegex(brain.BrainError,'does not exist'):brain.resolve_project(self.root,'missing',self.root)
    def test_no_parent_traversal(self):
        for p in ['../beta/private.md','/tmp/other','x/../../outside','x\\..\\outside']:
            with self.subTest(p=p),self.assertRaises(brain.BrainError):brain.safe_project_path(self.alpha,p)
    def test_nested_symlink_cannot_read_other_business(self):
        (self.alpha/'linked').symlink_to(self.beta,target_is_directory=True)
        with self.assertRaisesRegex(brain.BrainError,'Symlink'):brain.safe_project_path(self.alpha,'linked/private.md')
    def test_business_symlink_rejected(self):
        (self.root/'Projects/gamma').symlink_to(self.beta,target_is_directory=True)
        with self.assertRaises(brain.BrainError):brain.resolve_project(self.root,'gamma',self.root)
    def test_cwd_symlink_rejected(self):
        (self.root/'Projects/gamma').symlink_to(self.beta,target_is_directory=True)
        with self.assertRaises(brain.BrainError):brain.resolve_project(self.root,None,self.root/'Projects/gamma/wiki')
    def test_alias_above_toolkit_keeps_internal_symlink_checks(self):
        alias=self.base/'alias';alias.symlink_to(self.root,target_is_directory=True)
        (self.root/'Projects/gamma').symlink_to(self.beta,target_is_directory=True)
        with self.assertRaises(brain.BrainError):brain.resolve_project(self.root,None,alias/'Projects/gamma/wiki')
        self.assertEqual(brain.resolve_project(self.root,'alpha',alias),self.alpha)
    def test_business_loop_to_root_cannot_hide_business_boundary(self):
        (self.alpha/'loop').symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(brain.BrainError):
            brain.resolve_project(self.root,None,self.alpha/'loop/Projects/beta/wiki')
        alias=self.base/'outer-alias';alias.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(brain.BrainError):
            brain.resolve_project(self.root,None,alias/'Projects/alpha/loop/Projects/beta/wiki')
    def test_projects_root_symlink_rejected(self):
        shutil.move(self.root/'Projects',self.base/'elsewhere')
        (self.root/'Projects').symlink_to(self.base/'elsewhere',target_is_directory=True)
        with self.assertRaises(brain.BrainError):brain.resolve_project(self.root,'alpha',self.root)
    def test_new_project_does_not_overwrite(self):
        old=(self.alpha/'PROJECT.md').read_bytes()
        with self.assertRaises(brain.BrainError):brain.new_project(self.root,'alpha')
        self.assertEqual(old,(self.alpha/'PROJECT.md').read_bytes())
    def test_reserved_and_invalid_names(self):
        for name in ['../beta','Alpha','con','nul','a/b','a b','a'*65]:
            with self.subTest(name=name),self.assertRaises(brain.BrainError):brain.new_project(self.root,name)
    def test_workspace_types_and_purposes(self):
        for kind in brain.WORKSPACE_TYPES:
            with self.subTest(kind=kind):
                slug='example-'+kind
                result=brain.new_project(self.root,slug,'Example workspace',workspace_type=kind,purpose='Explore a fictional goal.')
                created=self.root/'Projects'/slug
                self.assertEqual(result['workspace_type'],kind)
                text=(created/'PROJECT.md').read_text()
                self.assertIn('Type: '+kind,text)
                self.assertIn('Purpose: Explore a fictional goal.',text)
                self.assertNotIn('{{',text)
                self.assertEqual(brain.resolve_project(self.root,slug,self.root),created)
        with self.assertRaisesRegex(brain.BrainError,'No workspace selected'):brain.resolve_project(self.root,None,self.root)
    def test_workspace_defaults_keep_legacy_positional_name(self):
        result=brain.new_project(self.root,'gamma','Existing API caller')
        text=(self.root/'Projects/gamma/PROJECT.md').read_text()
        self.assertEqual(result['project'],'gamma')
        self.assertEqual(result['workspace_type'],'general')
        self.assertIn('# Existing API caller\n',text)
        self.assertIn('Type: general\nPurpose: Unknown — not supplied.',text)
    def test_invalid_workspace_metadata_creates_nothing(self):
        cases=[{'workspace_type':'team'},{'workspace_type':None},{'name':''},{'name':' '},{'name':'x'*121},
               {'name':'two\nlines'},{'purpose':''},{'purpose':' '},{'purpose':'x'*501},
               {'purpose':'two\rline'},{'purpose':'control\x00text'},{'purpose':'two\u2028lines'},{'purpose':10}]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs),self.assertRaises(brain.BrainError):brain.new_project(self.root,'invalid',**kwargs)
            self.assertFalse((self.root/'Projects/invalid').exists())
    def test_new_project_cli_uses_workspace_metadata(self):
        output=io.StringIO()
        with patch.object(brain,'TOOLKIT_ROOT',self.root),redirect_stdout(output):
            code=brain.main(['new-project','sample-career','--name','Sample career','--type','career','--purpose','Practice a fictional interview.'])
        self.assertEqual(code,0)
        self.assertEqual(json.loads(output.getvalue())['workspace_type'],'career')
        text=(self.root/'Projects/sample-career/PROJECT.md').read_text()
        self.assertIn('Type: career\nPurpose: Practice a fictional interview.',text)
    def test_template_read_failure_leaves_no_partial_workspace(self):
        (self.root/'templates/project/zz-invalid.md').write_bytes(b'\xff')
        with self.assertRaises(UnicodeError):brain.new_project(self.root,'gamma')
        self.assertFalse((self.root/'Projects/gamma').exists())
    def test_finder_metadata_does_not_block_lifecycle_or_enter_outputs(self):
        metadata=['skills/.DS_Store','skills/brain-sample/.DS_Store','optional-skills/.DS_Store',
                  'templates/project/.DS_Store','templates/project/wiki/.DS_Store']
        for rel in metadata:(self.root/rel).write_bytes(b'Finder metadata')
        self.assertFalse(brain.verify(self.root)['installed'])
        brain.setup(self.root,True)
        brain.new_project(self.root,'gamma')
        for host in brain.HOSTS:
            self.assertFalse(list((self.root/host).rglob('.DS_Store')))
        self.assertFalse(list((self.root/'Projects/gamma').rglob('.DS_Store')))
        result=brain.build_release(self.root)
        with zipfile.ZipFile(result['archive']) as archive:
            self.assertFalse(any('.DS_Store' in name for name in archive.namelist()))
        self.assertTrue(all((self.root/rel).exists() for rel in metadata))
    def test_fresh_verify_rejects_uninstallable_bundle_path(self):
        (self.root/'skills/unexpected.md').write_text('Unbundled resource')
        with self.assertRaisesRegex(brain.BrainError,'Invalid skill bundle path'):brain.verify(self.root)
        self.assertFalse((self.root/brain.STATE).exists())
    def test_setup_idempotence(self):
        brain.setup(self.root);first=(self.root/brain.STATE).read_bytes()
        brain.setup(self.root);self.assertEqual(first,(self.root/brain.STATE).read_bytes())
        self.assertEqual(brain.verify(self.root,True)['canonical_skills'],2)
    def test_visual_opt_in_retained_on_upgrade(self):
        brain.setup(self.root);self.assertFalse((self.root/'.agents/skills/brain-visual').exists())
        brain.setup(self.root,visuals=True);brain.setup(self.root)
        self.assertTrue((self.root/'.agents/skills/brain-visual/SKILL.md').exists())
    def test_fresh_unprefixed_skills_install_for_both_hosts(self):
        self.rename_fixture_skills()
        self.assertEqual(brain.setup(self.root)['skills'],1)
        for host in brain.HOSTS:
            self.assertEqual((self.root/host/'sample/SKILL.md').read_bytes(),(self.root/'skills/sample/SKILL.md').read_bytes())
            self.assertFalse((self.root/host/'visual').exists())
            self.assertFalse((self.root/host/'brain-sample').exists())
        self.assertEqual(brain.setup(self.root,visuals=True)['skills'],2)
        self.assertTrue(brain.verify(self.root,installed=True)['installed'])
        for host in brain.HOSTS:self.assertTrue((self.root/host/'visual/SKILL.md').is_file())
    def test_renamed_skills_upgrade_legacy_manifest_and_prune_only_empty_owned_dirs(self):
        resource=self.root/'skills/brain-sample/references/example.md'
        resource.parent.mkdir();resource.write_text('Fictional shared method.')
        self.public.add(resource.relative_to(self.root).as_posix());self.write_allowlist()
        brain.setup(self.root,visuals=True)
        statepath=self.root/brain.STATE
        state=json.loads(statepath.read_text());state['version']='0.4.2';statepath.write_text(json.dumps(state))
        private_before=(self.alpha/'private.md').read_bytes()
        self.rename_fixture_skills()
        brain.setup(self.root)
        upgraded=json.loads(statepath.read_text())
        self.assertTrue(upgraded['visuals'])
        self.assertEqual(upgraded['version'],brain.VERSION)
        self.assertFalse(any('/brain-sample/' in path or '/brain-visual/' in path for path in upgraded['files']))
        for host in brain.HOSTS:
            self.assertFalse((self.root/host/'brain-sample').exists())
            self.assertFalse((self.root/host/'brain-visual').exists())
            self.assertEqual((self.root/host/'sample/references/example.md').read_text(),'Fictional shared method.')
            self.assertTrue((self.root/host/'visual/SKILL.md').is_file())
            self.assertTrue((self.root/host).is_dir())
        self.assertEqual((self.alpha/'private.md').read_bytes(),private_before)
        self.assertTrue(brain.verify(self.root,installed=True)['installed'])
        brain.uninstall(self.root)
        for host in brain.HOSTS:self.assertFalse((self.root/host/'sample/SKILL.md').exists())
    def test_rename_upgrade_preserves_modified_legacy_skill_without_partial_changes(self):
        brain.setup(self.root)
        (self.root/'.claude/skills/brain-sample/SKILL.md').write_text('User customized legacy skill.')
        self.rename_fixture_skills()
        before=self.snapshot()
        with self.assertRaisesRegex(brain.BrainError,'Locally modified generated file'):
            brain.setup(self.root)
        self.assertEqual(self.snapshot(),before)
        for host in brain.HOSTS:self.assertFalse((self.root/host/'sample').exists())
    def test_rename_upgrade_does_not_adopt_unmanaged_new_name_even_if_bytes_match(self):
        brain.setup(self.root)
        self.rename_fixture_skills()
        target=self.root/'.claude/skills/sample/SKILL.md'
        target.parent.mkdir();target.write_bytes((self.root/'skills/sample/SKILL.md').read_bytes())
        before=self.snapshot()
        with self.assertRaisesRegex(brain.BrainError,'Unmanaged file'):
            brain.setup(self.root)
        self.assertEqual(self.snapshot(),before)
        for host in brain.HOSTS:self.assertTrue((self.root/host/'brain-sample/SKILL.md').is_file())
    def test_rename_upgrade_preserves_unmanaged_legacy_directory_contents(self):
        brain.setup(self.root)
        preserved={
            '.agents/skills/brain-sample/my-notes.md':b'Custom notes remain.',
            '.agents/skills/brain-sample/.DS_Store':b'Finder metadata is not owned.',
            '.claude/skills/unrelated/SKILL.md':b'An unrelated local skill.',
        }
        for relative,data in preserved.items():
            path=self.root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        self.rename_fixture_skills()
        brain.setup(self.root)
        for relative,data in preserved.items():self.assertEqual((self.root/relative).read_bytes(),data)
        self.assertFalse((self.root/'.agents/skills/brain-sample/SKILL.md').exists())
        self.assertFalse((self.root/'.claude/skills/brain-sample').exists())
        self.assertTrue(brain.verify(self.root,installed=True)['installed'])
        brain.uninstall(self.root)
        for relative,data in preserved.items():self.assertEqual((self.root/relative).read_bytes(),data)
    def test_modified_generated_file_blocks_whole_setup(self):
        brain.setup(self.root)
        target=self.root/'.claude/skills/brain-sample/SKILL.md';target.write_text('my changes')
        source=self.root/'skills/brain-sample/SKILL.md';source.write_text(source.read_text()+'new canonical change\n')
        untouched=self.root/'.agents/skills/brain-sample/SKILL.md';before=untouched.read_bytes()
        with self.assertRaisesRegex(brain.BrainError,'modified'):brain.setup(self.root)
        self.assertEqual(target.read_text(),'my changes');self.assertEqual(before,untouched.read_bytes())
    def test_unknown_file_not_adopted(self):
        target=self.root/'.agents/skills/brain-sample/SKILL.md';target.parent.mkdir(parents=True);target.write_text('other installer')
        with self.assertRaisesRegex(brain.BrainError,'Unmanaged'):brain.setup(self.root)
        self.assertFalse((self.root/brain.STATE).exists())
    def test_generation_symlink_escape_rejected(self):
        (self.root/'.agents').symlink_to(self.base/'outside',target_is_directory=True)
        with self.assertRaises(brain.BrainError):brain.setup(self.root)
        self.assertFalse((self.base/'outside').exists())
    def test_canonical_symlink_rejected(self):
        (self.root/'skills/brain-sample/data').symlink_to(self.alpha,target_is_directory=True)
        with self.assertRaises(brain.BrainError):brain.setup(self.root)
    def test_manifest_traversal_rejected(self):
        p=self.root/brain.STATE;p.parent.mkdir();p.write_text(json.dumps({'schema_version':1,'toolkit':'brain','files':{'../outside':'0'*64}}))
        with self.assertRaisesRegex(brain.BrainError,'Unsafe'):brain.uninstall(self.root)
    def test_manifest_cannot_own_private_project(self):
        p=self.root/brain.STATE;p.parent.mkdir();p.write_text(json.dumps({'schema_version':1,'toolkit':'brain','files':{'Projects/alpha/private.md':'0'*64}}))
        with self.assertRaises(brain.BrainError):brain.setup(self.root)
    def test_upgrade_updates_only_owned_files(self):
        brain.setup(self.root)
        source=self.root/'skills/brain-sample/SKILL.md';source.write_text(source.read_text()+'A useful new instruction.\n')
        brain.setup(self.root)
        self.assertEqual(source.read_bytes(),(self.root/'.agents/skills/brain-sample/SKILL.md').read_bytes())
        self.assertEqual((self.alpha/'private.md').read_text(),'ALPHA_ONLY_SENTINEL')
    def test_uninstall_preserves_projects_and_other_skills(self):
        brain.setup(self.root)
        p=self.root/'.agents/skills/someone-elses/SKILL.md';p.parent.mkdir();p.write_text('not ours')
        brain.uninstall(self.root)
        self.assertEqual(p.read_text(),'not ours');self.assertTrue(self.alpha.exists())
        self.assertTrue((self.root/'skills/brain-sample/SKILL.md').exists())
        self.assertFalse((self.root/brain.STATE).exists())
    def test_uninstall_refuses_modified_files(self):
        brain.setup(self.root);p=self.root/'.agents/skills/brain-sample/SKILL.md';p.write_text('custom')
        with self.assertRaises(brain.BrainError):brain.uninstall(self.root)
        self.assertEqual(p.read_text(),'custom');self.assertTrue((self.root/brain.STATE).exists())
    def test_relocation_uses_relative_manifest(self):
        brain.setup(self.root,True);moved=self.base/'renamed toolkit';shutil.move(self.root,moved)
        self.assertTrue(brain.verify(moved,True)['installed'])
        self.assertEqual(brain.resolve_project(moved,'alpha',moved),moved/'Projects/alpha')
        brain.uninstall(moved);self.assertTrue((moved/'Projects/alpha/private.md').exists())
    def test_release_excludes_private_and_unlisted_files(self):
        brain.setup(self.root,True)
        (self.root/'.env').write_text('PRIVATE_CONFIGURATION_SENTINEL')
        (self.root/'raw/source.md').write_text('SHARED_PRIVATE_SOURCE_SENTINEL')
        legacy=self.root/'brain';legacy.mkdir();(legacy/'source.md').write_text('LEGACY_PRIVATE_SOURCE_SENTINEL')
        (self.root/'examples').mkdir();(self.root/'examples/unreviewed.md').write_text('NOT_APPROVED_SENTINEL')
        r=brain.build_release(self.root)
        with zipfile.ZipFile(r['archive']) as z:
            joined=b'\n'.join(z.read(name) for name in z.namelist())
            for sentinel in [b'ALPHA_ONLY',b'BETA_ONLY',b'PRIVATE_CONFIGURATION',b'NOT_APPROVED',b'SHARED_PRIVATE_SOURCE',b'LEGACY_PRIVATE_SOURCE']:
                self.assertNotIn(sentinel,joined)
            self.assertEqual(set(z.namelist()),{'Brain/'+x for x in self.public})
    def test_release_rejects_private_even_allowlisted(self):
        self.public.add('Projects/alpha/private.md');self.write_allowlist()
        with self.assertRaisesRegex(brain.BrainError,'Private'):brain.build_release(self.root)
        self.assertFalse((self.root/'dist').exists())
    def test_release_rejects_shared_and_legacy_private_roots_even_allowlisted(self):
        for relative in ('INDEX.md','registry.json','integrations.json','context/goals.md','raw/source.md','Projects/legacy.md','inbox/source.json','maintenance/runs/private.md','outputs/plan.md','brain/raw/old.md'):
            with self.subTest(relative=relative):
                self.public.add(relative);self.write_allowlist()
                with self.assertRaisesRegex(brain.BrainError,'Private or unknown release path'):brain.release_files(self.root)
                self.public.remove(relative)
    def test_malformed_release_allowlist_is_an_actionable_diagnostic(self):
        for manifest in ([{}],[None],[17],{'file':'README.md'}):
            with self.subTest(manifest=manifest):
                (self.root/'release-files.json').write_text(json.dumps(manifest))
                with self.assertRaisesRegex(brain.BrainError,'file path strings'):brain.release_files(self.root)
                report=brain.doctor(self.root)
                self.assertEqual(report['release_check']['status'],'blocked')
                self.assertIn('file path strings',report['release_check']['error'])
    def test_release_rejects_symlink_even_allowlisted(self):
        (self.root/'examples').mkdir();(self.root/'examples/link.md').symlink_to(self.alpha/'private.md')
        self.public.add('examples/link.md');self.write_allowlist()
        with self.assertRaises(brain.BrainError):brain.build_release(self.root)
    def test_release_detects_secret_fixture(self):
        (self.root/'examples').mkdir();(self.root/'examples/secret.md').write_text('gh'+'p_'+'x'*36)
        self.public.add('examples/secret.md');self.write_allowlist()
        with self.assertRaisesRegex(brain.BrainError,'Potential secret'):brain.build_release(self.root)
    def test_release_detects_quoted_credential_keys(self):
        folder=self.root/'examples';folder.mkdir()
        source=folder/'settings.json'
        self.public.add('examples/settings.json');self.write_allowlist()
        fields=['api'+'_key','access'+'_token','pass'+'word']
        for field in fields:
            for syntax in ('json','single-quoted','unquoted'):
                with self.subTest(field=field,syntax=syntax):
                    value='synthetic-'+'x'*24
                    if syntax=='json':text=json.dumps({field:value})
                    elif syntax=='single-quoted':text=repr(field)+': '+repr(value)
                    else:text=field+' = '+repr(value)
                    source.write_text(text)
                    with self.assertRaisesRegex(brain.BrainError,'Potential secret'):brain.release_files(self.root)
        source.write_text(json.dumps({field:None for field in fields}))
        self.assertTrue(brain.release_files(self.root))
    def test_release_detects_prefixed_credential_keys(self):
        folder=self.root/'examples';folder.mkdir()
        source=folder/'settings.txt'
        self.public.add('examples/settings.txt');self.write_allowlist()
        fields=['OPENAI_'+'API_KEY','SERVICE_'+'ACCESS_TOKEN','DB_'+'PASSWORD']
        for field in fields:
            for syntax in ('environment','json','single-quoted'):
                with self.subTest(field=field,syntax=syntax):
                    value='synthetic-'+'x'*24
                    if syntax=='json':text=json.dumps({field:value})
                    elif syntax=='single-quoted':text=repr(field)+': '+repr(value)
                    else:text=field+'='+repr(value)
                    source.write_text(text)
                    with self.assertRaisesRegex(brain.BrainError,'Potential secret'):brain.release_files(self.root)
    def test_release_rejects_finder_metadata_even_allowlisted(self):
        (self.root/'skills/.DS_Store').write_bytes(b'Finder metadata')
        self.public.add('skills/.DS_Store');self.write_allowlist()
        with self.assertRaisesRegex(brain.BrainError,'Private or unknown release path'):brain.release_files(self.root)
    def test_doctor_reports_release_readiness_without_reading_workspaces(self):
        original_read_bytes=Path.read_bytes
        original_read_text=Path.read_text
        def public_read_bytes(path,*args,**kwargs):
            self.assertFalse(path.is_relative_to(self.root/'Projects'))
            return original_read_bytes(path,*args,**kwargs)
        def public_read_text(path,*args,**kwargs):
            self.assertFalse(path.is_relative_to(self.root/'Projects'))
            return original_read_text(path,*args,**kwargs)
        with patch.object(Path,'read_bytes',public_read_bytes),patch.object(Path,'read_text',public_read_text):
            report=brain.doctor(self.root)
            self.assertEqual(report['release_check']['status'],'ready')
            self.assertEqual(report['release_check']['public_files'],len(self.public))
            (self.root/'skills/brain-sample/new-reference.md').write_text('Unreviewed public method')
            report=brain.doctor(self.root)
            self.assertEqual(report['verification']['status'],'verified')
            self.assertEqual(report['release_check']['status'],'blocked')
            self.assertIn('workflow resources',report['release_check']['error'])
        self.assertFalse((self.root/'dist').exists())
    def test_release_never_overwrites(self):
        r=brain.build_release(self.root);before=Path(r['archive']).read_bytes()
        with self.assertRaises(brain.BrainError):brain.build_release(self.root)
        self.assertEqual(before,Path(r['archive']).read_bytes())
    def test_release_race_preserves_other_archive(self):
        original_open=Path.open
        def competing_open(path,mode='r',*args,**kwargs):
            if mode=='xb' and path.suffix=='.zip':
                with original_open(path,'wb') as stream:stream.write(b'OTHER_ARCHIVE')
                raise FileExistsError('Another process created the archive.')
            return original_open(path,mode,*args,**kwargs)
        with patch.object(Path,'open',competing_open),self.assertRaises(FileExistsError):
            brain.build_release(self.root)
        self.assertEqual((self.root/f'dist/Brain-{brain.VERSION}.zip').read_bytes(),b'OTHER_ARCHIVE')
    def test_release_omitted_skill_resource_rejected(self):
        (self.root/'skills/brain-sample/reference.md').write_text('Unreviewed method')
        with self.assertRaisesRegex(brain.BrainError,'workflow resources'):brain.build_release(self.root)
    def test_release_omitted_getting_started_guide_rejected(self):
        self.public.remove('docs/GETTING_STARTED.md');self.write_allowlist()
        with self.assertRaisesRegex(brain.BrainError,'required entrypoints or workflow resources'):brain.build_release(self.root)
        self.assertFalse((self.root/'dist').exists())
    def test_release_destination_cannot_be_private(self):
        with self.assertRaises(brain.BrainError):brain.build_release(self.root,self.alpha/'export.zip')
        with self.assertRaises(brain.BrainError):brain.build_release(self.root,self.base/'export.zip')
    def test_missing_coverage_fails_verification(self):
        (self.root/'capabilities.json').write_text(json.dumps([{'capability':'forgotten','skill':'brain-missing'}]))
        with self.assertRaisesRegex(brain.BrainError,'Unimplemented'):brain.verify(self.root)
    def test_modified_manifest_detected_by_verify(self):
        brain.setup(self.root);p=self.root/brain.STATE;state=json.loads(p.read_text());state['files'][next(iter(state['files']))]='0'*64;p.write_text(json.dumps(state))
        with self.assertRaisesRegex(brain.BrainError,'hash mismatch'):brain.verify(self.root,True)

if __name__=='__main__':unittest.main()
