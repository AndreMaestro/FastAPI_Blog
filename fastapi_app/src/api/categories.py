from typing import List
from fastapi import APIRouter, status, Depends, Query

from schemas.categories import CategoryResponseSchema, CategoryCreateSchema, CategoryUpdateSchema
from domain.category.use_cases.get_category_by_slug import GetCategoryBySlugUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.create_category import CreateCategoryUseCase
from domain.category.use_cases.update_category import UpdateCategoryUseCase
from domain.category.use_cases.delete_category import DeleteCategoryUseCase
from domain.category.use_cases.get_all_categories import GetAllCategoriesUseCase

from api.depends import get_get_category_by_slug_use_case, get_get_category_by_id_use_case, get_create_category_use_case, get_update_category_use_case, get_delete_category_use_case, get_get_all_categories_use_case

router = APIRouter()


@router.get('/categories', status_code=status.HTTP_200_OK, response_model=List[CategoryResponseSchema])
async def get_all_categories(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetAllCategoriesUseCase = Depends(get_get_all_categories_use_case)) -> List[CategoryResponseSchema]:
    categories = await use_case.execute(limit=limit, offset=offset)
    return categories


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseSchema)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(get_get_category_by_id_use_case)) -> CategoryResponseSchema:
    category = await use_case.execute(category_id=category_id)
    return category


@router.get('/category/slug/{slug}', status_code=status.HTTP_200_OK, response_model=CategoryResponseSchema)
async def get_category_by_slug(
    slug: str,
    use_case: GetCategoryBySlugUseCase = Depends(get_get_category_by_slug_use_case)) -> CategoryResponseSchema:
    category = await use_case.execute(slug=slug)
    return category


@router.post('/category', status_code=status.HTTP_201_CREATED, response_model=CategoryResponseSchema)
async def create_category(
    dto: CategoryCreateSchema,
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case)) -> CategoryResponseSchema:
    category = await use_case.execute(dto=dto)
    return category


@router.put('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseSchema)
async def update_category(
    category_id: int,
    dto: CategoryUpdateSchema,
    use_case: UpdateCategoryUseCase = Depends(get_update_category_use_case)) -> CategoryResponseSchema:
    category = await use_case.execute(category_id=category_id, dto=dto)
    return category


@router.delete('/category/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends(get_delete_category_use_case)) -> dict:
    await use_case.execute(category_id=category_id)
    return {'message': 'Category has been deleted'}