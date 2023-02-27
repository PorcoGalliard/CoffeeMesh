from orders.web.api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema

import time
import uuid

from datetime import datetime
from uuid import UUID
from typing import Optional

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.web.app import app


ORDERS = []


# Untuk Register API Endpoint dan Validasi Response Payload
@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    if cancelled is None and limit is None:  # No parameter is set
        return {'orders': ORDERS}

    # If parameter is set, we filter list of item in query_set variable
    query_set = [order for order in ORDERS]

    if cancelled is not None:
        if cancelled:
            query_set = [
                order
                for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order
                for order in query_set
                if order['status'] != 'cancelled'
            ]

    if limit is not None and len(query_set) > limit:
        return {'orders': query_set[:limit]}

    return query_set


@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):  # <<< Untuk validasi request payload
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    ORDERS.append(order)
    return order


@app.get('/orders/{order_id}')
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException(
        staus_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )
