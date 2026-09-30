#!/usr/bin/env python3
"""Capture an explicitly supplied local source once; track workspace interpretations.

Python 3.11+, stdlib only. This helper does not fetch, classify, summarize, or schedule.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import struct
import unicodedata

import brain

TOOLKIT_ROOT = Path(__file__).resolve().parents[1]


def identity(source_id: str) -> tuple[str, str]:
    value = brain.one_line_text(source_id, 'Stable source ID', 500)
    return value, brain.digest(value.encode('utf-8'))


def checked_digest(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch('[a-f0-9]{64}', value):
        raise brain.BrainError('A full lowercase SHA-256 content digest is required.')
    return value


@contextmanager
def source_lock(root: Path, key: str):
    path = brain.safe_brain_path(root, f'maintenance/intake/{key}.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise brain.BrainError('This source is being processed. Retry after its run; inspect an abandoned lock before removing it.') from exc
    try:
        os.close(fd)
        yield
    finally:
        path.unlink()


def receipt_path(root: Path, key: str, digest: str) -> Path:
    return brain.safe_brain_path(root, f'maintenance/intake/{key}/{checked_digest(digest)}.json')


STORAGE_FILE = 'maintenance/intake/storage.json'
RESERVED_NAMES = re.compile(r'^(?:con|prn|aux|nul|conin\$|conout\$|com[1-9¹²³]|lpt[1-9¹²³])(?:\.|$)', re.I)


def portable_key(value: str) -> str:
    """Compare names as on case-insensitive, Unicode-normalizing filesystems."""
    return unicodedata.normalize('NFC', value).casefold()


def trim_bytes(value: str, limit: int) -> str:
    return value.encode('utf-8')[:limit].decode('utf-8', errors='ignore')


def safe_original_name(value: str) -> str:
    """Keep the supplied filename unless portability requires a visible substitution."""
    value = unicodedata.normalize('NFC', value)
    value = ''.join('_' if char in '<>:"/\\|?*' or unicodedata.category(char).startswith('C')
                    else char for char in value).rstrip(' .')
    if not value:
        value = 'source'
    if RESERVED_NAMES.match(value) or value in ('.DS_Store',):
        value = '_' + value
    # Leave ample room for filesystem byte limits; keep an ordinary extension.
    suffix = Path(value).suffix
    if len(suffix.encode('utf-8')) > 32:
        suffix = ''
    stem = value[:-len(suffix)] if suffix else value
    return trim_bytes(stem, 180 - len(suffix.encode('utf-8'))).rstrip(' .') + suffix


def title_slug(title: str) -> str:
    title = unicodedata.normalize('NFC', title).casefold()
    slug = re.sub(r'[^\w]+', '-', title, flags=re.UNICODE).replace('_', '-')
    slug = re.sub('-+', '-', slug).strip('-')
    return trim_bytes(slug, 96).rstrip('-') or 'source'


def capture_date(captured_at: str) -> str:
    try:
        instant = datetime.fromisoformat(captured_at.replace('Z', '+00:00'))
        if instant.tzinfo is None:
            raise ValueError('Missing timezone')
        return instant.astimezone(timezone.utc).date().isoformat()
    except (AttributeError, TypeError, ValueError) as exc:
        raise brain.BrainError('Capture time must be an ISO timestamp with a timezone; it is not an authorship date.') from exc


def is_finder_metadata(path: Path) -> bool:
    """Ignore recognizable Finder metadata, never arbitrary dot/underscore files."""
    if path.is_symlink() or not path.is_file():
        return False
    if path.name == '.DS_Store':
        with path.open('rb') as stream:
            return stream.read(8) == b'\x00\x00\x00\x01Bud1' and path.stat().st_size >= 32
    if not path.name.startswith('._'):
        return False
    size = path.stat().st_size
    with path.open('rb') as stream:
        header = stream.read(26)
        if len(header) < 26:
            return False
        magic, version = struct.unpack('>II', header[:8])
        count = struct.unpack('>H', header[24:26])[0]
        if magic != 0x00051607 or version != 0x00020000 or not 1 <= count <= 64:
            return False
        content = header + stream.read(count * 12)
    end = 26 + count * 12
    if len(content) < end:
        return False
    seen, ranges = set(), []
    for index in range(count):
        entry, offset, length = struct.unpack('>III', content[26 + index * 12:38 + index * 12])
        if entry not in range(2, 16) or entry in seen or offset < end or offset + length > size:
            return False
        if length and any(offset < upper and lower < offset + length for lower, upper in ranges):
            return False
        seen.add(entry)
        ranges.append((offset, offset + length))
    return True


def raw_entries(root: Path, directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise brain.BrainError('A raw source directory is occupied by a file; preserve it for review.')
    entries = []
    for child in directory.iterdir():
        candidate = brain.safe_brain_path(root, child.relative_to(brain.resolve_brain(root)).as_posix())
        if not is_finder_metadata(candidate):
            entries.append(candidate)
    return entries


def validate_v1_storage(root: Path, data: dict) -> dict:
    """Private, full-identity allocations authenticate readable paths and retries."""
    if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('sources'), dict):
        raise brain.BrainError('Invalid source storage allocations; preserve them for review.')
    directories = set()
    for key, item in data['sources'].items():
        if (not isinstance(item, dict) or not isinstance(item.get('source_id'), str)
                or identity(item['source_id'])[1] != key or not isinstance(item.get('directory'), str)
                or not isinstance(item.get('versions'), dict)):
            raise brain.BrainError('Invalid full source identity in storage allocations.')
        directory = brain.safe_brain_path(root, item['directory'])
        parts = Path(item['directory']).parts
        suffix = parts[-1].rsplit('--', 1)[-1]
        if (len(parts) != 2 or parts[0] != 'raw' or portable_key(item['directory']) in directories
                or len(suffix) not in range(8, 65, 4) or not key.startswith(suffix)):
            raise brain.BrainError('Invalid or colliding source directory allocation.')
        directories.add(portable_key(item['directory']))
        versions = set()
        for digest, version in item['versions'].items():
            checked_digest(digest)
            if (not isinstance(version, dict) or not isinstance(version.get('raw_path'), str)
                    or not isinstance(version.get('original_name'), str)):
                raise brain.BrainError('Invalid content version allocation.')
            date = capture_date(version.get('captured_at'))
            brain.one_line_text(version.get('title'), 'Stored source title', 500)
            raw = brain.safe_brain_path(root, version['raw_path'])
            suffix = raw.parent.name.removeprefix(date + '--')
            if (raw.parent.parent != directory or len(Path(version['raw_path']).parts) != 4
                    or portable_key(raw.parent.name) in versions
                    or not raw.parent.name.startswith(date + '--')
                    or len(suffix) not in range(8, 65, 4) or not digest.startswith(suffix)
                    or raw.name != safe_original_name(version['original_name'])):
                raise brain.BrainError('Invalid or colliding content version allocation.')
            versions.add(portable_key(raw.parent.name))
    return data


def checked_raw_path(root: Path, relative: str) -> Path:
    parts = relative.split('/')
    if (len(parts) < 3 or parts[0] != 'raw'
            or any(not part or part in ('.', '..') or safe_original_name(part) != part for part in parts)):
        raise brain.BrainError('Allocated source paths must use portable canonical filenames below raw/<folder>/.')
    return brain.safe_brain_path(root, relative)


def read_storage(root: Path) -> dict:
    path=brain.safe_brain_path(root,STORAGE_FILE)
    data=brain.read_json(path) if path.exists() else {'schema_version':2,'sources':{}}
    if (not isinstance(data,dict) or type(data.get('schema_version')) is not int
            or data['schema_version'] not in (1,2) or not isinstance(data.get('sources'),dict)):
        raise brain.BrainError('Invalid source storage allocations; preserve them for review.')
    if data['schema_version']==1:
        return validate_v1_storage(root,data)
    for key,item in data['sources'].items():
        if (not isinstance(item,dict) or not isinstance(item.get('source_id'),str)
                or identity(item['source_id'])[1]!=key or not isinstance(item.get('versions'),dict)):
            raise brain.BrainError('Invalid full source identity in storage allocations.')
        for digest,version in item['versions'].items():
            checked_digest(digest)
            if (not isinstance(version,dict) or not isinstance(version.get('raw_path'),str)
                    or not isinstance(version.get('original_name'),str) or not version['original_name']):
                raise brain.BrainError('Invalid content version allocation.')
            capture_date(version.get('captured_at'))
            brain.one_line_text(version.get('title'),'Stored source title',500)
            previous=version.get('previous_raw_paths',[])
            if not isinstance(previous,list) or any(not isinstance(value,str) for value in previous):
                raise brain.BrainError('Invalid prior source path allocations.')
            for relative in [version['raw_path'],*previous]:
                checked_raw_path(root,relative)
    path_reservations(data)
    return data


def storage_paths(storage: dict):
    for key,item in storage['sources'].items():
        for digest,version in item['versions'].items():
            for relative in [version['raw_path'],*version.get('previous_raw_paths',[])]:
                yield relative,(key,digest)


def path_reservations(storage: dict) -> tuple[dict, dict]:
    """Reserve file paths and directory spelling before a capture writes bytes."""
    files, directories = {}, {}
    for relative, owner in storage_paths(storage):
        normalized = portable_key(relative)
        if normalized in files and files[normalized] != (relative, owner):
            raise brain.BrainError('Colliding source file allocations; preserve them for review.')
        files[normalized] = (relative, owner)
        parts = relative.split('/')
        for length in range(1, len(parts)):
            directory = '/'.join(parts[:length])
            normalized_directory = portable_key(directory)
            if normalized_directory in directories and directories[normalized_directory] != directory:
                raise brain.BrainError('Allocated folders differ only by case or Unicode normalization; preserve them for review.')
            directories[normalized_directory] = directory
    if files.keys() & directories.keys():
        raise brain.BrainError('An allocated source file is also reserved as a folder; preserve it for review.')
    return files, directories


def checked_folder(root: Path, folder: str) -> str:
    if not isinstance(folder,str) or not folder or folder.startswith('/') or '\\' in folder:
        raise brain.BrainError('Source folder must be a portable relative path below raw/.')
    parts=folder.split('/')
    if any(not part or part in ('.','..') or part.startswith('.') or safe_original_name(part)!=part for part in parts):
        raise brain.BrainError('Source folder must use portable directory names without traversal.')
    parent=brain.safe_brain_path(root,'raw')
    for part in parts:
        if parent.exists():
            if not parent.is_dir():raise brain.BrainError('Source folder is occupied by a file.')
            if any(portable_key(child.name)==portable_key(part) and child.name!=part for child in parent.iterdir()):
                raise brain.BrainError('Source folder differs only by case or Unicode normalization from an existing name; use its exact spelling.')
        parent=brain.safe_brain_path(root,(parent/part).relative_to(brain.resolve_brain(root)).as_posix())
        if parent.exists() and not parent.is_dir():raise brain.BrainError('Source folder is occupied by a file.')
    return '/'.join(parts)


def checked_filename(filename: str) -> str:
    if not isinstance(filename,str) or not filename or '/' in filename or '\\' in filename or filename in ('.','..'):
        raise brain.BrainError('Supply a filename, not a path; use folder for categories.')
    return safe_original_name(filename)


def default_folder(data: dict) -> str:
    targets=list(data.get('targets',{}))
    return targets[0] if len(targets)==1 else ('shared' if targets else 'unassigned')


def allocation_plan(root: Path, data: dict, storage: dict, title: str | None = None,
                    folder: str | None = None, filename: str | None = None, *, relocate: bool=False) -> dict:
    source_id,key=identity(data['source_id'])
    digest=checked_digest(data['sha256'])
    existing=storage['sources'].get(key,{})
    version=existing.get('versions',{}).get(digest)
    if version and not relocate:
        return {'source_id':source_id,'sha256':digest,'directory':str(Path(version['raw_path']).parent),
                **version,'previous_raw_path':data.get('raw_path')}
    original=data.get('original_name')
    if not isinstance(original,str) or not original:
        raise brain.BrainError('The exact original filename is required before allocating readable storage.')
    captured_at=data['captured_at'];date=capture_date(captured_at)
    chosen_title=title if title is not None else (data.get('description') or {}).get('title')
    if chosen_title is None:
        chosen_title=' '.join(''.join(' ' if unicodedata.category(char).startswith('C') else char for char in Path(original).stem).split()) or 'Source'
    chosen_title=brain.one_line_text(chosen_title,'Source title',500)
    folder=checked_folder(root,folder if folder is not None else default_folder(data))
    name=checked_filename(filename if filename is not None else original)
    directory='raw/'+folder
    parent=brain.safe_brain_path(root,directory)
    reserved, reserved_folders = path_reservations(storage)
    for length in range(1, len(directory.split('/')) + 1):
        prefix = '/'.join(directory.split('/')[:length])
        normalized_prefix = portable_key(prefix)
        if normalized_prefix in reserved:
            raise brain.BrainError('Source folder is reserved as a source file; choose another folder.')
        if normalized_prefix in reserved_folders and reserved_folders[normalized_prefix] != prefix:
            raise brain.BrainError('Source folder differs only by case or Unicode normalization from a reserved folder; use its exact spelling.')
    occupied={portable_key(child.name) for child in parent.iterdir()} if parent.exists() else set()
    def available(candidate):
        relative=directory+'/'+candidate
        if portable_key(relative) in reserved_folders:
            return False
        reservation=reserved.get(portable_key(relative))
        owner=reservation[1] if reservation else None
        if owner==(key,digest) and relocate:
            # Only the exact previously authenticated spelling can be reused.
            return relative in [version['raw_path'],*version.get('previous_raw_paths',[])] if version else False
        return owner is None and portable_key(candidate) not in occupied
    selected=name
    if not available(selected):
        suffix=Path(name).suffix;stem=name[:-len(suffix)] if suffix else name
        other_versions=any(value!=digest for value in existing.get('versions',{}))
        token=digest if other_versions else key
        for length in range(8,65,4):
            addition=('--'+date if other_versions else '')+'--'+token[:length]
            selected=trim_bytes(stem,180-len((addition+suffix).encode())).rstrip(' .')+addition+suffix
            if available(selected):break
        else:raise brain.BrainError('Even the full identifier path is occupied; preserve it and resolve the collision explicitly.')
    return {'source_id':source_id,'sha256':digest,'directory':directory,'raw_path':directory+'/'+selected,
            'original_name':original,'captured_at':captured_at,'title':chosen_title,
            'previous_raw_path':data.get('raw_path'),'requested_folder':folder,'requested_filename':name}


def save_allocation(root: Path, plan: dict, storage: dict):
    _,key=identity(plan['source_id'])
    storage['schema_version']=2
    item=storage['sources'].setdefault(key,{'source_id':plan['source_id'],'versions':{}})
    previous=item['versions'].get(plan['sha256'],{})
    history=list(previous.get('previous_raw_paths',[]))
    for relative in (previous.get('raw_path'),plan.get('previous_raw_path')):
        if relative and relative!=plan['raw_path'] and relative not in history:history.append(relative)
    version={**previous,**{field:plan[field] for field in ('raw_path','original_name','captured_at','title')}}
    version['previous_raw_paths']=[relative for relative in history if relative!=plan['raw_path']]
    item['versions'][plan['sha256']]=version
    path_reservations(storage)
    # The old per-source directory remains descriptive legacy metadata only.
    brain.atomic_write(brain.safe_brain_path(root,STORAGE_FILE),(json.dumps(storage,indent=2,ensure_ascii=False)+'\n').encode())


def plan_relocation(root: Path, data: dict, title: str | None = None,
                    folder: str | None = None, filename: str | None = None) -> dict:
    """Read-only relocation proposal; source identity and bytes remain unchanged."""
    source_id,key=identity(data['source_id']);digest=checked_digest(data['sha256'])
    current=read_receipt(root,receipt_path(root,key,digest),source_id,key,digest)
    if current['raw_path']!=data['raw_path']:
        raise brain.BrainError('The receipt changed since it was read; refresh the relocation plan.')
    return allocation_plan(root,current,read_storage(root),title,folder,filename,relocate=True)


def register_relocation(root: Path, plan: dict):
    """Caller holds source_lock. Reserve a reviewed plan; never move bytes/receipts."""
    source_id,key=identity(plan['source_id']);digest=checked_digest(plan['sha256'])
    current=read_receipt(root,receipt_path(root,key,digest),source_id,key,digest)
    if current['raw_path'] not in (plan['previous_raw_path'],plan['raw_path']):
        raise brain.BrainError('The receipt path changed; refresh the relocation plan.')
    with source_lock(root,'storage'):
        storage=read_storage(root)
        allocated = storage['sources'].get(key, {}).get('versions', {}).get(digest, {})
        prior_paths = [current['raw_path'], allocated.get('raw_path'), *allocated.get('previous_raw_paths', [])]
        if plan.get('previous_raw_path') not in prior_paths:
            raise brain.BrainError('The relocation plan contains an unallocated prior path; plan again.')
        expected=allocation_plan(root,current,storage,plan.get('title'),plan.get('requested_folder'),plan.get('requested_filename'),relocate=True)
        if any(expected.get(field)!=plan.get(field) for field in ('source_id','sha256','directory','raw_path','original_name','captured_at','title','requested_folder','requested_filename')):
            raise brain.BrainError('Storage changed or the relocation plan was altered; plan again before copying.')
        save_allocation(root,plan,storage)


def read_receipt(root: Path, path: Path, source_id: str, key: str, digest: str) -> dict:
    if identity(source_id) != (source_id, key):
        raise brain.BrainError('Receipt key does not match its full source identity.')
    checked_digest(digest)
    data = brain.read_json(path)
    expected_parent = f'raw/{key}/{digest}/'
    if (not isinstance(data, dict) or data.get('schema_version') != 1
            or data.get('source_id') != source_id or data.get('sha256') != digest
            or not isinstance(data.get('raw_path'), str)
            or not isinstance(data.get('targets'), dict)
            or not isinstance(data.get('revisions'), list)
            or not all(isinstance(item, str) for item in data['revisions'])):
        raise brain.BrainError('Invalid intake receipt; preserve it for review.')
    raw = brain.safe_brain_path(root, data['raw_path'])
    if raw.parent != brain.safe_brain_path(root, expected_parent):
        allocated = read_storage(root)['sources'].get(key, {}).get('versions', {}).get(digest)
        if not allocated or data['raw_path'] not in [allocated['raw_path'],*allocated.get('previous_raw_paths',[])]:
            raise brain.BrainError('Invalid or unallocated raw source path in intake receipt.')
    for slug, target in data['targets'].items():
        brain.checked_slug(slug)
        if (not isinstance(target, dict) or target.get('status') not in ('pending', 'complete')
                or (target.get('status') == 'complete' and not isinstance(target.get('synthesis'), str))):
            raise brain.BrainError('Invalid workspace processing status in intake receipt.')
        if target['status'] == 'complete':
            workspace = brain.resolve_project(root, slug, root)
            relative = target['synthesis']
            synthesis = brain.safe_project_path(workspace, relative)
            if not relative.startswith('Ingestion/') or synthesis.suffix != '.md':
                raise brain.BrainError('Invalid completed synthesis path in intake receipt.')
            if not synthesis.is_file() or synthesis.stat().st_size == 0:
                data['targets'][slug] = {
                    **target, 'status': 'pending', 'synthesis': None,
                    'previous_synthesis': relative, 'reason': 'Recorded synthesis is missing or empty.',
                }
    if not raw.is_file() or brain.digest(raw.read_bytes()) != digest:
        raise brain.BrainError('Captured original is missing or changed; preserve the receipt and investigate before continuing.')
    return data


def status(data: dict) -> str:
    if not data['targets']:
        return 'unassigned'
    return 'complete' if all(item['status'] == 'complete' for item in data['targets'].values()) else 'pending'


def save_receipt(root: Path, key: str, data: dict):
    path = receipt_path(root, key, data['sha256'])
    queue = brain.safe_brain_path(root, f'inbox/{key}-{data["sha256"]}.json')
    pointer = {
        'schema_version': 1, 'source_id': data['source_id'],
        'receipt': path.relative_to(brain.resolve_brain(root)).as_posix(),
        'question': 'Which workspace or workspaces should receive this source?',
    }
    if queue.exists() and brain.read_json(queue) != pointer:
        raise brain.BrainError('Inbox pointer has unexpected content; preserve it for review.')
    data['status'] = status(data)
    brain.atomic_write(path, (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode())
    if data['status'] == 'unassigned':
        # The inbox points to the receipt; it contains no second copy of the source.
        if not queue.exists():
            brain.atomic_write(queue, (json.dumps(pointer, indent=2, ensure_ascii=False) + '\n').encode())
    elif queue.exists():
        # Only remove an intake-owned pointer. User notes elsewhere in inbox are untouched.
        queue.unlink()


def result(root: Path, key: str, data: dict, created: bool = False) -> dict:
    return {
        'source_id': data['source_id'], 'sha256': data['sha256'],
        'raw_path': str(brain.safe_brain_path(root, data['raw_path'])),
        'receipt': str(receipt_path(root, key, data['sha256'])),
        'status': status(data), 'created': created,
        'pending_projects': [slug for slug, item in data['targets'].items() if item['status'] == 'pending'],
    }


def capture(root: Path, file: Path, source_id: str, projects=(), revision: str | None = None,
            title: str | None = None, folder: str | None = None, filename: str | None = None) -> dict:
    brain.resolve_brain(root)
    source_id, key = identity(source_id)
    selected = sorted(set(projects))
    for slug in selected:
        brain.resolve_project(root, slug, root)
    if revision is not None:
        revision = brain.one_line_text(revision, 'Source revision', 500)
    if title is not None:
        title = brain.one_line_text(title, 'Source title', 500)
    if folder is not None:checked_folder(root,folder)
    if filename is not None:checked_filename(filename)
    file = Path(file)
    if not file.is_file():
        raise brain.BrainError('Supply one existing local source file; folders are not capture inputs.')
    if is_finder_metadata(file):
        raise brain.BrainError('Finder metadata is not a source capture input.')
    content = file.read_bytes()
    digest = brain.digest(content)
    with source_lock(root, key):
        path = receipt_path(root, key, digest)
        created = not path.exists()
        if path.exists():
            data = read_receipt(root, path, source_id, key, digest)
        else:
            data = {
                'schema_version': 1, 'source_id': source_id, 'sha256': digest,
                'original_name': file.name, 'captured_at': datetime.now(timezone.utc).isoformat(),
                'revisions': [], 'targets': {slug: {'status':'pending','synthesis':None} for slug in selected},
            }
            legacy = brain.safe_brain_path(root, f'raw/{key}/{digest}')
            prior = raw_entries(root, legacy)
            if prior:
                # Old interrupted captures have no allocation; preserve their path.
                if len(prior) != 1 or not prior[0].is_file() or not re.fullmatch(r'source\.[a-z0-9]{1,12}', prior[0].name):
                    raise brain.BrainError('Unexpected files in this legacy raw version; preserve them for review.')
                raw = prior[0]
                data['raw_path'] = raw.relative_to(brain.resolve_brain(root)).as_posix()
            else:
                # Allocate before writing bytes, so failed receipt writes and renamed
                # retries use the same exact filename and original capture time.
                with source_lock(root, 'storage'):
                    storage = read_storage(root)
                    plan = allocation_plan(root, data, storage, title, folder, filename)
                    save_allocation(root, plan, storage)
                for field in ('raw_path', 'original_name', 'captured_at'):
                    data[field] = plan[field]
                data['description'] = {'title': plan['title'], 'source_type': 'unknown',
                                       'known_gaps': [], 'evidence_links': []}
                raw = brain.safe_brain_path(root, data['raw_path'])
            raw.parent.mkdir(parents=True, exist_ok=True)
            if raw.exists():
                if not raw.is_file() or raw.read_bytes() != content:
                    raise brain.BrainError('An existing raw source differs; nothing was overwritten.')
            else:
                with raw.open('xb') as stream:
                    stream.write(content)
        if revision is not None and revision not in data['revisions']:
            data['revisions'].append(revision)
        for slug in selected:
            data['targets'].setdefault(slug, {'status': 'pending', 'synthesis': None})
        save_receipt(root, key, data)
        return result(root, key, data, created)


def mark_complete(root: Path, source_id: str, digest: str, project: str, synthesis: str) -> dict:
    source_id, key = identity(source_id)
    checked_digest(digest)
    workspace = brain.resolve_project(root, project, root)
    target = brain.safe_project_path(workspace, synthesis)
    if not synthesis.startswith('Ingestion/') or target.suffix != '.md' or not target.is_file() or target.stat().st_size == 0:
        raise brain.BrainError('Completion requires an existing Markdown synthesis under the selected workspace Ingestion/.')
    with source_lock(root, key):
        data = read_receipt(root, receipt_path(root, key, digest), source_id, key, digest)
        if project not in data['targets']:
            raise brain.BrainError('This workspace was not assigned this source. Confirm routing, then capture with --project first.')
        data['targets'][project] = {**data['targets'][project], 'status': 'complete', 'synthesis': synthesis}
        save_receipt(root, key, data)
        return result(root, key, data)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    cap = sub.add_parser('capture')
    cap.add_argument('--file', required=True, type=Path)
    cap.add_argument('--source-id', required=True, help='Non-secret stable provider:account:item identity; never a credential.')
    cap.add_argument('--project', action='append', default=[])
    cap.add_argument('--revision')
    cap.add_argument('--title', help='Descriptive source title; identity remains --source-id.')
    cap.add_argument('--folder', help='Optional portable category path below raw/; does not assign projects.')
    cap.add_argument('--filename', help='Optional readable filename; original_name remains preserved.')
    done = sub.add_parser('mark-complete')
    for argument in ('source-id', 'digest', 'project', 'synthesis'):
        done.add_argument('--' + argument, required=True)
    args = parser.parse_args(argv)
    try:
        if sys.version_info < (3, 11):
            raise brain.BrainError('Python 3.11 or newer is required.')
        if args.command == 'capture':
            output = capture(TOOLKIT_ROOT, args.file, args.source_id, args.project, args.revision, args.title, args.folder, args.filename)
        else:
            output = mark_complete(TOOLKIT_ROOT, args.source_id, args.digest, args.project, args.synthesis)
        print(json.dumps(output, indent=2))
        return 0
    except (brain.BrainError, OSError) as exc:
        print(f'Brain intake: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
