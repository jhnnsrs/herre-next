from pydantic import BaseModel, ConfigDict, Field
import ssl
import certifi
import aiohttp
from herre_next.fetcher.models import Token
import logging
from herre_next.fetcher.errors import UserFetchingError
from fakts_next import Fakts
from typing import Type

logger = logging.getLogger(__name__)


class FaktsUserFetcher(BaseModel):
    """The endpoint to fetch the user from"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    userModel: Type[BaseModel] = Field(
        description="The model to use for the user",
    )
    ssl_context: ssl.SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where()),
        exclude=True,
    )
    fakts: Fakts
    fakts_key: str

    """ An ssl context to use for the connection to the endpoint"""

    async def afetch_user(self, token: Token) -> BaseModel:
        """Fetches the user from the endpoint

        Parameters
        ----------
        token : Token
            The token to use for the request

        Returns
        -------
        BaseModel
            The userModel filled with the data from the endpoint
        """
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            headers={"Authorization": f"Bearer {token.access_token}"},
        ) as session:
            user_info_url = await self.fakts.aget(self.fakts_key)
            assert isinstance(user_info_url, str), "User info url is not a string"
            async with session.get(
                user_info_url + "/",
            ) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                    except aiohttp.ContentTypeError as e:
                        raise UserFetchingError(
                            "Malformed answer, expected json"
                        ) from e

                    try:
                        return self.userModel(**data)
                    except Exception as e:
                        logger.error(f"Malformed answer: {data}", exc_info=True)
                        raise UserFetchingError("Malformed Answer") from e

                else:
                    try:
                        resp.raise_for_status()
                    except Exception as e:
                        logger.error(f"Could not fetch user: {e}", exc_info=True)
                        raise UserFetchingError(
                            f"Could not fetch user from {user_info_url}. Maybe your token is invalid? Or you forgot to add the `openid` scope?"
                        ) from e

        raise UserFetchingError("Could not fetch user")
