#coding = UTF-8
import sys
from heartGameSocket import *
from lookAheadRobot import *
from log import *

def main(argv):
    argv_count = len(argv)
    if argv_count > 2:
        player_name = argv[1]
        player_number = argv[2]
        token = argv[3]
        connect_url = argv[4]
    else:
        player_name = "Look-Ahead Robot"
        player_number = 99
        token = "12345678"
        connect_url = "ws://localhost:8080/"

    robot = LookAheadRobot(player_name)
    game_socket  = HeartGameSocket(player_name, player_number, token, connect_url, robot)
    game_socket.doListen()

if __name__ == '__main__':
	main(sys.argv)