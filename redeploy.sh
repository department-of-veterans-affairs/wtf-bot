cd wtf-bot
BOT_DIR=$(pwd)

PROCESS_ID=$(pgrep -o python3.8)
sudo kill -9 $PROCESS_ID

CHILD_ID=$(pgrep -o python3.8)
sudo kill -9 $CHILD_ID

git pull
pip3 install -r requirements.txt dev-requirements.txt
sudo rm log.txt

sudo -i bash << EOF
cd $BOT_DIR
export FLASK_APP=$1
export SLACK_TOKENS=$2
export DATA_URL=$3
export FLASK_DEBUG=$4
touch log.txt
nohup python3.8 -m flask run -h 0.0.0.0 -p 80 > log.txt 2>&1 &
EOF