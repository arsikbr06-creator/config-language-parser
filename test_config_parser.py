"""
Comprehensive tests for Configuration Language Parser
Tests all language constructs including nested structures
"""

import pytest
import sys
import os
from config_lang_parser import ConfigParser


class TestBasicTypes:
    """Test basic data types"""
    
    def test_positive_number(self):
        parser = ConfigParser()
        result = parser.parse_string("42")
        assert result == [42]
    
    def test_negative_number(self):
        parser = ConfigParser()
        result = parser.parse_string("-15")
        assert result == [-15]
    
    def test_zero(self):
        parser = ConfigParser()
        result = parser.parse_string("0")
        assert result == [0]
    
    def test_large_number(self):
        parser = ConfigParser()
        result = parser.parse_string("123456789")
        assert result == [123456789]
    
    def test_simple_string(self):
        parser = ConfigParser()
        result = parser.parse_string('@"Hello World"')
        assert result == ["Hello World"]
    
    def test_empty_string(self):
        parser = ConfigParser()
        result = parser.parse_string('@""')
        assert result == [""]
    
    def test_string_with_special_chars(self):
        parser = ConfigParser()
        result = parser.parse_string('@"Hello, 123! @#$"')
        assert result == ["Hello, 123! @#$"]


class TestArrays:
    """Test array structures"""
    
    def test_empty_array(self):
        parser = ConfigParser()
        result = parser.parse_string("[]")
        assert result == [[]]
    
    def test_number_array(self):
        parser = ConfigParser()
        result = parser.parse_string("[1, 2, 3, 4, 5]")
        assert result == [[1, 2, 3, 4, 5]]
    
    def test_string_array(self):
        parser = ConfigParser()
        result = parser.parse_string('[@"hello", @"world"]')
        assert result == [["hello", "world"]]
    
    def test_mixed_array(self):
        parser = ConfigParser()
        result = parser.parse_string('[1, @"text", -5]')
        assert result == [[1, "text", -5]]
    
    def test_nested_arrays(self):
        parser = ConfigParser()
        result = parser.parse_string("[[1, 2], [3, 4]]")
        assert result == [[[1, 2], [3, 4]]]
    
    def test_deeply_nested_arrays(self):
        parser = ConfigParser()
        result = parser.parse_string("[[[1, 2]], [[3, 4]]]")
        assert result == [[[[1, 2]], [[3, 4]]]]


class TestDictionaries:
    """Test dictionary structures"""
    
    def test_empty_dict(self):
        parser = ConfigParser()
        result = parser.parse_string("{}")
        assert result == [{}]
    
    def test_simple_dict(self):
        parser = ConfigParser()
        result = parser.parse_string("{name => @\"John\", age => 30}")
        assert result == [{"name": "John", "age": 30}]
    
    def test_dict_with_array_value(self):
        parser = ConfigParser()
        result = parser.parse_string("{items => [1, 2, 3]}")
        assert result == [{"items": [1, 2, 3]}]
    
    def test_nested_dict(self):
        parser = ConfigParser()
        result = parser.parse_string("{person => {name => @\"Alice\", age => 25}}")
        assert result == [{"person": {"name": "Alice", "age": 25}}]
    
    def test_dict_with_multiple_types(self):
        parser = ConfigParser()
        result = parser.parse_string(
            '{name => @"Bob", age => 35, scores => [90, 85, 88]}'
        )
        assert result == [{"name": "Bob", "age": 35, "scores": [90, 85, 88]}]


