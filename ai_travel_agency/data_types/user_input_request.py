from pydantic import BaseModel


class UserInputRequest(BaseModel):
    user_input: str
    thread_id: str