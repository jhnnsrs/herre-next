from herre_next.grants.auto_login import (
    StoredUser,
)
from typing import Dict, Optional

import json
from pydantic import BaseModel, ConfigDict
from fakts_next import Fakts
import logging
from qtpy import QtCore

logger = logging.getLogger(__name__)


class OrderDefaults(BaseModel):
    """A model for the default user storage

    It is used to store the default user for the fakts
    key.

    """

    default_user: Dict[str, StoredUser] = {}


class FaktsQtStore(BaseModel):
    """Retrieves and stores users matching the currently
    active fakts grant"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    settings: QtCore.QSettings  # type: ignore
    default_user_key: str = "default_user_fakts"
    fakts: Fakts
    fakts_key: str

    async def aput_default_user(self, user: Optional[StoredUser]) -> None:
        """Puts the default user

        This method stores the user under a key that it retrieves from
        the fakts. This is done to ensure that the user is only stored
        for the correct fakts. (E.g. when the corresponding endpoint
        server changes)


        Parameters
        ----------
        user : StoredUser | None
            A stored user, with the token and the user, if None is provided
            the user is deleted

        """
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.default_user_key, None)  # type: ignore
        if not un_storage:
            storage = OrderDefaults()
        else:
            try:
                storage = OrderDefaults(**json.loads(un_storage))  # type: ignore
            except Exception as e:
                logger.debug(e, exc_info=True)
                storage = OrderDefaults()

        if user is None:
            if key in storage.default_user:
                del storage.default_user[key]
        else:
            storage.default_user[key] = user  # type: ignore

        self.settings.setValue(self.default_user_key, storage.model_dump_json())  # type: ignore

    async def aget_default_user(self) -> Optional[StoredUser]:
        """Gets the default user

        Gets the default user for the fakts key. If no user is stored
        for the fakts key, None is returned.

        Returns
        -------
        Optional[StoredUser]
            A stored user, with the token and the user
        """
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.default_user_key, None)  # type: ignore
        if not un_storage:
            return None
        try:
            storage = OrderDefaults(**json.loads(un_storage))  # type: ignore
            if key in storage.default_user:
                return storage.default_user[key]
        except Exception as e:
            logger.warning(e, exc_info=True)
            return None

        return None
