import os
from sys import path

from vaslapp5generator.config import *


replacements = {
    'namespace_base': 'com.vasl.ario.{module_name}'.format(module_name=module_name),
    'namespace_dto': 'api.dto.{entity_package}'.format(entity_package=entity_package),
    'namespace_adapter': 'api.adapter',
    'namespace_adapter_mapper': 'api.adapter.mapper',
    'namespace_api_adapter': 'api.adapter',
    'namespace_entity': 'dal.entity.{entity_package}'.format(entity_package=entity_package),
    'namespace_service': 'service',
    'namespace_service_mapper': 'service.mapper',
    'namespace_controller': 'api.controller',
    'namespace_repository': 'dal.repository',
    'namespace_repository_custom': 'dal.repository.custom',

    'entity_name': entity_name,
    'entity_names': entity_names,
    'entity_variable': entity_variable,
    'entity_variables': entity_variables,
    'entity_kebab': entity_kebab,

    'collection_name': collection_name,

    'module_name': module_name,
}


files_classes = {
    'adapter': {
        'namespace': replacements['namespace_adapter'],
        'class_name': '{entity_name}Adapter'.format(entity_name=entity_name),
    },
    'adapter_mapper': {
        'namespace': replacements['namespace_adapter_mapper'],
        'class_name': '{entity_name}AdapterMapper'.format(entity_name=entity_name),
    },
    'controller': {
        'namespace': replacements['namespace_controller'],
        'class_name': '{entity_name}Controller'.format(entity_name=entity_name),
    },
    'dto_input': {
        'namespace': replacements['namespace_dto'],
        'class_name': '{entity_name}InputDto'.format(entity_name=entity_name),
    },
    'dto_output': {
        'namespace': replacements['namespace_dto'],
        'class_name': '{entity_name}Dto'.format(entity_name=entity_name),
    },
    'dto_page_query_params': {
        'namespace': replacements['namespace_dto'],
        'class_name': '{entity_name}PageQueryParams'.format(entity_name=entity_name),
    },
    'entity': {
        'namespace': replacements['namespace_entity'],
        'class_name': entity_name,
    },
    'repository': {
        'namespace': replacements['namespace_repository'],
        'class_name': '{entity_name}Repository'.format(entity_name=entity_name),
    },
    'repository_custom': {
        'namespace': replacements['namespace_repository_custom'],
        'class_name': 'Custom{entity_name}Repository'.format(entity_name=entity_name),
    },
    'repository_custom_impl': {
        'namespace': replacements['namespace_repository_custom'],
        'class_name': 'Custom{entity_name}RepositoryImpl'.format(entity_name=entity_name),
    },
    'service': {
        'namespace': replacements['namespace_service'],
        'class_name': '{entity_name}Service'.format(entity_name=entity_name),
    },
    'service_impl': {
        'namespace': replacements['namespace_service'],
        'class_name': 'Simple{entity_name}Service'.format(entity_name=entity_name),
    },
    'service_mapper': {
        'namespace': replacements['namespace_service_mapper'],
        'class_name': '{entity_name}ServiceMapper'.format(entity_name=entity_name),
    },
}


def main():
    for stub_file_name, java_class_info in files_classes.items():
        stub_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stubs',
                                      '{file_name}.java'.format(file_name=stub_file_name))
        with open(stub_file_path) as stub_file:
            stub_file_content = str(stub_file.read())
            stub_file.close()
            for key, value in replacements.items():
                stub_file_content = stub_file_content.replace('{' + key + '}', value)

            java_class_filename = java_class_info['class_name'] + '.java'
            java_class_namespace = java_class_info['namespace']
            java_class_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                           *java_class_namespace.split('.'), java_class_filename)
            dir_path = os.path.dirname(java_class_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            print('Wrote file: {file}'.format(file=java_class_path))
            with open(java_class_path, 'w') as writable_file:
                writable_file.write(stub_file_content)
                writable_file.close()
    print('Done.')


# if __name__ == '__main__':
#     main()
