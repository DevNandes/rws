# ABSTRACT: Acoes no rws
#

.PHONY: all run_dev run_test run_pd push deploy install deploy_test commit push_image help

CONTAINER ?= rws
APP_ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# target: all - Executa o container de Desenv
all: run_dev


# target: run_dev - Executa o container name=rws, port=3071, type=dev, image=rws:latest, mem=20
run_dev:
	exec $(APP_ROOT_DIR)/scripts/host/run_container.sh -n rws -p 3071 -t dev -m 20 -i rws:latest

# target: push_image - Copia a imagem para um host remoto
push_image: guard-user guard-host
	rsync -v /home/renault/images/rws.tar.gz $(user)@$(host):/home/renault/images/


# target: deploy - Copia o conteudo relevante do diretorio APP_ROOT_DIR para um host remoto
deploy: guard-user guard-host
	$(APP_ROOT_DIR)/scripts/host/deploy_app.sh -u $(user) -h $(host)


# target: install - Instala os packages necessarios
install:
	docker exec $(CONTAINER) $(APP_ROOT_DIR)/scripts/container/install_packages.sh


# target: push - Push para os repositorios remotos do Git (especificar branch)
push:
	git push local $(branch)
	git push github $(branch)


# target: guard-% - Aborta se a variavel especificada nao estiver definida
guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Variavel $* indefinida"; \
		exit 1; \
	fi


# target: help - Mostra os targets que sao executaveis
help:
	@egrep "^# target:" [Mm]akefile
	
# target: commit - Executa 'git add .', 'git commit -a', 'make push'
commit:
	git add .
	git commit -a
	git push local $(branch)
	-git push bitbucket $(branch)
	git status

# EOF