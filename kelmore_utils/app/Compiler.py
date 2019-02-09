import os.path
import sys
from dataclasses import dataclass

import re
from typing import Type, Any, List, Set, Iterable

from ..Arrays import Arrays
from ..Files import Files


@dataclass
class ClassLines:
    class_name: str
    class_lines: List[str]

    def __init__(self, class_name: str, class_lines: List[str]):
        self.class_name = class_name
        self.class_lines = class_lines


class Imports:
    import_path: str
    text: str

    lines: List[str]

    all_imports: Set[str]
    python_imports: Set[str]
    workspace_imports: Set[str]
    workspace_import_classes: Set[str]

    class_names: Set[str]
    class_files: List[ClassLines]
    global_variables: List[str]

    def __init__(self, import_path: str):
        self.lines = []

        self.all_imports = set()
        self.python_imports = set()
        self.workspace_imports = set()
        self.workspace_import_classes = set()

        self.class_files = []
        self.global_variables = []

        self.import_path = import_path
        self._parse_text()
        self._parse_imports()
        self._parse_classes()
        self._parse_variables()

        self.class_names = {y for y in [x.class_name for x in self.class_files]}

    @staticmethod
    def _check_line(line: str):
        stripped: str = line.strip()
        if stripped == '' or stripped.startswith('#'):
            return ''

        return line

    def _parse_text(self):
        self.text = Files.read_file_(self.import_path)
        self.lines = [Imports._check_line(x) for x in self.text.split('\n')]

    def _parse_imports(self):
        to_remove: Set[int] = set()
        num_lines: int = len(self.lines)
        for line_idx in range(num_lines):
            line = self.lines[line_idx]
            stripped: str = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                past_line: line = self.lines[line_idx - 1] if line_idx - 1 < num_lines else ''
                to_remove.add(line_idx)

                if 'try' in past_line or 'except' in past_line:
                    to_remove.add(line_idx - 1)

                line = line.replace('\\\\', '').strip()
                while (line.endswith('\\') or line.endswith('\\\\')) and \
                        line_idx < len(self.lines):
                    line_idx += 1
                    line = line.replace('\\', '').strip()
                    line += ' ' + self.lines[line_idx].replace('\\\\', '').strip()
                    to_remove.add(line_idx)

                self.all_imports.add(line)

        self.lines = Arrays.remove_indexes(self.lines, list(to_remove))

    def _parse_classes(self):
        to_remove: Set[int] = set()
        for line_idx in range(len(self.lines)):
            line = self.lines[line_idx]

            if line.startswith('class '):
                class_lines: List[str] = [line]

                line = line[line.index('class ') + 6:]
                if '(' in line:
                    class_name: str = line[:line.rindex('(')]
                elif ':' in line:
                    class_name = line[:line.rindex(':')]
                else:
                    class_name = None

                if class_name is not None:
                    to_remove.add(line_idx)
                    while line_idx + 1 < len(self.lines):
                        line_idx += 1
                        next_line: str = self.lines[line_idx]

                        if next_line.startswith('    ') or next_line == '':
                            class_lines.append(next_line)
                            to_remove.add(line_idx)
                        else:
                            break

                    self.class_files.append(ClassLines(class_name, class_lines))

        Arrays.remove_indexes(self.lines, list(to_remove))

    def _parse_variables(self):
        # Whatever's left is a global variable :)
        self.global_variables = self.lines[:]
        self.global_variables = [x for x in self.global_variables if not x.startswith('from ')]

    def fix_imports(self, all_class_names: Set[str]):
        for class_name in all_class_names:
            for imports in self.all_imports:
                if class_name in imports:
                    self.workspace_imports.add(imports)
                    continue

        # self.workspace_import_classes = set([x[x.index('import ') + 7:]
        #   for x in self.workspace_imports])
        self.python_imports = [x for x in self.all_imports if x not in self.workspace_imports]
        # self.workspace_imports = [x for x in self.all_imports if x in all_class_names]

        for imports in self.workspace_imports:
            class_names: List[str] = imports[imports.index('import ') + 7:].split(',')
            class_names = [x.strip() for x in class_names]

            for class_name in class_names:
                if ' as ' in class_name:
                    class_name = class_name[:class_name.index(' as ')]
                self.workspace_import_classes.add(class_name)

    @staticmethod
    def remove_comments(lines: List[str]):
        to_remove: List[int] = []
        for line_idx, line in enumerate(lines):
            if line.strip().startswith('#'):
                to_remove.append(line_idx)
        Arrays.remove_indexes(lines, to_remove)


