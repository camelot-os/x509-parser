project('x509-parser', 'c',
  meson_version: '>=1.1.0',
  default_options: [
    'c_std=c11',
    'warning_level=3',
    'optimization=s',
    'default_library=static',
    'b_pie=false',
    'b_staticpic=false',
    'pkgconfig.relocatable=true',
    ],
    license: 'GPL-2.0-or-later',
    license_files: ['LICENSE'],
)

compiler = meson.get_compiler('c')
cli_enabled = get_option('cli')
ikos_enabled = get_option('ikos')
proof_enabled = get_option('proof')

compiler.check_header('stdint.h')
compiler.check_header('string.h')
compiler.check_header('unistd.h')

if not meson.is_cross_build() and cli_enabled
    compiler.check_header('stdio.h')
    compiler.check_header('stdlib.h')
    compiler.check_header('sys/stat.h')
    compiler.check_header('sys/mman.h')
    compiler.check_header('fcntl.h')
    compiler.check_header('errno.h')
endif

subdir('include')
subdir('src')

proof_test_enabled = proof_enabled and not meson.is_cross_build()

if proof_test_enabled
    subdir('proof')
elif proof_enabled and meson.is_cross_build()
    message('Proof enabled but cross build detected: skipping Frama-C proof test.')
endif

summary(
    {
        'cli': cli_enabled,
        'ikos': ikos_enabled,
                'proof': proof_test_enabled,
    },
    bool_yn: true,
    section: 'Targets',
)
