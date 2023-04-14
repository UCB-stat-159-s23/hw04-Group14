## Makefile to create environment, build JupyterBook, and clean for this repository 

.ONESHELL:
SHELL = /bin/bash

## create_environment : creates an environment
.PHONY : envs
envs : 
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml
	conda activate makeLigo
	conda install ipykernel
	python -m ipykernel install --user --name makeLigo --display-name "IPython - Make"


## html : builds jupyterbook
.PHONY : html
html:
	jb build .

## clean : removes audio, figure, and _build directories
.PHONY : clean
clean : 
	rm -f audio/*
	rm -f figures/*
	rm -r _build/*