# vim: sw=4:ts=4:et
#
# Copyright 2013 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

%global base_name katello
%global katello_requires python-iniparse python-simplejson python-kerberos m2crypto python-dateutil
%global locale_dir %{_datarootdir}/locale/
%global homedir %{_datarootdir}/%{base_name}

Name:          %{base_name}-cli
Summary:       Client package for managing application life-cycle for Linux systems
Group:         Applications/System
License:       GPLv2
URL:           http://www.katello.org
Version:       1.5.3
Release:       1%{?dist}
Source0:       https://fedorahosted.org/releases/k/a/katello/%{name}-%{version}.tar.gz
Requires:      %{base_name}-cli-common
BuildArch:     noarch
BuildRequires: pylint
BuildRequires: translate-toolkit
Obsoletes:     katello-cli-headpin < 1.0.1-1
Provides:      katello-cli-headpin = 1.0.1-1

# unit tests
BuildRequires: python-kerberos
BuildRequires: m2crypto
BuildRequires: python-nose
BuildRequires: python-mock

%description
Provides a client package for managing application life-cycle for
Linux systems with Katello

%package common
Summary:       Common Katello client bits
Group:         Applications/System
License:       GPLv2
Requires:      %{katello_requires}
BuildRequires: python2-devel
BuildRequires: gettext
BuildRequires: rpm-python
BuildRequires: /usr/bin/pod2man
BuildRequires: %{katello_requires}

BuildArch:     noarch

%description common
Common classes for katello clients


%package unit-tests
Summary:       Unit tests for Katello client
Group:         Applications/System
License:       GPLv2
Requires:      python-kerberos
Requires:      m2crypto
Requires:      python-nose
Requires:      python-mock
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description unit-tests
Unit tests for Katello client.
For more info see:
https://fedorahosted.org/katello/wiki/TestingHowto

%prep
%setup -q

%build
%if (0%{?fedora} == 18 || 0%{?rhel} == 6) && ! 0%{?fastbuild:1}
    PYTHONPATH=src/ pylint --rcfile=./etc/spacewalk-pylint.rc --additional-builtins=_ katello
%endif

# check for malformed gettext strings
scripts/check-gettext.sh

# generate usage docs and incorporate it into the man page
pushd man
PYTHONPATH=../src python ../scripts/usage.py "katello" >katello-usage.txt
PYTHONPATH=../src python ../scripts/usage.py "headpin" >headpin-usage.txt
sed -e '/^THE_USAGE/{r katello-usage.txt' -e 'd}' katello.pod |\
    sed -e 's/THE_VERSION/%{version}/g' |\
    /usr/bin/pod2man --name=katello -c "Katello Reference" --section=1 --release=%{version} - katello.man1
sed -e '/^THE_USAGE/{r headpin-usage.txt' -e 'd}' headpin.pod |\
    sed -e 's/THE_VERSION/%{version}/g' |\
    /usr/bin/pod2man --name=headpin -c "Headpin Reference" --section=1 --release=%{version} - headpin.man1
sed -e 's/THE_VERSION/%{version}/g' katello-debug-certificates.pod |\
/usr/bin/pod2man --name=katello -c "Katello Reference" --section=1 --release=%{version} - katello-debug-certificates.man1
popd

#check locale file and create locale files
make -C locale check all-mo %{?_smp_mflags}

