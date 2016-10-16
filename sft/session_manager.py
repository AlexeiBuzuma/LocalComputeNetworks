""" This module contains functionality for managing sessions.
"""

# ToDo: Session Reactivation

from sft.utils.common import Singleton
import time
from enum import Enum


class SessionStatus(Enum):
    """ Describes session status.

     active              -- fully active session
     inactive            -- fully inactive session, not need in processing, just saving the session state
     wait_for_activation -- state when session reactivate with 'connect' command, but no command executed yet
    """

    active = 0
    inactive = 1
    wait_for_activation = 2


class Session:
    """ Represent information about session.
    """

    def __init__(self, client_address,  socket, client_uuid):
        """ Initialize session.
        """

        self.client_address = client_address
        self.client_uuid = client_uuid

        # ToDo: It should create 'connect' command, not None
        self.__command = None
        self.__socket = socket

        self.__last_recv_time = time.time()
        self.__last_sent_time = time.time()

        self.__status = SessionStatus.active

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
    def socket(self):
        return self.__socket

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, value):
        # ToDo: VALIDATION
        if not isinstance(value, object):
            raise AttributeError()
        self.__command = value

    def update_recv_time(self):
        """ Update time from last receive packet.
        """

        self.__last_recv_time = time.time()

    def update_sent_time(self):
        """ Update time from last sent packet.
        """

        self.__last_sent_time = time.time()

    def __str__(self):
        return "Session: Client addr: '{}', Status: '{}'.".format(self.client_address, self.__status)


class SessionManager(metaclass=Singleton):
    """ Functionality for managing sessions.
    """

    def __init__(self):
        """ Initialize SessionManager.
        """

        self._sessions = []

    def _get_session_by_uuid(self, client_uuid):
        """ Return session object if successful, else None.
        """

        for session in self._sessions:
            if session.client_uuid == client_uuid:
                return session

        return None

    def create_session(self, client_address, socket, uuid):
        """
        Create session.
        If uuid already exists in SessionManager storage, they will return this session, but with no reactivation

        Returns: session object
        """

        # ToDo: It should only be called when processing 'connect' command.
        # ToDo: Session will be activate when executing the same command as the command in inactive session.

        session = self._get_session_by_uuid(uuid)
        if session:
            session.status = SessionStatus.wait_for_activation
            return session

        session = Session(client_address, uuid, socket)
        self._sessions.append(session)
        return session

    def get_all_active_sessions(self):
        """ Find and return sessions with active status.
        """

        active_sessions = [session for session in self._sessions if session.status == SessionStatus.active]
        return active_sessions

    def get_socket_by_address(self, client_address):
        """ Returns socket that bind with client address if successful else None.
        """

        for session in self.get_all_active_sessions():
            if session.client_address == client_address:
                return session.socket

        return None

    def get_session_by_address(self, client_address):
        """ Returns session that bind with client address if successful else None.
        """

        for session in self.get_all_active_sessions():
            if session.client_address == client_address:
                return session

        return None

    def get_all_sockets(self):
        """ Returns list of tuples with client address and socket.
        """

        return [(session.client_address, session.socket) for session in self.get_all_active_sessions()]


if __name__ == '__main__':
    """ Example of using SessionManager.
    """

    import mock

    client_addr = "client_addr"
    dummy_socket = mock.MagicMock()
    dummy_uuid = mock.MagicMock()

    manager = SessionManager()

    session = manager.create_session(client_addr, dummy_socket, dummy_uuid)
    print(session)
    print(session.last_recv_time)
    print(session.last_sent_time)

    assert manager.get_socket_by_address(client_addr) == session.socket
    assert manager.get_session_by_address(client_addr) == session
