#!/usr/bin/env bash

project_name="tickets-search-system"
base_dir="/home/ground/projects"

help() {
  cat <<-EOF
    -h --help       帮助文档
    -u --update     更新远程文件
    -c --crawl      爬取数据
EOF
  exit 0
}

update() {
  scp -r ./crawler hadoop-2:~/projects/tickets-search-system/
  scp -r ./raw_data/checkpoints.json \
    ./raw_data/mainCities.json \
    hadoop-2:~/projects/tickets-search-system/raw_data
  exit 0
}

proxypool() {
  if [ "$1" = "start" ]; then
    echo "ground" | sudo -S systemctl start redis
    cd "$base_dir"/proxy_pool-master || exit

    if [[ -f 1.pid ]]; then
      kill -9 $(cat 1.pid)
    fi
    if [[ -f 2.pid ]]; then
      kill -9 $(cat 2.pid)
    fi

    python3.9 proxyPool.py server > /dev/null 2>&1 &
    echo $! > 1.pid
    python3.9 proxyPool.py schedule > /dev/null 2>&1 &
    echo $! > 2.pid
  fi

  if [ "$1" = "stop" ]; then
    cd "$base_dir"/proxy_pool-master || exit
    kill -9 $(cat 1.pid)
    kill -9 $(cat 2.pid)
    rm 1.pid
    rm 2.pid
    echo "ground" | sudo -S systemctl stop redis

    cd "$base_dir"/tickets-search-system/data || exit
    cp checkpoints checkpoints.json
  fi

  exit 0
}

crawl() {
  cd "$base_dir"/"$project_name"/crawler || exit
  python3.9 ./ctrip.py

  exit 0
}

run() {
  exit 0
}

if [ -n "$1" ]; then #这里通过判断$1是否存在
  case $1 in
  -h | --help) help ;;
  -u | --update) update;;
  -p | --proxypool) proxypool "$2" ;;
  -c | --crawl) crawl ;;
  -r | --run) run ;;
  esac
else
  help
fi
