from pm4py.objects.petri.utils import remove_transition, remove_place, add_arc_from_to


def reduce_single_entry_transitions(net):
    """
    Reduces the number of the single entry transitions in the Petri net

    Parameters
    ----------------
    net
        Petri net
    """
    cont = True
    while cont:
        cont = False
        single_entry_transitions = [t for t in net.transitions if t.label is None and len(t.in_arcs) == 1]
        for i in range(len(single_entry_transitions)):
            t = single_entry_transitions[i]
            source_place = list(t.in_arcs)[0].source
            target_places = [a.target for a in t.out_arcs]
            if len(source_place.in_arcs) == 1 and len(source_place.out_arcs) == 1:
                source_transition = list(source_place.in_arcs)[0].source
                remove_transition(net, t)
                remove_place(net, source_place)
                for p in target_places:
                    add_arc_from_to(source_transition, p, net)
                cont = True
                break
    return net


def reduce_single_exit_transitions(net):
    """
    Reduces the number of the single exit transitions in the Petri net

    Parameters
    --------------
    net
        Petri net
    """
    cont = True
    while cont:
        cont = False
        single_exit_transitions = [t for t in net.transitions if t.label is None and len(t.out_arcs) == 1]
        for i in range(len(single_exit_transitions)):
            t = single_exit_transitions[i]
            target_place = list(t.out_arcs)[0].target
            source_places = [a.source for a in t.in_arcs]
            if len(target_place.in_arcs) == 1 and len(target_place.out_arcs) == 1:
                target_transition = list(target_place.out_arcs)[0].target
                remove_transition(net, t)
                remove_place(net, target_place)
                for p in source_places:
                    add_arc_from_to(p, target_transition, net)
                cont = True
                break
    return net


def apply_simple_reduction(net):
    """
    Apply a simple reduction to the Petri net

    Parameters
    --------------
    net
        Petri net
    """
    reduce_single_entry_transitions(net)
    reduce_single_exit_transitions(net)
    return net
