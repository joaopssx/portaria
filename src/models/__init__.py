"""Classes de dominio do sistema de portaria."""

from models.person import Person
from models.resident import Resident
from models.visitor import Visitor
from models.employee import Employee
from models.delivery_person import DeliveryPerson

__all__ = ["Person", "Resident", "Visitor", "Employee", "DeliveryPerson"]
