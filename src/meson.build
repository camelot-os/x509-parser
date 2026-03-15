x509_lib_sources = files(
  'x509-parser.c',
  'x509-cert-parser.c',
  'x509-crl-parser.c',
  'x509-common.c',
  'x509-utils.c',
)

pkgconfig = import('pkgconfig')

warning_cflags = []
base_cflags = []

if host_machine.system() != 'none'
base_cflags = warning_cflags + [
  '-pedantic',
  '-fno-builtin',
  '-D_FORTIFY_SOURCE=2',
  '-fstack-protector-strong',
]
else
base_cflags = base_cflags + [
    '-ffreestanding',
    '-fno-builtin',
    '-nostdlib',
    '-fdata-sections',
    '-ffunction-sections',
    '-fno-common',
    ]
endif
lib_shared_link_args = []
if compiler.has_link_argument('-Wl,-z,relro,-z,now')
  lib_shared_link_args += ['-Wl,-z,relro,-z,now']
endif

x509_parser_static = static_library(
  'x509-parser',
  x509_lib_sources,
  include_directories: libx509_inc,
  c_args: base_cflags,
  pic: host_machine.system() != 'none',
  install: true,
)

if host_machine.system() != 'none'
  x509_parser_shared = shared_library(
    'x509-parser',
    x509_lib_sources,
    include_directories: libx509_inc,
    c_args: base_cflags,
    link_args: lib_shared_link_args,
    install: true,
  )
  libx509_link_target = x509_parser_shared
else
  message('Bare-metal target detected: skipping shared library target x509-parser.so.')
  libx509_link_target = x509_parser_static
endif

libx509_dep = declare_dependency(
  include_directories: libx509_inc,
  link_with: libx509_link_target,
)


pkgconfig.generate(
  libx509_link_target,
  name: 'x509-parser',
  filebase: 'x509-parser',
  description: 'X.509 certificate and CRL parser library',
  subdirs: '.',
)

if cli_enabled and not meson.is_cross_build()
  bin_cflags = base_cflags + ['-D_FILE_OFFSET_BITS=64']
  bin_link_args = []

  if compiler.has_link_argument('-Wl,-z,relro,-z,now')
    bin_link_args += ['-Wl,-z,relro,-z,now']
  endif

  executable(
    'x509-parser',
    'main.c',
    include_directories: libx509_inc,
    c_args: bin_cflags,
    link_args: bin_link_args,
    dependencies: libx509_dep,
    pie: true,
  )
elif cli_enabled and meson.is_cross_build()
  message('CLI enabled but cross build detected: skipping x509-parser executable (src/main.c).')
else
  message('CLI disabled: skipping x509-parser executable (src/main.c).')
endif
