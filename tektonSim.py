import sys
import os
import math
import random
import time

SECONDS_PER_TICK = 0.6
SCYTHE_SPEED = 3  # 3 seconds, 5 ticks * 0.6

# TEKTON_DEF_LVL = 250
TEKTON_CRUSH_DEF = 105
TEKTON_SLASH_DEF = 165
# TEKTON_HP = 900


def hit(max_hit, accuracy):
    """
    Checks for a miss then returns a hit between 0 and max_hit (inclusive)
    """
    if accuracy > random.random():
        # Attack lands. Generate a hit between 0 and max_hit
        hit = random.choice(range(max_hit+1))
    else:
        # Attack misses
        hit = 0
    return hit


def max_hit(effective_strength_level, strength_bonus):
    """
    Returns maximum hit value for melee and ranged attacks
    Keyword arguments:
    effective_strenth_level = visible strength level + modifiers (piety, pots, ovl etc)
    strength_bonus = strength bonus given by the in-game equipment interface
    """
    hit = 0.5 + effective_strength_level * (strength_bonus + 64) / 640
    max_hit = math.floor(hit)
    return max_hit


def accuracy(
        effective_attack_level, attack_bonus,
        effective_defence_level, defence_bonus):
    """
    Returns number from 0-1 indicating chance to hit with a melee or ranged attack
    Keyword arguments:
    effective_attack_level = visible attacking level (of attacker) + modifiers,
        where the attacking stat is attack or ranged
    attack_bonus = equipment bonus given by the in-game equipment interface
        for the appropriate attack style (ranged, stab, slash, crush)
    effective_defence_level = visible defence level (of defender) + modifiers
        Value is given for NPCs in the RuneScape bestiary
    defence_bonus = equipment bonus given by the in-game equipment interface
        for the appropriate attack style (ranged, magic, stab, slash, crush)
        Value is given for NPCs in the RuneScape bestiary
    """
    attack_roll = _accuracy_roll(effective_attack_level, attack_bonus)
    defence_roll = _accuracy_roll(effective_defence_level, defence_bonus)

    if attack_roll > defence_roll:
        accuracy = 1 - (defence_roll + 2) / (2 * (attack_roll + 1))
    else:
        accuracy = attack_roll / (2 * (defence_roll + 1))

    return accuracy


def _accuracy_roll(effective_level, bonus):
    """
    Returns attack (or defence) roll used internally for accuracy calculation
    """
    return effective_level * (bonus + 64)


def roll_hammer_spec(TEKTON_DEF_LVL):
    """
    Calculate a hammer spec,
    return hammer damage if hit and 0 for miss
    """
    ham_accuracy = accuracy(141, 192, TEKTON_DEF_LVL, TEKTON_CRUSH_DEF)
    ham_damage = hit(max_hit(145, 148), ham_accuracy)
    if ham_damage > 0:
        return ham_damage
    else:
        return 0


def roll_scythe_hit(TEKTON_DEF_LVL):
    # accuracy(141, 99, TEKTON_DEF_LVL, TEKTON_CRUSH_DEF)
    # max_hit(145, 130)

    scy_hit = hit(max_hit(145, 130), accuracy(141, 99, TEKTON_DEF_LVL, TEKTON_CRUSH_DEF))  # wearing full inquisitor
    return scy_hit


def main():
    num_kills = int(input("Enter the total number of kills to simulate: "))
    for i in range(num_kills):

        TEKTON_DEF_LVL = 250
        TEKTON_HP = 900
        # print("Tekton's initial def lvl: ", TEKTON_DEF_LVL)

        # populate array of hammer hits
        hammer_hits = []
        for i in range(6):
            x = roll_hammer_spec(TEKTON_DEF_LVL)
            hammer_hits.append(x)

        # Calculate total def reduction and remaining HP using array of hammer hits
        for i in range(len(hammer_hits)):
            if hammer_hits[i] > 0:
                TEKTON_DEF_LVL -= (TEKTON_DEF_LVL * .30)  # calculate total def reduction
                # print("Tekton's new def lvl after hit: ", TEKTON_DEF_LVL)

        TEKTON_HP -= sum(hammer_hits)

        # print("Hammer hits: ", hammer_hits)
        # print("Tekton's final def lvl: ", TEKTON_DEF_LVL)
        # print("Tekton's remaining hp: ", TEKTON_HP)

        swings = 10.8  # Start swings at 10.8 to account for two hammer specs for each player
        while TEKTON_HP >= 0:
            # three total scythe swings every 3 seconds
            for i in range(3):
                swing_damage = roll_scythe_hit(TEKTON_DEF_LVL)
                TEKTON_HP -= swing_damage
                swings += 1
                # time.sleep(3)
        # print("Tekton killed in ", (swings), "seconds ")
        #swings += num_kills

    num_kills -= 1
    print("Over {0} kills, inquisitor averaged {1} seconds per kill in a trio".format(num_kills, (swings/3)))
    # desired output "over x number of tektons,
    # inquisitor averaged y seconds per kill and bandos averaged z seconds per kill"


if __name__ == "__main__":
    main()
