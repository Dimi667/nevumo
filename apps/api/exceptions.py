from fastapi import HTTPException


class NevumoException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(status_code=status_code, detail=message)


INVALID_PHONE = NevumoException(422, "INVALID_PHONE", "Phone number is required and must not be empty")
CATEGORY_NOT_FOUND = NevumoException(404, "CATEGORY_NOT_FOUND", "Category not found")
CITY_NOT_FOUND = NevumoException(404, "CITY_NOT_FOUND", "City not found")
PROVIDER_NOT_FOUND = NevumoException(404, "PROVIDER_NOT_FOUND", "Provider not found")
RATE_LIMIT_EXCEEDED = NevumoException(429, "RATE_LIMIT_EXCEEDED", "Too many requests. Maximum 5 leads per hour")
INVALID_MATCH_STATUS = NevumoException(422, "INVALID_MATCH_STATUS", "Status must be 'accepted' or 'rejected'")
LEAD_NOT_FOUND = NevumoException(404, "LEAD_NOT_FOUND", "Lead not found")