class TestConstants:
    """Test constant declarations and evaluation"""
    
    def test_constant_number(self):
        parser = ConfigParser()
        result = parser.parse_string("let x = 42\n.(x).")
        assert result == [42]
    
    def test_constant_string(self):
        parser = ConfigParser()
        result = parser.parse_string('let msg = @"Hello"\n.(msg).')
        assert result == ["Hello"]
    
    def test_constant_array(self):
        parser = ConfigParser()
        result = parser.parse_string("let arr = [1, 2, 3]\n.(arr).")
        assert result == [[1, 2, 3]]
    
    def test_constant_dict(self):
        parser = ConfigParser()
        result = parser.parse_string(
            'let config = {port => 8080, host => @"localhost"}\n.(config).'
        )
        assert result == [{"port": 8080, "host": "localhost"}]
    
    def test_multiple_constants(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "let a = 10\nlet b = 20\n[.(a)., .(b).]"
        )
        assert result == [[10, 20]]
    
    def test_constant_in_array(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "let val = 100\n[.(val)., 200, 300]"
        )
        assert result == [[100, 200, 300]]
    
    def test_constant_in_dict(self):
        parser = ConfigParser()
        result = parser.parse_string(
            'let port = 8080\n{server_port => .(port).}'
        )
        assert result == [{"server_port": 8080}]
    
    def test_undefined_constant_error(self):
        parser = ConfigParser()
        with pytest.raises(Exception):
            parser.parse_string(".(undefined).")


class TestComments:
    """Test comment handling"""
    
    def test_single_comment(self):
        parser = ConfigParser()
        result = parser.parse_string("; This is a comment\n42")
        assert result == [42]
    
    def test_multiple_comments(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "; Comment 1\n; Comment 2\n123"
        )
        assert result == [123]
    
    def test_comment_with_value(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "; Array of numbers\n[1, 2, 3]"
        )
        assert result == [[1, 2, 3]]
    
    def test_inline_comment_behavior(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "42\n; This is a comment"
        )
        assert result == [42]


class TestComplexNesting:
    """Test complex nested structures"""
    
    def test_array_of_dicts(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "[{name => @\"Alice\", age => 25}, {name => @\"Bob\", age => 30}]"
        )
        assert result == [[
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30}
        ]]
    
    def test_dict_with_nested_arrays_and_dicts(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "{users => [{name => @\"Alice\"}, {name => @\"Bob\"}], count => 2}"
        )
        assert result == [{
            "users": [{"name": "Alice"}, {"name": "Bob"}],
            "count": 2
        }]
    
    def test_deeply_nested_structure(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "{level1 => {level2 => {level3 => [1, 2, 3]}}}"
        )
        assert result == [{
            "level1": {
                "level2": {
                    "level3": [1, 2, 3]
                }
            }
        }]
    
    def test_constants_with_nested_structures(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "let defaults = {timeout => 30, retries => 3}\n"
            "{config => .(defaults)., enabled => 1}"
        )
        assert result == [{
            "config": {"timeout": 30, "retries": 3},
            "enabled": 1
        }]


class TestMultipleStatements:
    """Test multiple values in file"""
    
    def test_multiple_values(self):
        parser = ConfigParser()
        result = parser.parse_string("42\n@\"hello\"\n[1, 2, 3]")
        assert result == [42, "hello", [1, 2, 3]]
    
    def test_constants_and_values(self):
        parser = ConfigParser()
        result = parser.parse_string(
            "let x = 10\n.(x).\nlet y = 20\n.(y)."
        )
        assert result == [10, 20]


class TestYAMLConversion:
    """Test YAML output generation"""
    
    def test_number_to_yaml(self):
        parser = ConfigParser()
        data = parser.parse_string("42")
        yaml_output = parser.to_yaml(data)
        assert yaml_output.strip() == "42"
    
    def test_array_to_yaml(self):
        parser = ConfigParser()
        data = parser.parse_string("[1, 2, 3]")
        yaml_output = parser.to_yaml(data)
        assert "- 1" in yaml_output
        assert "- 2" in yaml_output
        assert "- 3" in yaml_output
    
    def test_dict_to_yaml(self):
        parser = ConfigParser()
        data = parser.parse_string("{name => @\"test\", value => 42}")
        yaml_output = parser.to_yaml(data)
        assert "name: test" in yaml_output
        assert "value: 42" in yaml_output


class TestErrorHandling:
    """Test error detection and messages"""
    
    def test_invalid_syntax(self):
        parser = ConfigParser()
        with pytest.raises(SyntaxError):
            parser.parse_string("{ invalid syntax")
    
    def test_undefined_constant(self):
        parser = ConfigParser()
        with pytest.raises(Exception):
            parser.parse_string(".(notdefined).")
    
    def test_file_not_found(self):
        parser = ConfigParser()
        with pytest.raises(FileNotFoundError):
            parser.parse_file("nonexistent_file.conf")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
