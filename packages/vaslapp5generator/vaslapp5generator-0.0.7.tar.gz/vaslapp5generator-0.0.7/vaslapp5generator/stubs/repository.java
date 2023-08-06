package {namespace_base}.{namespace_repository};

import {namespace_base}.{namespace_entity}.{entity_name};
import {namespace_base}.{namespace_repository_custom}.Custom{entity_name}Repository;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface {entity_name}Repository extends PagingAndSortingRepository<{entity_name}, String>, Custom{entity_name}Repository {
}
