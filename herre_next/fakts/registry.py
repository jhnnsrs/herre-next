from typing import Dict, Callable

from pydantic import BaseModel, ConfigDict, Field
from fakts_next.grants.base import BaseFaktsGrant
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class GrantType(str, Enum):
    """The grant type"""

    CLIENT_CREDENTIALS = "client-credentials"
    """The client credentials grant"""
    AUTHORIZATION_CODE = "authorization-code"
    """The authorization code grant"""


GrantBuilder = Callable[..., BaseFaktsGrant]
#


class GrantRegistry(BaseModel):
    """A registry for grants.

    This registry is used to register grants. It is used by the fakts
    grant to build the correct grant from the fakts.


    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    registered_grants: Dict[GrantType, GrantBuilder] = Field(default_factory=dict)

    def register_grant(self, grant_type: GrantType, grant: GrantBuilder) -> None:
        """Registers a grant.

        Parameters:
        ___________
        type: GrantType
            The type of the grant to register
        grant: Type[BaseGrant]
            The grant to register

        """
        if not self.registered_grants:
            self.registered_grants = {}
        self.registered_grants[grant_type] = grant

    def get_grant_for_type(self, grant_type: GrantType) -> GrantBuilder:
        """Gets the grant for a type.

        Parameters:
        ___________
        type: GrantType
            The type of the grant to get

        Returns:
        ________
        Type[BaseGrant]
            The grant for the type

        """
        return self.registered_grants[grant_type]
