#!/usr/bin/env bash

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
    ssh ground@hadoop-2 <<remotessh
    cd ~/projects/proxy_pool-master

    if [[ -f 1.pid ]]; then
      kill -9 \`cat 1.pid\`
    fi
    if [[ -f 2.pid ]]; then
      kill -9 \`cat 2.pid\`
    fi

    python proxyPool.py server > /dev/null 2>&1 &
    echo \$! > 1.pid
    python proxyPool.py schedule > /dev/null 2>&1 &
    echo \$! > 2.pid
    exit
remotessh
  fi

  if [ "$1" = "stop" ]; then
    ssh ground@hadoop-2 <<remotessh
    cd ~/projects/proxy_pool-master
    kill -9 \`cat 1.pid\`
    kill -9 \`cat 2.pid\`
    rm 1.pid
    rm 2.pid
    exit
remotessh
  fi
  exit 0
}

crawl() {
  ssh ground@hadoop-2 <<remotessh
  cd ~/projects/tickets-search-system/crawler
  python ./ctrip.py
  exit
remotessh
  exit 0
}

run() {
  exit 0
}

while [ -n "$1" ]; do #这里通过判断$1是否存在
  case $1 in
  -h | --help) help ;;
  -u | --update) update;;
  -p | --proxypool) proxypool "$2" ;;
  -c | --crawl) crawl ;;
  -r | --run) run ;;
  esac
done
