from typing import Annotated

from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import (
    Index,
    Search,
)
from fastapi import Depends

from src.catalogue.models.database import Product, Category
from src.catalogue.models.elasticsearch import (
    PRODUCT_INDEX, CATEGORY_INDEX,
    ProductIndex, CategoryIndex
)
from src.catalogue.models.pydantic import ProductElasticResponse
from src.common.databases.elasticsearch import elastic_client


class ProductElasticManager:
    def __init__(self, client: Annotated[AsyncElasticsearch, Depends(elastic_client)] = elastic_client):
        self.client = client

    async def init_indices(self):
        products_index = Index(
            name=PRODUCT_INDEX,
            using=self.client,
        )

        products_index.document(ProductIndex)

        if not  products_index.exists():
            await products_index.create()

    @staticmethod
    def build_product_search_query(keyword):
        search = Search(
            index='products_index',
        ).query(
            'multi_match',
            query=keyword,
            fields=['title', 'description', 'short_description'],
        )
        return search.to_dict()

    async def search_product(self, keyword):
        query = self.build_product_search_query(keyword)
        response = await self.client.search(body=query)
        await self.client.close()

        hits = response.get('hits', {}).get('hits', [])
        sorted_hits = sorted(hits, key=lambda x: x.get('_score', 0), reverse=True)

        sorted_response = [
            ProductElasticResponse(
                product_id=hit.get('_id', ''),
                title=hit.get('_source', {}).get('title', ''),
                score=hit.get('_score', {}),
            )
            for hit in sorted_hits
        ]

        return sorted_response

    async def update_index(self, products: list[Product]) -> None:
        bulk_data = []
        for product in products:
            action = {'index': {'_index': PRODUCT_INDEX, '_id': product.id}}
            data = {
                'title': product.title,
                'description': product.description,
                'short_description': product.short_description,
            }
            bulk_data.append(action)
            bulk_data.append(data)

            if len(bulk_data) >= 100:
                await self.client.bulk(body=bulk_data)
                bulk_data = []

        if bulk_data:
            await self.client.bulk(body=bulk_data)

class CategoryElasticManager:
    def __init__(self, client: Annotated[AsyncElasticsearch, Depends(elastic_client)] = elastic_client):
        self.client = client

    async def init_indices(self):
        categories_index = Index(
            name=CATEGORY_INDEX,
            using=self.client,
        )

        categories_index.document(CategoryIndex)

        exists = await self.client.indices.exists(index=CATEGORY_INDEX)
        if not exists:
            await self.client.indices.create(index=CATEGORY_INDEX)