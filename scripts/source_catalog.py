#!/usr/bin/env python3
"""Describe captured evidence and generate a guarded workspace source catalog.

Python 3.11+, stdlib only. Receipts remain canonical; this helper does not classify
sources, verify their claims, change routing, or edit captured originals.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote

import brain
import intake

TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
START = '<!-- BEGIN GENERATED SOURCE CATALOG -->'
END = '<!-- END GENERATED SOURCE CATALOG -->'
SOURCE_TYPES = {
    'primary_evidence': 'Primary evidence',
    'imported_summary': 'Imported wiki summary (secondary evidence)',
    'unknown': 'Unknown — source type has not been established',
}
HEX = re.compile(r'[a-f0-9]{64}\Z')


def checked_description(root: Path, description: dict) -> dict:
    """Validate explicitly supplied metadata; missing lists mean no recorded items."""
    if not isinstance(description, dict) or set(description) - {'title', 'source_type', 'known_gaps', 'evidence_links'}:
        raise brain.BrainError('Description must contain only title, source_type, known_gaps, and evidence_links.')
    title = brain.one_line_text(description.get('title'), 'Source title', 500)
    source_type = description.get('source_type')
    if not isinstance(source_type, str) or source_type not in SOURCE_TYPES:
        raise brain.BrainError('Source type must be primary_evidence, imported_summary, or unknown; do not infer it from a filename.')
    gaps = description.get('known_gaps', [])
    links = description.get('evidence_links', [])
    if not isinstance(gaps, list) or len(gaps) > 200:
        raise brain.BrainError('Known gaps must be a list of at most 200 single-line statements.')
    gaps = [brain.one_line_text(item, 'Known gap', 2000) for item in gaps]
    if not isinstance(links, list) or len(links) > 200:
        raise brain.BrainError('Evidence links must be a list of at most 200 local references.')
    checked_links = []
    for item in links:
        if not isinstance(item, dict) or set(item) != {'label', 'path'}:
            raise brain.BrainError('Each evidence link requires exactly label and path.')
        label = brain.one_line_text(item['label'], 'Evidence label', 500)
        relative = brain.one_line_text(item['path'], 'Evidence path', 2000)
        path = brain.safe_brain_path(root, relative)
        if not path.is_file():
            raise brain.BrainError('An evidence link does not resolve to an existing private Brain file.')
        # Store the canonical root-relative spelling, never a machine-specific path.
        checked_links.append({'label': label, 'path': path.relative_to(brain.resolve_brain(root)).as_posix()})
    return {'title': title, 'source_type': source_type, 'known_gaps': gaps, 'evidence_links': checked_links}


def describe(root: Path, source_id: str, digest: str, description: dict) -> dict:
    """Replace this version's description only; retain every other receipt field."""
    root = brain.resolve_brain(root)
    source_id, key = intake.identity(source_id)
    digest = intake.checked_digest(digest)
    description = checked_description(root, description)
    with intake.source_lock(root, key):
        path = intake.receipt_path(root, key, digest)
        data = intake.read_receipt(root, path, source_id, key, digest)
        data['description'] = description
        intake.save_receipt(root, key, data)
    return {'source_id': source_id, 'sha256': digest, 'receipt': str(path), 'description_updated': True}


def text(value: str) -> str:
    """Render untrusted plain text without creating Markdown or HTML structure."""
    # Legacy metadata may contain unsafe original filenames. Show control characters
    # literally without changing the canonical original_name or captured bytes.
    value = ''.join(f'\\u{ord(c):04x}' if ord(c) < 32 or c in '\u007f\u0085\u2028\u2029' else c for c in str(value))
    value = html.escape(value, quote=True)
    return re.sub(r'([\\`*_{}\[\]()!#|~])', r'\\\1', value)


def link(root: Path, workspace: Path, label: str, relative: str) -> str:
    path = brain.safe_brain_path(root, relative)
    if not path.is_file():
        raise brain.BrainError('A catalog citation is missing; preserve the existing catalog and repair its metadata.')
    href = quote(os.path.relpath(path, workspace).replace(os.sep, '/'), safe='/')
    return f'[{text(label)}]({href})'


def capture_time(data: dict) -> tuple[datetime, str]:
    value = data.get('captured_at')
    try:
        timestamp = datetime.fromisoformat(value.replace('Z', '+00:00')) if isinstance(value, str) else None
        if timestamp is None or timestamp.tzinfo is None:
            raise ValueError('Missing timezone')
        timestamp = timestamp.astimezone(timezone.utc)
        return timestamp, timestamp.isoformat().replace('+00:00', 'Z') + ' (UTC capture time)'
    except (ValueError, OverflowError):
        return datetime.min.replace(tzinfo=timezone.utc), 'Unknown (missing or invalid capture timestamp)'


