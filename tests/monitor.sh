if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

BUILD="$@"
if [ -z "$BUILD" ]
then
	BUILD="";
	#BUILD="all";
fi

ptw --verbose -c --runner "bash tests/run_tests.sh $BUILD" --ignore database/ --ext=".py,.sh,.html,.yml"
