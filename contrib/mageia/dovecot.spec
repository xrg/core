%define git_repo dovecot
%define git_head HEAD


%define build_gssapi 1
%define build_ldap 1
%define build_lucene 1
%define build_solr 1
%define build_mysql 1
%define build_pgsql 1
%define build_sqlite 1
%define build_fts 1

%{?_with_gssapi: %{expand: %%global build_gssapi 1}}
%{?_without_gssapi: %{expand: %%global build_gssapi 0}}
%{?_with_ldap: %{expand: %%global build_ldap 1}}
%{?_without_ldap: %{expand: %%global build_ldap 0}}
%{?_with_lucene: %{expand: %%global build_lucene 1}}
%{?_without_lucene: %{expand: %%global build_lucene 0}}
%{?_with_solr: %{expand: %%global build_solr 1}}
%{?_without_solr: %{expand: %%global build_solr 0}}
%{?_with_mysql: %{expand: %%global build_mysql 1}}
%{?_without_mysql: %{expand: %%global build_mysql 0}}
%{?_with_pgsql: %{expand: %%global build_pgsql 1}}
%{?_without_pgsql: %{expand: %%global build_pgsql 0}}
%{?_with_sqlite: %{expand: %%global build_sqlite 1}}
%{?_without_sqlite: %{expand: %%global build_sqlite 0}}

Summary:	Secure IMAP and POP3 server
Name:		dovecot
Version:	%git_get_ver
Release:	%mkrel %git_get_rel2
License:	MIT and LGPLv2 and BSD-like and Public Domain
Group:		System/Servers
URL:		http://dovecot.org
Source:		%git_bs_source %{name}-%{version}.tar.gz
Source1:	%{name}-gitrpm.version
Source2:	%{name}-changelog.gitrpm.txt
Provides:	imap-server pop3-server
Provides:	imaps-server pop3s-server
Requires(post):	systemd >= %{systemd_required_version}
Requires(pre):	rpm-helper >= 0.21
Requires(post):	rpm-helper >= 0.21
Requires(preun): rpm-helper >= 0.21
Requires(postun): rpm-helper >= 0.21
Requires(post):	openssl
# for /etc/ssl/ symlinks
Requires:	rootcerts >= 20121018.00-2.mga3
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
BuildRequires:	libsasl-devel
BuildRequires:	libcap-devel
BuildRequires:	gettext-devel
%if %{build_ldap}
BuildRequires:	openldap2-devel
%endif
%if %{build_lucene}
BuildRequires:	clucene-devel
%endif
%if %{build_solr}
BuildRequires:	expat-devel
BuildRequires:	curl-devel
%endif
%if %{build_mysql}
BuildRequires:	mysql-devel
%endif
%if %{build_pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{build_gssapi}
BuildRequires:	gssglue-devel
BuildRequires:	krb5-devel
%endif
%if %{build_sqlite}
BuildRequires: sqlite3-devel
%endif
%if %{build_fts}
BuildRequires: libicu-devel
%endif
BuildRequires:	rpm-helper >= 0.21
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel

%description
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems, written with
security primarily in mind. Although it's written with C, it uses several
coding techniques to avoid most of the common pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail clients
accessing the mailboxes directly.

You can build %{name} with some conditional build swithes;

(ie. use with rpm --rebuild):

    --with[out] gssapi		GSSAPI support (enabled)
    --with[out] ldap		LDAP support (enabled)
    --with[out] lucene		Lucene support (enabled)
    --with[out] solr		Solr support (enabled)
    --with[out] mysql		MySQL support (enabled)
    --with[out] pgsql		PostgreSQL support (enabled)
    --with[out] sqlite		SQLite support (enabled)

%if %{build_pgsql}
%package plugins-pgsql
Summary:	Postgres SQL backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description plugins-pgsql
This package provides the Postgres SQL backend for dovecot-auth etc.
%endif

%if %{build_mysql}
%package plugins-mysql
Summary:	MySQL backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description plugins-mysql
This package provides the MySQL backend for dovecot-auth etc.
%endif

%if %{build_ldap}
%package plugins-ldap
Summary:	LDAP support for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description plugins-ldap
This package provides LDAP capabilities to dovecot in a modular form.
%endif

%if %{build_gssapi}
%package plugins-gssapi
Summary:	GSSAPI support for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description plugins-gssapi
This package provides GSSAPI capabilities to dovecot in a modular form.
%endif

%if %{build_sqlite}
%package plugins-sqlite
Summary:	SQLite backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description plugins-sqlite
This package provides the SQLite backend for dovecot-auth etc.
%endif

%if %{build_fts}
%package plugins-fts
Summary:        Full Text Search engine for dovecot
Group:          System/Servers
Requires:       %{name} >= %{version}

%description plugins-fts
This package provides FTS engine for dovecot.
%endif

%package devel
Summary:	Development files for Dovecot IMAP and POP3 server
Group:		Development/C
Requires:	%{name} >= %{version}

%description devel
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems, written with
security primarily in mind. Although it's written with C, it uses several
coding techniques to avoid most of the common pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail clients
accessing the mailboxes directly.

This package contains development files for dovecot.

%prep
%git_get_source
%setup -q


%build
%serverbuild
./autogen.sh
%if %{build_lucene}
sed -i '/DEFAULT_INCLUDES *=/s|$| '"$(pkg-config --cflags libclucene-core)|" src/plugins/fts-lucene/Makefile.in
%endif

%configure2_5x \
    --disable-static \
    --with-sql=plugin \
    --with-ssl=openssl \
    --with-nss \
    --without-gc \
    --with-libcap \
%if %{build_ldap}
    --with-ldap=plugin \
%endif
%if %{build_pgsql}
    --with-pgsql \
%endif
%if %{build_mysql}
    --with-mysql \
%endif
%if %{build_sqlite}
    --with-sqlite \
%endif
%if %{build_gssapi}
    --with-gssapi=plugin \
%endif
%if %{build_lucene}
    --with-lucene \
%endif
%if %{build_solr}
    --with-solr \
%endif
    --with-ssldir=%{_sysconfdir}/pki/tls \
    --with-moduledir=%{_libdir}/%{name}/modules \
    --with-rundir=/run/%{name} \
    --with-statedir=%{_localstatedir}/lib/%{name} \
    --with-systemdsystemunitdir=%{_unitdir}

%make


%install
install -d %{buildroot}%{_sysconfdir}/%{name}/conf.d
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_libdir}/%{name}/modules
install -d %{buildroot}%{_localstatedir}/lib/%{name}

