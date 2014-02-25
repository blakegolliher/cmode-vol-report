#!/usr/bin/python
##
#
# A simple volume report
# Using netapp API and Python
# Should work just like vollist.pl
# Included in Ontap sample sources
#
# Blake Golliher - blakegolliher@gmail.com
#
##

import sys, string, os, getpass

usage = """
Usage: ./cmode-vol-report.py filername
e.g ./cmode-vol-report.py cmode-filer.mud.yahoo.com

"""


sys.path.append("/var/local/netapp-manageability-sdk-5.1/lib/python/NetApp")

from NaServer import *
if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

filer_name = sys.argv[1]

password = getpass.getpass()

def readable_size(size):
    for unit in ['bytes','KB','MB','GB','TB']:
        if size < 1000.0 and size > -1000.0:
            return "%3.2f %s" % (size, unit)
        size /= 1000.0
    return "%3.2f %s" % (size, 'PB')

filer = NaServer(filer_name,1,6)
filer.set_admin_user('admin', password)
cmd = NaElement('volume-get-iter')

out = filer.invoke_elem(cmd)

if(out.results_status() == "failed"):
        print "%s failed." % filer_name
        print(out.results_reason() + "\n")
        sys.exit(2)

if(out.child_get_int("num-records") == "0"):
        print "%s failed." % filer_name
        print "no volumes found.\n"
        sys.exit(2)

print '\n%s : Volume Report : \n' % filer_name

vollist = dict()
vollist = out.child_get('attributes-list')

for volattr in vollist.children_get():
	volstateattrs = dict()
	volstateattrs = volattr.child_get('volume-state-attributes')

for volstateattr in vollist.children_get():
	volsizeattrs = dict()
	volsizeattrs = volstateattr.child_get('volume-space-attributes')

for vol in vollist.children_get():
	volattrs = dict()
	volattrs = vol.child_get('volume-id-attributes')
	print 'VServer Name 	 : %s ' % volattrs.child_get_string('owning-vserver-name')
	print 'Volume Name 	 : %s ' % volattrs.child_get_string('name')
	print 'Aggregate Name 	 : %s ' % volattrs.child_get_string('containing-aggregate-name')
	print 'Volume Type	 : %s ' % volattrs.child_get_string('type')
	print 'Volume State 	 : %s ' % volstateattrs.child_get_string('state')
	print 'Volume Size	 : %s ' % readable_size(int(volsizeattrs.child_get_string('size')))
	print 'Volume Size Avail : %s ' % readable_size(int(volsizeattrs.child_get_string('size-available')))
	print '---------------------------------'
