## Makefile to build JupyterBook for this repository 

. ONESHELL:
SHELL = /bin/bash

## create_environment : create environment
.PHONY : create_environment
create_environment : 
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml
	conda activate notebook

## update_environment : install ipykernel and create kernel
.PHONY : update_environment 
update_environment :
	conda install ipykernel
	python -m ipykernel install --user --name make-env --display-name "IPython - Make"


## html : builds jupyterbook
.PHONY : html
html:
	mkdir audio
	mkdir figures
	jb build .

## clean : removes audio, figure, and _build directories
.PHONY : clean
clean : 
	rm -f audio/*
	rm -f figures/*
	rm -f _build/*