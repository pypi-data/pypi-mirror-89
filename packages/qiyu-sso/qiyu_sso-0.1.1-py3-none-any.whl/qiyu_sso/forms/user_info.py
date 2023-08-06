from pydantic import BaseModel, Field

__all__ = ["UserInfoForm"]


class UserInfoForm(BaseModel):
    """
    用户信息表单
    """

    access_token: str = Field(..., title="访问令牌", description="使用此访问令牌可以访问指定用户的信息")
