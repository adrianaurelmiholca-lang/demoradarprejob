#!/usr/bin/env python3
"""Read-only ESCO evidence checker for PREJOB. Python 3.10+, stdlib only.

Writes only local artifacts; never writes to DBP, GitHub or production.
Offline fixture mode verifies the parser but never grants OFFICIAL status.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

OCCUPATION = 'http://data.europa.eu/esco/occupation/4910419f-b4af-4f59-b544-9dbebc8a74f0'
ENDPOINT = 'https://ec.europa.eu/esco/api/resource/occupation'
COLUMNS = ['occupation_uri', 'skill_uri', 'candidate_label_en', 'candidate_skill_type',
           'reported_relation', 'api_relation', 'api_label_en', 'api_skill_type',
           'validation_status', 'quality_flags', 'evidence_sha256', 'api_url']


def candidates(path):
    with open(path, newline='', encoding='utf-8-sig') as stream:
        records = list(csv.DictReader(stream))
    if not records:
        raise ValueError('Candidate CSV is empty')
    uris = [r['skill_uri'] for r in records]
    if len(set(uris)) != len(uris):
        raise ValueError('Duplicate candidate skill URI')
    for record in records:
        if record['occupation_uri'] != OCCUPATION:
            raise ValueError('Unexpected occupation URI')
        if not record['skill_uri'].startswith('http://data.europa.eu/esco/skill/'):
            raise ValueError('Invalid candidate skill URI prefix')
    return records


def extraction(payload):
    if not isinstance(payload, dict) or payload.get('uri') != OCCUPATION:
        raise ValueError('API payload missing or mismatching occupation URI')
    links = payload.get('_links')
    if not isinstance(links, dict):
        raise ValueError('Expected ESCO HAL _links object')
    found = {}
    for relation, key in [('essential', 'hasEssentialSkill'), ('optional', 'hasOptionalSkill')]:
        links_list = links.get(key)
        if not isinstance(links_list, list):
            raise ValueError('Missing or malformed _links.' + key)
        for item in links_list:
            if not isinstance(item, dict) or not isinstance(item.get('uri'), str):
                raise ValueError('Malformed skill relation')
            uri = item['uri']
            if uri in found:
                raise ValueError('Duplicate/contradictory API skill relation ' + uri)
            found[uri] = (relation, item.get('title', ''), item.get('skillType', ''))
    return found


def fetch(version, timeout):
    query = urllib.parse.urlencode({'uri': OCCUPATION, 'language': 'en', 'selectedVersion': version})
    url = ENDPOINT + '?' + query
    request = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'PREJOB-ESCO-evidence-check/0.1'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = response.status
        body = response.read(4_000_001)
        if len(body) > 4_000_000:
            raise ValueError('Response over 4 MB cap')
        if status != 200:
            raise ValueError('HTTP ' + str(status))
        return url, status, body


def verify(rows, payload, evidence_mode, sha, api_url):
    indexed = extraction(payload)
    output = []
    for row in rows:
        match = indexed.get(row['skill_uri'])
        flags = []
        if not match:
            status = 'NOT_FOUND_IN_API' if evidence_mode == 'live' else 'FIXTURE_ABSENT_NOT_OFFICIAL'
        else:
            relation, label, skill_type_uri = match
            skill_type = skill_type_uri.rsplit('/', 1)[-1]
            if relation != row['relationship_in_attachment']:
                flags.append('RELATION_TYPE_MISMATCH')
            if skill_type != row['skill_type_in_attachment']:
                flags.append('SKILL_TYPE_MISMATCH')
            if label != row['skill_label_en_in_attachment']:
                flags.append('LABEL_MISMATCH')
            if not label or skill_type not in ('skill', 'knowledge'):
                flags.append('MISSING_OR_UNEXPECTED_API_FIELDS')
            if evidence_mode != 'live':
                status = 'FIXTURE_MATCH_NOT_OFFICIAL'
            elif flags:
                status = 'API_RELATION_REQUIRES_REVIEW'
            else:
                status = 'API_RELATION_CONFIRMED_VERSION_UNVERIFIED'
        output.append({
            'occupation_uri': row['occupation_uri'], 'skill_uri': row['skill_uri'],
            'candidate_label_en': row['skill_label_en_in_attachment'],
            'candidate_skill_type': row['skill_type_in_attachment'],
            'reported_relation': row['relationship_in_attachment'],
            'api_relation': match[0] if match else '',
            'api_label_en': match[1] if match else '',
            'api_skill_type': match[2].rsplit('/', 1)[-1] if match else '',
            'validation_status': status, 'quality_flags': '|'.join(flags),
            'evidence_sha256': sha, 'api_url': api_url
        })
    return output, indexed


def not_tested(rows):
    return [{
        'occupation_uri': row['occupation_uri'], 'skill_uri': row['skill_uri'],
        'candidate_label_en': row['skill_label_en_in_attachment'],
        'candidate_skill_type': row['skill_type_in_attachment'],
        'reported_relation': row['relationship_in_attachment'], 'api_relation': '',
        'api_label_en': '', 'api_skill_type': '',
        'validation_status': 'NOT_TESTED', 'quality_flags': '',
        'evidence_sha256': '', 'api_url': ''
    } for row in rows]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidates', required=True, type=pathlib.Path)
    parser.add_argument('--out', required=True, type=pathlib.Path)
    parser.add_argument('--selected-version', default='latest')
    parser.add_argument('--timeout', type=float, default=12)
    parser.add_argument('--fixture', type=pathlib.Path, help='Local fixture for parser tests only; never official evidence')
    args = parser.parse_args(argv)
    if args.selected_version not in ('latest', '1.2.1', '1.2.0', '1.1.2', '1.0.9'):
        parser.error('Unsupported selected-version value')
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    rows = candidates(args.candidates)
    args.out.mkdir(parents=True, exist_ok=True)
    evidence_mode = 'fixture' if args.fixture else 'live'
    error = None
    status_code = None
    api_url = ''
    sha = ''
    count_api = 0
    try:
        if args.fixture:
            body = args.fixture.read_bytes()
        else:
            api_url, status_code, body = fetch(args.selected_version, args.timeout)
        payload = json.loads(body)
        sha = hashlib.sha256(body).hexdigest()
        output, indexed = verify(rows, payload, evidence_mode, sha, api_url)
        count_api = len(indexed)
        # Store raw bytes only for a successful live request, never a Qwen chat reconstruction.
        if evidence_mode == 'live':
            (args.out / 'esco_electrician_http200_raw.json').write_bytes(body)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
        error = f'{type(exc).__name__}: {exc}'
        output = not_tested(rows)
    with (args.out / 'esco_electrician_validation.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(output)
    counts = {label: sum(r['validation_status'] == label for r in output) for label in sorted({r['validation_status'] for r in output})}
    meta = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'occupation_uri': OCCUPATION, 'selected_version_requested': args.selected_version,
        'version_confirmed_from_payload': None,
        'mode': evidence_mode, 'http_status': status_code,
        'official_evidence_url': api_url or None, 'sha256': sha or None,
        'candidate_count': len(rows), 'api_relation_count': count_api,
        'counts': counts, 'error': error,
        'warning': ('Fixture output is never official evidence.' if args.fixture else
                    'API response (if retrieved) confirms only the observed relationship at requested '
                    'version; version and provenance review required before any DBP promotion.'),
    }
    (args.out / 'esco_electrician_manifest.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0 if not error else 2


if __name__ == '__main__':
    sys.exit(main())