def records_for_project(root: Path, project: str) -> list[dict]:
    """Read canonical receipt-shaped paths, never allocation state or Finder files."""
    folder = brain.safe_brain_path(root, 'maintenance/intake')
    if not folder.exists():
        return []
    records = []
    for directory in sorted(folder.iterdir()):
        if not HEX.fullmatch(directory.name):
            continue
        directory = brain.safe_brain_path(root, directory.relative_to(root).as_posix())
        if not directory.is_dir():
            raise brain.BrainError('An intake source directory is not a directory; catalog coverage is incomplete.')
        for path in sorted(directory.iterdir()):
            if intake.is_finder_metadata(path):
                continue
            if path.suffix != '.json' or not HEX.fullmatch(path.stem):
                raise brain.BrainError('Unexpected content in an intake source directory; catalog coverage is incomplete.')
            path = brain.safe_brain_path(root, path.relative_to(root).as_posix())
            data = brain.read_json(path)
            if not isinstance(data, dict) or not isinstance(data.get('targets'), dict):
                raise brain.BrainError('An intake receipt has unreadable routing; catalog coverage is incomplete.')
            source_id, key = intake.identity(data.get('source_id'))
            if key != directory.name or data.get('sha256') != path.stem or data.get('schema_version') != 1:
                raise brain.BrainError('An intake receipt has invalid identity metadata; catalog coverage is incomplete.')
            if project not in data['targets']:
                continue
            data = intake.read_receipt(root, path, source_id, key, path.stem)
            if 'description' in data:
                stored = data['description']
                if not isinstance(stored, dict):
                    raise brain.BrainError('Invalid source description; preserve the receipt for review.')
                description = checked_description(root, {
                    'title': data.get('original_name') or 'Untitled captured source',
                    'source_type': 'unknown', 'known_gaps': [], 'evidence_links': [], **stored,
                })
            else:
                description = {'title': data.get('original_name') or 'Untitled captured source',
                               'source_type': 'unknown', 'known_gaps': [], 'evidence_links': []}
            records.append({'data': data, 'description': description, 'receipt': path.relative_to(root).as_posix()})
    return records


def render(root: Path, project: str) -> tuple[bytes, dict]:
    root = brain.resolve_brain(root)
    workspace = brain.resolve_project(root, project, root)
    records = records_for_project(root, project)
    groups = {}
    for record in records:
        groups.setdefault(record['data']['source_id'], []).append(record)
    for versions in groups.values():
        versions.sort(key=lambda r: (capture_time(r['data'])[0], r['data']['sha256']))
    grouped = sorted(groups.items(), key=lambda pair: (str(pair[1][-1]['description']['title']).casefold(), pair[0]))
    gaps_count = sum(len(r['description']['known_gaps']) for r in records)
    pending_count = sum(r['data']['targets'][project]['status'] != 'complete' for r in records)
    unknown_count = sum(r['description']['source_type'] == 'unknown' for r in records)
    lines = ['# Sources', '', START, '',
             'Generated from canonical intake receipts. Update receipt descriptions and regenerate this view; '
             'keep personal notes in interpretations or decision records.', '',
             'Capture dates describe retrieval, not authorship. A completed interpretation does not establish '
             'that a source is current, accurate, or authoritative. Only versions assigned to this workspace appear here.', '',
             f'**Inventory:** {len(groups)} sources; {len(records)} captured content versions; '
             f'{pending_count} pending interpretations; {unknown_count} versions with unknown source type; '
             f'{gaps_count} recorded gap statements.', '', '## What remains uncertain', '']
    if not records:
        lines += ['No captured sources are assigned to this workspace. Source coverage and uncertainty are unknown.', '']
    else:
        any_uncertainty = False
        for source_id, versions in grouped:
            for record in versions:
                data, description = record['data'], record['description']
                title_link = link(root, workspace, description['title'], data['raw_path'])
                prefix = title_link + ' (version ' + data['sha256'][:8] + ')'
                for gap in description['known_gaps']:
                    lines.append(f'- {prefix}: {text(gap)}')
                    any_uncertainty = True
                if description['source_type'] == 'unknown':
                    lines.append(f'- {prefix}: source type has not been established; do not assume this is primary evidence.')
                    any_uncertainty = True
                if capture_time(data)[0].year == 1:
                    lines.append(f'- {prefix}: capture time is missing or invalid in the receipt.')
                    any_uncertainty = True
                target = data['targets'][project]
                if target['status'] != 'complete':
                    reason = target.get('reason') or 'Workspace interpretation has not been completed.'
                    lines.append(f'- {prefix}: {text(reason)}')
                    any_uncertainty = True
        if not any_uncertainty:
            lines.append('No specific gaps are recorded. This is not proof of completeness, freshness, or authority.')
        lines += ['', 'Supporting evidence and interpretation links appear with each captured version below.', '']
    lines += ['## Source inventory', '']
    for source_id, versions in grouped:
        title = versions[-1]['description']['title']
        lines += [f'### {text(title)}', '', f'Stable source ID: {text(source_id)}', '',
                  f'{len(versions)} captured content version(s) assigned here. Versions are listed by capture time; '
                  'later capture does not establish authority.', '']
        for number, record in enumerate(versions, 1):
            data, description = record['data'], record['description']
            receipt_link = link(root, workspace, 'Canonical receipt (full identity and checksum)', record['receipt'])
            original_link = link(root, workspace, 'Captured original', data['raw_path'])
            revisions = ', '.join(text(item) for item in data['revisions']) or 'None recorded'
            lines += [f'#### Content version {number}: {data["sha256"][:8]}', '',
                      f'- Title: {text(description["title"])}',
                      f'- Source type: {SOURCE_TYPES[description["source_type"]]}',
                      f'- Original filename: {text(data.get("original_name") or "Unknown (legacy receipt)")}',
                      f'- Captured: {capture_time(data)[1]}', f'- Recorded source revisions: {revisions}',
                      f'- SHA-256: `{data["sha256"]}`', f'- Evidence: {original_link}; {receipt_link}']
            target = data['targets'][project]
            if target['status'] == 'complete':
                synthesis = f'Projects/{project}/{target["synthesis"]}'
                lines.append('- Interpretation: complete — ' + link(root, workspace, 'Read workspace interpretation', synthesis))
            else:
                lines.append('- Interpretation: pending — ' + text(target.get('reason') or 'No completed interpretation is recorded.'))
            if description['source_type'] == 'imported_summary':
                lines.append('- Evidence caution: this is an imported summary; follow its cited primary evidence before relying on its claims.')
            if description['known_gaps']:
                lines.append('- Known gaps: ' + '; '.join(text(item) for item in description['known_gaps']))
            else:
                lines.append('- Known gaps: none recorded; coverage and factual accuracy have not been established by this catalog.')
            if description['evidence_links']:
                lines.append('- Gap/context evidence: ' + '; '.join(link(root, workspace, item['label'], item['path']) for item in description['evidence_links']))
            lines.append('')
    lines += [END, '']
    return '\n'.join(lines).encode('utf-8'), {'sources': len(groups), 'content_versions': len(records),
           'pending_interpretations': pending_count, 'unknown_source_types': unknown_count, 'recorded_gaps': gaps_count}


