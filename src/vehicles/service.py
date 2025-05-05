from .repository import VehiclesRepository


class VehiclesService:
    def __init__(self, repository: VehiclesRepository):
        self.repository: VehiclesRepository = repository
