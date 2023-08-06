package {namespace_base}.{namespace_repository_custom};

import {namespace_base}.{namespace_dto}.{entity_name}PageQueryParams;
import {namespace_base}.{namespace_entity}.{entity_name};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.support.PageableExecutionUtils;
import org.springframework.stereotype.Repository;
import org.springframework.util.ObjectUtils;

import java.util.List;

@Repository
public class Custom{entity_name}RepositoryImpl implements Custom{entity_name}Repository {

    private final MongoTemplate mongoTemplate;

    public Custom{entity_name}RepositoryImpl(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    @Override
    public Page<{entity_name}> findAllByPageQueryParams({entity_name}PageQueryParams {entity_variable}PageQueryParams, Pageable pageable) {
        Query query = new Query().with(pageable);
        if (!ObjectUtils.isEmpty({entity_variable}PageQueryParams.getName())) {
            query.addCriteria(Criteria.where("name").regex(".*" + {entity_variable}PageQueryParams.getName().trim() + ".*", "i"));
        }
        List<{entity_name}> list = mongoTemplate.find(query, {entity_name}.class);
        return PageableExecutionUtils.getPage(
                list, pageable, () -> mongoTemplate.count(query.skip(-1).limit(-1), {entity_name}.class));
    }


}
