package {namespace_base}.service;

import com.vasl.ario.crudutil.service.CRUDService;
import {namespace_base}.{namespace_dto}.{entity_name}PageQueryParams;
import {namespace_base}.{namespace_entity}.{entity_name};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface {entity_name}Service extends CRUDService<{entity_name}> {
    Page<{entity_name}> getPageByQueryParams({entity_name}PageQueryParams {entity_variable}PageQueryParams, Pageable pageable);
}
