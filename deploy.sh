#!/usr/bin/env bash

project_name="tickets-search-system"
base_dir="/home/ground/projects"

help() {
  cat <<-EOF
    -h --help                   帮助文档
    -p --proxypool [start|stop] 开启/关闭 IP代理池
    -c --crawl                  爬取数据
    -e --env [start|stop]       启动/关闭 大数据环境
    -u --update                 更新数据库
EOF
  exit 0
}

update() {
  cd "$base_dir"/"$project_name"/instance || exit
  exec "$base_dir"/"$project_name"/scripts/update.sh
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

hadoop() {
  if [ "$1" = "start" ]; then
    echo "ground" | sudo -S systemctl start postgresql
    start-dfs.sh
    start-yarn.sh
    start-history-server.sh
    start-spark.sh
  fi

  if [ "$1" = "stop" ]; then
    stop-spark.sh
    stop-history-server.sh
    stop-yarn.sh
    stop-dfs.sh
    echo "ground" | sudo -S systemctl stop postgresql
  fi
}

if [ -n "$1" ]; then #这里通过判断$1是否存在
  case $1 in
  -h | --help) help ;;
  -u | --update) update ;;
  -p | --proxypool) proxypool "$2" ;;
  -c | --crawl) crawl ;;
  -e | --env) hadoop "$2" ;;
  esac
else
  help
fi
