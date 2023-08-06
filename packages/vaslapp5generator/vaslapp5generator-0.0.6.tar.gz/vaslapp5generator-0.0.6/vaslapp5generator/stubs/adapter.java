package {namespace_base}.{namespace_adapter};

import com.vasl.ario.crudutil.{namespace_adapter}.CRUDAdapter;
import com.vasl.ario.crudutil.repository.RepositoryUtils;
import {namespace_base}.{namespace_adapter_mapper}.{entity_name}AdapterMapper;
import {namespace_base}.{namespace_dto}.{entity_name}Dto;
import {namespace_base}.{namespace_dto}.{entity_name}InputDto;
import {namespace_base}.{namespace_dto}.{entity_name}PageQueryParams;
import {namespace_base}.{namespace_entity}.{entity_name};
import {namespace_base}.{namespace_service}.{entity_name}Service;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

@Component
public class {entity_name}Adapter extends CRUDAdapter<{entity_name}, {entity_name}Dto> {

    private final {entity_name}AdapterMapper mapper;
    private final {entity_name}Service service;

    public {entity_name}Adapter({entity_name}Service {entity_variable}Service) {
        super({entity_variable}Service, {entity_name}AdapterMapper.INSTANCE);
        this.service = {entity_variable}Service;
        mapper = {entity_name}AdapterMapper.INSTANCE;
    }

    public Page<{entity_name}Dto> getAll({entity_name}PageQueryParams {entity_variable}PageQueryParams) {
        return service.getPageByQueryParams(
                {entity_variable}PageQueryParams,
                RepositoryUtils.getPageableFromPageQueryParams({entity_variable}PageQueryParams)
        ).map(mapper::getDto);
    }

    public {entity_name}Dto create({entity_name}InputDto dto) {
        {entity_name} entity = mapper.getEntityFromInputDto(dto);
        entity = service.create(entity);
        return mapper.getDto(entity);
    }

    public {entity_name}Dto update({entity_name}InputDto dto, String id) {
        {entity_name} entity = mapper.getEntityFromInputDto(dto);
        entity.setId(id);
        entity = service.update(entity);
        return mapper.getDto(entity);
    }

}
