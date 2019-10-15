"""Test the sql_sankey function."""

import xml.etree.ElementTree as ET

import pytest

import kettlediff


def test_caseless():
    """Test the text normalization."""
    assert kettlediff.caseless("AbcDe") == "abcde"
    assert kettlediff.caseless("abcde") == "abcde"
    assert kettlediff.caseless("ÄÖÜß") == "äöüss"


def test_xml_element_key():
    """Test the name builder function."""
    tree = ET.parse("test/test.ktr").getroot()
    names = ["info", "notepads", "order", "hops", "■stepadd a checksum",
             "■stepgenerate rows", "step_error_handling",
             "slave-step-copy-partition-distribution", "slave_transformation"]
    for element in tree:
        assert kettlediff.xml_element_key(element) in names
    elements = []
    for name in ["Abc", "def", "step", "connection", "entries"]:
        element = ET.Element(name)
        sub = ET.Element(name)
        sub.text = "Text"
        element.append(sub)
        elements.append(element)
    for element in elements:
        assert kettlediff.xml_element_key(element) in (
            "abc", "def", "■steptext", "■entriestext", "■connectiontext")


def test_hop_key():
    """Test the name builder for non-uniquely named elements."""
    element = ET.Element("Test_element")
    sub = ET.Element("from")
    sub.text = "Basis"
    element.append(sub)
    sub = ET.Element("to")
    sub.text = "Target"
    element.append(sub)
    assert kettlediff.hop_key(element) == "basis ■ ■ target"


def test_hop_element_idx():
    """Test the edge node finder."""
    element = ET.Element("Test_element")
    element.append(ET.Element("Somevalue"))
    element.append(ET.Element("Someothervalue"))
    assert kettlediff.hop_element_idx(element) is None
    element.append(ET.Element("order"))
    assert kettlediff.hop_element_idx(element) == 2
    element.remove(element[2])
    element.append(ET.Element("Morevalues"))
    element.append(ET.Element("hops"))
    element.append(ET.Element("Evenmorevalues"))
    assert kettlediff.hop_element_idx(element) == 3


def test_data_cleaning():
    """Test the data normalizer function."""

    func = kettlediff.data_cleaning
    # Html tag recognition
    data = "&Auml;&amp;&ouml;"
    assert func(data, "PDI") == "Ä&ö"
    # Empty tags normalization
    data = "    <test>\n\r    \n\r    </test>"
    assert func(data, "PDI") == "    <test> </test>"
    # Shortening of long sparse tags
    data = ("    <field>\n    <name>The name</name>\n<rename/>\n"
            "<length>-2</length>\n    <precision>-2</precision>")
    assert func(data, "PDI") == "    <field>\n    <name>The name</name>"
    # Remove collator if set to no
    data = ("</case_sensitive>"
            "\r\n<collator_enabled>N</collator_enabled>"
            "\r\n<collator_strength>2</collator_strength>"
            "\n    <presorted>")
    assert func(data, "PDI") == "</case_sensitive>\n    <presorted>"
    # Remove create parent folder if set to no
    data = ("</output_file_field>\r\n<create_parent_folder>N"
            "</create_parent_folder>\n   <parameters>")
    assert func(data, "PDI") == "</output_file_field>\n   <parameters>"
    # Remove run configuration setting if none
    data = ("</logging_remote_work>\n"
            "<run_configuration/>\n<parameters>")
    assert func(data, "PDI") == "</logging_remote_work>\n<parameters>"
    data = ("</pass_export>\n"
            "<run_configuration/>\n<parameters>")
    assert func(data, "PDI") == "</pass_export>\n<parameters>"

    # Difference emerging from different PRD versions
    data = ("Somename:   <element-style>\n"
            "Somename:   </element-style>\n")
    assert func(data, "PRD") == ""
    data = ("Somename:   <style:element-style>\n"
            "Somename:   </style:element-style>\n")
    assert func(data, "PRD") == ""


def test_colordiff():
    """Test the builtin diffing."""
    assert kettlediff.colordiff("Abc\nDef\nGhi\nJkl", "Abc\ndef\nGhi") == (
        "\x1b[31m--- None\n"
        "\x1b[0m\n"
        "\x1b[32m+++ None\n"
        "\x1b[0m\n"
        "\x1b[36m@@ -1,4 +1,3 @@\n"
        "\x1b[0m\n Abc\n"
        "\x1b[31m-Def\x1b[0m\n"
        "\x1b[32m+def\x1b[0m\n"
        " Ghi\n"
        "\x1b[31m-Jkl\x1b[0m"
    )


if __name__ == '__main__':
    pytest.main()