class Compiler:
    main_module_path: str
    to_compile: Type[Any]

    def __init__(self, main_module_path: str, to_compile: Type[Any]):
        self.main_module_path = main_module_path
        self.to_compile = to_compile

    def compile(self):  # , file_path: str, file_name: str = 'AppCompact.py'):
        # compile: Type[Any] = self.to_compile

        # output_file: Files = Files(file_path=file_path, file_name=file_name)
        output: str = ''

        modules: List[str] = list(sys.modules.keys())

        # print(modules)

        modules = [x for x in modules if 'lib.' in x]

        python_file_paths: Set[str] = set()
        python_imports: List[Imports] = []

        # From workspace
        all_class_names: Set[str] = set()
        all_python_imports: Set[str] = set()

        for module in modules:
            module = os.path.join(self.main_module_path, module.replace('.', '/'))
            temp_check = module + '.py'

            if os.path.exists(temp_check):
                python_file_paths.add(temp_check)
            elif os.path.isdir(module):
                Compiler.add_directory_to_paths(module, python_file_paths)

        print('Found {} files to parse\n'.format(len(python_file_paths)))
        print('Parsing...')
        for new_file_path in python_file_paths:
            python_imports.append(Imports(new_file_path))

        for imports in python_imports:
            all_class_names = all_class_names.union(imports.class_names)

        for imports in python_imports:
            imports.fix_imports(all_class_names)
            all_python_imports = all_python_imports.union(imports.python_imports)

        print('All classes, class names, workspace imports, and python imports parsed')
        print('Creating the big guy')

        python_imports.sort(key=lambda x: len(x.workspace_imports))

        temp_python_imports = list(all_python_imports)
        temp_python_imports.sort()

        output += '\n'.join(temp_python_imports) + '\n\n'

        # print(output)

        output = Compiler.add_classes_to_output(output, python_imports)
        output = re.sub(r'\n\n+', '\n\n', output)

        # TODO: Save to file rather than print :P
        print(output)

        print('Done')

    @staticmethod
    def fix_global_variables(output: str, global_variables: List[str]) -> str:
        variables: str = ''
        for variable in global_variables:
            if variable not in output or variable.strip() == '':
                variables += variable + '\n'

        to_remove: List[int] = []
        module_path_check: List[str] = variables.split('\n')
        for line_idx in range(1, len(module_path_check) - 1):
            line: str = module_path_check[line_idx]

            if 'module_path' in line and line.startswith('    '):
                to_remove.append(line_idx)

        Arrays.remove_indexes(module_path_check, to_remove)
        module_path_check = [x for x in module_path_check if 'try' not in x and 'except' not in x]

        return '\n'.join(module_path_check)

    @staticmethod
    def add_classes_to_output(output: str, module_list: List[Imports]) -> str:
        added_classes: Set[str] = set()

        while module_list:
            to_remove: List[int] = []
            for imports_idx, imports in enumerate(module_list):
                imports = module_list[imports_idx]

                if not imports.workspace_import_classes or \
                        Compiler.check_all_in(list(imports.workspace_import_classes),
                                              added_classes):
                    to_remove.append(imports_idx)
                    output = Compiler._add_class_to_output(output, imports, added_classes)

            # TODO: Find fix for last step - like 6 classes left of 52
            if not to_remove:
                output = Compiler._add_class_to_output(output, module_list.pop(0), added_classes)

            Arrays.remove_indexes(module_list, to_remove)

        return output

    @staticmethod
    def _add_class_to_output(output: str, imports: Imports, added_classes: Set[str]) -> str:
        output += '\n\n{}\n\n' \
            .format(Compiler.fix_global_variables(output, imports.global_variables))

        for class_file in imports.class_files:
            output += '\n\n{}\n\n'.format('\n'.join(class_file.class_lines))
            added_classes.add(class_file.class_name)
        Compiler._add_variables_helper(imports.global_variables, added_classes)
        return output

    @staticmethod
    # TODO: This removes most of the "module_paths" variables across all classes,
    # TODO:     but still needs some work
    # TODO: Probably going to have to go back to naming all module variables "module_path"
    # TODO: And then probably remove path_appends and module_paths all together
    def _add_variables_helper(global_variables: List[str], added_classes: Set[str]):
        for variable in global_variables:
            if not variable.startswith('    ') and ' = ' in variable:
                if ':' in variable:
                    added_classes.add(variable[:variable.index(':')])
                else:
                    added_classes.add(variable[:variable.index(' ')])

    # TODO: Move to arrays
    @staticmethod
    def check_all_in(searching: List[Any], to_be_searched: Iterable[Any]):
        for item in searching:
            if item not in to_be_searched:
                return False
        return True

    @staticmethod
    def sort_by_import_size(import_a: Imports, import_b: Imports):
        return len(import_a.workspace_imports) - len(import_b.workspace_imports)

    @staticmethod
    def add_directory_to_paths(directory: str, file_paths: Set[str]) -> Set[str]:
        if os.path.isdir(directory):
            file_paths = file_paths.union(Files.get_all_files_(directory))
        return file_paths
