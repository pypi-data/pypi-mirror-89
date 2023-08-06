from pydantic import BaseModel, Field

__all__ = ["ClientBaseForm"]


class ClientBaseForm(BaseModel):
    """
    附带客户认证接口的表单
    """

    client_id: str = Field(..., title="客户ID", max_length=100)
    client_secret: str = Field(..., title="客户机密", max_length=255)
