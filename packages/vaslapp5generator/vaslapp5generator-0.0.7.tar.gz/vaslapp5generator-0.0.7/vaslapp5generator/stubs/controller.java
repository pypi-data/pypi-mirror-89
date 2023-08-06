package {namespace_base}.{namespace_controller};

import com.vasl.ario.crudutil.api.validation.AddGroup;
import com.vasl.ario.crudutil.api.validation.EditGroup;
import {namespace_base}.{namespace_adapter}.{entity_name}Adapter;
import {namespace_base}.{namespace_dto}.{entity_name}Dto;
import {namespace_base}.{namespace_dto}.{entity_name}InputDto;
import {namespace_base}.{namespace_dto}.{entity_name}PageQueryParams;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;
import io.swagger.annotations.ApiParam;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/api/v1/{module_name}/{entity_kebab}")
public class {entity_name}Controller {

    private final {entity_name}Adapter {entity_variable}Adapter;

    public {entity_name}Controller({entity_name}Adapter {entity_variable}Adapter) {
        this.{entity_variable}Adapter = {entity_variable}Adapter;
    }

    @GetMapping
    @PreAuthorize(value = "hasAnyAuthority('api.v1.{module_name}.{entity_variable}.getAll')")
    @ApiImplicitParams(
            @ApiImplicitParam(name = "Accept-Language", value = "Language", paramType = "header", dataTypeClass = String.class, example = "fa")
    )
    public Page<{entity_name}Dto> getPaginated{entity_names}({entity_name}PageQueryParams {entity_variable}PageQueryParams) {
        return {entity_variable}Adapter.getAll({entity_variable}PageQueryParams);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @PreAuthorize(value = "hasAnyAuthority('api.v1.{module_name}.{entity_variable}.create')")
    @ApiImplicitParams(
            @ApiImplicitParam(name = "Accept-Language", value = "Language", paramType = "header", dataTypeClass = String.class, example = "fa")
    )
    public {entity_name}Dto create{entity_name}(@RequestBody @Validated(AddGroup.class) {entity_name}InputDto {entity_variable}InputDto) {
        return {entity_variable}Adapter.create({entity_variable}InputDto);
    }

    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.ACCEPTED)
    @PreAuthorize(value = "hasAnyAuthority('api.v1.{module_name}.{entity_variable}.update')")
    @ApiImplicitParams(
            @ApiImplicitParam(name = "Accept-Language", value = "Language", paramType = "header", dataTypeClass = String.class, example = "fa")
    )
    public {entity_name}Dto update{entity_name}(@PathVariable("id") String id,
                               @RequestBody @Validated(EditGroup.class) {entity_name}InputDto {entity_variable}InputDto) {
        return {entity_variable}Adapter.update({entity_variable}InputDto, id);
    }

    @GetMapping("/{id}")
    @PreAuthorize(value = "hasAnyAuthority('api.v1.{module_name}.{entity_variable}.get')")
    @ApiImplicitParams(
            @ApiImplicitParam(name = "Accept-Language", value = "Language", paramType = "header", dataTypeClass = String.class, example = "fa")
    )
    public {entity_name}Dto get{entity_name}(@PathVariable("id") @ApiParam(name = "id", example = "12345678990") String id) {
        return {entity_variable}Adapter.get(id);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @PreAuthorize(value = "hasAnyAuthority('api.v1.{module_name}.{entity_variable}.delete')")
    @ApiImplicitParams(
            @ApiImplicitParam(name = "Accept-Language", value = "Language", paramType = "header", dataTypeClass = String.class, example = "fa")
    )
    public void delete{entity_name}(@PathVariable("id") @ApiParam(name = "id", example = "12345678990") String id) {
        {entity_variable}Adapter.delete(id);
    }

}
