DIST_VERSIONS = el8 el9

RPM_BUILD_FLAGS = --define "dist .$@"
SPECTOOL_BUILD_FLAGS =

ifdef REF
    RPM_BUILD_FLAGS += --define "ref ${REF}"
    SPECTOOL_BUILD_FLAGS += --define "ref ${REF}"
endif

.PHONY: all
all: ${DIST_VERSIONS}

${DIST_VERSIONS}:
	spectool -g -R ${SPECTOOL_BUILD_FLAGS} slurm-job-exporter.spec
	rpmbuild ${RPM_BUILD_FLAGS} -ba slurm-job-exporter.spec
