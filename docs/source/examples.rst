Example LTOP creation
=====================

The LTOP workflow can be run from the run_ltop_complete.py script or it can be instantiated 
from elsewhere with the following code: 

``example = RunLTOPFull(params.params,max_time = 60)``       
``example.runner()``

where params.params is the result of import params and then referencing the dictionary inside the module. This means that one could also 
do something like:    
``from run_ltop_complete import Run LTOPFull``

This call to the RunLTOPFull class will kick of the entire LTOP workflow. The max_time argument is optional and has a default of 
1200 seconds set in the class. This will be changed in future versions or can be overriden.