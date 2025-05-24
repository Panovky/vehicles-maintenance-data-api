from fastapi import APIRouter, Path, status, Response, Body
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from src.dependencies import CurrentManagerDep, ServiceClientsServiceDep, CurrentManagerOrWorkerDep
from typing import Annotated
from src.users.schemas import UserRead

router = APIRouter(
    tags=['service clients']
)


@router.post(
    '/services/{service_id}/clients/invite',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Invitation successfully sent'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied or client is not registered'},
        404: {'description': 'Service not found'}
    },
    summary='Send email to invite a client to the service'
)
async def invite_client(
        current_manager: CurrentManagerDep,
        email: Annotated[EmailStr, Body(embed=True)],
        service_id: Annotated[int, Path(gt=0)],
        service_clients_service: ServiceClientsServiceDep
) -> Response:
    await service_clients_service.invite_client(service_id, email)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/services/{service_id}/clients/attach',
    response_class=RedirectResponse,
    summary='Attach the client to the service'
)
async def attach_client(
        service_id: Annotated[int, Path(gt=0)],
        token: str,
        service_clients_service: ServiceClientsServiceDep
) -> RedirectResponse:
    return await service_clients_service.attach_client(service_id, token)


@router.get(
    '/services/{service_id}/clients',
    responses={
            200: {'description': 'Service clients successfully received'},
            401: {'description': 'Access token are invalid'},
            403: {'description': 'Access for current user denied'},
            404: {'description': 'Service not found'}
        },
    summary='Get all service clients'
)
async def get_service_clients(
        current_manager: CurrentManagerOrWorkerDep,
        service_id: Annotated[int, Path(gt=0)],
        service_clients_service: ServiceClientsServiceDep
) -> list[UserRead]:
    return await service_clients_service.get_service_clients(service_id)
