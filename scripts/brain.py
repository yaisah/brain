#!/usr/bin/env python3
"""Local setup, project routing and allowlisted releases. Python 3.11+, stdlib only."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import hashlib
import html
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import zipfile

TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.5.0'
SLUG = re.compile(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z')
# Current unprefixed names and legacy brain-* manifest paths share this format.
SKILL = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
RESERVED = {'con','prn','aux','nul',*(f'com{i}' for i in range(1,10)),*(f'lpt{i}' for i in range(1,10))}
HOSTS = ('.agents/skills', '.claude/skills')
STATE = '.local/installation.json'
WORKSPACE_TYPES = ('business', 'career', 'personal', 'research', 'general')
IGNORED_FILE_NAMES = {'.DS_Store'}
WORKSPACE_STATUSES = ('active', 'paused', 'archived')
PROJECT_SCOPES = ('active', 'planning', 'review', 'all')
INDEX_START = '<!-- BEGIN WORKSPACES -->'
INDEX_END = '<!-- END WORKSPACES -->'
BRAIN_FILES = ('INDEX.md','registry.json','integrations.json','context/goals.md','context/preferences.md')
BRAIN_DIRS = ('Projects','inbox','raw','maintenance/runs','maintenance/evaluations','maintenance/cache','outputs')
PRIVATE_DIRECTORIES = frozenset({'Projects','inbox','raw','maintenance','outputs','context'})
PRIVATE_FILES = frozenset({'INDEX.md','registry.json','integrations.json'})

class BrainError(Exception):
    """An actionable validation error; no implicit fallback is permitted."""

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def checked_slug(value: str) -> str:
    if not isinstance(value,str) or not SLUG.fullmatch(value) or len(value)>64 or value in RESERVED:
        raise BrainError('Use a workspace/artifact name of at most 64 lowercase letters, digits and hyphens, starting with a letter; reserved device names are not allowed.')
    return value

def safe_under(base: Path, relative: str, *, allow_root: bool=False) -> Path:
    """Validate a relative path without following any symlink within base."""
    base = Path(base)
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in relative:
        raise BrainError(f'Unsafe relative path: {relative!r}')
    if not rel.parts and not allow_root:
        raise BrainError('An empty destination is not allowed.')
    if base.is_symlink():
        raise BrainError(f'Symlink boundary is not allowed: {base.name}')
    candidate = base
    for part in rel.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise BrainError(f'Symlinks are not allowed within this boundary: {relative}')
    if not candidate.resolve().is_relative_to(base.resolve()):
        raise BrainError('Resolved path escapes its boundary.')
    return candidate

def safe_project_path(project_path: Path, relative: str) -> Path:
    return safe_under(project_path, relative)

def require_root(root: Path) -> Path:
    root = Path(root).resolve()
    marker = safe_under(root, '.brain')
    version = marker.read_text().strip() if marker.is_file() else None
    if version == 'brain:1':
        raise BrainError('Legacy toolkit layout found. No files were moved or initialized. Back up the existing folder and follow docs/MIGRATION.md before using the flat Brain layout; changing only the marker is not a migration.')
    if version != 'brain:2':
        raise BrainError('This is not a Brain root with a valid .brain marker. Open a current Brain release or follow docs/MIGRATION.md; no files were initialized or adopted.')
    return root

def brain_location(root: Path) -> Path:
    root=require_root(root)
    legacy=safe_under(root,'brain')
    if legacy.exists():
        raise BrainError('Legacy nested brain/ found. No files were moved or selected. Back up the folder and follow docs/MIGRATION.md before using the flat Brain layout.')
    return root

def safe_brain_path(root: Path, relative: str) -> Path:
    """Validate private root content without allowing writes to toolkit files."""
    brain_path=brain_location(root)
    destination=safe_under(brain_path,relative)
    parts=Path(relative).parts
    if not (parts[0] in PRIVATE_DIRECTORIES or (len(parts)==1 and parts[0] in PRIVATE_FILES)):
        raise BrainError(f'Not a private Brain path: {relative!r}; toolkit files are outside this boundary.')
    return destination

def validate_registry(data, brain_path: Path):
    if not isinstance(data,dict) or type(data.get('schema_version')) is not int or data['schema_version']!=1 or not isinstance(data.get('workspaces'),list):
        raise BrainError('Invalid brain registry. Expected schema_version 1 and a workspaces list; preserve it and repair the metadata before continuing.')
    seen=set()
    for entry in data['workspaces']:
        if not isinstance(entry,dict):raise BrainError('Every registry workspace must be an object.')
        slug=checked_slug(entry.get('slug'))
        if slug in seen:raise BrainError(f'Duplicate registry workspace: {slug}.')
        seen.add(slug)
        one_line_text(entry.get('name'),'Registry workspace name',120)
        if entry.get('type') not in WORKSPACE_TYPES:raise BrainError(f'Invalid workspace type in registry: {slug}.')
        if entry.get('status') not in WORKSPACE_STATUSES:raise BrainError(f'Invalid workspace status in registry: {slug}.')
        if any(type(entry.get(field)) is not bool for field in ('planning','review')):
            raise BrainError(f'Registry planning and review flags must be booleans: {slug}.')
        # Slugs define paths. Do not accept registry path overrides or inspect app trees.
        if 'path' in entry:raise BrainError(f'Registry workspace paths are derived from slugs, not path overrides: {slug}.')
        workspace=safe_under(brain_path,f'Projects/{slug}')
        app=entry.get('application')
        if app is not None:
            if not isinstance(app,dict) or app.get('kind') not in ('internal','external') or not isinstance(app.get('path'),str):
                raise BrainError(f'Invalid application reference: {slug}.')
            path=app['path']
            one_line_text(path,'Application path',4096)
            if app['kind']=='internal':
                safe_under(workspace,path)
            elif not Path(path).is_absolute() or '..' in Path(path).parts or '\\' in path:
                raise BrainError(f'External application reference must be an explicit absolute path without traversal: {slug}.')
    return data

def read_brain_metadata(root: Path):
    brain_path=brain_location(root)
    for relative in BRAIN_FILES:
        if not safe_under(brain_path,relative).is_file():
            raise BrainError('The shared brain is not initialized. Run python3 scripts/brain.py init-brain first.')
    projects=safe_under(brain_path,'Projects')
    if not projects.is_dir():raise BrainError('The shared brain is incomplete: missing Projects/. Run init-brain to restore missing scaffold files.')
    return brain_path,validate_registry(read_json(safe_under(brain_path,'registry.json')),brain_path)

def resolve_brain(root: Path) -> Path:
    return read_brain_metadata(root)[0]

def load_registry(root: Path):
    return read_brain_metadata(root)[1]

def registered_project_path(brain_path: Path, entry: dict) -> Path:
    target=safe_under(brain_path,f'Projects/{entry["slug"]}')
    if not target.is_dir() or not safe_under(target,'PROJECT.md').is_file():
        raise BrainError(f'Registered workspace {entry["slug"]!r} is missing its directory or PROJECT.md. Restore it or explicitly repair the registry; nothing was selected implicitly.')
    return target

def require_registered_folders(brain_path: Path, registry: dict):
    projects=safe_under(brain_path,'Projects')
    if not projects.exists():return
    known={entry['slug'] for entry in registry['workspaces']}
    unknown=[]
    for child in projects.iterdir():
        if child.name in IGNORED_FILE_NAMES or child.name=='.gitkeep':continue
        safe_under(projects,child.name)
        if child.is_dir() and child.name not in known:unknown.append(child.name)
    if unknown:
        raise BrainError('Unregistered workspace folders: '+', '.join(sorted(unknown))+'. Back up the brain and explicitly repair registry.json using docs/MIGRATION.md; no folders were adopted or omitted silently.')

def list_projects(root: Path, scope: str='active'):
    if scope not in PROJECT_SCOPES:raise BrainError('Project scope must be active, planning, review, or all.')
    brain_path,registry=read_brain_metadata(root)
    require_registered_folders(brain_path,registry)
    result=[]
    for entry in registry['workspaces']:
        if scope!='all' and entry['status']!='active':continue
        if scope in ('planning','review') and not entry[scope]:continue
        item={**entry,'path':str(safe_under(brain_path,f'Projects/{entry["slug"]}'))}
        try:
            registered_project_path(brain_path,entry)
            item['available']=True
        except (BrainError,OSError) as exc:
            # A registered but unavailable workspace remains visible in coverage.
            # Independent workspaces can still be reviewed; single resolution fails.
            item.update(available=False,error=str(exc))
        result.append(item)
    return result

def resolve_project(root: Path, project: str | None=None, cwd: Path | None=None) -> Path:
    root = require_root(root)
    brain_path, registry = read_brain_metadata(root)
    projects = safe_under(brain_path, 'Projects')
    here = Path.cwd() if cwd is None else Path(cwd)
    # Inspect the lexical path as well as its resolution, to reject project symlinks.
    lexical = Path(os.path.abspath(here))
    # Normalize aliases ABOVE the toolkit (e.g. macOS /var -> /private/var)
    # without resolving a workspace-level symlink before validation.
    for anchor in reversed((lexical, *lexical.parents)):
        if anchor.resolve() == root:
            lexical = root / lexical.relative_to(anchor)
            break
    try:
        rel = lexical.relative_to(projects)
    except ValueError:
        rel = None
    inferred = None
    if rel and rel.parts:
        safe_under(projects, str(rel))
        inferred = checked_slug(rel.parts[0])
    else:
        resolved = here.resolve()
        if resolved.is_relative_to(projects.resolve()):
            if not lexical.is_relative_to(projects):
                raise BrainError('A symlink alias into a workspace is not a valid working directory. Use its actual project path.')
            rel = resolved.relative_to(projects.resolve())
            if rel.parts:
                inferred = checked_slug(rel.parts[0])
    if project:
        checked_slug(project)
    if project and inferred and project != inferred:
        raise BrainError(f'Project conflict: request names {project!r}, working directory names {inferred!r}. Ask which workspace to use; return to the toolkit root after confirming.')
    selected = project or inferred
    if not selected:
        raise BrainError('No workspace selected. Ask the user for a workspace, then use --project <slug>, or work inside Projects/<slug>. For an explicitly whole-brain request, use resolve-brain and list-projects. No workspace content was read.')
    entry=next((item for item in registry['workspaces'] if item['slug']==selected),None)
    if entry is None:raise BrainError(f'Workspace {selected!r} does not exist in the registry. Create it with new-project, or explicitly register a restored workspace after reviewing its metadata.')
    return registered_project_path(brain_path,entry)

def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise BrainError(f'Cannot read {path.name}: {exc}') from exc

def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.brain-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp): os.unlink(temp)

def walk_files(folder: Path):
    if folder.is_symlink(): raise BrainError(f'Symlink is not allowed: {folder.name}')
    if not folder.is_dir(): raise BrainError(f'Missing directory: {folder.name}')
    found=[]
    for parent, dirs, names in os.walk(folder, followlinks=False):
        for name in dirs+names:
            p=Path(parent)/name
            if p.is_symlink(): raise BrainError(f'Symlink is not allowed: {p.relative_to(folder)}')
        for name in names:
            p=Path(parent)/name
            if not p.is_file(): raise BrainError(f'Non-regular file: {p.name}')
            if name not in IGNORED_FILE_NAMES and '__pycache__' not in p.parts and p.suffix != '.pyc': found.append(p)
    return sorted(found)

def canonical_files(root: Path, visuals: bool=False) -> dict[str, bytes]:
    result={}
    for kind in (['skills','optional-skills'] if visuals else ['skills']):
        source=safe_under(root,kind)
        for p in walk_files(source):
            rel=p.relative_to(source)
            if len(rel.parts)<2 or not SKILL.fullmatch(rel.parts[0]):
                raise BrainError(f'Invalid skill bundle path: {kind}/{rel}')
            for host in HOSTS:
                result[f'{host}/{rel.as_posix()}']=p.read_bytes()
    return result

def owned_path(value: str) -> bool:
    p=Path(value)
    return (not p.is_absolute() and '..' not in p.parts and '\\' not in value
            and len(p.parts)>=4 and '/'.join(p.parts[:2]) in HOSTS
            and bool(SKILL.fullmatch(p.parts[2])))

def load_state(root: Path):
    path=safe_under(root,STATE)
    if not path.exists(): return {'schema_version':1,'toolkit':'brain','files':{}}
    state=read_json(path)
    if not isinstance(state,dict) or state.get('schema_version')!=1 or state.get('toolkit')!='brain' or not isinstance(state.get('files'),dict):
        raise BrainError('Unrecognized installation manifest. Preserve it and run doctor; nothing was overwritten.')
    for rel,sha in state['files'].items():
        if not owned_path(rel) or not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{64}',sha):
            raise BrainError('Unsafe installation manifest; no files were changed.')
    return state

def prune_empty_owned_skill_dirs(root: Path, removed_paths):
    """Remove empty directories belonging to removed manifest files, never contents."""
    for relative in sorted(removed_paths, key=lambda value:len(Path(value).parts), reverse=True):
        if not owned_path(relative):
            raise BrainError('Unsafe removed skill path; no directory cleanup attempted.')
        path=safe_under(root,relative).parent
        skill_root=root.joinpath(*Path(relative).parts[:3])
        while path.is_relative_to(skill_root):
            try:path.rmdir()
            except FileNotFoundError:pass
            except OSError:break  # Custom/unmanaged content keeps its directory.
            path=path.parent


def setup(root: Path, visuals: bool=False):
    root=require_root(root)
    state=load_state(root)
    # The legacy 'visuals' API keyword/manifest field means all optional skills.
    # Retain it for existing installations and keep optional skills on upgrades.
    visuals=visuals or bool(state.get('visuals'))
    desired=canonical_files(root,visuals)
    prior=state['files']
    for rel in sorted(set(prior)|set(desired)):
        p=safe_under(root,rel)
        if p.exists():
            if not p.is_file(): raise BrainError(f'Expected file at {rel}; no changes made.')
            if rel not in prior: raise BrainError(f'Unmanaged file at {rel}; preserve or move it before setup. No changes made.')
            if digest(p.read_bytes()) != prior[rel]:
                raise BrainError(f'Locally modified generated file: {rel}. Copy your edits to canonical skills first; no changes made.')
    safe_under(root,STATE)
    for rel,data in desired.items():
        p=safe_under(root,rel)
        if not p.exists() or p.read_bytes()!=data: atomic_write(p,data)
    removed=set(prior)-set(desired)
    for rel in removed:
        p=safe_under(root,rel)
        if p.exists(): p.unlink()
    prune_empty_owned_skill_dirs(root,removed)
    manifest={'schema_version':1,'toolkit':'brain','version':VERSION,'visuals':visuals,'files':{rel:digest(data) for rel,data in sorted(desired.items())}}
    atomic_write(safe_under(root,STATE),(json.dumps(manifest,indent=2)+'\n').encode())
    names={Path(rel).parts[2] for rel in desired}
    return {'status':'ready','skills':len(names),'hosts':['Codex','Claude Code'],'global_changes':False}

def uninstall(root: Path):
    root=require_root(root); state=load_state(root)
    for rel,sha in state['files'].items():
        p=safe_under(root,rel)
        if p.exists() and (not p.is_file() or digest(p.read_bytes())!=sha):
            raise BrainError(f'Locally modified generated file: {rel}. Preserve it before uninstall. No files removed.')
    for rel in state['files']:
        p=safe_under(root,rel)
        if p.exists():p.unlink()
    # Only remove empty generated directories, never recursively delete.
    for rel in sorted(state['files'],key=lambda s:len(Path(s).parts),reverse=True):
        p=(root/rel).parent
        while p!=root and p.name not in ('.agents','.claude'):
            try:p.rmdir()
            except OSError:break
            p=p.parent
    p=safe_under(root,STATE)
    if p.exists():p.unlink()
    return {'status':'uninstalled','projects_preserved':True,'canonical_skills_preserved':True}

def one_line_text(value: str, field: str, limit: int) -> str:
    if not isinstance(value,str) or not value.strip() or len(value)>limit or any(ord(c)<32 or c in '\u007f\u0085\u2028\u2029' for c in value):
        raise BrainError(f'{field} must be nonempty single-line text, at most {limit} characters.')
    return value.strip()

def render_workspace_index(text: str, registry: dict) -> str:
    if text.count(INDEX_START)!=1 or text.count(INDEX_END)!=1 or text.index(INDEX_END)<text.index(INDEX_START):
        raise BrainError('INDEX.md must contain one ordered BEGIN WORKSPACES / END WORKSPACES marker pair. Preserve your notes and restore these markers from templates/root/INDEX.md.')
    lines=[]
    for entry in registry['workspaces']:
        name=html.escape(entry['name']).replace('\\','\\\\').replace('[','\\[').replace(']','\\]')
        lines.append(f'- [{name}](Projects/{entry["slug"]}/PROJECT.md) — {entry["type"]}; {entry["status"]}.')
    content='\n'.join(lines) if lines else 'No workspaces registered yet.'
    start=text.index(INDEX_START)+len(INDEX_START)
    end=text.index(INDEX_END)
    return text[:start]+'\n\n'+content+'\n\n'+text[end:]

def plan_brain_init(root: Path):
    """Read and validate the whole scaffold before creating any missing files."""
    root=require_root(root)
    brain_path=brain_location(root)
    source_root=safe_under(root,'templates/root')
    desired={p.relative_to(source_root).as_posix():p.read_bytes() for p in walk_files(source_root)}
    if not set(BRAIN_FILES).issubset(desired):raise BrainError('The public templates/root scaffold is incomplete. Restore it before initializing the private brain.')
    missing={}
    for relative,data in desired.items():
        destination=safe_brain_path(brain_path,relative)
        for parent in destination.parents:
            if parent==brain_path.parent:break
            if parent.exists() and not parent.is_dir():raise BrainError(f'Expected a directory at {parent.relative_to(root)}; no files were changed.')
        if destination.exists():
            if not destination.is_file():raise BrainError(f'Expected file at {relative}; no files were changed.')
        else:missing[relative]=data
    for relative in BRAIN_DIRS:
        directory=safe_under(brain_path,relative)
        if directory.exists() and not directory.is_dir():raise BrainError(f'Expected directory at {relative}; no files were changed.')
    projects=safe_under(brain_path,'Projects')
    if 'registry.json' in missing and projects.is_dir() and any(child.name not in IGNORED_FILE_NAMES and child.name!='.gitkeep' for child in projects.iterdir()):
        raise BrainError('registry.json is missing while existing workspace material remains. Restore it from backup or explicitly reconstruct it using docs/MIGRATION.md; an empty registry was not created.')
    def current_bytes(relative):
        return missing[relative] if relative in missing else safe_under(brain_path,relative).read_bytes()
    try:
        registry=validate_registry(json.loads(current_bytes('registry.json')),brain_path)
        integrations=json.loads(current_bytes('integrations.json'))
        index=current_bytes('INDEX.md').decode('utf-8')
    except (ValueError,UnicodeError) as exc:raise BrainError('Brain metadata must be valid UTF-8/JSON; preserve the existing files and repair them before initializing.') from exc
    if not isinstance(integrations,dict) or type(integrations.get('schema_version')) is not int or integrations['schema_version']!=1 or any(not isinstance(integrations.get(field),list) for field in ('connections','sources','routes')):
        raise BrainError('integrations.json must use schema_version 1 with connections, sources, and routes lists; nothing was changed.')
    require_registered_folders(brain_path,registry)
    render_workspace_index(index,registry)  # Validate markers without overwriting user edits.
    return brain_path,missing,registry,index

def apply_brain_init(brain_path: Path, missing: dict):
    brain_path.mkdir(parents=True,exist_ok=True)
    for relative in BRAIN_DIRS:safe_under(brain_path,relative).mkdir(parents=True,exist_ok=True)
    for relative,data in missing.items():
        destination=safe_brain_path(brain_path,relative)
        destination.parent.mkdir(parents=True,exist_ok=True)
        try:
            with destination.open('xb') as stream:stream.write(data)
        except FileExistsError as exc:raise BrainError(f'{relative} appeared during initialization; it was not overwritten. Rerun init-brain to validate the current state.') from exc

@contextmanager
def brain_metadata_lock(root: Path):
    root=require_root(root)
    brain_location(root)  # Reject legacy layouts before creating even a lock.
    path=safe_under(root,'.local/brain-metadata.lock')
    created_parent=not path.parent.exists()
    path.parent.mkdir(parents=True,exist_ok=True)
    acquired=False
    try:
        try:fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except FileExistsError as exc:
            raise BrainError('Brain metadata is being updated. Retry after that operation; inspect an abandoned .local/brain-metadata.lock before removing it.') from exc
        acquired=True
        os.close(fd)
        yield
    finally:
        if acquired:path.unlink()
        if created_parent:
            try:path.parent.rmdir()
            except OSError:pass

def init_brain(root: Path):
    with brain_metadata_lock(root):
        brain_path,missing,_,_=plan_brain_init(root)
        apply_brain_init(brain_path,missing)
        return {'status':'initialized' if missing else 'ready','path':str(brain_path),'created_files':sorted(missing)}

def new_project(root: Path, slug: str, name: str | None=None, *, workspace_type: str='general', purpose: str | None=None):
    with brain_metadata_lock(root):
        return create_project_locked(root,slug,name,workspace_type=workspace_type,purpose=purpose)

def create_project_locked(root: Path, slug: str, name: str | None=None, *, workspace_type: str='general', purpose: str | None=None):
    root=require_root(root); checked_slug(slug)
    if workspace_type not in WORKSPACE_TYPES:
        raise BrainError('Workspace type must be one of: '+', '.join(WORKSPACE_TYPES)+'.')
    title=one_line_text(name if name is not None else slug.replace('-',' ').title(),'Workspace display name',120)
    workspace_purpose=one_line_text(purpose if purpose is not None else 'Unknown — not supplied.','Workspace purpose',500)
    brain_path,missing,registry,index=plan_brain_init(root)
    target=safe_under(brain_path,f'Projects/{slug}')
    if target.exists() or any(item['slug']==slug for item in registry['workspaces']):
        raise BrainError(f'Workspace {slug!r} already exists or is registered; nothing was overwritten.')
    files=walk_files(safe_under(root,'templates/project'))
    values={'PROJECT_SLUG':slug,'PROJECT_NAME':title,'WORKSPACE_TYPE':workspace_type,'WORKSPACE_PURPOSE':workspace_purpose}
    prepared=[]
    for source in files:
        relative=source.relative_to(root/'templates/project').as_posix()
        text=re.sub(r'\{\{(PROJECT_SLUG|PROJECT_NAME|WORKSPACE_TYPE|WORKSPACE_PURPOSE)\}\}',lambda match:values[match.group(1)],source.read_text())
        prepared.append((relative,text.encode()))
    if not any(relative=='PROJECT.md' for relative,_ in prepared):raise BrainError('Missing templates/project/PROJECT.md; nothing was created.')
    entry={'slug':slug,'name':title,'type':workspace_type,'status':'active','planning':True,'review':True,'application':None}
    updated={**registry,'workspaces':registry['workspaces']+[entry]}
    updated_index=render_workspace_index(index,updated)
    apply_brain_init(brain_path,missing)
    target.mkdir(parents=True,exist_ok=False)
    for relative,data in prepared:
        atomic_write(safe_project_path(target,relative),data)
    atomic_write(safe_under(brain_path,'registry.json'),(json.dumps(updated,indent=2,ensure_ascii=False)+'\n').encode())
    atomic_write(safe_under(brain_path,'INDEX.md'),updated_index.encode())
    return {'status':'created','project':slug,'path':str(target),'workspace_type':workspace_type}

def catalog(root: Path):
    data=read_json(safe_under(root,'capabilities.json'))
    if not isinstance(data,list):raise BrainError('Capability catalog must be a list.')
    return data

def verify(root: Path, installed: bool=False):
    root=require_root(root); errors=[]
    # Validate installable bundles even before setup has created an installation manifest.
    canonical_files(root,visuals=True)
    names={}
    for kind in ('skills','optional-skills'):
        for p in walk_files(safe_under(root,kind)):
            if p.name!='SKILL.md':continue
            content=p.read_text()
            if not content.startswith('---\n') or '\n---\n' not in content[4:]: errors.append(f'Missing frontmatter: {p.relative_to(root)}');continue
            front=content.split('---',2)[1]
            match=re.search(r'^name:\s*[\"\']?([a-z0-9-]+)',front,re.M)
            if not match or match.group(1)!=p.parent.name or not SKILL.fullmatch(p.parent.name):errors.append(f'Invalid name: {p.relative_to(root)}')
            if not re.search(r'^description:\s*\S',front,re.M):errors.append(f'Missing description: {p.relative_to(root)}')
            if p.parent.name in names:errors.append(f'Duplicate skill: {p.parent.name}')
            names[p.parent.name]=kind
    entries=catalog(root)
    for item in entries:
        if item.get('skill') not in names:errors.append(f'Unimplemented capability: {item.get("capability")}')
    covered={item.get('skill') for item in entries}
    for name in names:
        if name not in covered: errors.append(f'Unlisted skill: {name}')
    statepath=safe_under(root,STATE)
    if installed or statepath.exists():
        if not statepath.exists():errors.append('Project-local skills are not installed. Run setup.')
        else:
            state=load_state(root);desired=canonical_files(root,bool(state.get('visuals')))
            if set(state['files']) != set(desired):errors.append('Generated file set differs from canonical skills. Run setup.')
            for rel,data in desired.items():
                p=safe_under(root,rel)
                if not p.is_file() or p.read_bytes()!=data:errors.append(f'Generated skill differs or missing: {rel}')
                elif state['files'].get(rel)!=digest(data):errors.append(f'Manifest hash mismatch: {rel}')
    if errors:raise BrainError('\n'.join(errors))
    return {'status':'verified','canonical_skills':len(names),'source_capabilities':len(entries),'installed':statepath.exists()}

def doctor(root: Path):
    root=require_root(root)
    report={'python':sys.version.split()[0],'platform':sys.platform,'root':str(root),'project_local_setup':safe_under(root,STATE).exists(),
            'optional_dependencies':{k:bool(importlib.util.find_spec(k)) for k in ('openpyxl','pptx')},
            'global_configuration':"not changed; existing global skills may share names; use this toolkit's canonical skill paths when ambiguous",
            'platform_status':'validated target' if sys.platform=='darwin' else 'not yet independently validated'}
    try:report['verification']=verify(root)
    except BrainError as exc:report['verification_error']=str(exc)
    try:report['release_check']={'status':'ready','public_files':len(release_files(root))}
    except (BrainError,OSError) as exc:report['release_check']={'status':'blocked','error':str(exc)}
    return report

def release_files(root: Path):
    manifest=read_json(safe_under(root,'release-files.json'))
    if not isinstance(manifest,list) or any(not isinstance(relative,str) for relative in manifest):raise BrainError('Release allowlist must contain a list of file path strings.')
    if len(manifest)!=len(set(manifest)):raise BrainError('Release allowlist must contain unique file paths.')
    result=[]
    allowed_roots={'README.md','LICENSE','NOTICE.md','.gitignore','.brain','AGENTS.md','CLAUDE.md','capabilities.json','release-files.json','skills','optional-skills','templates','examples','scripts','tests','docs','requirements-artifacts.txt','VERSION'}
    banned={'.git','.local','.agents','.claude','__pycache__','.env','.venv','dist','node_modules'} | IGNORED_FILE_NAMES
    for rel in manifest:
        if not isinstance(rel,str):raise BrainError('Release paths must be strings.')
        parts=Path(rel).parts
        if not parts or parts[0] in (PRIVATE_DIRECTORIES | PRIVATE_FILES | {'brain'}) or parts[0] not in allowed_roots or any(x in banned or x.startswith('.env.') for x in parts):
            raise BrainError(f'Private or unknown release path rejected: {rel}')
        p=safe_under(root,rel)
        if not p.is_file():raise BrainError(f'Missing release file: {rel}')
        if p.suffix in {'.pyc','.pem','.key','.p12','.sqlite','.db'}:raise BrainError(f'Private/runtime file rejected: {rel}')
        raw=p.read_bytes()
        # Defense-in-depth only: an allowlist + human provenance review is primary.
        text=raw.decode('utf-8',errors='replace')
        secret_patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{24,}',r'(?i)(?:api[_-]?key|access[_-]?token|password)\b[\"\']?\s*[:=]\s*[\"\'][^\"\'\r\n]{16,}[\"\']']
        if any(re.search(pattern,text) for pattern in secret_patterns):raise BrainError(f'Potential secret in public file: {rel}; inspect before release.')
        result.append((rel,raw))
    required={'README.md','LICENSE','docs/OPERATING_GUIDE.md','AGENTS.md','CLAUDE.md','.brain','capabilities.json','release-files.json','scripts/brain.py','docs/GETTING_STARTED.md'}
    for folder in ('skills', 'optional-skills', 'templates', 'scripts'):
        required.update(p.relative_to(root).as_posix() for p in walk_files(safe_under(root,folder)))
    if not required.issubset(manifest):raise BrainError('Release allowlist omits required entrypoints or workflow resources. Review new files before adding them.')
    return sorted(result)

def build_release(root: Path, output: Path | None=None):
    root=require_root(root);verify(root)
    files=release_files(root)
    destination=Path(output) if output else safe_under(root,f'dist/Brain-{VERSION}.zip')
    if not destination.is_absolute():destination=Path.cwd()/destination
    destination=Path(os.path.abspath(destination))
    if not destination.is_relative_to(root):raise BrainError('Release archives must be written within this toolkit dist/ directory.')
    if not destination.is_relative_to(root/'dist'):raise BrainError('Release archives must be written inside dist/.')
    destination=safe_under(root,destination.relative_to(root).as_posix())
    if destination.exists():raise BrainError('Release archive already exists. Choose a new filename; nothing overwritten.')
    destination.parent.mkdir(parents=True,exist_ok=True)
    created = False
    try:
        with destination.open('xb') as stream:
            created = True
            with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as archive:
                for rel,raw in files:
                    info=zipfile.ZipInfo('Brain/'+rel,date_time=(2026,1,1,0,0,0))
                    info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                    archive.writestr(info,raw)
    except Exception:
        if created and destination.exists():destination.unlink()
        raise
    return {'status':'built','archive':str(destination),'files':len(files),'sha256':digest(destination.read_bytes())}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    s=sub.add_parser('setup')
    s.add_argument('--with-optional','--with-visuals',dest='with_optional',action='store_true',
                   help='Install all optional skills; --with-visuals remains a compatibility alias.')
    sub.add_parser('init-brain')
    sub.add_parser('resolve-brain')
    listing=sub.add_parser('list-projects');listing.add_argument('--scope',choices=PROJECT_SCOPES,default='active')
    listing.add_argument('--require-nonempty',action='store_true',
                         help='Fail if no workspaces match the scope; useful before recurring runs.')
    n=sub.add_parser('new-project');n.add_argument('slug');n.add_argument('--name')
    n.add_argument('--type',dest='workspace_type',choices=WORKSPACE_TYPES,default='general',help='Workspace type; defaults to general.')
    n.add_argument('--purpose',help='Optional single-line workspace purpose, at most 500 characters.')
    r=sub.add_parser('resolve');r.add_argument('--project');r.add_argument('--cwd',type=Path)
    sub.add_parser('doctor')
    v=sub.add_parser('verify');v.add_argument('--installed',action='store_true')
    b=sub.add_parser('build-release');b.add_argument('--output',type=Path)
    sub.add_parser('uninstall')
    args=parser.parse_args(argv)
    try:
        if sys.version_info<(3,11):raise BrainError('Python 3.11 or newer is required.')
        if args.command=='setup':result=setup(TOOLKIT_ROOT,args.with_optional)
        elif args.command=='init-brain':result=init_brain(TOOLKIT_ROOT)
        elif args.command=='resolve-brain':print(resolve_brain(TOOLKIT_ROOT));return 0
        elif args.command=='list-projects':
            result=list_projects(TOOLKIT_ROOT,args.scope)
            if args.require_nonempty and not result:
                raise BrainError(f'No workspaces match scope {args.scope!r}; no workspace review or planning was performed. '
                                 'Inspect list-projects --scope all and registry.json for an empty registry, lifecycle states, '
                                 'or disabled flags. Preserve intentional exclusions; change only user-authorized scope.')
        elif args.command=='new-project':result=new_project(TOOLKIT_ROOT,args.slug,args.name,workspace_type=args.workspace_type,purpose=args.purpose)
        elif args.command=='resolve':
            print(resolve_project(TOOLKIT_ROOT,args.project,args.cwd));return 0
        elif args.command=='doctor':result=doctor(TOOLKIT_ROOT)
        elif args.command=='verify':result=verify(TOOLKIT_ROOT,args.installed)
        elif args.command=='build-release':result=build_release(TOOLKIT_ROOT,args.output)
        elif args.command=='uninstall':result=uninstall(TOOLKIT_ROOT)
        print(json.dumps(result,indent=2));return 0
    except (BrainError,OSError) as exc:
        print(f'Brain: {exc}',file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