@contextmanager
def catalog_lock(root: Path, project: str):
    path = brain.safe_brain_path(root, f'maintenance/source-catalogs/{project}.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise brain.BrainError('This source catalog is being generated; retry after its owner finishes.') from exc
    try:
        os.close(fd)
        yield
    finally:
        path.unlink()


def generate(root: Path, project: str) -> dict:
    """Generate SOURCES.md only when absent, pristine, or an unchanged owned view."""
    root = brain.resolve_brain(root)
    workspace = brain.resolve_project(root, project, root)
    target = brain.safe_project_path(workspace, 'SOURCES.md')
    state_path = brain.safe_brain_path(root, f'maintenance/source-catalogs/{project}.json')
    with catalog_lock(root, project):
        content, summary = render(root, project)
        current = target.read_bytes() if target.exists() else None
        state = brain.read_json(state_path) if state_path.exists() else None
        if state is not None and (not isinstance(state, dict) or state.get('schema_version') != 1
                                  or state.get('project') != project or not isinstance(state.get('sha256'), str)
                                  or not HEX.fullmatch(state['sha256'])):
            raise brain.BrainError('Invalid catalog generation state; preserve it and the catalog for review.')
        template_path = brain.safe_under(root, 'templates/project/SOURCES.md')
        template = template_path.read_bytes() if template_path.is_file() else None
        owned = state is not None and current is not None and brain.digest(current) == state['sha256']
        pristine = state is None and template is not None and current == template
        # Exact desired bytes are also safe after an interrupted state write: no
        # user content would be lost by adopting that deterministic view.
        if current is not None and current != content and not owned and not pristine:
            raise brain.BrainError('SOURCES.md contains unmanaged or edited content. Preserve those notes in a separate file and explicitly restore the generated version before retrying; nothing was overwritten.')
        changed = current != content
        if changed:
            brain.atomic_write(target, content)
        state_data = {'schema_version': 1, 'project': project, 'sha256': brain.digest(content)}
        if state != state_data:
            brain.atomic_write(state_path, (json.dumps(state_data, indent=2) + '\n').encode('utf-8'))
    return {'catalog': str(target), 'changed': changed, **summary}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    description = sub.add_parser('describe', help='Replace one receipt description with explicitly supplied JSON metadata.')
    description.add_argument('--source-id', required=True)
    description.add_argument('--digest', required=True)
    description.add_argument('--metadata-json', required=True, type=Path)
    catalog = sub.add_parser('generate', help='Regenerate a selected workspace catalog without overwriting user edits.')
    catalog.add_argument('--project', required=True)
    args = parser.parse_args(argv)
    try:
        if sys.version_info < (3, 11):
            raise brain.BrainError('Python 3.11 or newer is required.')
        if args.command == 'describe':
            output = describe(TOOLKIT_ROOT, args.source_id, args.digest, brain.read_json(args.metadata_json))
        else:
            output = generate(TOOLKIT_ROOT, args.project)
        print(json.dumps(output, indent=2))
        return 0
    except (brain.BrainError, OSError) as exc:
        print(f'Brain source catalog: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
