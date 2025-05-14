from fastapi import APIRouter, Path, status, Response
from src.dependencies import CurrentManagerDep, ServiceWorkersServiceDep
from .schemas import ServiceWorkerInvite
from typing import Annotated

router = APIRouter(
    tags=['service workers']
)


@router.post(
    '/services/{service_id}/workers/invite',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Invitation successfully sent'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
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
