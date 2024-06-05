#!/bin/bash
#
# ABSTRACT: Script para executar o container rws
#
# - Parte do principio que os diretorios para os volumes ja estao criados
# - Cria os named volumes adequadamente (dev, test ou pd)
#
# Porque convinha que aquele, por cuja causa e por quem todas as coisas
# existem, conduzindo muitos filhos a gloria, aperfeicoasse, por meio de
# sofrimentos, o Autor da salvacao deles. Hebreus 2.10

# Functions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

function main () {    


    # Parameters >>>>>>>>>>>
    container_type="$1"
    container_memory="$2"
    image_name="$3"
    run_policy="$4"
    port="$5"
    container_name="$6"
    # <<<<<<<<<<<<<<<<<<<<<<<


    host_name=$(hostname)
    app_root_dir=$(get_root_dir)

    if [ ! -e "$app_root_dir" ]; then
        echo "ERRO: Nao encontrou o dir ROOT: ${app_root_dir}"
        exit 1
    fi

    docker inspect --type=image $image_name
    if [ "$?" != "0" ]; then
        echo "ERRO: Imagem ${image_name} nao localizada..."
        exit 1
    fi

    nr='/nr/rws'
    volumes='/volumes/rws'
    memory_size=$container_memory
    memory_swappiness=0
    case "$container_type" in
        dev)
            "${app_root_dir}/scripts/host/create_dev_volumes.sh"
            gen_repos='dev_gen_repos'
            output_storage='dev_output_storage'
            shared_memory_size='1g'
            env_file="${app_root_dir}/etc/env.list.dev"
            ;;
        test)
            "${app_root_dir}/scripts/host/create_dev_volumes.sh"
            gen_repos='dev_gen_repos'
            output_storage='dev_output_storage'
            shared_memory_size='1g'
            env_file="${app_root_dir}/etc/env.list.test"
            ;;
        pd)
            "${app_root_dir}/scripts/host/create_pd_volumes.sh"
            gen_repos='pd_gen_repos'
            output_storage='pd_output_storage'
            shared_memory_size='2g'
            env_file="${app_root_dir}/etc/env.list.pd"
            ;;
        *)
            echo "ERRO: Opcao desconhecida: $container_type"
            ;;
    esac

    if [ ! -e $env_file ]; then
        echo "ERRO: Nao encontrou arquivo ENV: ${env_file}"
        exit 1
    fi


    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    exec docker run \
        --security-opt='seccomp=unconfined' \
        --security-opt='apparmor=unconfined' \
        --memory="$memory_size" \
        --memory-swap="$memory_size" \
        --memory-swappiness="$memory_swappiness" \
        --shm-size="$shared_memory_size" \
        --env RUN_PORT="$port" \
        --env-file="$env_file" \
        --volume="${app_root_dir}/etc/csh.cshrc":'/etc/csh.cshrc' \
        --volume="${app_root_dir}":"${app_root_dir}" \
        --volume="${nr}":'/nr' \
        --volume="$gen_repos":'/mnt/gen_repos' \
        --volume="/output3/$output_storage":'/mnt/output_storage' \
        --env='DISPLAY' \
        --net='host' \
        --hostname="$host_name" \
        --ipc='host' \
        --init \
        --detach \
        "$run_policy" \
        --name="$container_name" \
        "$image_name"
}


function get_root_dir () {
    script_path="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
    echo "$(dirname $(dirname ${script_path}))"
}


function usage() { 
    echo "Usage: $0 [-p <port>] [-n <container name>] [-t <dev|pd|test>] [-m <memory usage percentage: 10, 75...>] [-i <image>] [-r]" 1>&2; 
    exit 1; 
}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Main >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

run_policy='--restart=always'
while getopts ":n:p:t:m:i:r" o; do
    case "${o}" in
        n)
            container_name=${OPTARG}
            ;;
        p)
            port=${OPTARG}
            echo "$port" | egrep '^[0-9]+$' >/dev/null
            test $? -eq 0 || usage      
            ;;
        t)
            t=${OPTARG}
            ((t == "dev" || t == "pd" || t == "test")) || usage
            ;;
        m)
            memory_percentage=${OPTARG}
            echo "$memory_percentage" | egrep '^[0-9]+[.]?[0-9]*$' >/dev/null
            test $? -eq 0 || usage            
            if [ $(echo "($memory_percentage < 1) || ($memory_percentage > 99.0)" | bc -l) -eq 1 ]; then
                echo "Range invalido para a memoria: ${memory_percentage}"
                usage
            fi

            physical_memory=$(free -g | grep -oP '\d+' | head -n 1)
            container_memory_value=$(echo "scale=2; ${physical_memory} * (${memory_percentage} / 100.0)" | bc -l | sed 's/^\./0./')
            container_memory="${container_memory_value}g"
            ;;
        i)
            i=${OPTARG}
            ;;
        r)
            run_policy='--rm'
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${container_name}" ] || \
    [ -z "${port}" ] || \
    [ -z "${t}" ] || \
    [ -z "${container_memory}" ] || \
    [ -z "${i}" ] || \
    [ -z "${run_policy}" ] ; then
    usage
fi

main $t $container_memory $i $run_policy $port $container_name

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# EOF
