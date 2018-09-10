from websocket import create_connection
from log import *
import json

class HeartGameSocket(object):
    ws = ''
    def __init__ (self, player_name, player_number, token, connect_url, game_bot):
        self.player_name = player_name
        self.connect_url = connect_url
        self.player_number = player_number
        self.game_bot = game_bot
        self.token = token

    def takeAction (self, action, data):
       if  action == 'new_deal':
           self.game_bot.receive_cards(data)
       elif action == 'pass_cards':
           pass_cards=self.game_bot.pass_cards(data)
           self.ws.send(json.dumps(
                {
                    'eventName': 'pass_my_cards',
                    'data': {
                        'dealNumber': data['dealNumber'],
                        'cards': pass_cards
                    }
                }))
       elif action == 'receive_opponent_cards':
           self.game_bot.receive_opponent_cards(data)
       elif action =='expose_cards':
           export_cards = self.game_bot.expose_my_cards(data)
           if export_cards!=None:
               self.ws.send(json.dumps(
                   {
                       'eventName': 'expose_my_cards',
                       'data': {
                           'dealNumber': data['dealNumber'],
                           'cards': export_cards
                       }
                   }))
       elif action == 'expose_cards_end':
           self.game_bot.expose_cards_end(data)
       elif action == 'your_turn':
           pick_card = self.game_bot.pick_card(data)
           message='Send message:{}'.format(json.dumps(
                {
                   'eventName': 'pick_card',
                   'data': {
                       'dealNumber': data['dealNumber'],
                       'roundNumber': data['roundNumber'],
                       'turnCard': pick_card
                   }
               }))
           system_log.show_message(message)
           system_log.save_logs(message)
           self.ws.send(json.dumps(
               {
                   'eventName': 'pick_card',
                   'data': {
                       'dealNumber': data['dealNumber'],
                       'roundNumber': data['roundNumber'],
                       'turnCard': pick_card
                   }
               }))
       elif action == 'turn_end':
           self.game_bot.turn_end(data)
       elif action == 'round_end':
           self.game_bot.round_end(data)
       elif action == 'deal_end':
           self.game_bot.deal_end(data)
           self.game_bot.reset_card_his()
       elif action == 'game_end':
           self.game_bot.game_over(data)
           self.ws.close()
    def doListen (self):
        try:
            self.ws = create_connection(self.connect_url)
            self.ws.send(json.dumps({
                'eventName': 'join',
                'data': {
                    'playerNumber':self.player_number,
                    'playerName':self.player_name,
                    'token':self.token
                }
            }))
            while 1:
                result = self.ws.recv()
                msg = json.loads(result)
                event_name = msg['eventName']
                data = msg['data']
                system_log.show_message(event_name)
                system_log.save_logs(event_name)
                system_log.show_message(data)
                system_log.save_logs(data)
                self.takeAction(event_name, data)
        except Exception, e:
            system_log.show_message(e)
            system_log.save_logs(e)
            self.doListen()