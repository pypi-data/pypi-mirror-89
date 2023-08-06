# -*- coding: utf-8 -*-
from py_rete.production import Production
from py_rete.production import AndCond
from py_rete.production import Cond
from py_rete.production import Neg
from py_rete.production import Ncc
from py_rete.common import WME
from py_rete.common import Token
from py_rete.network import Network


def test_network_case0():
    net = Network()
    c0 = Cond('x', 'id', '1')
    c1 = Cond('x', 'kind', '8')
    p0 = net.add_production(Production('test0', AndCond(c0, c1)))

    w0 = WME('x', 'id', '1')
    w1 = WME('x', 'kind', '8')

    net.add_wme(w0)
    assert not p0.items

    net.remove_wme(w0)
    net.add_wme(w1)
    assert not p0.items

    net.add_wme(w0)
    net.add_wme(w1)
    assert p0.items


def test_network_case1():
    # setup
    net = Network()
    c0 = Cond('$x', 'on', '$y')
    c1 = Cond('$y', 'left-of', '$z')
    c2 = Cond('$z', 'color', 'red')
    net.add_production(Production('test', AndCond(c0, c1, c2)))
    # end

    wmes = [
        WME('B1', 'on', 'B2'),
        WME('B1', 'on', 'B3'),
        WME('B1', 'color', 'red'),
        WME('B2', 'on', 'table'),
        WME('B2', 'left-of', 'B3'),
        WME('B2', 'color', 'blue'),
        WME('B3', 'left-of', 'B4'),
        WME('B3', 'on', 'table'),
        WME('B3', 'color', 'red')
    ]
    for wme in wmes:
        net.add_wme(wme)

    am0 = net.build_or_share_alpha_memory(c0)
    am1 = net.build_or_share_alpha_memory(c1)
    am2 = net.build_or_share_alpha_memory(c2)
    dummy_join = am0.successors[0]
    join_on_value_y = am1.successors[0]
    join_on_value_z = am2.successors[0]
    match_c0 = dummy_join.children[0]
    match_c0c1 = join_on_value_y.children[0]
    match_c0c1c2 = join_on_value_z.children[0]

    assert am0.items == [wmes[0], wmes[1], wmes[3], wmes[7]]
    assert am1.items == [wmes[4], wmes[6]]
    assert am2.items == [wmes[2], wmes[8]]
    assert len(match_c0.items) == 4
    assert len(match_c0c1.items) == 2
    assert len(match_c0c1c2.items) == 1

    t0 = Token(Token(None, None), wmes[0])
    t1 = Token(t0, wmes[4])
    t2 = Token(t1, wmes[8])
    assert match_c0c1c2.items[0] == t2

    print(wmes[0].tokens)
    print(match_c0.items)
    print(match_c0c1.items)
    print(match_c0c1c2.items)
    print()

    net.remove_wme(wmes[0])

    print(wmes[0].tokens)
    print(match_c0.items)
    print(match_c0c1.items)
    print(match_c0c1c2.items)

    assert am0.items == [wmes[1], wmes[3], wmes[7]]
    assert am1.items == [wmes[4], wmes[6]]
    assert am2.items == [wmes[2], wmes[8]]
    assert len(match_c0.items) == 3
    assert len(match_c0c1.items) == 1
    assert len(match_c0c1c2.items) == 0


def test_dup():
    # setup
    net = Network()
    c0 = Cond('$x', 'self', '$y')
    c1 = Cond('$x', 'color', 'red')
    c2 = Cond('$y', 'color', 'red')
    net.add_production(Production('test', AndCond(c0, c1, c2)))

    wmes = [
        WME('B1', 'self', 'B1'),
        WME('B1', 'color', 'red'),
    ]
    for wme in wmes:
        net.add_wme(wme)
    # end

    am = net.build_or_share_alpha_memory(c2)
    join_on_value_y = am.successors[1]
    match_for_all = join_on_value_y.children[0]

    assert len(match_for_all.items) == 1


