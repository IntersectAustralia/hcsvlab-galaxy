Configuration and tool wrappers for the HCSvLab Galaxy instance.

TO CONFIGURE GALAXY
-------------------
change __GALAXY_PORT__ to the desired port in <galaxy-dist>/universe_wsgi.ini
change MCRROOT in <galaxy-dist>/tools/psysound/run_psysound3Compiled.sh to point to your installed MCR (version v716 required)

TO START GALAXY
---------------
cd <galaxy-dist>
./galaxy start

TO STOP GALAXY
--------------
cd <galaxy-dist>
./galaxy stop

see github documents for more information: https://github.com/IntersectAustralia/hcsvlab-docs
