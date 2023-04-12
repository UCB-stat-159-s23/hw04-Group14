. ONESHELL:
SHELL = /bin/bash

env : 
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml
	conda activate notebook
	conda install ipykernel
	python -m ipykernel install --user --name make-env --display-name "IPython - Make"


html:
	mkdir audio
	mkdir figures
	jupyter-book create mybook/
	jupyter-book config sphinx .
	sphinx-build . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000


.PHONY : clean
clean : 
	rm -f audio/*
	rm -f figures/*
	rm -f _build/*