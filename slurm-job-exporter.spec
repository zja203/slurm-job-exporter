Name:	  slurm-job-exporter
Version:  0.0.1
Release:  1%{?dist}
Summary:  Prometheus exporter for stats in slurm accounting cgroups

License:  Apache License 2.0
URL:      https://github.com/BCH-High-Performance-Computing/%{name}
# Define ref to the tag with the same name as the package version if not defined from commandline
# ref can be any reference known to git like a commit hash, branch name, tag, etc
%{!?ref: %global ref v%{version}}
Source0:  https://github.com/BCH-High-Performance-Computing/%{name}/archive/%{ref}/%{name}-%{ref}.tar.gz

BuildArch:      noarch
BuildRequires:	systemd
Requires:       python3
Requires:       python3-psutil
Requires:       python3-py3nvml

%description
Prometheus exporter for the stats in the cgroup accounting with slurm. This can also collect stats of a job using NVIDIA GPUs.

%prep
%setup -q -T -c -n %{name}-%{ref}
cd %{_builddir}/%{name}-%{ref}
tar xf %{_sourcedir}/%{name}-%{ref}.tar.gz --strip-components=1

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}

sed -i -e '1i#!/usr/libexec/platform-python' slurm-job-exporter.py
install -m 0755 %{name}.py %{buildroot}/%{_bindir}/%{name}
install -m 0744 get_gpus.sh %{buildroot}/%{_bindir}/get_gpus.sh
install -m 0644 slurm-job-exporter.service %{buildroot}/%{_unitdir}/slurm-job-exporter.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_bindir}/get_gpus.sh
%{_unitdir}/slurm-job-exporter.service

# The prometheus-client python library doesn't seem to have an official rpm package
%post
pip3 install prometheus-client==0.9.0
