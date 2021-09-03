Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.17.2
Release: 1
License: MIT
URL: http://c-ares.haxx.se/
Source0: %{name}-%{version}.tar.bz2
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: libstdc++-devel

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%package doc
Summary: Documentation for c-ares
BuildArch: noarch

%description doc
This package contains documentation of the c-ares.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

# Only run offline tests
sed -e '/ares-test-live.cc/d'  -i test/Makefile.inc

f=CHANGES ; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
%cmake \
    -DCARES_BUILD_TOOLS:BOOL=OFF \
    -DCARES_BUILD_TESTS:BOOL=ON \
    -B build \
    -Wno-dev \
    -S .

%make_build -C build

%install
cd build
%make_install

%check
# Make sure we pick up c-ares that we just build instead of
# the one from the system
export LD_LIBRARY_PATH=$PWD/build/%{_lib}
%__make -C build/test test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_libdir}/cmake/c-ares/

%files doc
%license LICENSE.md
%doc README.cares CHANGES NEWS
%{_mandir}/man3/ares_*
