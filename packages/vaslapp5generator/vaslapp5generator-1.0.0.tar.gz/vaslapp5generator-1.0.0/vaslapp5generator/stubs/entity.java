package {namespace_base}.{namespace_entity};

import com.vasl.ario.crudutil.entity.Entity;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@EqualsAndHashCode(callSuper = true)
@Data
@Document(collection = "{collection_name}")
public class {entity_name} extends Entity {
    private String name;
}