%install
install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_sysconfdir}/%{base_name}/
install -d %{buildroot}%{python_sitelib}/%{base_name}
install -d %{buildroot}%{python_sitelib}/%{base_name}/client
install -d %{buildroot}%{python_sitelib}/%{base_name}/client/api
install -d %{buildroot}%{python_sitelib}/%{base_name}/client/cli
install -d %{buildroot}%{python_sitelib}/%{base_name}/client/core
install -d %{buildroot}%{python_sitelib}/%{base_name}/client/lib
install -d %{buildroot}%{python_sitelib}/%{base_name}/client/lib/ui
install -d %{buildroot}%{python_sitelib}/%{base_name}/client/lib/utils
install -pm 0644 bin/%{base_name} %{buildroot}%{_bindir}/%{base_name}
install -pm 0644 bin/_complete_%{base_name} %{buildroot}%{_bindir}/_complete_%{base_name}
install -pm 0644 bin/%{base_name}-debug-certificates %{buildroot}%{_bindir}/%{base_name}-debug-certificates
install -pm 0644 etc/client.conf %{buildroot}%{_sysconfdir}/%{base_name}/client.conf
install -Dp -m0644 etc/%{base_name}.completion.sh %{buildroot}%{_sysconfdir}/bash_completion.d/%{base_name}
install -pm 0644 src/%{base_name}/*.py %{buildroot}%{python_sitelib}/%{base_name}/
install -pm 0644 src/%{base_name}/client/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/
install -pm 0644 src/%{base_name}/client/api/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/api/
install -pm 0644 src/%{base_name}/client/cli/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/cli/
install -pm 0644 src/%{base_name}/client/core/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/core/
install -pm 0644 src/%{base_name}/client/lib/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/lib/
install -pm 0644 src/%{base_name}/client/lib/ui/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/lib/ui/
install -pm 0644 src/%{base_name}/client/lib/utils/*.py %{buildroot}%{python_sitelib}/%{base_name}/client/lib/utils/
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -m 0644 man/%{base_name}.man1 %{buildroot}%{_mandir}/man1/%{base_name}.1
install -m 0644 man/headpin.man1 %{buildroot}%{_mandir}/man1/headpin.1
install -m 0644 man/%{base_name}-debug-certificates.man1 %{buildroot}%{_mandir}/man1/%{base_name}-debug-certificates.1

# install locale files
pushd locale
rm -f messages.mo # created by pofilter check
for MOFILE in $(find . -name "*.mo"); do
    DIR=$(dirname "$MOFILE")
    install -d -m 0755 %{buildroot}%{locale_dir}/$DIR/LC_MESSAGES
    install -m 0644 $DIR/*.mo %{buildroot}%{locale_dir}/$DIR/LC_MESSAGES
done
popd
%find_lang %{name}

# several scripts are executable
chmod 755 %{buildroot}%{python_sitelib}/%{base_name}/client/main.py

mkdir -p %{buildroot}%{homedir}/tests/%{name}/unit-tests
cp -ap test/katello %{buildroot}%{homedir}/tests/%{name}/unit-tests
sed -i -e 's|main_path = .*|main_path = "%{python_sitelib}/%{base_name}"|g' %{buildroot}%{homedir}/tests/%{name}/unit-tests/katello/__init__.py

pushd %{buildroot}%{_bindir}
ln -svf %{_bindir}/%{base_name} headpin
popd

%check
pushd test/katello
nosetests
popd

%files -f %{name}.lang
%attr(755,root,root) %{_bindir}/%{base_name}
%attr(755,root,root) %{_bindir}/_complete_%{base_name}
%attr(755,root,root) %{_bindir}/headpin
%attr(755,root,root) %{_bindir}/%{base_name}-debug-certificates
%config(noreplace) %{_sysconfdir}/%{base_name}/client.conf
%{_sysconfdir}/bash_completion.d/%{base_name}
%doc README.md LICENSE
%{_mandir}/man1/%{base_name}.1*
%{_mandir}/man1/headpin.1*
%{_mandir}/man1/%{base_name}-debug-certificates.1*

%files common -f %{name}.lang
%dir %{_sysconfdir}/%{base_name}
%{python_sitelib}/%{base_name}/

%files unit-tests
%{homedir}/tests

%changelog

* Fri Oct 18 2013 Partha Aji <paji@redhat.com> 1.5.3-1
- 1019172: Limiting the keys for puppet module metadata (daviddavis@redhat.com)
- 1018236: Node Sync: Update to support reporting unsuccessful/errors
  (bbuckingham@redhat.com)
- 918157: errata list: fix the listing of errata ID (bbuckingham@redhat.com)
- 986845 - fixing package update all for system (groups) (jsherril@redhat.com)
- Bug #1010339: uploading all repo content before generating metadata.
  (walden@redhat.com)
- modifying cli for new applicability (jsherril@redhat.com)

* Fri Oct 11 2013 Partha Aji <paji@redhat.com> 1.5.1-1
- Bumping package versions for 1.5 (paji@redhat.com)

* Fri Oct 11 2013 Partha Aji <paji@redhat.com> 1.4.4-1
- 1012927 - fixing repo discovery on product create (jsherril@redhat.com)
- 1016624 - fixing issue where system action task result contained array
  instead of string (jsherril@redhat.com)
- 1016312: Improving content upload errors (daviddavis@redhat.com)
- Bug 974098: Adds output of error message to user if an unknown system group
  is supplied when trying to add systems to a group. (ericdhelms@gmail.com)
- 1014747 - CLI 'distributor custom_info' does not exist (komidore64@gmail.com)
- 990478: Filter out marketing products by default (daviddavis@redhat.com)
- 1012978: Preventing error when removing products and repos
  (daviddavis@redhat.com)
- 1013656: Showing a more helpful error message for puppet modules
  (daviddavis@redhat.com)
- 1012572: Check the upload type against the repo's content type
  (daviddavis@redhat.com)
- 1011092: No longer require feed url for repositories (daviddavis@redhat.com)
- 1004248 -  Fixed a get_filter call bug (paji@redhat.com)
- Autobuild f19 packages (paji@redhat.com)
- 955626: Validate rule inclusion/exclusion type (daviddavis@redhat.com)
- 990476: system_group: improve behavior of [add|remove]_systems
  (bbuckingham@redhat.com)
- 1004240 - Removed 'id' on filter create (paji@redhat.com)
- 997364 - removing dep calculation for changesets (jsherril@redhat.com)
- Puppet Uploads: Parse JSON before returning it from puppet utils
  (daviddavis@redhat.com)
- Content Uploads: Worked on tests for directory upload (daviddavis@redhat.com)
- Content uploads: Supporting directories for filepath option
  (daviddavis@redhat.com)
- Moved upload_api defn to ContentUpload class (mtapaswi@redhat.com)
- Content Uploads: Edited comments for utils files (daviddavis@redhat.com)
- Content Uploads: Checking for exceptions and other tweaks
  (daviddavis@redhat.com)
- Fix CLI tests for package uploads (mtapaswi@redhat.com)
- Add python rpm package for travis (mtapaswi@redhat.com)
- Fix CLI tests for package uploads (mtapaswi@redhat.com)
- BZ# 1007128 - Fixes formatting of localized strings. (ogmaciel@gnome.org)
- Content uploads: Puppet module uploading support (daviddavis@redhat.com)
- Package uploads: Got CLI working with API (daviddavis@redhat.com)
- Add Package Upload CLI Support (mtapaswi@redhat.com)
- converting cli to use new repo discovery api (jsherril@redhat.com)
- If running in headpin mode, don't show default_environment option.
  (ogmaciel@gnome.org)
- The logic behind updating users for headpin referred to variable that wasn't
  declared. (ogmaciel@gnome.org)
- Puppet: Adding support for puppet filter rules (daviddavis@redhat.com)
- 1001202 - distributor remove_custom_info command removes the distributor but
  throws an invalid error message (komidore64@gmail.com)
- Repositories: Handling non-yum info for info and list (daviddavis@redhat.com)
- Puppet: Created puppet_module command (daviddavis@redhat.com)
- 879241 - [RFE] [cli] missing "Machine Type" in return of `system subscription
  (komidore64@gmail.com)
- cli node support (jsherril@redhat.com)
- 966263 - ldap mode: cli new user creation mandates unnecessary parameters
  (komidore64@gmail.com)
- 987937 - CLI - empty string as organization name (komidore64@gmail.com)
- Puppet Repos: Wrote a system test for puppet repos (daviddavis@redhat.com)
- headpin-actkey - update act key CLI headpin mode (thomasmckay@redhat.com)
  extra-long-branch-name-of-awesomeness (komidore64@gmail.com)
- 966168 - System custom_info add: Duplicate cli error messages
  (komidore64@gmail.com)
- 973929 - Message after updating custom info for distributor is invalid in cli
  (komidore64@gmail.com)
- Repositories: Added content_type option to repo creation
  (daviddavis@redhat.com)

* Wed Jul 31 2013 Bryan Kearney <bkearney@redhat.com> 1.4.3-1
- Merge pull request #55 from komidore64/org-heal-magic (komidore64@gmail.com)
- Merge pull request #56 from beav/add-get-deleted-consumer-call
  (cduryee@redhat.com)
- Fix rhsm-related system tests (inecas@redhat.com)
- Fix content views handling in system tests (inecas@redhat.com)
- org auto-attach - adding tests (komidore64@gmail.com)
- org auto-attach - attach available subscriptions to all systems within an
  organization (komidore64@gmail.com)
- Merge pull request #57 from parthaa/system-test-fix (parthaa@gmail.com)
- Adding the Update method for Providers to both Headpin and Katello mode.
  (ogmaciel@gnome.org)
- Fix for some system tests (paji@redhat.com)
- add get_deleted_consumers call (cduryee@redhat.com)
- Systems: Fixing tests and more (daviddavis@redhat.com)
- Fixing the activation key system tests (daviddavis@redhat.com)
- Merge pull request #52 from Katello/delete-legacy-promotion
  (daviddavis@redhat.com)
- Initial CLI support for the new About API. (ogmaciel@gnome.org)
- Merge pull request #50 from beav/master (cduryee@redhat.com)
- add last_checkin time to register (cduryee@redhat.com)
- system tests - don't throw away test results (inecas@redhat.com)
- system tests - the usage of packagegroup info changed a bit
  (inecas@redhat.com)
- system tests - skip subscription-manager release --set (inecas@redhat.com)
- system tests - postpone system unregister (inecas@redhat.com)
- Merge pull request #45 from pitr-ch/story/foreign-keys (kontakt@pitr.ch)
- Merge pull request #47 from thomasmckay/980523-user-env
  (thomasmckay@redhat.com)
- system-tests - The environment is needed for RHSM registration
  (inecas@redhat.com)
- 980523-user-env - do not require --default_environment in headpin mode
  (thomasmckay@redhat.com)
- Automatic commit of package [katello-cli-tests] release [1.4.2-1].
  (inecas@redhat.com)
- Fake manifests signed (inecas@redhat.com)
- Merge pull request #42 from daviddavis/task_commands (daviddavis@redhat.com)
- Fix date formatting for BSD (git@pitr.ch)
- 974264 - switch to new search API syntax vs hard coded UUID
  (mmccune@redhat.com)
- Tasks: Added tests for list and status (daviddavis@redhat.com)
- Merge pull request #40 from Katello/bkearney/952236 (bryan.kearney@gmail.com)
- 952236: Null lists or empty lists of systems should show not found to user
  (bkearney@redhat.com)
- Tasks: Worked on show and added list (daviddavis@redhat.com)
- Fixed ContentViewDefinition's 'show' method to return only the json object.
  (ogmaciel@gnome.org)
- Merge pull request #32 from komidore64/dancewalkers (komidore64@gmail.com)
- default_info sync - converting apply to sync (komidore64@gmail.com)
- 969371: Fix a type in the return message (bkearney@redhat.com)
- Merge pull request #39 from jlsherrill/cv_remove (jlsherrill@gmail.com)
- 929067 - content definition remove_view would fail if view was not associated
  (jsherril@redhat.com)
- Content Views: Fixing verbage for add/remove view for definition
  (daviddavis@redhat.com)
- Merge pull request #37 from tstrachota/bug_967467_parse_tokens
  (inecas@redhat.com)
- 967467 - updated regexp for parsing input line in shell mode
  (tstrachota@redhat.com)
- Merge pull request #36 from xsuchy/pull-req-fix-unit-tests
  (miroslav@suchy.cz)
- run unit test in %%check phase (msuchy@redhat.com)
- fix path in production mode (msuchy@redhat.com)
- comment out another failing test in katello_agent (msuchy@redhat.com)
- Merge pull request #33 from xsuchy/pull-req-comment-out (miroslav@suchy.cz)
- comment out failing test (msuchy@redhat.com)
- Merge pull request #31 from pitr-ch/story/foreign-keys (kontakt@pitr.ch)
- Better command and output formatting on failure. (git@pitr.ch)
- Add --pause option (git@pitr.ch)
- Add --services option (git@pitr.ch)
- Escape search query variables (git@pitr.ch)
- Ignore .idea files (git@pitr.ch)
- Fixing errata tests (git@pitr.ch)
- Remove domain tests (git@pitr.ch)
- Merge pull request #30 from daviddavis/temp_1369061847
  (daviddavis@redhat.com)
- Cleaning up and fixing setup.py (daviddavis@redhat.com)
- Updating README (daviddavis@redhat.com)
- Merge pull request #26 from thomasmckay/headpin-lib-cli
  (thomasmckay@redhat.com)
- Merge pull request #27 from komidore64/cores-yo (komidore64@gmail.com)
- pass in installed products on register (cduryee@redhat.com)
- core/ram subs - displaying subscriptions limits (komidore64@gmail.com)
- headpin-lib-cli - remove env edit commands from headpin
  (thomasmckay@redhat.com)
- Merge pull request #16 from jlsherrill/repo-set-fix (bbuckingham@redhat.com)
- Content views: Updating activation key and system options
  (daviddavis@redhat.com)
- CLI: add messages to filter rule creation and deletion, fixes #956151.
  (walden@redhat.com)
- Revert "Revert "Removing legacy promotion path"" (daviddavis@redhat.com)
- Revert "Removing legacy promotion path" (daviddavis@redhat.com)
- Merge pull request #17 from jlsherrill/failed_sync (jlsherrill@gmail.com)
- Merge pull request #22 from thomasmckay/reasons (thomasmckay@redhat.com)
- Merge pull request #20 from parthaa/949937 (parthaa@gmail.com)
- reasons - api call to get subscription status (thomasmckay@redhat.com)
- Merge pull request #18 from daviddavis/temp_1367948119
  (daviddavis@redhat.com)
- Merge pull request #19 from daviddavis/temp_1367951278
  (daviddavis@redhat.com)
- Merge pull request #21 from jlsherrill/all_verbs (jlsherrill@gmail.com)
- 949937 - Modified the order of the params in a permission error
  (paji@redhat.com)
- 955612 - Fixing filter rule example (daviddavis@redhat.com)
- fixes 2065 - adding all_verbs to permission creation (jsherril@redhat.com)
- Added cv options. fixes Katello/katello#2088 (daviddavis@redhat.com)
- Merge pull request #15 from daviddavis/rope (daviddavis@redhat.com)
- fixing issue where failed syncs are not detected (jsherril@redhat.com)
- Ignoring rope files (daviddavis@redhat.com)
- fixes 1777 - adding proper product validation for reposet cli commands
  (jsherril@redhat.com)
- Merge pull request #1 from xsuchy/pull-req-tx-reorg (miroslav@suchy.cz)
- sys-sla - allow passing of empty string for service level
  (thomasmckay@redhat.com)
- Merge pull request #11 from daviddavis/temp_1367580457
  (daviddavis@redhat.com)
- switching to README.md as our readme file (mmccune@redhat.com)
- making pylint happy and adding a return statement (komidore64@gmail.com)
- asynchronous default_info info apply in the CLI (komidore64@gmail.com)
- Merge pull request #10 from daviddavis/temp_1367493317
  (daviddavis@redhat.com)
- Updating README for katello-cli (daviddavis@redhat.com)
- org-sla-cli - allow update of org default service level
  (thomasmckay@redhat.com)
- Removing legacy promotion path (daviddavis@redhat.com)
- Merge pull request #3 from pitr-ch/bug/953524 (kontakt@pitr.ch)
- Merge pull request #9 from tstrachota/api_v2 (martin.bacovsky@gmail.com)
- adding find_by_custom_info to python api (jsherril@redhat.com)
- Merge pull request #6 from daviddavis/temp_1367344162 (daviddavis@redhat.com)
- Ignoring ctags (daviddavis@redhat.com)
- dist-cli - provider refresh_manifest (thomasmckay@redhat.com)
- workaround that "tito tag" does not create correct path in metadata file if
  package is in git-root (msuchy@redhat.com)
- katello-agent is no more in this git repo (msuchy@redhat.com)
- copy nightly scripts from katello.git (msuchy@redhat.com)
- 953524 - CLI synced 'repo status' shows error (git@pitr.ch)
- correct paths in .tx/config after git reorganization (msuchy@redhat.com)
- katello.katello resource is no more in this git (msuchy@redhat.com)
- return back original .tx/config (msuchy@redhat.com)
- Travis - Adding travis config. (ehelms@redhat.com)
- Api V2 - distributors controller added (mbacovsk@redhat.com)
- api v2 - error handling refactored (mbacovsk@redhat.com)

* Sat Apr 27 2013 Mike McCune <mmccune@redhat.com> 1.4.2-1
- adding rel-eng directory for new location (mmccune@redhat.com)
- errata - api/cli - update to use errata_id vs id (bbuckingham@redhat.com)
- 948733 - Worked on content view definition update options
  (daviddavis@redhat.com)
- Errata list should require either repo_id or repo info
  (daviddavis@redhat.com)
- Fixed filters cli to now associate partial products from cvd
  (paji@redhat.com)
- Allowing content views to be deleted from CLI (daviddavis@redhat.com)
- dist-fixes - allow create in headpin mode dist-fixes - renamed SMA to
  distributor splice-api-update - updates to api splice-api-updates - download
  manifest api splice-api-updates - export api splice-api-updates - api for
  /consumers/<id>/checkin (thomasmckay@redhat.com)
- Adding filter id option to CLI (daviddavis@redhat.com)
- Reusing option parser content view function for add_view
  (daviddavis@redhat.com)
- Implementation for add/remove filter rules via cli (paji@redhat.com)
- Updating tests for filter id changes (daviddavis@redhat.com)
- Removing duplicate apis from content view definition CLI
  (daviddavis@redhat.com)
- Querying filters with filter_id rather than filter_name
  (daviddavis@redhat.com)
- 952249 - Validating overlapping content in component views
  (daviddavis@redhat.com)
- 952249 - Validating overlapping content in component views
  (daviddavis@redhat.com)
- 951538 - Fixing CLI publish message (daviddavis@redhat.com)
- 950539 - Adding content view option to package/errata list
  (daviddavis@redhat.com)
- Fixing composite content view smoke test (daviddavis@redhat.com)
* Fri Apr 12 2013 Justin Sherrill <jsherril@redhat.com> 1.4.1-1
- version bump to 1.4 (jsherril@redhat.com)

* Fri Apr 12 2013 Justin Sherrill <jsherril@redhat.com> 1.3.6-1
- 947859 - Created a way to remove views from keys (daviddavis@redhat.com)
- Remove Foreman specific code - cli (inecas@redhat.com)
- 947869 - Allowing users to create composite definitions from CLI
  (daviddavis@redhat.com)
- Rails32 - Fixing copyright years. (ehelms@redhat.com)
- requiring pylint (jsherril@redhat.com)
- removing requirement for spacewalk-pylint (jsherril@redhat.com)
- using our own pylint config, not in /etc (jsherril@redhat.com)
- 929106 - Displaying user friendly task not found error
  (daviddavis@redhat.com)
- waive pylint warning (msuchy@redhat.com)
- 924253 - Fixed definition delete message in CLI (daviddavis@redhat.com)
- fix pylint and add --unprotected to more commands (jsherril@redhat.com)
- manifest-refresh - changes related to refreshing manifest manifest-refresh -
  updates to distributors manifest-refresh - pylint cleaning
  (thomasmckay@redhat.com)
- Addressed some whitespace issues as suggested in PR 1882 (paji@redhat.com)
- adding ability to enable http publishing on a per-repo basis
  (jsherril@redhat.com)
- System groups: allow users to update systems via CLI (daviddavis@redhat.com)
- cli custom_info restructure (komidore64@gmail.com)
- Translations - Download translations from Transifex for katello-cli.
  (jsherril@redhat.com)
- Content Views: allow definitions to be cloned from CLI
  (daviddavis@redhat.com)
- cli now correctly allows you to add custom_info without including a value
  (komidore64@gmail.com)
- Content views: fix filter add_product error (daviddavis@redhat.com)
- cli - fix in import manifest async task (tstrachota@redhat.com)
- custom_info in the UI is now using the API (komidore64@gmail.com)
- Content view: Addressed feedback for filters (daviddavis@redhat.com)
- default info in the UI for systems (komidore64@gmail.com)
- manifest-async - switch to async job on server for CLI/api manifest import
  (thomasmckay@redhat.com)
- Added code to associate product/repos to a filter (paji@redhat.com)
- 918452 - Fixed an issue where cli repo info call was not working
  (paji@redhat.com)
- remove old changelog entries (msuchy@redhat.com)
- Content views: added some system tests (daviddavis@redhat.com)
- i18n - fixing regression in gettext packaging for cli (lzap+git@redhat.com)
- Removing system template code (daviddavis@redhat.com)
- renamed filter to content_filter when the file gets imported to help with
  pylint (paji@redhat.com)
- Intial commit of filters functionality (paji@redhat.com)

* Thu Mar 14 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-1
- large refactor of organization level default system info keys
  (komidore64@gmail.com)
- 917608 - cli - fix activation key update (bbuckingham@redhat.com)
- 917639 - cli - fix changeset update add_repo command (bbuckingham@redhat.com)
- fix pylint error (pchalupa@redhat.com)
- CLI - Adding a requirements file for development dependencies and updating
  Travis config to use. (ehelms@redhat.com)
- fix pylint warnings for travis job (pchalupa@redhat.com)
- CLI - Updates to setup.py to switch to distutils and the inclusion of a
  requirements.pip file for installing into a virtualenv with pip. Fixes
  incorrect inclusion of locale files in setup.py. (ehelms@redhat.com)
- CLI - Updating Spec file for locale changes. (ehelms@redhat.com)
- CLI - Moves locale files to katello-cli namespace for consistency with other
  Linux programs.  Updates Transifex config. (ehelms@redhat.com)
- CLI - Updates the Makefile to properly clean .mo files and removes those
  added by a previous commit. (ehelms@redhat.com)
- CLI - Adds a setup.py file for packaging the CLI for registration on the PyPI
  index. (ehelms@redhat.com)
- CLI - Adds environment variable for setting client conf location.
  (ehelms@redhat.com)
- CLI - Moves each po file into it's own directory to mimic server locale
  structure and that of the standard deployment for locale files.
  (ehelms@redhat.com)
- CLI - Moves po directory to locale for consistency with server and standard
  python projects. (ehelms@redhat.com)
- fixing descriptions and spacing (jsherril@redhat.com)
- allowing the use of repo set name for enable disable (jsherril@redhat.com)
- fast import - migrating cli methods to use evaluate_task_status
  (jsherril@redhat.com)
- attempting to fix odd pylint error (jsherril@redhat.com)
- fast import - adding repo set disable to cli (jsherril@redhat.com)
- cli - evaluation of async task status refactored (tstrachota@redhat.com)
- Content views: worked on some locale strings (daviddavis@redhat.com)
- if we use $FILE, it is very usefull to set it first (msuchy@redhat.com)
- Content views: fix column headers in CLI (daviddavis@redhat.com)
- 869378 - API does not list providedProducts for custom content
  (lzap+git@redhat.com)
- fixing pylint error (jsherril@redhat.com)
- enable pofilter checking on katello-cli (msuchy@redhat.com)
- cs - (pofilter) variables: Do not translate: %%s, %%s (msuchy@redhat.com)
- ru - (pofilter) urls: Different URLs (msuchy@redhat.com)
- check localization files for corectness (msuchy@redhat.com)
- fix Project-Id-Version for cli/po/ml.po (msuchy@redhat.com)
- Content views: add more definition opts to CLI (daviddavis@redhat.com)
- 869581 - Product without repo cannot be promoted (ares@igloonet.cz)
- adding cli support for repo sets (jsherril@redhat.com)
- cli completion - fixed import path to 'fix_io_encoding'
  (tstrachota@redhat.com)
- 880019 - learn optparser how to handle unicode errors (msuchy@redhat.com)
- Added a space to make pylint happy (paji@redhat.com)
- Fixed some broken cli tests (paji@redhat.com)
- Fixed more merge conflicts (paji@redhat.com)
- Cli gettext script (jhadvig@redhat.com)
- fixing usage.py script client.conf reference (jsherril@redhat.com)
- fix incorrect string (msuchy@redhat.com)
- spec changes (tstrachota@redhat.com)
- cli - usage moved (tstrachota@redhat.com)
- cli - import fix for compute resources (tstrachota@redhat.com)
- cli - lib.control (tstrachota@redhat.com)
- cli tests - source path fix (tstrachota@redhat.com)
- cli - lib.async (tstrachota@redhat.com)
- cli - lib.ui.progress (tstrachota@redhat.com)
- cli - lib.util.io (tstrachota@redhat.com)
- cli - lib.util.data (tstrachota@redhat.com)
- cli - lib.ui.formatters (tstrachota@redhat.com)
- cli - printer moved to lib.ui (tstrachota@redhat.com)
- cli - utilities moved to lib (tstrachota@redhat.com)
- merge translation from SAM (msuchy@redhat.com)
- Translations - Download translations from Transifex for katello-cli.
  (msuchy@redhat.com)
- Fixed some merge conflicts (paji@redhat.com)
- hw models - cli refactoring (tstrachota@redhat.com)
- hw models - cli for update (tstrachota@redhat.com)
- hw models - cli for deletion (tstrachota@redhat.com)
- hw models - cli for creation (tstrachota@redhat.com)
- hw models - cli for info (tstrachota@redhat.com)
- hw models - fix for api binding comments (tstrachota@redhat.com)
- hw models - cli for listing (tstrachota@redhat.com)
- Content views: various fixes to UI and CLI (daviddavis@redhat.com)
- Fixed a typo in a cli script (paji@redhat.com)
- Fixed some files missed in previous merges (paji@redhat.com)
- Content views: fixing cli bug from sending org id (daviddavis@redhat.com)
- Content views: supporting async publishing (daviddavis@redhat.com)
- Content views: added opts to the system register test (daviddavis@redhat.com)
- Content views: some things I found preparing for the demo
  (daviddavis@redhat.com)
- Content views: added CLI for systems with content views
  (daviddavis@redhat.com)
- Content views: added some activation key tests (daviddavis@redhat.com)
- Content views: content view can be set on keys in CLI (daviddavis@redhat.com)
- Removing filters from the content view branch (paji@redhat.com)
- Content views: handling new refresh code from CLI/API (daviddavis@redhat.com)
- Content views: api refresh test (daviddavis@redhat.com)
- Content views: refreshing views from the CLI (daviddavis@redhat.com)
- Created CLI command to show tasks' statuses (daviddavis@redhat.com)
- Content views: Added tests for new arguments (daviddavis@redhat.com)
- Content views: fixed tests and feedback for def args (daviddavis@redhat.com)
- Content views: converted method to classmethod (daviddavis@redhat.com)
- Content views: added id and name to cli definition commands
  (daviddavis@redhat.com)
- Content views: added id and name to cv arguments (daviddavis@redhat.com)
- Content views: content view promotion async support (daviddavis@redhat.com)
- Content views: showing repo info in cli (daviddavis@redhat.com)
- Content views: changed dictionary key in cli command (daviddavis@redhat.com)
- Content views: changesets can have views in CLI (daviddavis@redhat.com)
- Content views: removed unused import (daviddavis@redhat.com)
- Content views: handling async view promotion (daviddavis@redhat.com)
- Content views: creating changeset during promotion shortcut
  (daviddavis@redhat.com)
- Content views: added cli promote command (daviddavis@redhat.com)
- Content views: cli info and list work (daviddavis@redhat.com)
- Content views: removing unused import (daviddavis@redhat.com)
- Content views: re-enabled info cli commands (daviddavis@redhat.com)
- Content views: fixed add/remove repo commands (daviddavis@redhat.com)
- fixing bad merge (jsherril@redhat.com)
- Content views: fixing pylint warnings (daviddavis@redhat.com)
- Content views: fixing up cli tests (daviddavis@redhat.com)
- Content views: created nested resources in cli (daviddavis@redhat.com)
- content view - allow publishing to views by giving name/lable/description
  (jsherril@redhat.com)
- Content views: fixed pylint warnings (daviddavis@redhat.com)
- Content views: delete cli test (daviddavis@redhat.com)
- Content views: added CLI tests (daviddavis@redhat.com)
- Content views: created published/unpublished arguments
  (daviddavis@redhat.com)
- Content views: created add_view and remove_view (daviddavis@redhat.com)
- Content views: added env argument to list (daviddavis@redhat.com)
- Content views: fixed product :bug: with cp_id (daviddavis@redhat.com)
- Content views: added repo cli commands (daviddavis@redhat.com)
- Content views: Added add_product for cli (daviddavis@redhat.com)
- Content views: fixed update cli command (daviddavis@redhat.com)
- Content views: added destroy to api controller/cli (daviddavis@redhat.com)
- Content views: Worked on labels and cli (daviddavis@redhat.com)
- Content views: initial setup of models (daviddavis@redhat.com)

* Wed Jan 30 2013 Justin Sherrill <jsherril@redhat.com> 1.3.4-1
- removing pulpv2 prefix from pulpv2 branch (jsherril@redhat.com)
- 880125 - Errors message when no key can be found (ares@igloonet.cz)
- smart proxies - listing available features in cli info
  (tstrachota@redhat.com)
- 875117 - fix in msg when repo not found in CLI (tstrachota@redhat.com)
- 839584 - cli system_group info should show max allowed systems
  (tstrachota@redhat.com)
- comp. res. cli - pylint fixes (tstrachota@redhat.com)
- comp. res. cli - deleting (tstrachota@redhat.com)
- comp. res. cli - updating (tstrachota@redhat.com)
- comp. res. cli - create (tstrachota@redhat.com)
- comp. res. cli - actions list and info (tstrachota@redhat.com)
- cli - case insensitive choices for optparse options (tstrachota@redhat.com)
- 895735 - [RFE] Specifying the keyname when removing custom info from a system
  should be required (komidore64@gmail.com)
- Automatic commit of package [katello-cli] release [1.3.3-1].
  (jsherril@redhat.com)
- Translations - Update .po and POTFILES.in files for katello-cli.
  (jsherril@redhat.com)
- Translations - Download translations from Transifex for katello-cli.
  (jsherril@redhat.com)
- 894480 - remove PyXML dependency (msuchy@redhat.com)
- resolve pylint errors on Fedora 19 (msuchy@redhat.com)
- Revert "Pylint - Updates to remove disablement of pylint warnings present in"
  (msuchy@redhat.com)
- cli completion - fix in sed expression (tstrachota@redhat.com)
- fix config_template info formatting (pchalupa@redhat.com)
- Cli Fix (jhadvig@gmail.com)
- 886462 - [cli] ping returns $? == 30 (but all services are OK)
  (komidore64@gmail.com)
- 853385: Display the environment in the output of system info
  (komidore64@gmail.com)
- fricken pylint (komidore64@gmail.com)
- unifying "blah blah blah [ %%s ]" in CLI" (komidore64@gmail.com)
- 879151, 879161, 879169, 879174, 879195, 880031, 880048, 880054, 880066,
  880073, 880089, 880131, 880566 (komidore64@gmail.com)
- 879151, 879161, 879169, 879174, 879195, 880031, 880048, 880054, 880066,
  880073, 880089, 880131, 880566 (komidore64@gmail.com)
-  Adding environment tests in CLI (jomara@redhat.com)
- fixing zh_TW.po (msuchy@redhat.com)
- fix pt.po (msuchy@redhat.com)
- fix ko.po (msuchy@redhat.com)
- fixing ko.po (msuchy@redhat.com)
- fix zh_CN.po (msuchy@redhat.com)
- update pt.po (msuchy@redhat.com)
- fix ru.po (msuchy@redhat.com)
- fix ja.po (msuchy@redhat.com)
- fix zh_TW.po (msuchy@redhat.com)
- forward port translation from SAM (msuchy@redhat.com)
- Adding environment name change to CLI (jomara@redhat.com)
- 876248: Successful actions should be logged as info, not as errors
  (bkearney@redhat.com)

* Tue Jan 15 2013 Justin Sherrill <jsherril@redhat.com> 1.3.3-1
- Translations - Update .po and POTFILES.in files for katello-cli.
  (jsherril@redhat.com)
- Translations - Download translations from Transifex for katello-cli.
  (jsherril@redhat.com)
- 894480 - remove PyXML dependency (msuchy@redhat.com)
- resolve pylint errors on Fedora 19 (msuchy@redhat.com)
- Revert "Pylint - Updates to remove disablement of pylint warnings present in"
  (msuchy@redhat.com)
- cli completion - fix in sed expression (tstrachota@redhat.com)
- fix config_template info formatting (pchalupa@redhat.com)

* Tue Jan 08 2013 Lukas Zapletal <lzap+git@redhat.com> 1.3.2-1
- Merge pull request #1341 from komidore64/cli-ping
- 886462 - [cli] ping returns $? == 30 (but all services are OK)
- 853385: Display the environment in the output of system info
- fricken pylint
- unifying "blah blah blah [ %%s ]" in CLI" (komidore64@gmail.com)
- 879151, 879161, 879169, 879174, 879195, 880031, 880048, 880054, 880066,
  880073, 880089, 880131, 880566
- Merge pull request #1322 from jsomara/envname
-  Adding environment tests in CLI
- fixing locales
- forward port translation from SAM
- Adding environment name change to CLI
- 876248: Successful actions should be logged as info, not as errors

* Tue Dec 18 2012 Miroslav Suchý <msuchy@redhat.com> 1.3.1-1
- smart proxies - cli CRUD actions (tstrachota@redhat.com)
- cli - packaged completion script (tstrachota@redhat.com)
- cli - python based shell completion (tstrachota@redhat.com)
- Bumping package versions for 1.3. (ehelms@redhat.com)

* Thu Dec 06 2012 Eric D Helms <ehelms@redhat.com> 1.2.2-1
- correcting activation key help message for cli (komidore64@gmail.com)
- Switched to python or (jomara@redhat.com)
- 879245 - optionally displaying uuid instead of name (jomara@redhat.com)
- 879561 - Throw exception if system not found (daviddavis@redhat.com)
- 879320 - removing ipv4 address from system list (jomara@redhat.com)
- 866972 - katello-debug needs to take headpin into consideration
  (komidore64@gmail.com)
- subnet cli - CRUD actions (tomas.str@gmail.com)
- cli utils - fix in unnest_one (tstrachota@redhat.com)
- 875609-hypervisor - allow hypervisors to successfully register and list in
  katello (thomasmckay@redhat.com)
- 874280 - terminology changes for consistency across subman, candlepin, etc
  (jomara@redhat.com)
- Translations - Update .po and POTFILES.in files for katello-cli.
  (ehelms@redhat.com)
- Translations - New translations from Transifex for katello-cli.
  (ehelms@redhat.com)
- Translations - Download translations from Transifex for katello-cli.
  (ehelms@redhat.com)
- simplify code (msuchy@redhat.com)
- code cleanup (msuchy@redhat.com)
- 798675 - display "required" if option is required (msuchy@redhat.com)
- 871622 - correctly set provides and obsoletes (msuchy@redhat.com)
- Revert "871622 - fixing obsoletes to correctly upgrade from katello-cli-
  headpin" (msuchy@redhat.com)
- 871622 - fixing obsoletes to correctly upgrade from katello-cli-headpin
  (jomara@redhat.com)
- 863461 - Headpin Cli automation : Failure to list the org updated with
  special chars other than ascii chars (komidore64@gmail.com)
- fixing pylint error (lzap+git@redhat.com)
- 865528 - improving error handling in the cli code (lzap+git@redhat.com)
- cli - method batch_add_columns applied (tstrachota@redhat.com)
- cli printer - tests and utils (tstrachota@redhat.com)
- 871622 - correctly set version in obsolete (msuchy@redhat.com)
- Pylint - Updates to remove disablement of pylint warnings present in 0.26
  since pylint 0.25 is what is available in Fedora. (ehelms@redhat.com)
- Pylint - Fixes a regex and silences the anonmolous backlash warnings from the
  color declarations in the Spinner. (ehelms@redhat.com)
- CLI Unittest - Fixes issue where CLI unittests couldn't pass on a clean
  system by mocking the get_katello_mode call. (ehelms@redhat.com)
- cli config - fix for missing section in get_katello_mode
  (tstrachota@redhat.com)
- Travis - Adds first pass at a Travis configuration. (ericdhelms@gmail.com)
- 865571 - man page for headpin shows katello context (komidore64@gmail.com)
- 869575 - CLI - changeset - fix error during add/remove repo/pkg/errata
  (bbuckingham@redhat.com)
- 869575 - changeset add_product - correctly handle product request
  (bbuckingham@redhat.com)
- forgot to check with pylint (komidore64@gmail.com)
- 818903 - Name of the pdf generated for headpin system report command should
  be modified (komidore64@gmail.com)
- RAM entitlements (jomara@redhat.com)
- 855267 - fix string issue raised in pull request review
  (bbuckingham@redhat.com)
- 855267 - changeset - moving common logic for product opts to a class method
  (bbuckingham@redhat.com)
- fixing busted cli tests (komidore64@gmail.com)
- 855267 - fix few strings based on pull request review
  (bbuckingham@redhat.com)
- 855267 - CLI - pylint, template and changeset fixes (bbuckingham@redhat.com)
- 855267 - fixes for pylint errors (bbuckingham@redhat.com)
- 859892 - system info contains "u"-s in "OS release" field
  (komidore64@gmail.com)
- 855267 - CLI - updates to changesets based on product chgs
  (bbuckingham@redhat.com)
- 855267 - CLI - updates to errata/package/repo based on product chgs
  (bbuckingham@redhat.com)
- 855267 - CLI add product label and id whereever product name is supported
  (bbuckingham@redhat.com)

* Fri Oct 19 2012 Miroslav Suchý <msuchy@redhat.com> 1.2.1-1
- gettext - fix malformed gettext stings in CLI code (inecas@redhat.com)
- Fix pylint katello.client.core.organization C0301 (inecas@redhat.com)
- default custom info for systems by org (komidore64@gmail.com)
- custom info rework (work it!) (komidore64@gmail.com)
- fix failing system tests (pchalupa@redhat.com)
- domains cli - fix for listing without --order or --search
  (tstrachota@redhat.com)
- cli - pylint fixes (tstrachota@redhat.com)
- manifests - Added delete manifest while in headpin mode (not enabled in
  katello) manifests - fixed 857949
  https://bugzilla.redhat.com/show_bug.cgi?id=857949 (thomasmckay@redhat.com)
- architectures - slice_dict extracted to utils (tstrachota@redhat.com)
- architectures - various cli fixes (tstrachota@redhat.com)
- architectures - cli unit tests (tomas.str@gmail.com)
- 866323 - do not print binary files to log (msuchy@redhat.com)
- Bumping package versions for 1.1. (lzap+git@redhat.com)
- remove old get ext imports (pchalupa@redhat.com)
- Architectures API fix (pajkycz@gmail.com)
- Added test_foreman_record to CLI utils to validate foreman resources
  (pajkycz@gmail.com)
- Added system tests for domains, config templates (pajkycz@gmail.com)
- CLI - rename show->info, destroy->delete (pajkycz@gmail.com)
- Foreman Config Templates improvements (pajkycz@gmail.com)
- Config templates CLI - print template kind (pajkycz@gmail.com)
- Foreman domains added to CLI client (pajkycz@gmail.com)
- Foreman's Config Templates added to CLI client. (pajkycz@gmail.com)
- architectures cli - show action renamed to info to keep naming consistency
  (tomas.str@gmail.com)
- cli - removed mutable types form default param values in Server class
  (tstrachota@redhat.com)
- architectures - CRUD CLI actions (tstrachota@redhat.com)
- cli - util functions for manipulating dicts and options
  (tstrachota@redhat.com)

* Fri Oct 12 2012 Lukas Zapletal <lzap+git@redhat.com> 1.1.10-1
- Merge pull request #846 from lzap/copyright-update
- updating copyrights
- katello-cli-headpin != katello-headpin-cli
- 864372 - CLI - some keys does not work in "shell"
- fixing 'ta' translations
- merge katello.cli translation from CFSE
- Merge pull request #808 from tstrachota/Bug_845198_locale_cannot_be_switched
- 845198 - fixed getlocale locale.getlocale was used with wrong parameter.
  LC_ALL is not allowed. See:
  http://docs.python.org/library/locale.html#locale.getlocale
- removing unused import in cli utils printer.py (komidore64@gmail.com)
- Merge pull request #803 from komidore64/org-list-fail
- Merge pull request #797 from xsuchy/pull-req-raise
- 863461 - Headpin Cli automation : Failure to list the org updated with
  special chars other than ascii chars (komidore64@gmail.com)
- 858960 - always set the utf-8 writer for stdout and stderr
- do not mask original error by raise in exception
- unify string "Couldn't find user role"
- unify string "Couldn't find user"
- unify string "Couldn't find template"
- 857576 - Fixing variable name in filter code
- 857576 - Fixed package code indentation

* Thu Sep 27 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.9-1
- convert string to unicode (msuchy@redhat.com)
- 857576 - Added update filter test (davidd@scimedsolutions.com)
- 857576 - Package filter name can be edited by cli
  (davidd@scimedsolutions.com)
- move custom notes to separate file (msuchy@redhat.com)
- remove duplicate code (msuchy@redhat.com)
- W0104:228,8:GrepStrategy._print_header: Statement seems to have no effect
  (msuchy@redhat.com)
- W0212:135,8:VerboseStrategy._print_header: Access to a protected member
  _println of a client class E0602:135,8:VerboseStrategy._print_header:
  Undefined variable 'self' (msuchy@redhat.com)
- C0301:124,0: Line too long (129/120) C0301:971,0: Line too long (147/120)
  (msuchy@redhat.com)
- if using delimiter, then do not print padding spaces (msuchy@redhat.com)
- do not print first delimiter (msuchy@redhat.com)
- 801560 - correctly calculate length of asian characters (msuchy@redhat.com)
- 845995 - fixing typo (msuchy@redhat.com)
- refresh translations string for katello-cli (msuchy@redhat.com)
- some small python changes (komidore64@gmail.com)
- adding uuid arguments to system's custom info actions in the cli
  (komidore64@gmail.com)
- 858011 - pylint fixes (mmccune@redhat.com)
- removing a couple missed debugger statements (komidore64@gmail.com)
- CustomInfo for Systems (komidore64@gmail.com)
- object labels - fix cli tests broken during addition of object labels
  (bbuckingham@redhat.com)
- 797297 - fix typo (msuchy@redhat.com)
- 845995 - write error is systemgroup does not exist (msuchy@redhat.com)
- object-labels - adding CLI and API calls to support object labeling
  (mmccune@redhat.com)
- 836575 - fix encoding errors when reporting failure messages in CLI
  (inecas@redhat.com)
- Revert "regenerating localization strings for cli" (komidore64@gmail.com)
- regenerating localization strings for cli (komidore64@gmail.com)
- 820634 - Katello String Updates (komidore64@gmail.com)
- handle exception when katello server is down (msuchy@redhat.com)
- update cli source strings of localization (msuchy@redhat.com)
- object-label - organization - rename column cp_key to label
  (bbucking@dhcp231-20.rdu.redhat.com)
- cli - remove unused import (inecas@redhat.com)

* Wed Sep 12 2012 Ivan Necas <inecas@redhat.com> 1.1.8-1
- 837000 - [RFE] when updating sync plan by CLI, it resets the interval.
  (pajkycz@gmail.com)
- 809259 - activation key - cli permissions changes (continued)
  (bbuckingham@redhat.com)
- 809259 - activation key - cli permissions changes (bbuckingham@redhat.com)

* Wed Sep 12 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.7-1
- Fixing provides/obsoletes bug (jomara@redhat.com)
- Removing extra configure code for headpin bin; adding provides to cli script
  for headpin (jomara@redhat.com)
- Fencing headpin CLI into katello cli. CLI will now load appropriate functions
  based on client.conf configuration. Katello cli now ships with headpin
  symlink (jomara@redhat.com)

* Thu Sep 06 2012 Ivan Necas <inecas@redhat.com> 1.1.6-1
- 835591 - usage limit is properly displayed in the list (lzap+git@redhat.com)
- make pylint happy on el6 (msuchy@redhat.com)
- cli - introducing %%{fastbuild} rpm macro use (lzap+git@redhat.com)
- 835591 - usage limit must be higher than 0 (lzap+git@redhat.com)
- cli - pull request review (lzap+git@redhat.com)
- cli refactoring - removing unused code (lzap+git@redhat.com)
- cli refactoring - update_dict_unless_none (lzap+git@redhat.com)
- cli - pull request review (lzap+git@redhat.com)
- fail to build if code contains pylint errors or warnings (msuchy@redhat.com)
- returning back docstring (msuchy@redhat.com)
- code cleanup - class Bytes is not used (msuchy@redhat.com)
- cli - removing unused global variable (lzap+git@redhat.com)
- 853995 - error handling for non-existing systems (lzap+git@redhat.com)
- since AsyncJob is instance of AsyncTask, there is no need for
  wait_for_async_job and we can use wait_for_async_task instead
  (msuchy@redhat.com)
- make _task attribute of instance instead of attribute of class
  (msuchy@redhat.com)
- Simplify AsyncJob by inheriting from AsyncTask (msuchy@redhat.com)
- create __str__() for AsyncJob (msuchy@redhat.com)
- cli - introducing debug log level env variable (lzap+git@redhat.com)
- 851142 - CLI: changeset update shows strange error (pajkycz@gmail.com)
- C0301: 26,0: Line too long (131/120) C0301:390,0: Line too long (135/120)
  (msuchy@redhat.com)
- removing reference to class that was removed (mmccune@redhat.com)
- removing reference to class that was removed (mmccune@redhat.com)
- waive W0221:177,4:KatelloCLI.error: Arguments number differs from overridden
  method (msuchy@redhat.com)
- waive R0904: 20,0:SystemGroupAPI: Too many public methods (21/20)
  (msuchy@redhat.com)
- waive R0904: 18,0:RepoAPI: Too many public methods (21/20 (msuchy@redhat.com)
- waive R0904: 19,0:SystemAPI: Too many public methods (29/20)
  (msuchy@redhat.com)
- waive W0702:478,4:get_term_width: No exception type(s) specified
  (msuchy@redhat.com)
- W0221:483,4:KatelloServer.PUT: Arguments number differs from overridden
  method (msuchy@redhat.com)
- W0221:480,4:KatelloServer.POST: Arguments number differs from overridden
  method (msuchy@redhat.com)
- W0221:474,4:KatelloServer.GET: Arguments number differs from overridden
  method (msuchy@redhat.com)
- W0702:364,8:KatelloServer._process_response: No exception type(s) specified
  (msuchy@redhat.com)
- waive R0904: 39,0:OptionParser: Too many public methods (39/20)
  (msuchy@redhat.com)
- W1201: 51,12:KatelloShell.history_file: Specify string format arguments as
  logging function parameters (msuchy@redhat.com)
- R0904: 30,0:KatelloShell: Too many public methods (21/20) (msuchy@redhat.com)
- W0201:279,12:Cmd.complete: Attribute 'completion_matches' defined outside
  __init__ (msuchy@redhat.com)
- W0703:186,15:Discovery.discover_repositories: Catching too general exception
  Exception (msuchy@redhat.com)
- R0904:170,0:ListAvailableVerbs: Too many public methods (22/20)
  (msuchy@redhat.com)
- R0904:183,0:UpdateContent: Too many public methods (21/20 (msuchy@redhat.com)
- W0611: 25,0: Unused import get_product (msuchy@redhat.com)
- R0904:272,0:Update: Too many public methods (26/20) (msuchy@redhat.com)
- remove false statement (msuchy@redhat.com)
- R0201: 35,4:EnvironmentAction.get_prior_id: Method could be a function
  (msuchy@redhat.com)
- W0622:503,12:Errata.run: Redefining built-in 'id' (msuchy@redhat.com)
- W0622:460,12:Packages.run: Redefining built-in 'id' (msuchy@redhat.com)
- C0301:331,0: Line too long (122/120) C0301:407,0: Line too long (122/120)
  C0301:409,0: Line too long (122/120) C0301:411,0: Line too long (145/120)
  C0301:413,0: Line too long (126/120) C0301:415,0: Line too long (126/120)
  C0301:417,0: Line too long (124/120) C0301:484,0: Line too long (124/120)
  (msuchy@redhat.com)
- R0201:233,4:ShowSubscriptions.convert_timestamp: Method could be a function
  R0201:239,4:ShowSubscriptions.extract_sla_from_product: Method could be a
  function (msuchy@redhat.com)
- R0201: 53,4:DateTimeFormatter.local_timezone: Method could be a function
  (msuchy@redhat.com)
- W0621: 42,35:DateTimeFormatter.build_datetime: Redefining name 'time' from
  outer scope (line 18) (msuchy@redhat.com)
- W0621: 39,28:DateTimeFormatter.contains_zone: Redefining name 'time' from
  outer scope (line 18) (msuchy@redhat.com)
- W0621: 36,25:DateTimeFormatter.date_valid: Redefining name 'time' from outer
  scope (line 18) (msuchy@redhat.com)
- W0621: 33,25:DateTimeFormatter.time_valid: Redefining name 'time' from outer
  scope (line 18) (msuchy@redhat.com)
- W0232: 24,0:DateTimeFormatter: Class has no __init__ method
  (msuchy@redhat.com)
- R0201: 35,4:ActivationKeyAction.get_template_id: Method could be a function
  (msuchy@redhat.com)
- C0301: 62,0: Line too long (126/120) C0301:233,0: Line too long (144/120)
  (msuchy@redhat.com)
- waive Method could be a function (msuchy@redhat.com)
- waive unused arguments (msuchy@redhat.com)
- W0702:387,12:BaseAction.main: No exception type(s) specified
  (msuchy@redhat.com)
- R0201:342,4:BaseAction.load_saved_options: Method could be a function
  (msuchy@redhat.com)
- W0702:278,8:Command._extract_command: No exception type(s) specified
  (msuchy@redhat.com)
- R0201:257,4:Command.__build_command_usage_lines: Method could be a function
  (msuchy@redhat.com)
- R0201:214,4:Action.__process_option_errors: Method could be a function
  (msuchy@redhat.com)
- waive unused arguments (msuchy@redhat.com)
- C0301:333,0: Line too long (179/120) C0301:335,0: Line too long (172/120)
  (msuchy@redhat.com)
- W0611: 19,0: Unused import Command (msuchy@redhat.com)
- simplify code (msuchy@redhat.com)
- R0201: 86,4:Status.__sortedStatuses: Method could be a function R0201:
  93,4:Status.__buildOverallStatusDetail: Method could be a function R0201:
  99,4:Status.__buildServiceStatusDetail: Method could be a function
  (msuchy@redhat.com)
- waive W0612: 70,12:Status.__returnCode: Unused variable 'serviceName'
  (msuchy@redhat.com)
- R0201: 39,4:SyncPlanAction.parse_datetime: Method could be a function
  (msuchy@redhat.com)
- C0301:115,0: Line too long (127/120) C0301:118,0: Line too long (147/120)
  C0301:150,0: Line too long (127/120) (msuchy@redhat.com)
- R0201:289,4:Promote.create_cs_name: Method could be a function
  (msuchy@redhat.com)
- rename isMarketingProduct to isNotMarketingProduct to avoid confusion of
  future generations (msuchy@redhat.com)
- W0702:159,16:List.run.isMarketingProduct: No exception type(s) specified
  (msuchy@redhat.com)
- W0622:132,8:List.run: Redefining built-in 'all' (msuchy@redhat.com)
- R0201: 58,4:SingleProductAction.set_product_select_options: Method could be a
  function R0201: 64,4:SingleProductAction.check_product_select_options: Method
  could be a function (msuchy@redhat.com)
- C0301: 29,0: Line too long (135/120) C0301:228,0: Line too long (134/120)
  C0301:248,0: Line too long (124/120) C0301:308,0: Line too long (121/120)
  C0301:312,0: Line too long (128/120) C0301:314,0: Line too long (158/120)
  (msuchy@redhat.com)
- W0201:354,8:Update.resetParameters: Attribute 'items' defined outside
  __init__ (msuchy@redhat.com)
- W0201:291,8:Update.store_from_product: Attribute 'current_product' defined
  outside __init__ (msuchy@redhat.com)
- R0201:418,4:Update.productNamesToIds: Method could be a function
  R0201:429,4:Update.repoNamesToIds: Method could be a function
  (msuchy@redhat.com)
- waive unused arguments (msuchy@redhat.com)
- R0201:223,4:Export.open_file: Method could be a function (msuchy@redhat.com)
- W0702:211,8:Export.run: No exception type(s) specified (msuchy@redhat.com)
- W0622:204,8:Export.run: Redefining built-in 'format' (msuchy@redhat.com)
- R0201:177,4:Import.open_file: Method could be a function (msuchy@redhat.com)
- W0702:167,8:Import.run: No exception type(s) specified (msuchy@redhat.com)
- R0201:125,4:Info._build_nvrea: Method could be a function (msuchy@redhat.com)
- R0201: 39,4:TemplateAction.get_parent_id: Method could be a function
  (msuchy@redhat.com)
- C0301:171,0: Line too long (129/120) C0301:193,0: Line too long (123/120)
  C0301:215,0: Line too long (133/120) C0301:311,0: Line too long (137/120)
  C0301:313,0: Line too long (155/120) C0301:314,0: Line too long (123/120)
  C0301:317,0: Line too long (124/120) C0301:319,0: Line too long (146/120)
  C0301:320,0: Line too long (152/120) C0301:323,0: Line too long (123/120)
  C0301:325,0: Line too long (132/120) C0301:327,0: Line too long (141/120)
  C0301:329,0: Line too long (147/120) C0301:400,0: Line too long (134/120)
  (msuchy@redhat.com)
- correctly use pylint: disable (msuchy@redhat.com)
- 746765 - systems can be referenced by uuid (lzap+git@redhat.com)

* Fri Aug 31 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.5-1
- code style fixes (msuchy@redhat.com)
- 847858 - only remove act keys when resource not found error
  (thomasmckay@redhat.com)

* Wed Aug 29 2012 Ivan Necas <inecas@redhat.com> 1.1.4-1
- evironment is now stored to environment variable instead env
  (msuchy@redhat.com)
- fix unit tests (msuchy@redhat.com)
- add to path correct search location (msuchy@redhat.com)
- package unit tests (msuchy@redhat.com)
- Available subscriptions on systems page now allow filtering matching what is
  available in subscription-manager-gui (thomasmckay@redhat.com)
- waive pylint R0201: 43,4:KatelloShell.history_file: Method could be a
  function (msuchy@redhat.com)
- Revert "declare method as function" (msuchy@redhat.com)
- waive pylint R0201: 30,4:KatelloAPI.server: Method could be a function
  (msuchy@redhat.com)
- Revert "R0201: 30,4:KatelloAPI.server: Method could be a function"
  (msuchy@redhat.com)
- 845198 - do not fail with 'C' locale (msuchy@redhat.com)
- 845198 - set locale even in usage.py to allow building (msuchy@redhat.com)
- 845198 - receive translation from gettext as unicode (msuchy@redhat.com)
- fixing various unit tests from content deletion and param unification
  (mmccune@redhat.com)
- stylecheck fixes (msuchy@redhat.com)
- there is no option -environment in this action (msuchy@redhat.com)
- 848038 - installing localisation files for cli (tstrachota@redhat.com)
- 850790 - Content promotion from CLI no longer works (lzap+git@redhat.com)
- 798679 - Read correct argument (msuchy@redhat.com)
- fix incorrect argument (msuchy@redhat.com)
- 798679 - be consistent with --environment option help (msuchy@redhat.com)
- 798679 - be consistent with --org option help (msuchy@redhat.com)
- 798679 - remove duplicate code handling --product option (msuchy@redhat.com)
- 798679 - be consistent with --product option help (msuchy@redhat.com)
- 846321: Support creating permissions for all tags from the API and the cli
  (bkearney@redhat.com)
- 845995: Add local and server side checks for passing in bad group names and
  ids (bkearney@redhat.com)
- 771186 - katello ak info now shows aks (lzap+git@redhat.com)
- 845198 - always use utf-8 as output encoding (tomas.str@gmail.com)
- 845198 - enable setting locale via LC_ALL in cli (tomas.str@gmail.com)

* Thu Aug 23 2012 Mike McCune <mmccune@redhat.com> 1.1.3-1
- 850935 - katello-cli-common should own only /etc/katello and not its content
  (msuchy@redhat.com)
- 795520 - modifying manual page (lzap+git@redhat.com)
- 795520 - removing unused variable (lzap+git@redhat.com)
- 795520 - adding support of noheading cli option (lzap+git@redhat.com)
- Merge pull request #436 from omaciel/userlocale (mmccune@gmail.com)
- Validation of locale during update handled by model. (ogmaciel@gnome.org)
- Allow user to update his/her own localevia cli. Also, output the default
  locale when using the info parameter. (ogmaciel@gnome.org)
- Added --default_locale to CLI for user creation. (ogmaciel@gnome.org)
- Fixed some merge conflicts (paji@redhat.com)
- content deletion - proper deletion support in the CLI (mmccune@redhat.com)
- content deletion - adding back in the CLI promote and apply
  (mmccune@redhat.com)
- content deletion - removing hard coded type (mmccune@redhat.com)
- content deletion - adding CLI actions (mmccune@redhat.com)

* Thu Aug 16 2012 Lukas Zapletal <lzap+git@redhat.com> 1.1.2-1
- 822926 - katello-cli-common now owns config dir
- 822926 - fixing incorrect license in a header

* Sat Aug 11 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-1
- cli docs - removed version from config (tomas.str@gmail.com)
- cli - Config inicialization moved to functions It was causing problems in
  test when we tried to init it at include time. Unused Config inits were
  removed. (tstrachota@redhat.com)
- cli doc - added docs for cli generator (tstrachota@redhat.com)
- cli doc - first version of sphinx documentation (tstrachota@redhat.com)
- buildroot and %%clean section is not needed (msuchy@redhat.com)
- Bumping package versions for 1.1. (msuchy@redhat.com)

* Tue Jul 31 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-1
- bump up version to 1.0 (msuchy@redhat.com)
- update copyright years (msuchy@redhat.com)
- point Source0 to fedorahosted.org where tar.gz are stored (msuchy@redhat.com)

* Wed Jul 25 2012 Miroslav Suchý <msuchy@redhat.com> 0.2.45-1
- 840531 - Fixes issue with inability to individually promote packages attached
  to a system template or changeset that have more than a single dash in the
  name. (ehelms@redhat.com)
- 817845 - updating katello man page entry (adprice@redhat.com)

* Mon Jul 23 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.44-1
- system groups - API accepts max_systems and CLI unit tests
- system groups - wrong variable name in error message
- system groups - removing local modifications not intended for upstream
- group copy cli and API first pass

* Mon Jul 16 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.43-1
- 798323 - remove double setting of UTF decoder
- system groups - removing the 'locked' feature from system groups UI/API/CLI
- system groups - update errata list cli based on pull request feedback
- system groups - api/cli - add ability to list errata by group
- cli - fix for url options not allowing file:// and ftp://

* Mon Jul 02 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.42-1
- system groups - cli - fix broken test
- system groups - cli - creating a group should default max systems to
  unlimited
- system groups - cli - add description to the AsyncJob
- system groups - cli - split history in to 2 actions per review feedback
- system groups - api/cli to support errata install
- system groups - remove unused code from package action CLI
- system groups - api/cli to support package and package group actions

* Mon Jun 25 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.41-1
- ulimit - brad's review
- BZ 825262: support for moving systems between environments from CLI
- ulimit - fixing cli makefile for unit tests
- ulimit - backend api and cli
- system groups - cli/api - provide user option to delete systems when deleting
  group
- cli - updated makefile and readme to mirror the latest changes in cli
  unittests.

* Mon Jun 18 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.40-1
- Updates for broken cli unit tests that were a result of re-factoring work
  previously done.
- system groups - api - include total system count in system group info
- system group cli - removed excess lines
- cli - fix for printing version on -v option
- cli unit tests - tests splitted into packages and modules
- 822484 - cli - sync_plan list traceback
- cli - pep8 fixes
- cli - action base class renamed
- cli - usage script modified to use command container
- cli - auth methods extracted form server class
- cli - fixed shell completion and line preprocessing
- cli - katello cli turned to new-style command
- cli - unittests fixed after introduction of new option types
- cli - allow to use only user config file
- 818726 - updated i18n translations
- cli - new option types - url and list
- 818726 - update to both ui and cli and zanata pushed

* Fri Jun 01 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.39-1
- system grops - a few fixes for history cli
- cli - None check in date_formatter + enabled system test for deleting filters
- system groups - adding group history to cli
- cli - adding log file location to traceback error
- 821644 - cli admin crl_regen command - unit and system test
- 822926 - katello-cli package fedora review - fix

* Fri May 25 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.38-1
- 822926 - katello-cli package fedora review
- Fixed typo s/fing/find. Fixes BZ #824749.
- system groups - Updates for help text around options that take lists and
  command naming for adding groups to a system.
- 795525 - renaming cli column name 'subscriptions'
- system groups - Updates the system groups CLI work to be consistent with re-
  factoring work.
- system groups - merge conflict
- system groups - Updates to not require max_systems on creation in CLI.
- Two minor tweaks to output strings for removing systems from a system group.
- system groups - Adds the maximum systems paramter for CLI create/update.
- system groups - Cleans up CLI code to fit re-factoring changes from master.
- system groups - Adds CLI support for add/remove of a system group from an
  activation key.
- system groups - Clean up CLI code around adding systems to a system group
- system group - Adds CLI/API support for adding and removing system groups
  from a system
- system groups - Adds support for removing systems from a system group in CLI.
- system groups - Adds support for adding systems to a system group in the CLI
- Adds system group basic update support for the CLI
- system group - Adds system group delete to CLI.
- system group - Adds system group creation support to CLI.
- system group - Adds support for locking and unlocking a system group in the
  CLI
- system groups - Adds CLI support for listing systems in a system group.
- system groups - Adds ability to view info of single system group from CLI.
- system-groups - Adds CLI system group basics and calls to list system groups
  for a given organization.

* Thu May 24 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.37-1
- 824069 - adding new parameter --all to cli product list
- cli - workaround for error when action was not found This commit fixes error
  "object has no attribute 'parser'" appearing after attempt to call a non-
  existing action. The error is gone but classes Command and KatelloCLI need
  more cleanup. There's redundant code and they touch each other's
  responsibility.
- cli - fix for missing section 'options' client.conf Some versions of
  OptionParser throw error when you try to iterate items from non-existing
  section.
- cli validator - complete unit tests
- cli - validator and parser moved from class to local variables This helps the
  code to be more testable.
- cli - fix for wrong param validation in system register
- cli - CLITestCase divided into two classes
- cli - unit tests for required options simplified
- cli - methods for validation extracted from cli Action

* Fri May 18 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.36-1
- rpm review - katello-cli review preparation

* Fri May 18 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.35-1
- cli registration regression with aks

* Thu May 17 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.34-1
- cli_man - katello(1) man page and generator
- Changing wording for hypervisor deletion record delete
- 812891 - Adding hypervisor record deletion to katello cli
- product status cli - fix for key error Formatting moved to printer that
  checks whether the key exist prior to printing it.

* Thu May 10 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.33-1
- cli - pep8 fixes - code reidentation - trailing spaces removal - unused
  imports removed
- cli - fixes in unit tests
- cli - removal of redundant code
- task list cli - print part refactored Duplicit lines removed and changed to
  use new style printer.
- cli - new method for testing success of a record creation
- cli - api util methods changed to raise exceptions instead of returning None
  when a record was not found. This allows us to remove the ubiquitous checks
  for None value from action bodies.
- systems cli - actions use new api util method get_system
- systems cli - method get_environment moved out from system api class
- Added cli tests for ldap_roles
- Added mocks for ldap_group api call
- 808172 - Added code to show version information for katello cli
- systems - cli for listing systems for a pool_id

* Fri Apr 27 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.32-1
- Fixed addColumn to match new name
- Fixing various LDAP issues from the last pull request
- Loading group roles from ldap
- 767925 - search packages command in CLI/API

* Tue Apr 24 2012 Petr Chalupa <pchalupa@redhat.com> 0.2.31-1
- katello-cli, katello - setting default environment for user

* Thu Apr 19 2012 Tomas Strachota <tstrachota@redhat.com> 0.2.30-1
- cli - fixed wrong formatters used for product and repo last sync time

* Thu Apr 19 2012 Tomas Strachota <tstrachota@redhat.com> 0.2.29-1
- periodic-build
* Wed Apr 18 2012 Petr Chalupa <pchalupa@redhat.com> 0.2.28-1
- 812842 - complete removal of skipping None values in verbose print strategy
- 741595 - uebercert POST/GET/DELETE - either support or delete the calls from
  CLI

* Tue Apr 17 2012 Tomas Strachota <tstrachota@redhat.com> 0.2.27-1
- 812842 - fix for cli printer skipping values that are evaluated as False
- 798918 - Headpin cli unregister doesn't have environment option

* Fri Apr 13 2012 Tomas Strachota <tstrachota@redhat.com> 0.2.26-1
- cli - documentation strings for printer
- cli - output formatters in printer
- cli - fix for method set_output_mode removed from Printer
- cli - printer refactored to enable more output modes
- cli - printer class moved out from utils.py into separate file

* Thu Apr 12 2012 Ivan Necas <inecas@redhat.com> 0.2.25-1
- cp-releasever - release as a scalar value in API system json
- 769302 - CLI `system register` needs enhancement

* Wed Apr 11 2012 Petr Chalupa <pchalupa@redhat.com> 0.2.24-1
- 713153 - RFE: include IP information in consumers/systems related API calls.
- 768243 - Error msg needs to be improved

* Tue Apr 10 2012 Tomas Strachota <tstrachota@redhat.com> 0.2.23-1
- slas - all cli options --service_level renamed to --servicelevel

* Fri Apr 06 2012 Tomas Strachota <tstrachota@redhat.com> 0.2.22-1
- slas - field for SLA in hash export of consumer renamed We used service_level
  but subscription-manager requires serviceLevel and checks for it's presence.
* Wed Apr 04 2012 Petr Chalupa <pchalupa@redhat.com> 0.2.21-1
- 798649 - RFE - Better listing of products and repos

* Mon Apr 02 2012 Lukas Zapletal <lzap+git@redhat.com> 0.2.20-1
- cleanup - removing unused imports and variables
- 744199 - cli now reports all errors to stderr
