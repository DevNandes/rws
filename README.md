# DESCRIPTION

API da RenaultRisk.

## CONFIGURACAO DO AMBIENTE DOCKER

As secoes seguintes detalham a criacao da imagem Docker e do container.

### CRIACAO DA IMAGEM

Foi criada uma imagem com todas as dependencias pre-instaladas.
Esta imagem pode ser carregada em qualquer computador que tenha o Docker instalado.
A rotina abaixo descreve o processo para as intalacoes dos softwares e a criacao da imagem.

```bash

# Este passo aqui NAO deve ser executado em estacoes com configuracoes antigas (centos) >>>>
sudo mkdir /home/renault
sudo chown -R cir38:cir38 /home/renault # Ajuste conforme o usuario
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

cd /home/renault
git clone [URL] #
cd /home/renault/rws/

# Dirs
sudo /home/renault/rws/scripts/host/create_dirs.pl

# Criacao da imagem
docker build -t rws:latest .

# Sobe o container
make run_dev

# Importante: utilizar o id do container nos comandos commit
docker commit --message='Install packages' $(docker ps -aqf "name=rws") rws:latest

docker images
mkdir /home/renault/images
docker save rws:latest | gzip > /home/renault/images/rws.tar.gz

docker image inspect -f {{.Config.Cmd}} rws:latest
docker image history rws:latest

```

### CRIACAO DO CONTAINER

```bash

# Na estacao DEV  >>>>>>>
ssh-copy-id USER@HOST
ssh USER@HOST
# <<<<<<<<<<<<<<<<<<<<<<<

# Na estacao de destino >>>>>>>>>>>>>>>>>>>>>>>>
sudo mkdir -p /home/renault/images
sudo mkdir -p /home/renault/rws
sudo chown -R $USER:$USER /home/renault/rws
sudo chmod -R 0775 /home/renault/rws
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Na estacao DEV >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
cd /home/renault/rws
make push_image user=USER host=HOST  # USER / HOST na estacao remota
make deploy user=USER host=HOST      # USER / HOST na estacao remota
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# A partir daqui, as acoes devem ser executadas na estacao remota de destino
docker load < /home/renault/images/rws.tar.gz
docker images
docker ps -a

cd /home/renault/rws

# Dirs
sudo /home/renault/rws/scripts/host/create_dirs.pl

# Coloca app para rodar
make run_dev

# Em outro terminal...
docker ps
docker stats # Conferir a memoria
ss -tulnap | grep 3071

# Log: logrotate
sudo cp /home/renault/rws/etc/logrotate.d/rws /etc/logrotate.d/
sudo chmod 0644 /etc/logrotate.d/rws
sudo logrotate -d /etc/logrotate.d/rws
sudo logrotate /etc/logrotate.d/rws

# Firewall
# Debian / Ubuntu
sudo ufw allow 3070/tcp
sudo ufw allow 3073/tcp
sudo ufw status verbose

```

## TESTES

```bash

curl 'http://127.0.0.1:3070/documents/datasheet/departments'
curl --cacert /home/renault/nx/etc/certs/CA.crt 'https://127.0.0.1:3073/documents/datasheet/departments'

```


## TODO

- Configuracoes para escalabilidade

https://pythonspeed.com/articles/gunicorn-in-docker/
gunicorn --workers=2 --threads=4 --worker-class=gthread 

https://www.digitalocean.com/community/tutorials/how-to-scale-and-secure-a-django-application-with-docker-nginx-and-let-s-encrypt
