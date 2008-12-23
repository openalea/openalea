# script to generate the epydoc API of the  visualea package 
# T. Cokelaer 

epydoc --html -o . ../src/visualea/ -v --include-log --show-sourcecode --docformat  restructuredText --parse-only
