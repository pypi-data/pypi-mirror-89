package {namespace_base}.service;

import com.vasl.ario.crudutil.entity.Entity;
import com.vasl.ario.crudutil.service.SimpleCRUDService;
import com.vasl.ario.crudutil.service.exception.DuplicationException;
import com.vasl.ario.crudutil.service.exception.NotFoundException;
import {namespace_base}.{namespace_dto}.{entity_name}PageQueryParams;
import {namespace_base}.{namespace_entity}.{entity_name};
import {namespace_base}.{namespace_repository}.{entity_name}Repository;
import {namespace_base}.{namespace_service_mapper}.{entity_name}ServiceMapper;
import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class Simple{entity_name}Service extends SimpleCRUDService<{entity_name}> implements {entity_name}Service {

    private final {entity_name}Repository repository;
    private final {entity_name}ServiceMapper serviceMapper;
    private final MessageSource messageSource;

    public Simple{entity_name}Service({entity_name}Repository {entity_variable}Repository, {entity_name}ServiceMapper serviceMapper,
                              MessageSource messageSource) {
        super({entity_variable}Repository, {entity_name}ServiceMapper.INSTANCE);
        this.repository = {entity_variable}Repository;
        this.serviceMapper = serviceMapper;
        this.messageSource = messageSource;
    }

    @Override
    public Page<{entity_name}> getPageByQueryParams({entity_name}PageQueryParams {entity_variable}PageQueryParams, Pageable pageable) {
        return repository.findAllByPageQueryParams({entity_variable}PageQueryParams, pageable);
    }

    @Override
    public {entity_name} create({entity_name} entity) {
        try {
            return super.create(entity);
        } catch (DuplicateKeyException exception) {
            throw new DuplicationException(
                    messageSource.getMessage("error.{entity_kebab}.duplicated-name", null, LocaleContextHolder.getLocale())
            );
        }
    }

    @Override
    public void deleteById(String id) {
        // get entity (and throw exception if not found)
        try {
            super.deleteById(id);
        } catch (NotFoundException exception) {
            throw new NotFoundException(messageSource.getMessage("error.{entity_kebab}.not-found", null, LocaleContextHolder.getLocale()));
        }
    }

    public {entity_name} update({entity_name} newOne) {
        {entity_name} existing = getById(newOne.getId());

        Entity existingBaseClone = null;
        try {
            existingBaseClone = (Entity) (existing).clone();
        } catch (CloneNotSupportedException ignored) {
        }
        serviceMapper.updateEntity(existing, newOne);
        serviceMapper.updateBaseEntity(existing, existingBaseClone);

        return repository.save(existing);
    }

}
