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

summary(
    {
        'cli': cli_enabled,
    },
    bool_yn: true,
    section: 'Targets',
)
