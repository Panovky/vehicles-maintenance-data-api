from fastapi import APIRouter, Path, status, Response
from fastapi.responses import RedirectResponse
from src.dependencies import CurrentManagerDep, ServiceWorkersServiceDep, CurrentUserByAccessTokenDep
from typing import Annotated
from .schemas import ServiceWorkerInvite, ServiceWorkerRead

router = APIRouter(
    tags=['service workers']
)


@router.post(
    '/services/{service_id}/workers/invite',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Invitation successfully sent'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied or worker is not registered'},
        404: {'description': 'Service not found'}
    },
    summary='Send email to invite a worker to the service'
)
async def invite_worker(
        current_manager: CurrentManagerDep,
        data: ServiceWorkerInvite,
        service_id: Annotated[int, Path(gt=0)],
        service_workers_service: ServiceWorkersServiceDep
) -> Response:
    await service_workers_service.invite_worker(service_id, data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/services/{service_id}/workers/attach',
    response_class=RedirectResponse,
    summary='Attach the worker to the service'
)
async def attach_worker(
        service_id: Annotated[int, Path(gt=0)],
        token: str,
        service_workers_service: ServiceWorkersServiceDep
) -> RedirectResponse:
    return await service_workers_service.attach_worker(service_id, token)


@router.get(
    '/services/{service_id}/workers',
    responses={
        200: {'description': 'Service workers successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Service not found'}
    },
    summary='Get a list of service workers by the service id'
)
async def get_service_workers(
        current_user: CurrentUserByAccessTokenDep,
        service_id: Annotated[int, Path(gt=0)],
        service_workers_service: ServiceWorkersServiceDep
) -> list[ServiceWorkerRead]:
    return await service_workers_service.get_service_workers(service_id)
