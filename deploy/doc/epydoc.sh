# script to generate epydoc API
# t.Cokelaer
epydoc --html -o doc ../src/openalea/deploy -v --include-log --show-sourcecode --docformat  restructuredText --parse-only