%makeinstall_std

cat contrib/mageia/dovecot-pamd > %{buildroot}%{_sysconfdir}/pam.d/%{name}

install -m 644 doc/example-config/%{name}*.conf* %{buildroot}%{_sysconfdir}/%{name}
install -m 644 doc/example-config/conf.d/*.conf* %{buildroot}%{_sysconfdir}/%{name}/conf.d

# Since 2.2, Dovecot tries to listen to IPv4 and IPv6 interfaces by default.
# Dovecot won't start out of the box if IPv6 interface is not present.
# Let's switch to IPv4-only configuration for now.
sed -e "/listen =/ a\listen = *" -i %{buildroot}%{_sysconfdir}/%{name}/dovecot.conf

cp contrib/mageia/migration_wuimp_to_dovecot.pl .
cp contrib/mageia/mboxcrypt.pl .

install -D -p -m 0644 contrib/mageia/dovecot-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf

#  automatic reloading for new plugins
install -d %{buildroot}%{_var}/lib/rpm/filetriggers
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/%{name}.filter << EOF
^.%{_libdir}/%{name}/modules/.*\.so$
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/%{name}.script << EOF
#!/bin/sh
systemctl try-restart %{name}.service
EOF
chmod 755 %{buildroot}%{_var}/lib/rpm/filetriggers/%{name}.script

# remove the libtool archives
find %{buildroot} -name '*.la' -delete

%pre
%_pre_useradd %{name} /var/lib/%{name} /bin/false
%_pre_groupadd %{name} %{name}
%_pre_useradd dovenull /var/lib/%{name} /bin/false
%_pre_groupadd dovenull dovenull

%post
%_tmpfilescreate %{name}
%_post_service %{name}
%_create_ssl_certificate %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name}
%_postun_userdel dovenull
%_postun_groupdel dovenull

%files
%doc AUTHORS COPYING* NEWS README TODO
%doc mboxcrypt.pl migration_wuimp_to_dovecot.pl
%doc %{_docdir}/%{name}

%dir %{_sysconfdir}/dovecot
%dir %{_sysconfdir}/dovecot/conf.d
%config(noreplace) %{_sysconfdir}/dovecot/README
#list all so we'll be noticed if upstream changes anything
%config(noreplace) %{_sysconfdir}/dovecot/dovecot.conf
%config(noreplace) %{_sysconfdir}/dovecot/dovecot-dict-auth.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/dovecot-dict-sql.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/dovecot-ldap.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/dovecot-sql.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-auth.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-director.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-logging.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/11-object-storage.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-mail.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-master.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-ssl.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/15-lda.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/15-mailboxes.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-imap.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-lmtp.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-pop3.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-acl.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-quota.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-plugin.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-checkpassword.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-deny.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-dict.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-ldap.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-master.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-passwdfile.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-sql.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-static.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-system.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-vpopmail.conf.ext

%config(noreplace) %{_sysconfdir}/pam.d/%{name}

%attr(0750,dovecot,dovecot) %dir %{_localstatedir}/lib/%{name}

%{_bindir}/doveadm
%{_bindir}/doveconf
%{_bindir}/dsync
%{_sbindir}/%{name}

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/dovecot-config
%{_libdir}/%{name}/modules
%exclude %{_libdir}/%{name}/modules/libdriver*sql*.so
%exclude %{_libdir}/%{name}/modules/*/libdriver*sql*.so
%{_libdir}/%{name}/libdovecot.so*
%{_libdir}/%{name}/libdovecot-compression.so*
%{_libdir}/%{name}/libdovecot-lda.so*
%{_libdir}/%{name}/libdovecot-login.so*
%{_libdir}/%{name}/libdovecot-sql.so*
%{_libdir}/%{name}/libdovecot-storage.so*
%{_libdir}/%{name}/libdovecot-dsync.so*
%{_libdir}/%{name}/libdcrypt_openssl.so*

