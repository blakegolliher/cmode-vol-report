#!/usr/local/python-2.7.2/bin/python
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
from math import log

sys.path.append("/var/local/netapp-manageability-sdk-5.1/lib/python/NetApp")
from NaServer import *

password = getpass.getpass()

filer_name = sys.argv[1]

## Thanks internet!
## http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB'], [0, 0, 1, 2, 2])
def sizeof_fmt(num):
    """Human friendly file size"""
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'

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
	print 'Volume Size	 : %s ' % sizeof_fmt(int(volsizeattrs.child_get_string('size')))
	print 'Volume Size Avail : %s ' % sizeof_fmt(int(volsizeattrs.child_get_string('size-available')))
	print '---------------------------------'
