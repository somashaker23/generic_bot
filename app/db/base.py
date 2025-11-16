from .base_class import Base

# These imports are need to load them when Base model is loaded
from app.models.car_inventory import Car
from app.models.car_image import CarImage
from app.models.callback_request import CallbackRequest
from app.models.test_drive_booking import TestDrive
from app.models.car_valuation import CarValuation
from app.models.whatsapp_log import WhatsAppLog