%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/aggregator
%{_libexecdir}/%{name}/anvil
%{_libexecdir}/%{name}/auth
%{_libexecdir}/%{name}/checkpassword-reply
%{_libexecdir}/%{name}/config
%{_libexecdir}/%{name}/decode2text.sh
%{_libexecdir}/%{name}/deliver
%{_libexecdir}/%{name}/dict
%{_libexecdir}/%{name}/director
%{_libexecdir}/%{name}/dns-client
%{_libexecdir}/%{name}/doveadm-server
%{_libexecdir}/%{name}/dovecot-lda
%{_libexecdir}/%{name}/gdbhelper
%{_libexecdir}/%{name}/imap
%{_libexecdir}/%{name}/imap-login
%{_libexecdir}/%{name}/imap-urlauth
%{_libexecdir}/%{name}/imap-urlauth-login
%{_libexecdir}/%{name}/imap-urlauth-worker
%{_libexecdir}/%{name}/imap-hibernate
%{_libexecdir}/%{name}/indexer
%{_libexecdir}/%{name}/indexer-worker
%{_libexecdir}/%{name}/ipc
%{_libexecdir}/%{name}/lmtp
%{_libexecdir}/%{name}/log
%{_libexecdir}/%{name}/maildirlock
%{_libexecdir}/%{name}/pop3
%{_libexecdir}/%{name}/pop3-login
%{_libexecdir}/%{name}/quota-status
%{_libexecdir}/%{name}/rawlog
%{_libexecdir}/%{name}/replicator
%{_libexecdir}/%{name}/script
%{_libexecdir}/%{name}/script-login
%{_libexecdir}/%{name}/ssl-params
%{_libexecdir}/%{name}/stats
%{_libexecdir}/%{name}/xml2text

%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_tmpfilesdir}/%{name}.conf

%{_mandir}/man1/doveadm*.1*
%{_mandir}/man1/dovecot*.1*
%{_mandir}/man1/doveconf*.1*
%{_mandir}/man1/deliver.1*
%{_mandir}/man1/dsync.1*
%{_mandir}/man7/doveadm*.7*

%{_var}/lib/rpm/filetriggers/%{name}.*

%dir %{_datadir}/%{name}

%if %{build_ldap}
%files plugins-ldap
%{_libdir}/%{name}/modules/auth/libauthdb_ldap.so
%{_libdir}/%{name}/libdovecot-ldap.so*
%endif

%if %{build_gssapi}
%files plugins-gssapi
%{_libdir}/%{name}/modules/auth/libmech_gssapi.so
%endif

%if %{build_sqlite}
%files plugins-sqlite
%{_libdir}/%{name}/modules/libdriver_sqlite.so
%{_libdir}/%{name}/modules/auth/libdriver_sqlite.so
%{_libdir}/%{name}/modules/dict/libdriver_sqlite.so
%endif

%if %{build_mysql}
%files plugins-mysql
%{_libdir}/%{name}/modules/libdriver_mysql.so
%{_libdir}/%{name}/modules/auth/libdriver_mysql.so
%{_libdir}/%{name}/modules/dict/libdriver_mysql.so
%endif

%if %{build_pgsql}
%files plugins-pgsql
%{_libdir}/%{name}/modules/libdriver_pgsql.so
%{_libdir}/%{name}/modules/auth/libdriver_pgsql.so
%{_libdir}/%{name}/modules/dict/libdriver_pgsql.so
%endif

%if %{build_fts}
%files plugins-fts
%{_datadir}/%{name}/stopwords/stopwords_*.txt
%{_libdir}/%{name}/libdovecot-fts.so*
%endif


%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/%{name}/dovecot-config
%{_datadir}/aclocal/%{name}.m4


%changelog -f %{_sourcedir}/%{name}-changelog.gitrpm.txt
