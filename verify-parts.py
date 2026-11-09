"""Verify immutable publication fragments; optional exact offline reconstruction."""
from pathlib import Path
import argparse, hashlib, json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, help='Also compare against an existing standalone HTML')
parser.add_argument('--output', type=Path, help='Write reconstructed HTML; never overwrite')
args = parser.parse_args()
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'parts-manifest.json').read_text(encoding='utf-8'))
sha = lambda data: hashlib.sha256(data).hexdigest()
expected_index = ('---\nlayout: none\n---\n' + ''.join('{% include ' + p['file'] + ' %}' for p in manifest['parts'])).encode('utf-8')
index = (root / 'index.html').read_bytes()
assert index == expected_index, 'Index has changed or contains extra whitespace'
assert sha(index) == manifest['indexSha256']
opening, closing = manifest['rawOpening'].encode('ascii'), manifest['rawClosing'].encode('ascii')
fragments, total, digest = [], 0, hashlib.sha256()
for part in manifest['parts']:
    assert Path(part['file']).name == part['file'], 'Invalid fragment name'
    data = (root / '_includes' / part['file']).read_bytes()
    assert len(data) == part['wrappedBytes'] <= manifest['maxWrappedPartBytes']
    assert sha(data) == part['wrappedSha256'], part['file']
    assert data.startswith(opening) and data.endswith(closing)
    payload = data[len(opening):-len(closing)]
    payload.decode('utf-8')
    assert b'{%' not in payload and b'{{' not in payload, 'Unexpected Liquid syntax'
    assert part['offset'] == total and len(payload) == part['payloadBytes']
    assert sha(payload) == part['payloadSha256']
    total += len(payload)
    digest.update(payload)
    fragments.append(payload)
assert total == manifest['sourceBytes']
assert digest.hexdigest() == manifest['sourceSha256'], 'Reassembled HTML differs'
for name, expected in manifest['copiedFiles'].items():
    data = (root / name).read_bytes()
    assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
if args.source:
    original = args.source.read_bytes()
    assert len(original) == total and sha(original) == digest.hexdigest()
    assert b''.join(fragments) == original, 'Byte comparison failed'
if args.output:
    with args.output.open('xb') as output:
        for payload in fragments:
            output.write(payload)
print(json.dumps({'passed': True, 'parts': len(fragments), 'bytes': total,
                  'sha256': digest.hexdigest(), 'sourceCompared': bool(args.source),
                  'output': str(args.output) if args.output else None}, indent=2))
