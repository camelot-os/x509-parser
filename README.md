# x509-parser project

## Copyright and license
Copyright (C) 2022-2026

This software is licensed under a dual BSD and GPL v2 license.
See [LICENSE](LICENSE) file at the root folder of the project.

## Authors

  * Arnaud EBALARD (<mailto:arnaud.ebalard@ssi.gouv.fr>)

## Contributors

  * Ryad BENADJILA (<mailto:ryad.benadjila@ssi.gouv.fr>)
  * Patricia MOUY (<mailto:patricia.mouy@ssi.gouv.fr>)
  * H2Lab Development Team (<mailto:bureau@h2lab.org>)

## Description

This software implements a X.509 certificate parser, annotated using
ACSL annotations for verification with Frama-C (version 18/Argon).

## Building

The main [Makefile](Makefile) is in the root directory, and compiling is
as simple as executing:

<pre>
	$ make
</pre>

This will compile different elements in the [build](build/) directory:

  * the `x509-parser` binary, which can be used on a DER certificate (or
    a concatenation of such elements)
  * the static and shared libraries (`x509-parser.a` and `x509-parser.so`)

### Building with Meson

Meson support is also available.

Native build (libraries only, by default):

<pre>
	$ meson setup builddir
	$ meson compile -C builddir
</pre>

Enable the CLI binary (`src/main.c`) in native mode:

<pre>
	$ meson setup builddir-cli -Dcli=true
	$ meson compile -C builddir-cli
</pre>

Cross build with a Meson cross file (libraries only):

<pre>
	$ meson setup builddir-cross --cross-file your-cross-file.ini
	$ meson compile -C builddir-cross
</pre>

In cross mode, only the library targets are built. The `x509-parser` binary
from `src/main.c` is intentionally restricted to native builds.

For bare-metal targets (`system = 'none'` in the cross file), Meson builds the
static library only.

Install libraries, headers and pkg-config metadata:

<pre>
	$ meson install -C builddir
</pre>

Meson installs `x509-parser.pc` in the platform `pkgconfig` directory
(`$libdir/pkgconfig`).

Example usage:

<pre>
	$ pkg-config --cflags --libs x509-parser
</pre>

### Meson options

| Option | Default | Description |
| --- | --- | --- |
| `cli` | `false` | Build the `x509-parser` executable from `src/main.c` (native builds only). |
| `ikos` | `false` | Enable the Meson `ikos` target that generates `ikos.db` from `src/x509-parser.c` (native builds only). |
| `proof` | `false` | Enable the Meson Frama-C proof test (native builds only). |

Public headers are in `include/x509` and must be included using:

<pre>
	#include &lt;x509/x509-parser.h&gt;
</pre>

## Validating

The main [Makefile](Makefile) has targets to run several static analyzers.

### Frama-C

To verify the project with [Frama-C](https://frama-c.com/), use the `frama-c`
target:

<pre>
	$ make frama-c
</pre>

Equivalent Meson test:

<pre>
	$ meson setup builddir-proof -Dproof=true
	$ meson test -C builddir-proof frama-c
</pre>

The Meson proof test passes the generated `compile_commands.json` directly to
Frama-C.

Frama-C must have been installed prior to calling that target. Installing
Frama-C can be done using OPAM. More details can be found on
[Frama-C](https://frama-c.com/) project website. Frama-C may also be
available as a common package on your distribution.

### IKOS

To verify the project with [IKOS](https://github.com/NASA-SW-VnV/ikos), use the
`ikos` target:

<pre>
	$ make ikos
</pre>

Equivalent Meson target:

<pre>
	$ meson setup builddir-ikos -Dikos=true
	$ meson compile -C builddir-ikos ikos
</pre>

IKOS must have been installed prior to calling that target.
See the [installation instructions](https://github.com/NASA-SW-VnV/ikos/tree/master/doc/install).
