. ONESHELL:
SHELL = /bin/bash

## env : create environment
.PHONY : env
env : 
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml
	conda activate notebook
	conda install ipykernel
	python -m ipykernel install --user --name make-env --display-name "IPython - Make"

## html : builds jupyterbook
.PHONY : html
html:
	mkdir audio
	mkdir figures
	jb build .
	cd _build/html
	python -m http.server

## clean : removes audio, figure, and _build directories
.PHONY : clean
clean : 
	rm -f audio/*
	rm -f figures/*
	rm -f _build/*