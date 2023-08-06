Compare XML
===========
Comparator for XML Elements

Copyright (c) 2020 Fabian Fröhlich <compare-xml@f-froehlich.de> [https://projects.f-froehlich.de/compare-xml](https://projects.f-froehlich.de/compare-xml)


# Donate
This project needs donations. Please check out [https://projects.f-froehlich.de/Donate](https://projects.f-froehlich.de/Donate) for details.


# Quick setup

* install python 3.7 (other versions may also work)
* install python3-pip
* install [Nmap](https://github.com/nmap/nmap) 
* `pip3 install compare-xml`

# Usage

```python
from compare_xml.Comparator import compare, compare_lists
from xml.etree.ElementTree import ElementTree

xml1 = ElementTree().parse(source=filepath1)
xml2 = ElementTree().parse(source=filepath2)

compare(xml1, xml2)  # False
compare(xml2, xml1)  # False
compare(xml1, xml1)  # True
compare(xml2, xml2)  # True

compare_lists([xml1], [])  # False
compare_lists([xml1], [xml2])  # False
compare_lists([xml1], [xml1])  # True
compare_lists([xml1, xml2], [xml2, xml1])  # True
compare_lists([xml1, xml2], [xml2, xml2])  # False

```