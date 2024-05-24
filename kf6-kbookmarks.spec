#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.2
%define		qtver		5.15.2
%define		kfname		kbookmarks

Summary:	Web browser bookmark management
Name:		kf6-%{kfname}
Version:	6.2.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	348c46a5e1ce5e215a0be89296df242b
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcodecs-devel >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kconfigwidgets-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf6-kxmlgui-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	kf5-%{kfname} < %{version}
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	Qt6Xml >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kcodecs >= %{version}
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kconfigwidgets >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
Requires:	kf6-kxmlgui >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KBookmarks lets you access and manipulate bookmarks stored using the
XBEL format: http://pyxml.sourceforge.net/topics/xbel/

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Obsoletes:	kf5-%{kfname}-devel < %{version}
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	Qt6Xml-devel >= %{qtver}
Requires:	cmake >= 3.16
Requires:	kf6-kwidgetsaddons-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF6Bookmarks.so.*.*
%ghost %{_libdir}/libKF6Bookmarks.so.6
%attr(755,root,root) %{_libdir}/libKF6BookmarksWidgets.so.*.*
%ghost %{_libdir}/libKF6BookmarksWidgets.so.6
%{_datadir}/qlogging-categories6/kbookmarks.categories
%{_datadir}/qlogging-categories6/kbookmarks.renamecategories
%{_datadir}/qlogging-categories6/kbookmarkswidgets.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KBookmarks
%{_includedir}/KF6/KBookmarksWidgets
%{_libdir}/cmake/KF6Bookmarks
%{_libdir}/libKF6Bookmarks.so
%{_libdir}/libKF6BookmarksWidgets.so
