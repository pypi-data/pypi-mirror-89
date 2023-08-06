import argparse
import json
import os


def main():
    current_dir = os.getcwd()

    parser = argparse.ArgumentParser(description='Vaslapp 5 generator')
    parser.add_argument('option', type=str, help='Enter action to generate (config, entity)', nargs=1)
    args = parser.parse_args()
    option = args.option

    option = option[0]

    sample_config = open(os.path.join(os.path.dirname(__file__), 'sample-config.json')).read()

    if option == 'config':
        with open(os.path.join(current_dir, 'va-config.json'), 'w') as config_file:
            config_file.write(sample_config)

    elif option == 'entity':

        config = json.loads(open(os.path.join(current_dir, 'va-config.json')).read())

        replacements = {
            'namespace_base': 'com.vasl.ario.{module_name}'.format(module_name=config['module_name']),
            'namespace_dto': 'api.dto.{entity_package}'.format(entity_package=config['entity_package']),
            'namespace_adapter': 'api.adapter',
            'namespace_adapter_mapper': 'api.adapter.mapper',
            'namespace_api_adapter': 'api.adapter',
            'namespace_entity': 'dal.entity.{entity_package}'.format(entity_package=config['entity_package']),
            'namespace_service': 'service',
            'namespace_service_mapper': 'service.mapper',
            'namespace_controller': 'api.controller',
            'namespace_repository': 'dal.repository',
            'namespace_repository_custom': 'dal.repository.custom',

            'entity_name': config['entity_name'],
            'entity_names': config['entity_names'],
            'entity_variable': config['entity_variable'],
            'entity_variables': config['entity_variables'],
            'entity_kebab': config['entity_kebab'],

            'collection_name': config['collection_name'],

            'module_name': config['module_name'],
        }

        files_classes = {
            'adapter': {
                'namespace': replacements['namespace_adapter'],
                'class_name': '{entity_name}Adapter'.format(entity_name=config['entity_name']),
            },
            'adapter_mapper': {
                'namespace': replacements['namespace_adapter_mapper'],
                'class_name': '{entity_name}AdapterMapper'.format(entity_name=config['entity_name']),
            },
            'controller': {
                'namespace': replacements['namespace_controller'],
                'class_name': '{entity_name}Controller'.format(entity_name=config['entity_name']),
            },
            'dto_input': {
                'namespace': replacements['namespace_dto'],
                'class_name': '{entity_name}InputDto'.format(entity_name=config['entity_name']),
            },
            'dto_output': {
                'namespace': replacements['namespace_dto'],
                'class_name': '{entity_name}Dto'.format(entity_name=config['entity_name']),
            },
            'dto_page_query_params': {
                'namespace': replacements['namespace_dto'],
                'class_name': '{entity_name}PageQueryParams'.format(entity_name=config['entity_name']),
            },
            'entity': {
                'namespace': replacements['namespace_entity'],
                'class_name': config['entity_name'],
            },
            'repository': {
                'namespace': replacements['namespace_repository'],
                'class_name': '{entity_name}Repository'.format(entity_name=config['entity_name']),
            },
            'repository_custom': {
                'namespace': replacements['namespace_repository_custom'],
                'class_name': 'Custom{entity_name}Repository'.format(entity_name=config['entity_name']),
            },
            'repository_custom_impl': {
                'namespace': replacements['namespace_repository_custom'],
                'class_name': 'Custom{entity_name}RepositoryImpl'.format(entity_name=config['entity_name']),
            },
            'service': {
                'namespace': replacements['namespace_service'],
                'class_name': '{entity_name}Service'.format(entity_name=config['entity_name']),
            },
            'service_impl': {
                'namespace': replacements['namespace_service'],
                'class_name': 'Simple{entity_name}Service'.format(entity_name=config['entity_name']),
            },
            'service_mapper': {
                'namespace': replacements['namespace_service_mapper'],
                'class_name': '{entity_name}ServiceMapper'.format(entity_name=config['entity_name']),
            },
        }

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
                java_class_path = os.path.join(current_dir, 'vaslapp5-{entity}'.format(entity=config['entity_name']),
                                               *java_class_namespace.split('.'), java_class_filename)
                dir_path = os.path.dirname(java_class_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                print('Wrote file: {file}'.format(file=java_class_path))
                with open(java_class_path, 'w') as writable_file:
                    writable_file.write(stub_file_content)
                    writable_file.close()
    print('Done.')


if __name__ == '__main__':
    main()
