#!/bin/sh
#E requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=5000): Max retries exceeded with url: /buyer/new_order (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000002760D165208>: Fa
#iled to establish a new connection: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。'))


function commitErr(){
    if [ $? -ne 0 ];then
        echo "pause because of failed to commit "
        #沉睡100秒，以便查看异常信息
        sleep 1
        #当调用者使用Ctrl + C打断沉睡之后，直接退出脚本，阻止脚本向下执行
        exit
    fi
}
function pushErr(){
    if [ $? -ne 0 ];then
        echo "pause because of failed "
        #沉睡100秒，以便查看异常信息
        sleep 1
        read -r -p "push failed!do you want to push with force? [n/Y] " input
    if [ -z $res ];then
      push
    else
        case $input in
            [yY][eE][sS]|[yY])
            git push -f origin master
            git rm -r --cached .
            ;;

            [nN][oO]|[nN])
            echo "push failed"
            exit 1
                ;;

            *)
            echo "Invalid input..."
            exit 1
            ;;
        esac
        exit
    fi
    fi
}
function push(){
      SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
			echo $SHELL_FOLDER
			read -p "THE NAME OF COMMIT?:" COMMITNAME
			git add .
			git commit -m $COMMITNAME
			commitErr
			git push origin master
			pushErr
}
while true
do
	read -r -p "Are you yzy? [Y/n] " input
  if [ -z $res ];then
    push
  else
    case $input in
        [yY][eE][sS]|[yY])
        push
        exit 1
        ;;

        [nN][oO]|[nN])

        exit 1
        ;;
        *)
        echo "Invalid input..."
        ;;
    esac
	fi
done
