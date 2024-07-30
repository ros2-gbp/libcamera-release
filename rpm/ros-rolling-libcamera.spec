%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-libcamera
Version:        0.3.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS libcamera package

License:        LGPL-2.1
URL:            https://libcamera.org
Source0:        %{name}-%{version}.tar.gz

Requires:       libatomic
Requires:       libudev-devel
Requires:       libyaml-devel
Requires:       openssl-devel
Requires:       python%{python3_pkgversion}-devel
Requires:       ros-rolling-ros-workspace
BuildRequires:  libatomic
BuildRequires:  libudev-devel
BuildRequires:  libyaml-devel
BuildRequires:  meson
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  pybind11-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-yaml
BuildRequires:  python3-jinja2
BuildRequires:  python3-ply
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
An open source camera stack and framework for Linux, Android, and ChromeOS

%prep
%autosetup -p1

%build
# override macro
%define __meson_auto_features auto
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
# call meson executable instead of using the 'meson' macro to use default paths
%__meson setup \
    --prefix="/opt/ros/rolling" \
    --cmake-prefix-path="/opt/ros/rolling" \
    --libdir=lib \
    --libexecdir=lib \
    %{_target_platform}
%meson_build -C %{_target_platform}

%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    %{_builddir}/src/ipa/ipa-sign-install.sh %{_builddir}/%{name}-%{version}/%{_vpath_builddir}/src/ipa-priv-key.pem %{buildroot}/%{_libdir}/libcamera/ipa_*.so \
%{nil}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%meson_install -C %{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__ninja -C %{_target_platform} -t targets | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%meson_test -C %{_target_platform} || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Tue Jul 30 2024 Christian Rauch <Rauch.Christian@gmx.de> - 0.3.1-1
- Autogenerated by Bloom

* Fri May 24 2024 Christian Rauch <Rauch.Christian@gmx.de> - 0.3.0-3
- Autogenerated by Bloom

* Tue May 21 2024 Christian Rauch <Rauch.Christian@gmx.de> - 0.3.0-2
- Autogenerated by Bloom

* Tue May 21 2024 Christian Rauch <Rauch.Christian@gmx.de> - 0.3.0-1
- Autogenerated by Bloom
