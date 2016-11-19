""" This module contains functionality for managing sessions.
"""

# ToDo: Session Reactivation
# ToDo TCP -> activate_session when processing 'CONNECT' command

import time
from enum import Enum

from sft.common.commands.base import CommandBase, CommandFinished, CommandIds, ProgramFinished
from sft.common.commands.factory import CommandFactory
from sft.common.config import Config
from sft.common.utils.common import Singleton
from sft.common.utils.packets import get_heartbeat_payload

_conf = Config()


class SessionStatus(Enum):
    """ Describes session status.

        active              -- fully active session
        inactive            -- fully inactive session, not need in processing, just saving the session state
        wait_for_activation -- state when session reactivate with 'connect' command, but no command executed yet
    """

    active = 0
    inactive = 1
    wait_for_activation = 2
    wait_for_close = 3


class Session:
    """Represent information about session."""

    def __init__(self, client_address):
        """Initialize session."""

        self.client_address = client_address
        self.client_uuid = None

        self.__command = CommandFactory().get_command_by_id(CommandIds.CONNECT_COMMAND_ID)(self)

        self.__last_recv_time = time.time()
        self.__last_sent_time = time.time()

        self.__status = SessionStatus.wait_for_activation

    def activate_session(self, uuid):

        self.update_recv_time()
        self.update_sent_time()
        self.status = SessionStatus.active
        self.client_uuid = uuid

    @property
    def last_recv_time(self):
        return self.__last_recv_time

    @property
    def last_sent_time(self):
        return self.__last_sent_time

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if not isinstance(value, SessionStatus):
            raise AttributeError("Status should be an instance of 'SessionStatus' class.")
        self.__status = value

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, value):
        if not isinstance(value, CommandBase):
            raise AttributeError()
        self.__command = value

    def command_receive_data(self, data):
        if self.__command is None:
            self.__command = CommandFactory().create_command(data)
        else:
            try:
                self.__command.receive_data(data)
            except CommandFinished as e:
                self.__command = None

    def command_generate_data(self):
        data = None
        if self.__command is not None:
            try:
                data = self.__command.generate_data()
            except CommandFinished:
                self.__command = None
        if data is None:
            last_sent_interval = time.time() - self.__last_sent_time
            if last_sent_interval > _conf.heartbeat_sender_interval:
                data = get_heartbeat_payload()
        return data

    def update_recv_time(self):
        """Update time from last receive packet."""

        self.__last_recv_time = time.time()

    def update_sent_time(self):
        """Update time from last sent packet."""

        self.__last_sent_time = time.time()

    def __str__(self):
        return "Session: Client addr: '{}', Status: '{}' uuid: '{}' command: {}"\
            .format(self.client_address, self.__status, self.client_uuid, self.command)

    def __repr__(self):
        return "<Session: Client addr: '{}', Status: '{}' uuid: '{}' command: '{}'>"\
            .format(self.client_address, self.__status, self.client_uuid, self.command)


class SessionManager(metaclass=Singleton):
    """Functionality for managing sessions."""

    def __init__(self):
        """Initialize SessionManager."""

        self._sessions = []

    def _get_session_by_uuid(self, client_uuid):
        """Return session object if successful, else None."""

        for session in self._sessions:
            if session.client_uuid == client_uuid:
                return session

        return None

    def create_session(self, client_address):
        """Create session.

           Returns: session object
        """

        # ToDo: write into command field 'Connect' command
        # ToDo: It should only be called when processing 'connect' command.
        # ToDo: Session will be activate when executing the same command as the command in inactive session.

        session = Session(client_address)
        self._sessions.append(session)
        return session

    def activate_session(self, client_address, uuid):

        # Try to find session by uuid
        session = self._get_session_by_uuid(uuid)
        if session:
            session.activate_session(uuid)
            return session

        # Try to find session be client address
        session = self.get_session_by_address(client_address)
        if session:
            session.activate_session(uuid)
            return session

        # Create new session, if client_addr and uuid not exists in storage
        session = self.create_session(client_address)
        session.activate_session()
        return session

    def deactivate_session_by_address(self, client_address):
        """Set inactive status for session, if session exists."""

        session = self.get_session_by_address(client_address, create_new=False)

        if session is None:
            raise Exception("Session for client '{}' not found".format(client_address))

        session.status = SessionStatus.inactive

    def get_all_not_inactive_sessions(self):
        """Find and return sessions with not inactive status."""

        active_sessions = [session for session in self._sessions if session.status != SessionStatus.inactive]
        return active_sessions

    def get_session_by_address(self, client_address, create_new=True):
        """Returns session that bind with client address.

           If session doesn't exist new session object will be created
           according to 'create_new' argument.
        """

        for session in self.get_all_not_inactive_sessions():
            if session.client_address == client_address:
                return session

        # Create session for this client, if session doesn't exist
        if create_new:
            session = self.create_session(client_address)
            return session

        return None

    def delete_session_by_uuid(self, uuid):
        for session in self._sessions:
            if session.client_uuid == uuid:
                address = session.client_address
                self._sessions.remove(session)
                return address
