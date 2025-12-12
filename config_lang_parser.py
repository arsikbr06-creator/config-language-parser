"""
Configuration Language Parser
Parses educational configuration language and converts to YAML
"""

from lark import Lark, Transformer, v_args, Tree, Token
from lark.exceptions import LarkError
import yaml
import sys
import argparse
from typing import Any, Dict, List, Union


# Grammar for the configuration language
GRAMMAR = r"""
    start: statement*

    ?statement: comment
              | constant_decl
              | value

    comment: ";" COMMENT_TEXT?

    constant_decl: "let" NAME "=" value

    ?value: number
          | string
          | array
          | dict
          | const_expr

    number: SIGNED_NUMBER
    
    string: "@\"" STRING_CONTENT? "\""

    array: "[" [value ("," value)*] "]"

    dict: "{" [dict_pair ("," dict_pair)*] "}"
    
    dict_pair: NAME "=>" value

    const_expr: ".(" NAME ")."

    COMMENT_TEXT: /[^\n]+/
    
    STRING_CONTENT: /[^"]+/

    NAME: /[a-z][a-z0-9_]*/
    
    SIGNED_NUMBER: /[+-]?([1-9][0-9]*|0)/

    %import common.WS
    %ignore WS
"""


class ConfigTransformer(Transformer):
    """Transforms parse tree into Python data structures"""
    
    def __init__(self):
        super().__init__()
        self.constants: Dict[str, Any] = {}
        self.result: List[Any] = []
    
    def start(self, statements):
        """Process all statements and return non-comment results"""
        return [s for s in statements if s is not None]
    
    def comment(self, args):
        """Comments are ignored"""
        return None
    
    def number(self, args):
        """Convert number token to int"""
        return int(args[0])
    
    def string(self, args):
        """Extract string content"""
        # May receive STRING_CONTENT or nothing (empty string)
        if args and len(args) > 0:
            return str(args[0])
        return ""
    
    def array(self, items):
        """Create array/list"""
        # Filter out None from optional items
        return [item for item in items if item is not None]
    
    def dict(self, pairs):
        """Create dictionary from pairs"""
        result = {}
        for pair in pairs:
            if isinstance(pair, tuple) and len(pair) == 2:
                key, value = pair
                result[key] = value
        return result
    
    def dict_pair(self, args):
        """Create key-value pair"""
        return (str(args[0]), args[1])
    
    def constant_decl(self, args):
        """Store constant definition"""
        name_str = str(args[0])
        self.constants[name_str] = args[1]
        return None
    
    def const_expr(self, args):
        """Evaluate constant expression"""
        name_str = str(args[0])
        if name_str not in self.constants:
            raise ValueError(f"Undefined constant: {name_str}")
        return self.constants[name_str]
    
    def NAME(self, token):
        """Pass through NAME tokens as strings"""
        return str(token)


class ConfigParser:
    """Main parser class for configuration language"""
    
    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr')
    
    def parse_file(self, filepath: str) -> List[Any]:
        """
        Parse configuration file and return data structures
        
        Args:
            filepath: Path to input configuration file
            
        Returns:
            List of parsed values
            
        Raises:
            FileNotFoundError: If file doesn't exist
            SyntaxError: If parsing fails
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_string(content)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        except LarkError as e:
            raise SyntaxError(f"Syntax error in configuration file: {e}")
    
    def parse_string(self, content: str) -> List[Any]:
        """
        Parse configuration string
        
        Args:
            content: Configuration language content
            
        Returns:
            List of parsed values
            
        Raises:
            SyntaxError: If parsing fails
        """
        try:
            tree = self.parser.parse(content)
            transformer = ConfigTransformer()
            result = transformer.transform(tree)
            return result
        except LarkError as e:
            raise SyntaxError(f"Syntax error: {e}")
    
    def to_yaml(self, data: Union[List[Any], Any]) -> str:
        """
        Convert parsed data to YAML format
        
        Args:
            data: Parsed configuration data
            
        Returns:
            YAML formatted string
        """
        # Ensure data is a list
        if not isinstance(data, list):
            data = [data]
            
        if len(data) == 0:
            return ""
        elif len(data) == 1:
            output = yaml.dump(data[0], allow_unicode=True, sort_keys=False, explicit_end=False)
            # Remove explicit end marker if present
            if output.endswith('...\n'):
                output = output[:-4] + '\n'
            return output
        else:
            output = yaml.dump(data, allow_unicode=True, sort_keys=False, explicit_end=False)
            if output.endswith('...\n'):
                output = output[:-4] + '\n'
            return output


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Convert educational configuration language to YAML'
    )
    parser.add_argument(
        'input_file',
        help='Path to input configuration file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)',
        default=None
    )
    
    args = parser.parse_args()
    
    try:
        config_parser = ConfigParser()
        data = config_parser.parse_file(args.input_file)
        yaml_output = config_parser.to_yaml(data)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(yaml_output)
            print(f"Output written to {args.output}", file=sys.stderr)
        else:
            print(yaml_output, end='')
        
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except SyntaxError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
