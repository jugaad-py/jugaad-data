export PYTHONWARNINGS="ignore:Unverified HTTPS request"
CNT=0
while true; do 
	OUTPUT=$(inotifywait jugaad_data/ tests/ -q -e create -e close_write -e attrib -e move )
	clear
	echo $OUTPUT
	#TEST_OP=$(env/bin/python -m unittest tests.test_cli  2>&1)
	TEST_OP=$(env/bin/python -m unittest discover 2>&1)
	echo  "$TEST_OP"
    CNT=$((CNT+1))
    echo $CNT


done

