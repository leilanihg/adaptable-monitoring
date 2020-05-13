First, get the air policy reasoner to run the code.
1.  Get the code from https://github.mit.edu/dig/air-demo-dhs-2015
2.  Get rdflib (pip install pdflib)
3.  Try to run the generic reasoner with a car example:
python <PATH TO AIR DEMO CODE BASE>/air-demo-dhs-2015/reasoners/latest/tmswap/policyrunner.py test <PATH TO ADAPTABLE-MONITOR>/rules/car-rules.n3 <ABSOLUTE FILE PATH TO ADPATABLE MONITOR>/logs/car-log.n3 > out.n3
  ex: python reasoners/latest/tmswap/policyrunner.py test /Users/lgilpin/workspace/monitors/adaptable/rules/car-rules.n3 file:///Users/lgilpin/workspace/monitors/adaptable/logs/car-log.n3 

Note - the last input (the log file) MUST be an absolute path.
