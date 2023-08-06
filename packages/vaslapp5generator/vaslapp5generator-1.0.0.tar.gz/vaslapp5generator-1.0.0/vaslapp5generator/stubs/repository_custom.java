package {namespace_base}.{namespace_repository_custom};

import {namespace_base}.{namespace_dto}.{entity_name}PageQueryParams;
import {namespace_base}.{namespace_entity}.{entity_name};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface Custom{entity_name}Repository {
    Page<{entity_name}> findAllByPageQueryParams({entity_name}PageQueryParams {entity_variable}PageQueryParams, Pageable pageable);
}
