if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

FLASK_ENV="testing"

FLAGS="$1 --capture=no --disable-pytest-warnings --strict-markers --tb=line -rs --ignore=database/test_data.py --ignore=tests/mail_test.py --ignore=db_test.py --ignore=app/scripts"

RED='\033[0;31m'
GREEN='\033[0;32m'
L_CYAN='\033[1;36m'
NC='\033[0m' # No Color

echo -e "\n${GREEN}Running tests${NC}, with args ($L_CYAN$FLAGS$NC)"
#python3 -m pytest $FLAGS -m "unit or integration"
coverage run -m pytest $FLAGS -m "unit or integration" 

