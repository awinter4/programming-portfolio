from saalmonagerie import Saalmonagerie

def fight(sm1: Saalmonagerie, sm2: Saalmonagerie, verbose: bool, base_damage: int=5) -> None:
    '''
    Conducts a fight between two Saalmonageries, consisting of the following
    steps:
    <ol>
        <li>Saalmon from each Saalmonagerie are paired to fight, in sequence
            starting from index 0.</li>
        <li>Saalmon that faint (have 0 or less health) are removed from their
            respective Saalmonagerie.</li>
        <li>Repeat until one or both Saalmonagerie have no remaining Saalmon.</li>
    </ol>

    :param sm1: one of the fighting Saalmonagerie
    :param sm2: one of the fighting Saalmonagerie
    :param verbose: whether or not the fight's steps are printed
    '''
    sm1_i = sm2_i = -1
    fight_log = '[!] Combat Starting!\n'

    while not sm1.empty() and not sm2.empty():
        sm1_i = (sm1_i + 1) % len(sm1)
        sm2_i = (sm2_i + 1) % len(sm2)

        s1 = sm1.get(sm1_i)
        s2 = sm2.get(sm2_i)
        fight_log += f'  [VS] New Round: {s1} vs {s2}\n'

        # Attack phase
        if (
            s1.take_damage(
                base_damage + s2.get_level(), s2.get_damage_type()
            )
            <= 0
        ):
            sm1.remove(sm1_i)
            sm1_i -= 1

        if (
            s2.take_damage(
                base_damage + s1.get_level(), s1.get_damage_type()
            )
            <= 0
        ):
            sm2.remove(sm2_i)
            sm2_i -= 1
        fight_log += f'    [>] Combat Results: {s1} vs {s2}\n'

    fight_log += f'[!] Combat Finished! Victor: {"TIE MATCH!" if (sm1.empty() and sm2.empty()) else f"Saalmonagerie {2 if sm1.empty() else 1}"}\n'
    if verbose:
        print(fight_log)