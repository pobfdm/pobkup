#
# Regular cron jobs for the pobkup package
#
0 4	* * *	root	[ -x /usr/bin/pobkup_maintenance ] && /usr/bin/pobkup_maintenance
