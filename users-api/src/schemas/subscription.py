from pydantic import BaseModel

class SubscriptionKeySchema(BaseModel):
    subscription_key: str

class SubscribeRequest(BaseModel):
    target_username: str 
