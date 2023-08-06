package {namespace_base}.{namespace_adapter}.mapper;

import com.vasl.ario.crudutil.{namespace_adapter}.mapper.CRUDAdapterMapper;
import {namespace_base}.{namespace_dto}.{entity_name}Dto;
import {namespace_base}.{namespace_dto}.{entity_name}InputDto;
import {namespace_base}.{namespace_entity}.{entity_name};
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface {entity_name}AdapterMapper extends CRUDAdapterMapper<{entity_name}, {entity_name}Dto> {

    {entity_name}AdapterMapper INSTANCE = Mappers.getMapper({entity_name}AdapterMapper.class);

    {entity_name} getEntityFromInputDto({entity_name}InputDto dto);
}
