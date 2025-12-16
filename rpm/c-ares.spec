%undefine __cmake_in_source_build

Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.34.6
Release: 1
License: MIT
URL: https://github.com/sailfishos/c-ares
Source0: %{name}-%{version}.tar.bz2
BuildRequires: cmake
BuildRequires: libstdc++-devel
BuildRequires: pkgconfig(gmock)

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

%build
%cmake . \
    -DCARES_BUILD_TOOLS:BOOL=OFF \
    -DCARES_BUILD_TESTS:BOOL=ON \
    -Wno-dev

%cmake_build

%install
%cmake_install

%check
%ctest

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_dns_record.h
%{_includedir}/ares_nameser.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_libdir}/cmake/c-ares/

%files doc
%license LICENSE.md
%doc README.md
%{_mandir}/man3/ares_*
