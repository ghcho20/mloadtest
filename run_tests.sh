source .env

function show_menu() {
    echo "Test Options:"
    echo "  1    doc_size: 512B , R:  0% , W: 100%"
    echo "  2    doc_size:   1K , R:  0% , W: 100%"
    echo "  3    doc_size:  10K , R:  0% , W: 100%"
    echo "  4    doc_size: 100K , R:  0% , W: 100%"
    echo "  5    doc_size: rand , R:  0% , W: 100%"
    echo
    echo " 11    doc_size: 512B , R: 50% , W:  50%"
    echo " 12    doc_size:   1K , R: 50% , W:  50%"
    echo " 13    doc_size:  10K , R: 50% , W:  50%"
    echo " 14    doc_size: 100K , R: 50% , W:  50%"
    echo " 15    doc_size: rand , R: 50% , W:  50%"
    echo
    echo " 21    doc_size: 512B , R: 95% , W:   5%"
    echo " 22    doc_size:   1K , R: 95% , W:   5%"
    echo " 23    doc_size:  10K , R: 95% , W:   5%"
    echo " 24    doc_size: 100K , R: 95% , W:   5%"
    echo " 25    doc_size: rand , R: 95% , W:   5%"
    echo
    echo "  0    inserts while doing collection scan" # doc_size: 0, R: 0%, W: 0%
    echo "100    doc_size: 1M , R:  0% , W: 100%"
}

function date_time() {
    echo $(date '+%Y-%m-%dT%H:%M:%S')
}

# params: $1 - LOCUST_PROFILE
# params: $2 - DOC_SIZE
# params: $3 - R_WEIGHT
# params: $4 - W_WEIGHT
# params: $5 - Locust users
function run() {
    echo ">> Running default Locust test with 2 workers..."
    export LOCUST_PROFILE=$1
    export DOC_SIZE=$2
    export FIND_WEIGHT=$3
    export BULK_INSERT_WEIGHT=$4
    export TEST_USERS=$5
    nworkers=${NWORKERS:-8}
    # if [ ${FIND_WEIGHT} -eq 0 ] && [ ${BULK_INSERT_WEIGHT} -eq 0 ]; then
    #     nworkers=2
    # fi
    nohup docker-compose up --scale worker=${nworkers} 2>&1 | tee ${LOCUST_PROFILE}.$(date_time).log &
}

show_menu
echo
read -p "Enter your choice: " choice

case $choice in
    1)
        run "512B_R0_W100" 512 0 1
        ;;
    2)
        run "1K_R0_W100" 1024 0 1
        ;;
    3)
        run "10K_R0_W100" $((1024*10)) 0 1
        ;;
    4)
        run "100K_R0_W100" $((1024*100)) 0 1
        ;;
    5)
        run "RND_R0_W100" 0 0 1
        ;;
    11)
        run "512B_R50_W50" 512 1 1
        ;;
    12)
        run "1K_R50_W50" 1024 1 1
        ;;
    13)
        run "10K_R50_W50" $((1024*10)) 1 1
        ;;
    14)
        run "100K_R50_W50" $((1024*100)) 1 1
        ;;
    15)
        run "RND_R50_W50" 0 1 1
        ;;
    21)
        run "512_R95_W5" 512 19 1
        ;;
    22)
        run "1K_R95_W5" 1024 19 1
        ;;
    23)
        run "10K_R95_W5" $((1024*10)) 19 1
        ;;
    24)
        run "100K_R95_W5" $((1024*100)) 19 1
        ;;
    25)
        run "RND_R95_W5" 0 19 1
        ;;
    0)
        run "SCANandWR" $((1024*100)) 0 0 "TestUser ScanUser"
        ;;
    100)
        run "1M_R0_W100" $((1024**2)) 0 1
        ;;
    *)
        echo "Please try again. Invalid option: [$choice]"
        ;;
esac