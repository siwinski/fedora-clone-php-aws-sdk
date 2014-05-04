%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-aws-//' -e 's/-/_/g')
%global channelname pear.amazonwebservices.com

Name:		php-aws-sdk
Version:	2.6.1
Release:	1%{?dist}
Summary:	Amazon Web Services framework for PHP

License:	ASL 2.0
URL:		http://aws.amazon.com/sdkforphp/
Source0:	http://pear.amazonwebservices.com/get/sdk-%{version}.tgz

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
Requires:	php-Monolog
Requires:	php-Monolog-dynamo
Requires:	php-symfony-yaml
Requires:	php-guzzle-Guzzle >= 3.7.0
Requires:	php-guzzle-Guzzle < 3.9.0
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
        -e '/sdk.class.php/s/md5sum="[0-9,a-z]\{32\}"//' \
        -e '/_docs/s/role="php"/role="doc"/' \
        -e '/_compatibility_test/s/role="php"/role="doc"/' \
        -e '/_sql/s/role="php"/role="doc"/' \
        -e '/LICENSE/s/role="php"/role="doc"/' \
        -e '/README/s/role="php"/role="doc"/' \
        package2.xml >%{pear_name}-%{version}/%{name}.xml

%build
# Empty build section, most likely nothing required.

%install

cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm $RPM_BUILD_ROOT%{pear_phpdir}/AWSSDKforPHP/aws.phar
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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/AWSSDKforPHP/


%changelog
* Sun May 04 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.6.1-1
- Update to latest upstream release
* Sun Mar 16 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.3-1
- Update to latest upstream release
* Fri Feb 21 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.2-1
- Update to latest upstream release
* Fri Jan 03 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-5
- Remove the aws.phar with other uneaded files on %%install
* Fri Jan 03 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-4
- Keep the aws.phar file for workaround on install
* Thu Jan 02 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-3
- Fix file installation
* Mon Dec 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-2
- add php-Monolog-dynamo dependency
- update naming on dependency php-symfony-yaml
- fix max version require on guzzle dependency
* Sun Dec 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-1
- update to latest upstrean version
* Mon Nov 18 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.10-1
- update to latest upstream version
- add php-symfony2-Yaml(version2) and php-Monolog
- remove dependency php-symfony2-YAML(version1)
- set version contraint for php-guzzle-Guzzle dependency
* Mon Sep 09 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.5-2
- add guzzle dependency.
- remove aws.phar file
* Thu Sep 05 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.5-1
- Update to 2.4.5
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
