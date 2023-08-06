"""
create node by ArkFBP cli
"""
import os

from django.core.management import CommandError
from django.core.management.templates import TemplateCommand

import arkfbp

NODE_CLASS_MAP = {
    'base': 'Node',
    'start': 'StartNode',
    'stop': 'StopNode',
    'function': 'FunctionNode',
    'if': 'IFNode',
    'loop': 'LoopNode',
    'nop': 'NopNode',
    'api': 'APINode',
    'test': 'TestNode',
    'auth_token': 'AuthTokenNode',
    'serializer': 'SerializerNode',
    'field': 'FieldNode',
    'char_field': 'CharFieldNode',
}


class Command(TemplateCommand):
    """
    native command of django
    """
    help = ("Creates a Arkfbp Node for the given node name.")
    missing_args_message = "You must provide an node name."

    @staticmethod
    def _file_name(node_name):
        """
        convert to node file name
        """
        # pylint: disable=invalid-name
        file_name = [node_name[0].lower()]
        for x in node_name[1:]:
            if x.isupper():
                file_name.append(f'_{x.lower()}')
            else:
                file_name.append(x)
        return ''.join(file_name)

    @staticmethod
    def _class_name(node_name):
        """
        convert to node class name
        """
        # pylint: disable=invalid-name
        # 1）`_`后面字母大写
        capital_idx = [0]
        for idx, x in enumerate(node_name):
            if x == '_' and idx + 1 <= len(node_name):
                capital_idx.append(idx + 1)

        node_name = list(node_name)
        for x in capital_idx:
            node_name[x] = node_name[x].upper()
        node_name = ''.join(node_name)
        # 2）去除`_`
        return node_name.replace('_', '')

    # pylint: disable=arguments-differ
    def handle(self, **options):
        node_name = options.pop('name')
        target = options.pop('topdir')
        base_class = options.pop('class')
        node_id = options.pop('id')

        if node_id is None:
            raise CommandError('Node ID Required.')

        app_name = self._file_name(node_name)
        camel_case_node_name = self._class_name(node_name)

        if base_class:
            clz = NODE_CLASS_MAP.get(base_class.lower(), None)
            if not clz:
                raise CommandError('Invalid Node Class.')
            options.update(node_base_class=clz)

        if not target:
            target = os.getcwd()

        options.update(camel_case_node_name=camel_case_node_name)
        options.update(node_id=node_id)
        options.update(template=f'file://{arkfbp.__path__[0]}/common/django/conf/node_template')

        super().handle('app', app_name, target, **options)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--topdir', type=str, help='Specifies the file path for the node.')
        parser.add_argument('--class',
                            type=str,
                            help='Select the class that the node needs to inherit from.',
                            default='base',
                            choices=NODE_CLASS_MAP.keys())
        parser.add_argument('--id',
                            type=str,
                            help='Specifies the ID for the node(No practical use, '
                            'currently only available for vscode plug-ins).')
