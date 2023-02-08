# For now takes 2 arguments, name for client 1 and name for client 2.
# In the future: use looping to create multiple instances

# Setup client instance
_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Clear old files
rm -rf ./data/
rm -rf ./cli_1/
rm -rf ./cli_2/

# Generate new Genesis Block and move it to cli_1
python3 ../genesis.py

mkdir ./cli_1
mkdir ./cli_1/data

cp ./data/* ./cli_1/data/

mkdir ./cli_2
mkdir ./cli_2/data
cp ./data/* ./cli_2/data/

cp ../*.py ./cli_1/
cp ../*.py ./cli_2/

mkdir ./cli_1/core
mkdir ./cli_1/keys


mkdir ./cli_2/core
mkdir ./cli_2/keys


cp ../core/* ./cli_1/core
cp ../keys/* ./cli_1/keys

cp ../core/* ./cli_2/core
cp ../keys/* ./cli_2/keys


rm -rf ./cli_1/chainspec.py
cp ./artifacts/cli_1/chainspec.py ./cli_1

rm -rf ./cli_2/chainspec.py
cp ./artifacts/cli_2/chainspec.py ./cli_2
