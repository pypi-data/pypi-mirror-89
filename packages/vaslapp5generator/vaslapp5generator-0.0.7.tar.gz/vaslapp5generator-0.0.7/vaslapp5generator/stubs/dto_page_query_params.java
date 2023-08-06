package {namespace_base}.{namespace_dto};

import com.vasl.ario.crudutil.service.model.PageQueryParams;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class {entity_name}PageQueryParams extends PageQueryParams {
    private String name;
}
