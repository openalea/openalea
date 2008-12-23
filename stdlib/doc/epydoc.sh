# script to generate the epydoc API of the stdlib package 
# T. Cokelaer 

epydoc --html -o . ../src/openalea/ -v --include-log --show-sourcecode --docformat  restructuredText --parse-only
