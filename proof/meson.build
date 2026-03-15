frama_c = find_program('frama-c', required: true, native: true)
nproc = find_program('nproc', required: false, native: true)

frama_wp_jobs = '1'
if nproc.found()
  nproc_result = run_command(nproc, check: false)
  if nproc_result.returncode() == 0
    detected_jobs = nproc_result.stdout().strip()
    if detected_jobs != ''
      frama_wp_jobs = detected_jobs
    endif
  endif
endif

frama_timeout = '30'
frama_session = join_paths(meson.current_build_dir(), 'frama-c-rte-eva-then-wp.session')
frama_compdb = join_paths(meson.project_build_root(), 'compile_commands.json')

frama_sources = [
  join_paths(meson.project_source_root(), 'proof/entrypoint_cert.c'),
  join_paths(meson.project_source_root(), 'src/x509-utils.c'),
  join_paths(meson.project_source_root(), 'src/x509-common.c'),
  join_paths(meson.project_source_root(), 'src/x509-crl-parser.c'),
  join_paths(meson.project_source_root(), 'src/x509-cert-parser.c'),
  join_paths(meson.project_source_root(), 'src/x509-parser.c'),
]

framac_gen_opts = [
  '-machdep', 'x86_64',
  '-pp-annot',
  '-json-compilation-database', frama_compdb,
  '-cpp-extra-args=-I' + join_paths(meson.project_source_root(), 'include'),
]

framac_rte_eva_opts = [
  '-warn-left-shift-negative',
  '-warn-right-shift-negative',
  '-warn-signed-downcast',
  '-warn-signed-overflow',
  '-warn-unsigned-downcast',
  '-warn-unsigned-overflow',
  '-rte',
  '-then',
  '-eva',
  '-wp-dynamic',
  '-eva-slevel', '1',
  '-eva-warn-undefined-pointer-comparison', 'none',
  '-then',
]

framac_wp_opts = [
  '-wp',
  '-wp-steps', '100000',
  '-wp-dynamic',
  '-wp-no-init-const',
  '-wp-par', frama_wp_jobs,
  '-wp-timeout', frama_timeout,
]

test(
  'frama-c',
  frama_c,
  args: [
    frama_sources,
    framac_gen_opts,
    framac_rte_eva_opts,
    framac_wp_opts,
    '-save', frama_session,
  ],
  env: {
    'FRAMAC_SESSION': frama_session,
  },
  suite: 'proof',
  timeout: 0,
  is_parallel: false,
)
