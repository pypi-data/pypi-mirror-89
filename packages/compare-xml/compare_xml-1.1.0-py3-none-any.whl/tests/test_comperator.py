from xml.etree.ElementTree import ElementTree

import pytest

from compare_xml.Comparator import compare, compare_lists


def create_xml(filepath):
    et = ElementTree()
    return et.parse(source=filepath)


@pytest.mark.parametrize(("filepath1", "filepath2", "expected"), [
    ('testdata/1.xml', 'testdata/1.xml', True),
    ('testdata/1.xml', 'testdata/2.xml', True),
    ('testdata/1.xml', 'testdata/3.xml', False),
    ('testdata/1.xml', 'testdata/4.xml', False),
    ('testdata/2.xml', 'testdata/1.xml', True),
    ('testdata/2.xml', 'testdata/2.xml', True),
    ('testdata/2.xml', 'testdata/3.xml', False),
    ('testdata/2.xml', 'testdata/4.xml', False),
    ('testdata/3.xml', 'testdata/1.xml', False),
    ('testdata/3.xml', 'testdata/2.xml', False),
    ('testdata/3.xml', 'testdata/3.xml', True),
    ('testdata/3.xml', 'testdata/4.xml', False),
    ('testdata/4.xml', 'testdata/1.xml', False),
    ('testdata/4.xml', 'testdata/2.xml', False),
    ('testdata/4.xml', 'testdata/3.xml', False),
    ('testdata/4.xml', 'testdata/4.xml', True),
])
def test_equals(filepath1, filepath2, expected):
    xml1 = create_xml(filepath1)
    xml2 = create_xml(filepath2)

    assert expected == compare(xml1, xml2)


def test_equals_wrong_instance():
    xml = create_xml('testdata/4.xml')

    assert not compare(xml, 'foo')
    assert not compare('foo', xml)


@pytest.mark.parametrize(("filepath1", "filepath2", "expected"), [
    ([1], [1], True),
    ([1], [2], True),
    ([1], [1, 2], False),
    ([1, 2], [2], False),
    ([1, 2], [1, 2], True),
    ([1, 2], [2, 1], True),
    ([1, 2], [2, 2], True),
    ([2, 1], [1, 2], True),
    ([2, 1], [2, 1], True),
    ([2, 1], [2, 2], True),
    ([1, 3], [1, 2], False),
    ([1, 2], [1, 3], False),
    ([1, 2, 3], [3, 1, 3], True),
])
def test_compare_lists(filepath1, filepath2, expected):
    l1 = [create_xml('testdata/' + str(file) + '.xml') for file in filepath1]
    l2 = [create_xml('testdata/' + str(file) + '.xml') for file in filepath2]

    assert expected == compare_lists(l1, l2)


def test_compare_lists_wrong_instance():
    xml = create_xml('testdata/4.xml')

    assert not compare_lists([xml], 'foo')
    assert not compare_lists('foo', [xml])
