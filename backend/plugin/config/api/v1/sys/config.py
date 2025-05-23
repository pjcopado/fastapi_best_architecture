#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    GetConfigDetail,
    SaveBuiltInConfigParam,
    UpdateConfigParam,
)
from backend.plugin.config.service.config_service import config_service

router = APIRouter()


@router.get('/website', summary='获取网站参数配置', dependencies=[DependsJwtAuth])
async def get_website_config() -> ResponseSchemaModel[list[GetConfigDetail]]:
    config = await config_service.get_built_in_config('website')
    return response_base.success(data=config)


@router.post(
    '/website',
    summary='保存网站参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:website:add')),
        DependsRBAC,
    ],
)
async def save_website_config(objs: list[SaveBuiltInConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, 'website')
    return response_base.success()


@router.get('/protocol', summary='获取用户协议', dependencies=[DependsJwtAuth])
async def get_protocol_config() -> ResponseSchemaModel[list[GetConfigDetail]]:
    config = await config_service.get_built_in_config('protocol')
    return response_base.success(data=config)


@router.post(
    '/protocol',
    summary='保存用户协议',
    dependencies=[
        Depends(RequestPermission('sys:config:protocol:add')),
        DependsRBAC,
    ],
)
async def save_protocol_config(objs: list[SaveBuiltInConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, 'protocol')
    return response_base.success()


@router.get('/policy', summary='获取用户政策', dependencies=[DependsJwtAuth])
async def get_policy_config() -> ResponseSchemaModel[list[GetConfigDetail]]:
    config = await config_service.get_built_in_config('policy')
    return response_base.success(data=config)


@router.post(
    '/policy',
    summary='保存用户政策',
    dependencies=[
        Depends(RequestPermission('sys:config:policy:add')),
        DependsRBAC,
    ],
)
async def save_policy_config(objs: list[SaveBuiltInConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, 'policy')
    return response_base.success()


@router.get('/{pk}', summary='获取参数配置详情', dependencies=[DependsJwtAuth])
async def get_config(pk: Annotated[int, Path(description='参数配置 ID')]) -> ResponseSchemaModel[GetConfigDetail]:
    config = await config_service.get(pk)
    return response_base.success(data=config)


@router.get(
    '',
    summary='分页获取所有参数配置',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_configs(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='参数配置名称')] = None,
    type: Annotated[str | None, Query()] = None,
) -> ResponseSchemaModel[PageData[GetConfigDetail]]:
    config_select = await config_service.get_select(name=name, type=type)
    page_data = await paging_data(db, config_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:add')),
        DependsRBAC,
    ],
)
async def create_config(obj: CreateConfigParam) -> ResponseModel:
    await config_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:edit')),
        DependsRBAC,
    ],
)
async def update_config(pk: Annotated[int, Path(description='参数配置 ID')], obj: UpdateConfigParam) -> ResponseModel:
    count = await config_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:del')),
        DependsRBAC,
    ],
)
async def delete_config(pk: Annotated[list[int], Query(description='参数配置 ID 列表')]) -> ResponseModel:
    count = await config_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
