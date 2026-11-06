#!/usr/bin/env python3
"""Compare two *real* ESCO occupation JSON payloads without altering DBP.

A missing previous payload generates NO_BASELINE. An unavailable current payload
generates NOT_TESTED. Never calls GitHub or the ESCO API on its own.
"""
import argparse
import hashlib
import json
from pathlib import Path

OCCUPATION = 'http://data.europa.eu/esco/occupation/4910419f-b4af-4f59-b544-9dbebc8a74f0'
RELATION_KEYS = {'hasEssentialSkill': 'essential', 'hasOptionalSkill': 'optional'}


def unpack(path):
    data_bytes = Path(path).read_bytes()
    data = json.loads(data_bytes)
    if data.get('uri') != OCCUPATION or not isinstance(data.get('_links'), dict):
        raise ValueError('Unexpected occupation or missing _links')
    entries = {}
    for key, relation in RELATION_KEYS.items():
        group = data['_links'].get(key)
        if not isinstance(group, list):
            raise ValueError('Missing / invalid relationship: ' + key)
        for item in group:
            uri = item.get('uri')
            if not isinstance(uri, str) or uri in entries:
                raise ValueError('Missing / duplicated URI')
            entries[uri] = {'relationship': relation,
                            'title': item.get('title', ''),
                            'skill_type': item.get('skillType', '').rsplit('/', 1)[-1]}
    return entries, hashlib.sha256(data_bytes).hexdigest()


def compare(current, previous):
    new, removed, changed = [], [], []
    for uri in sorted(current.keys() - previous.keys()):
        new.append({'uri': uri, **current[uri]})
    for uri in sorted(previous.keys() - current.keys()):
        removed.append({'uri': uri, **previous[uri]})
    for uri in sorted(current.keys() & previous.keys()):
        if current[uri] != previous[uri]:
            changed.append({'uri': uri, 'previous': previous[uri], 'current': current[uri]})
    return {'new_relations': new, 'removed_relations': removed, 'modified_relations': changed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current', required=True)
    parser.add_argument('--previous')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {'status': 'NOT_TESTED', 'promotion_authorized': False}
    try:
        if not Path(args.current).is_file():
            result['reason'] = 'Current live JSON unavailable; no comparison can be made'
        else:
            cur, sha = unpack(args.current)
            result.update(status='NO_BASELINE', current_sha256=sha,
                          current_relation_count=len(cur))
            if args.previous and Path(args.previous).is_file():
                prev, prev_sha = unpack(args.previous)
                result.update(status='COMPARED', previous_sha256=prev_sha,
                              previous_relation_count=len(prev),
                              **compare(cur, prev))
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        result = {'status': 'COMPARISON_FAILED', 'reason': str(exc), 'promotion_authorized': False}
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'out': str(output)}))
    return 0 if result['status'] in ('COMPARED', 'NO_BASELINE', 'NOT_TESTED') else 2


if __name__ == '__main__':
    raise SystemExit(main())