def test_negative_condition():
    # setup
    net = Network()
    c0 = Cond('$x', 'on', '$y')
    c1 = Cond('$y', 'left-of', '$z')
    c2 = Neg('$z', 'color', 'red')
    p0 = net.add_production(Production('test', AndCond(c0, c1, c2)))
    # end

    wmes = [
        WME('B1', 'on', 'B2'),
        WME('B1', 'on', 'B3'),
        WME('B1', 'color', 'red'),
        WME('B2', 'on', 'table'),
        WME('B2', 'left-of', 'B3'),
        WME('B2', 'color', 'blue'),
        WME('B3', 'left-of', 'B4'),
        WME('B3', 'on', 'table'),
        WME('B3', 'color', 'red'),
    ]
    for wme in wmes:
        net.add_wme(wme)

    am0 = net.build_or_share_alpha_memory(c0)
    am1 = net.build_or_share_alpha_memory(c1)
    am2 = net.build_or_share_alpha_memory(c2)
    dummy_join = am0.successors[0]
    join_on_value_y = am1.successors[0]
    join_on_value_z = am2.successors[0]
    match_c0 = dummy_join.children[0]
    match_c0c1 = join_on_value_y.children[0]
    match_c0c1c2 = join_on_value_z.children[0]

    print(match_c0.items)
    print(match_c0c1.items)
    print(type(join_on_value_z))
    print(match_c0c1c2.items)

    assert p0.items[0].wmes == [
        WME('B1', 'on', 'B3'),
        WME('B3', 'left-of', 'B4'),
        None
    ]


def test_multi_productions():
    net = Network()
    c0 = Cond('$x', 'on', '$y')
    c1 = Cond('$y', 'left-of', '$z')
    c2 = Cond('$z', 'color', 'red')
    c3 = Cond('$z', 'on', 'table')
    c4 = Cond('$z', 'left-of', 'B4')

    p0 = net.add_production(Production('test0', AndCond(c0, c1, c2)))
    p1 = net.add_production(Production('test1', AndCond(c0, c1, c3, c4)))

    wmes = [
        WME('B1', 'on', 'B2'),
        WME('B1', 'on', 'B3'),
        WME('B1', 'color', 'red'),
        WME('B2', 'on', 'table'),
        WME('B2', 'left-of', 'B3'),
        WME('B2', 'color', 'blue'),
        WME('B3', 'left-of', 'B4'),
        WME('B3', 'on', 'table'),
        WME('B3', 'color', 'red'),
    ]
    for wme in wmes:
        net.add_wme(wme)

    # add product on the fly
    p2 = net.add_production(Production('test2', AndCond(c0, c1, c3, c2)))

    assert len(p0.items) == 1
    assert len(p1.items) == 1
    assert len(p2.items) == 1
    assert p0.items[0].wmes == [wmes[0], wmes[4], wmes[8]]
    assert p1.items[0].wmes == [wmes[0], wmes[4], wmes[7], wmes[6]]
    assert p2.items[0].wmes == [wmes[0], wmes[4], wmes[7], wmes[8]]

    net.remove_production(p2)

    print(type(p2))
    assert len(p2.items) == 0


def test_ncc():
    net = Network()
    c0 = Cond('$x', 'on', '$y')
    c1 = Cond('$y', 'left-of', '$z')
    c2 = Cond('$z', 'color', 'red')
    c3 = Cond('$z', 'on', '$w')

    p0 = net.add_production(Production('test0', AndCond(c0, c1, Ncc(c2, c3))))
    wmes = [
        WME('B1', 'on', 'B2'),
        WME('B1', 'on', 'B3'),
        WME('B1', 'color', 'red'),
        WME('B2', 'on', 'table'),
        WME('B2', 'left-of', 'B3'),
        WME('B2', 'color', 'blue'),
        WME('B3', 'left-of', 'B4'),
        WME('B3', 'on', 'table'),
    ]
    for wme in wmes:
        net.add_wme(wme)
    assert len(p0.items) == 2
    net.add_wme(WME('B3', 'color', 'red'))
    assert len(p0.items) == 1


def test_black_white():
    net = Network()
    c1 = Cond('$item', 'cat', '$cid')
    c2 = Cond('$item', 'shop', '$sid')
    white = Ncc(
        Neg('$item', 'cat', '100'),
        Neg('$item', 'cat', '101'),
        Neg('$item', 'cat', '102'),
    )
    n1 = Neg('$item', 'shop', '1')
    n2 = Neg('$item', 'shop', '2')
    n3 = Neg('$item', 'shop', '3')
    p0 = net.add_production(Production('test0', AndCond(c1, c2, white, n1, n2,
                                                        n3)))
    wmes = [
        WME('item:1', 'cat', '101'),
        WME('item:1', 'shop', '4'),
        WME('item:2', 'cat', '100'),
        WME('item:2', 'shop', '1'),
    ]
    for wme in wmes:
        net.add_wme(wme)

    assert len(p0.items) == 1
    assert p0.items[0].get_binding('$item') == 'item:1'
