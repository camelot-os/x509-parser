#!/usr/bin/env python3

import argparse
import json
import pathlib
import shlex
import subprocess
import sys

PAIR_FLAGS = {
    '-I',
    '-isystem',
    '-iquote',
    '-idirafter',
    '-include',
    '-imacros',
    '--sysroot',
}

PREFIX_FLAGS = (
    '-I',
    '-D',
    '-U',
    '-isystem',
    '-iquote',
    '-idirafter',
    '-include',
    '-imacros',
    '--sysroot=',
)

SINGLE_FLAGS = {
    '-nostdinc',
    '-nostdinc++',
}

EXCLUDED_DEFINE_NAMES = {
    '_FORTIFY_SOURCE',
}


def normalize_path(path: str, base_dir: pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(path)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    return candidate.resolve()


def load_compdb(compdb_path: pathlib.Path):
    with compdb_path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def expand_response_files(tokens, cwd: pathlib.Path):
    for token in tokens:
        if token.startswith('@') and len(token) > 1:
            response_file = pathlib.Path(token[1:])
            if not response_file.is_absolute():
                response_file = cwd / response_file
            if response_file.exists():
                content = response_file.read_text(encoding='utf-8', errors='ignore')
                response_tokens = shlex.split(content)
                yield from expand_response_files(response_tokens, response_file.parent)
                continue
        yield token


def entry_tokens(entry, default_cwd: pathlib.Path):
    if 'arguments' in entry and entry['arguments']:
        tokens = list(entry['arguments'])
    elif 'command' in entry and entry['command']:
        tokens = shlex.split(entry['command'])
    else:
        tokens = []

    entry_cwd = pathlib.Path(entry.get('directory', str(default_cwd))).resolve()
    return list(expand_response_files(tokens, entry_cwd))


def find_compdb_entry(compdb, source_abs: pathlib.Path, build_dir: pathlib.Path):
    matches = []
    for entry in compdb:
        entry_file = entry.get('file')
        if not entry_file:
            continue
        entry_dir = pathlib.Path(entry.get('directory', str(build_dir))).resolve()
        entry_abs = normalize_path(entry_file, entry_dir)
        if entry_abs == source_abs:
            return entry
        if entry_abs.name == source_abs.name:
            matches.append(entry)

    if len(matches) == 1:
        return matches[0]

    if matches:
        return matches[0]

    raise RuntimeError(f'No compilation database entry found for {source_abs}')


def extract_preprocessor_flags(tokens):
    extracted = []
    seen = set()

    index = 1 if tokens else 0
    while index < len(tokens):
        token = tokens[index]

        if token in PAIR_FLAGS:
            if index + 1 < len(tokens):
                value = tokens[index + 1]
                key = ('pair', token, value)
                if key not in seen:
                    extracted.extend([token, value])
                    seen.add(key)
            index += 2
            continue

        if token.startswith(PREFIX_FLAGS):
            if token.startswith('-D') or token.startswith('-U'):
                define_value = token[2:]
                define_name = define_value.split('=', 1)[0] if define_value else ''
                if define_name in EXCLUDED_DEFINE_NAMES:
                    index += 1
                    continue

            key = ('prefix', token)
            if key not in seen:
                extracted.append(token)
                seen.add(key)
            index += 1
            continue

        if token in SINGLE_FLAGS:
            key = ('single', token)
            if key not in seen:
                extracted.append(token)
                seen.add(key)

        index += 1

    return extracted


def to_define_flags(values):
    define_flags = []
    for value in values:
        if value.startswith('-D'):
            define_flags.append(value)
        else:
            define_flags.append(f'-D{value}')
    return define_flags


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ikos', default='ikos')
    parser.add_argument('--compdb', required=True)
    parser.add_argument('--build-dir', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--define', action='append', default=[])
    return parser.parse_args()


def main():
    args = parse_args()

    build_dir = pathlib.Path(args.build_dir).resolve()
    compdb_path = pathlib.Path(args.compdb)
    source_abs = normalize_path(args.source, build_dir)

    try:
        compdb = load_compdb(compdb_path)
        entry = find_compdb_entry(compdb, source_abs, build_dir)
        tokens = entry_tokens(entry, build_dir)
        preproc_flags = extract_preprocessor_flags(tokens)
    except Exception as error:
        print(f'IKOS helper error: {error}', file=sys.stderr)
        return 1

    ikos_command = [
        args.ikos,
        args.source,
        *preproc_flags,
        *to_define_flags(args.define),
        '-o',
        args.output,
    ]

    process = subprocess.run(ikos_command, cwd=build_dir)
    return process.returncode


if __name__ == '__main__':
    raise SystemExit(main())
