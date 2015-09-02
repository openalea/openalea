#!/bin/bash
NAME=$1
conda create --name $NAME --file openalea.yaml
source activate $NAME
pip install -r requirements_openalea.txt
default_env=`conda info --envs | grep "*"`
env_path=`python -c "name, _, path = \"${default_env}\".split(); print(path)"`

cd ../../deploy
python setup.py install

alea_config --install-dyn-lib=${env_path}/lib


mv ~/.openalea.sh ${env_path}/



conda list --export

uninstall system nose
conda install nose
pip install nose
