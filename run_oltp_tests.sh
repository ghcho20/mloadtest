source .env

function show_menu() {
    echo "Test Options:"
    echo " 1     4K W: 50% , 2K R: 50%"
    echo " 2     8K W: 50% , 2K R: 50%"
    echo " 3    16K W: 50% , 2K R: 50%"
    echo " 4    32K W: 50% , 2K R: 50%"
    echo " 5    64K W: 50% , 2K R: 50%"
}

function date_time() {
    echo $(date '+%Y-%m-%dT%H:%M:%S')
}

# params: $1 - LOCUST_PROFILE
# params: $2 - DOC_SIZE
function run() {
    echo ">> Running default Locust test with 2 workers..."
    export LOCUST_PROFILE=$1
    export DOC_SIZE=$2
    nworkers=${NWORKERS:-8}
    nohup docker-compose -f docker-compose.oltp.yml up --scale worker=${nworkers} 2>&1 | tee ${LOCUST_PROFILE}.$(date_time).log &
}

show_menu
echo
read -p "Enter your choice: " choice

case $choice in
    1)
        run "4KW_4KR" $((1024*4))
        ;;
    2)
        run "8KW_4KR" $((1024*8))
        ;;
    3)
        run "16KW_4KR" $((1024*16))
        ;;
    4)
        run "32KW_4KR" $((1024*32))
        ;;
    5)
        run "64KW_4KR" $((1024*64))
        ;;
    *)
        echo "Please try again. Invalid option: [$choice]"
        ;;
esac