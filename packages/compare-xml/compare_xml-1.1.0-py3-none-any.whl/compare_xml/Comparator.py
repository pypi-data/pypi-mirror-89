#!/usr/bin/python3
# -*- coding: utf-8

import logging
#  compare-xml
#
#  Comparator for XML Elements
#
#  Copyright (c) 2020 Fabian Fröhlich <compare-xml@f-froehlich.de> <https://projects.f-froehlich.de/compare-xml>
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#  Checkout this project on github <https://github.com/f-froehlich/compare-xml>
#  and also my other projects <https://github.com/f-froehlich>
from xml.etree.ElementTree import Element
from lxml import etree


def compare(e1, e2):
    if not isinstance(e1, Element) and not isinstance(e1, etree._Element):
        logging.debug('e1 is not instance of xml.etree.ElementTree.Element')
        return False
    if not isinstance(e2, Element) and not isinstance(e2, etree._Element):
        logging.debug('e2 is not instance of xml.etree.ElementTree.Element')
        return False

    if e1.tag != e2.tag:
        logging.debug('Tag mismatch ("{t1}" != "{t2}"'.format(t1=e1.tag, t2=e2.tag))
        return False
    if e1.text != e2.text:
        logging.debug('Text mismatch ("{t1}" != "{t2}"'.format(t1=e1.text, t2=e2.text))
        return False
    if e1.attrib != e2.attrib:
        logging.debug('Attributes mismatch ("{t1}" != "{t2}"'.format(t1=e1.attrib, t2=e2.attrib))
        return False
    if len(e1) != len(e2):
        logging.debug('Children length mismatch ("{t1}" != "{t2}"'.format(t1=len(e1), t2=len(e2)))
        return False

    return compare_children(e1, e2) and compare_children(e2, e1)


def compare_children(e1, e2):
    elements_child1 = list(e1)
    for child2 in list(e2):
        exist = False
        for child1 in elements_child1:
            if compare(child1, child2):
                elements_child1.remove(child1)
                exist = True
                break
        if not exist:
            return False
    return True


def compare_lists(l1, l2):
    return compare_all_l1_in_l2(l1, l2) and compare_all_l1_in_l2(l2, l1)


def compare_all_l1_in_l2(l1, l2):
    if not isinstance(l1, list):
        logging.debug('l1 is not instance of list')
        return False

    if not isinstance(l2, list):
        logging.debug('l2 is not instance of list')
        return False

    if len(l1) != len(l2):
        logging.debug('Length mismatch ("{t1}" != "{t2}"'.format(t1=len(l1), t2=len(l2)))
        return False
    for e1 in l1:
        exist = False
        for e2 in l2:
            if compare(e1, e2):
                exist = True
                break
        if not exist:
            logging.debug('List does not match other')
            return False

    return True
