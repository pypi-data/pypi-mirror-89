package {namespace_base}.{namespace_dto};

import com.vasl.ario.crudutil.api.validation.AddGroup;
import com.vasl.ario.crudutil.api.validation.EditGroup;
import lombok.Data;

import javax.validation.constraints.NotEmpty;

@Data
public class {entity_name}InputDto {

    @NotEmpty(groups = {AddGroup.class, EditGroup.class})
    private String name;

}
