#!

LOCPATH=$(pwd)
rm -Rf dist
mkdir dist

for DIR in core visualea deploy deploygui stdlib sconsx openalea_meta
do
cd $DIR &&
rm -Rf build &&
rm -Rf dist &&
python setup.py bdist_egg -d ../dist sdist -d ../dist --format=gztar 
rm -Rf build &&
cd $LOCPATH
echo $LOCPATH
done
