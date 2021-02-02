if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

BUILD="$@"
if [ -z "$BUILD" ]
then
	BUILD="all";
fi

ptw --verbose -c --runner "bash tests/run_tests.sh $BUILD" --ext=".py,.sh,.html"
