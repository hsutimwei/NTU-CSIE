from game.players import BasePokerPlayer
from game.engine.hand_evaluator import HandEvaluator
from game.engine.card import Card
import random

def estimate(num_test,hole_card,community_card):

    hole_card=[Card.from_str(s).to_id() for s in hole_card]
    community_card=[Card.from_str(s).to_id() for s in community_card]

    sum=0
    for i in range(num_test):
        #隨機挑接下來可能的community_card
        
        used = hole_card + community_card
        unused = [card_id for card_id in range(1, 53) if card_id not in used]
        choiced = random.sample(unused, 5-len(community_card))
        full_community_card = community_card+choiced
        
        used=hole_card + full_community_card
        unused = [card_id for card_id in range(1, 53) if card_id not in used]
        opponents_hole = random.sample(unused, 2)
        
        full_community_card=[Card.from_id(card_id) for card_id in full_community_card]
        opponents_hole=[Card.from_id(card_id) for card_id in opponents_hole]
        hole_cards=[Card.from_id(card_id) for card_id in hole_card]
        
        opponents_score = HandEvaluator.eval_hand(opponents_hole, full_community_card)

        my_score = HandEvaluator.eval_hand(hole_cards, full_community_card)

        if my_score >= opponents_score:
            sum+=1

    return sum/num_test

class CallPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        oppo_pay=0
        my_pay=0
        uuid=0
        mystack=0
        last_oppo_action=0
        round_count=round_state["round_count"]
        for i in round_state["seats"]:
            if i["name"]=="b09902140":
                uuid=i["uuid"]
                mystack=i["stack"]

        for i in round_state["action_histories"]:
            for j in round_state["action_histories"][i]:
                if j["uuid"]!=uuid:
                    oppo_pay+=j["amount"]
                if j["uuid"]==uuid:
                    my_pay+=j["amount"]
        
        if mystack>=1000+7.5*(20-round_count):
            return valid_actions[0]["action"],valid_actions[0]["amount"]
        
        win_rate=estimate(1000,hole_card, round_state['community_card'])
        
        a=random.random()
        
        if win_rate>0.5:
            
            if oppo_pay>=mystack/2 and my_pay>=100 and win_rate>0.8:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["max"]
                if valid_actions[2]["amount"]["max"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif oppo_pay>=mystack/2 and my_pay>=100 and win_rate>0.8:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["max"]
                if valid_actions[2]["amount"]["min"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif oppo_pay<mystack/20 and my_pay<mystack/20 and round_state['community_card']==[] and win_rate>0.95:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["max"]
                if valid_actions[2]["amount"]["max"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif oppo_pay<mystack/20 and my_pay<mystack/20 and round_state['community_card']!=[] and win_rate>0.85:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["min"]*0.85+valid_actions[2]["amount"]["max"]*0.15
                if valid_actions[2]["amount"]["max"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif oppo_pay<mystack/20 and my_pay<mystack/20 and win_rate>0.6:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["min"]
                if valid_actions[2]["amount"]["min"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif oppo_pay>=(2000-mystack)/2 and my_pay<=100 and a<(1-win_rate)**0.2:
                action = valid_actions[0]["action"]
                amount = valid_actions[0]["amount"]
            elif oppo_pay>=(2000-mystack)/5 and my_pay<=50 and a<(1-win_rate)**0.5:
                action = valid_actions[0]["action"]
                amount = valid_actions[0]["amount"]
            elif oppo_pay>=(2000-mystack)/20 and my_pay<=30 and a<(1-win_rate)**2:
                action = valid_actions[0]["action"]
                amount = valid_actions[0]["amount"]
            elif a<0.8 and oppo_pay>150:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["min"]
                if valid_actions[2]["amount"]["min"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            else:
                action = valid_actions[1]["action"]
                amount = valid_actions[1]["amount"]
                
        else:
            if a<0.01 and win_rate>0.4 and mystack<=950:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["max"]
                if valid_actions[2]["amount"]["max"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif a<0.03 and win_rate>0.4 and oppo_pay<(2000-mystack)/10 and mystack<=900:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["max"]
                if valid_actions[2]["amount"]["max"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            elif win_rate>0.1 and oppo_pay<=30 and round_state['community_card']==[] and a<0.7:
                action = valid_actions[1]["action"]
                amount = valid_actions[1]["amount"]
            elif valid_actions[1]["amount"]==0:
                action = valid_actions[1]["action"]
                amount = valid_actions[1]["amount"]
            elif my_pay>=60 and win_rate>0.3:
                action = valid_actions[1]["action"]
                amount = valid_actions[1]["amount"]
            elif a<win_rate and oppo_pay>150:
                action = valid_actions[2]["action"]
                amount = valid_actions[2]["amount"]["min"]
                if valid_actions[2]["amount"]["min"]==-1:
                    action = valid_actions[1]["action"]
                    amount = valid_actions[1]["amount"]
            else:
                action = valid_actions[0]["action"]
                amount = valid_actions[0]["amount"]
        print(action, amount)
        return action, amount  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return CallPlayer()
