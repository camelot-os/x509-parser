.SUFFIXES:

MESON ?= meson

BUILD_DIR ?= build-meson
BUILD_DIR_PROOF ?= build-meson-proof
BUILD_DIR_IKOS ?= build-meson-ikos

PROOF_SESSION := $(BUILD_DIR_PROOF)/proof/frama-c-rte-eva-then-wp.session
IKOS_DATABASE := $(BUILD_DIR_IKOS)/src/ikos.db

.PHONY: all clean frama-c frama-c-gui ikos ikos-gui

all:
	$(MESON) setup $(BUILD_DIR) -Dcli=true -Ddefault_library=both
	$(MESON) compile -C $(BUILD_DIR)

clean:
	@rm -rf $(BUILD_DIR) $(BUILD_DIR_PROOF) $(BUILD_DIR_IKOS)
	@find -name '*~' -exec rm -f '{}' \;

frama-c:
	$(MESON) setup $(BUILD_DIR_PROOF) -Dproof=true
	$(MESON) test -C $(BUILD_DIR_PROOF) frama-c

ikos:
	$(MESON) setup $(BUILD_DIR_IKOS) -Dikos=true
	$(MESON) compile -C $(BUILD_DIR_IKOS) ikos

ikos-gui:
	ikos-view $(IKOS_DATABASE)
