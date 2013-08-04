%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-aws-//' -e 's/-/_/g')
%global channelname pear.amazonwebservices.com

Name:		php-aws-sdk
Version:	1.6.2
Release:	6%{?dist}
Summary:	Amazon Web Services framework for PHP

#The entire source code is ASL 2.0 except lib/cachecore/ and lib/requestcore/ which are BSD and lib/dom/ which is MIT
License:	ASL 2.0 and BSD and MIT
URL:		http://aws.amazon.com/sdkforphp/
Source0:	http://pear.amazonwebservices.com/get/sdk-%{version}.tgz

# integration patches
Patch10:	%{name}-unbundle-sfyaml.diff

BuildArch:	noarch
BuildRequires:	php-pear(PEAR)
BuildRequires:	php-channel(%{channelname})

Requires(post):		%{__pear}
Requires(postun):	%{__pear}

Requires:	php-common >= 5.2
Requires:	php-pear(PEAR)
Requires:	php-channel(%{channelname})
Requires:	php-pdo
Requires:	php-reflection
Requires:	php-spl
Requires:	php-simplexml
Requires:	php-ctype
Requires:	php-curl
Requires:	php-date
Requires:	php-dom
Requires:	php-hash
Requires:	php-json
Requires:	php-libxml
Requires:	php-mbstring
Requires:	php-openssl
Requires:	php-pcre
Requires:	php-session
Requires:	php-sqlite3
Requires:	php-pear(pear.symfony-project.com/YAML)

Provides:	php-pear(%{pear_name}) = %{version}
Provides:	php-pear(%{channelname}/%{pear_name}) = %{version}

%description
Amazon Web Services SDK for PHP enables developers to build solutions for 
Amazon Simple Storage Service (Amazon S3), Amazon Elastic Compute Cloud 
(Amazon EC2), Amazon SimpleDB, and more.


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml

# fix doc roles
sed -e '/_samples/s/role="php"/role="doc"/' \
	-e '/lib\/yaml/d' \
	-e '/sdk.class.php/s/md5sum="[0-9,a-z]\{32\}"//' \
	-e '/_docs/s/role="php"/role="doc"/' \
	-e '/_compatibility_test/s/role="php"/role="doc"/' \
	-e '/_sql/s/role="php"/role="doc"/' \
	-e '/LICENSE/s/role="php"/role="doc"/' \
	-e '/README/s/role="php"/role="doc"/' \
	package2.xml >%{pear_name}-%{version}/%{name}.xml


cd %{pear_name}-%{version}
# unbundle
rm -rf lib/yaml

%patch10


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%if 0%{?rhel}
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*
%else
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*
%endif

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
	%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/AWSSDKforPHP/


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 08 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.2-5
- unbundle sfyaml
- fix requires
- mark doc in package.xml
* Wed May 01 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-4
- Add dependencies
- Add license clarification
* Tue Apr 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-3
- Fix Source, remove empty folder _doc 
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-2
- Fix License, Fix Description, move doc files
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-1
- initial package
