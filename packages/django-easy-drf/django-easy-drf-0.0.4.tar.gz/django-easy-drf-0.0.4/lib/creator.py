#!/usr/bin/env python3

import ast
import astunparse
import re


def create_serializers_and_views():
    with open('lib/models.py', 'r') as file:
        models_ast = ast.parse(file.read())


    serializers_ast = _read_template('serializers')
    views_ast = _read_template('views')
    urls_ast = _read_template('urls')

    model_classes = [clss for clss in models_ast.body if clss.__class__ is ast.ClassDef]

    for mc in model_classes:
        class_fields = [field for field in mc.body if field.__class__ is ast.Assign]

        serializers_ast.body.append(_read_template('serializer', model_class_name=mc.name, 
            field_names=", ".join([f"'{field_name.targets[0].id}'" for field_name in class_fields])))

        views_ast.body.append(_read_template('viewset', model_class_name=mc.name))


        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        mc_name_snake = pattern.sub('-', mc.name).lower()
        urls_ast.body.insert(len(urls_ast.body)-1, _read_template('url', model_class_name=mc.name, model_class_name_snake=mc_name_snake))

    _write_result('lib/serializers.py', serializers_ast)
    _write_result('lib/views.py', views_ast)
    _write_result('lib/urls.py', urls_ast)




def _read_template(template_name, **kwargs):
    with open(f'lib/templates/{template_name}', 'r') as template:
        return ast.parse(template.read().format(**kwargs))

def _write_result(result_file_name, ast_name):
    with open(result_file_name, 'w') as wfile:
        wfile.write(astunparse.unparse(ast_name)) 

if __name__ == '__main__':
    create_serializers_and_views()