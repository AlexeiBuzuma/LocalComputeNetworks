""" This module contains functionality for managing sessions.
"""

# ToDo: Session Reactivation

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

    def __init__(self, client_address, status=SessionStatus.wait_for_activation, uuid=None):
        """Initialize session."""
        self.client_address = client_address
        self.client_uuid = uuid
        self.status = status

        current_time = time.time()
        self.last_recv_time = current_time
        self.last_sent_time = current_time

        self.command = CommandFactory().get_command_by_id(CommandIds.CONNECT_COMMAND_ID)(self)

    def activate_session(self, uuid):
        current_time = time.time()
        self.last_recv_time = current_time
        self.last_sent_time = current_time

        self.status = SessionStatus.active
        self.client_uuid = uuid

    def command_receive_data(self, data):
        if self.command is None:
            self.command = CommandFactory().create_command(data)
        else:
            try:
                self.command.receive_data(data)
            except CommandFinished as e:
                self.command = None

    def command_generate_data(self):
        data = None
        if self.command is not None:
            try:
                data = self.command.generate_data()
            except CommandFinished:
                self.command = None
        if data is None:
            last_sent_interval = time.time() - self.last_sent_time
            if last_sent_interval > _conf.heartbeat_sender_interval:
                data = get_heartbeat_payload()
        return data

    def update_recv_time(self):
        """Update time from last receive packet."""
        self.last_recv_time = time.time()

    def update_sent_time(self):
        """Update time from last sent packet."""
        self.last_sent_time = time.time()

    def __str__(self):
        return "Session: Client addr: '{}', Status: '{}' uuid: '{}' command: {}"\
            .format(self.client_address, self.status, self.client_uuid, self.command)

    def __repr__(self):
        return "<Session: Client addr: '{}', Status: '{}' uuid: '{}' command: '{}'>"\
            .format(self.client_address, self.status, self.client_uuid, self.command)


class SessionManager(metaclass=Singleton):
    """Functionality for managing sessions."""
    def __init__(self):
        """Initialize SessionManager."""
        self._sessions = []
        for _ in SessionStatus:
            self._sessions.append([])
        self._not_inactive_sessions = []
        self._sessions_by_uuid = {}
        self._sessions_by_address = {}

    def create_session(self, client_address, status=SessionStatus.wait_for_activation, uuid=None):
        session = Session(client_address, status, uuid)

        self._sessions[session.status.value].append(session)
        self._sessions_by_address[session.client_address] = session
        if uuid is not None:
            self._sessions_by_uuid[uuid] = session
        if status != SessionStatus.inactive:
            self._not_inactive_sessions.append(session)

        return session

    def get_session(self, uuid=None, client_address=None, create_new=True):
        """Returns session by client address or uuid.

           UUID argument has more priority. If session doesn't
           exist new session object will be created according
           to 'create_new' argument.
        """
        session = None
        try:
            if uuid is not None:
                session = self._sessions_by_uuid[uuid]
            elif client_address is not None:
                session = self._sessions_by_address[client_address]
        except KeyError:
            pass
        else:
            return session

        if create_new:
            if client_address is None:
                raise RuntimeError('Client address is needed to create new session object')
            session = self.create_session(client_address, uuid=uuid)

        return session

    # def get_inactive_session(self, uuid):
    #     for session in self._sessions[SessionStatus.inactive]:
    #         if session.client_uuid = uuid

    def get_all_not_inactive_sessions(self):
        """Find and return sessions with not inactive status."""
        return self._not_inactive_sessions

    def delete_session(self, uuid=None, client_address=None):
        session = self.get_session(uuid=uuid, client_address=client_address, create_new=False)
        if session is not None:
            try:
                self._sessions[session.status.value].remove(session)
                self._not_inactive_sessions.remove(session)
            except ValueError:
                pass
            if session.client_uuid:
                self._sessions_by_uuid.pop(session.client_uuid)
            if session.client_address:
                self._sessions_by_address.pop(session.client_address)
            return session.client_address
        return None

    def activate_session(self, uuid, client_address=None, session=None, create_new=False):
        if session is None:
            session = self.get_session(self, uuid, client_address, create_new=create_new)
        session_status = session.status
        session.activate_session(uuid)
        self._sessions[session_status.value].remove(session)
        self._sessions[session.status.value].append(session)
        self._sessions_by_uuid[uuid] = session
        return session

    def deactivate_session(self, session=None, client_address=None, uuid=None):
        """Set inactive status for session, if session exists."""
        if session is None:
            session = self.get_session(client_address=client_address, uuid=uuid, create_new=False)
            if session is None:
                raise Exception("Session for client '{}' not found".format(client_address))

        session_status = session.status
        session.status = SessionStatus.inactive
        self._sessions[session_status.value].remove(session)
        self._sessions[session.status.value].append(session)
        try:
            self._not_inactive_sessions.remove(session)
        except ValueError:
            pass
