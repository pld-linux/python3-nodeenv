#
# Conditional build:
%bcond_with	tests	# unit tests

%define		module	nodeenv
Summary:	Node.js virtual environment builder
Summary(pl.UTF-8):	Narzędzie do budowania środowisk wirtualnych Node.js
Name:		python3-%{module}
Version:	1.9.1
Release:	3
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.debian.net/nodeenv/%{module}-%{version}.tar.gz
# Source0-md5:	48e8369f9770952639e51f41366f651d
URL:		https://pypi.org/project/nodeenv/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nodeenv (node.js virtual environment) is a tool to create isolated
node.js environments.

%description -l pl.UTF-8
nodeenv (środowisko wirtualne node.js) to narzędzie do tworzenia
izolowanych środowisk node.js.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README.rst
%lang(ru) %doc README.ru.rst
%attr(755,root,root) %{_bindir}/nodeenv
%{py3_sitescriptdir}/nodeenv.py
%{py3_sitescriptdir}/__pycache__/nodeenv.cpython*.py[co]
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
