package {namespace_base}.{namespace_service_mapper};

import com.vasl.ario.crudutil.{namespace_service_mapper}.CRUDServiceMapper;
import {namespace_base}.{namespace_entity}.{entity_name};
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface {entity_name}ServiceMapper extends CRUDServiceMapper<{entity_name}> {
    {entity_name}ServiceMapper INSTANCE = Mappers.getMapper({entity_name}ServiceMapper.class);
}
