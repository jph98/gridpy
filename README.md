Grid.py
=======

Grid.py provides a simple grid monitoring interface for viewing queue/job information.  

Requirements
------------

Grid.py is based on:
* Python 2.7.1

Grid.py was tested with the following:
* Sun Grid Engine 6.2 update 7

You will need to have the grid engine binaries (qstat, qacct etc...) on your PATH in order
for Grid.py to parse output.  

Future Plans
------------

Supprt for 
* IBM LSF (Load Sharing Facility) - http://www-03.ibm.com/systems/technicalcomputing/platformcomputing/products/lsf/index.html
* Torque Resource Manager - http://www.adaptivecomputing.com/products/open-source/torque/
* Condor - http://research.cs.wisc.edu/condor/
* Microsoft HPC
