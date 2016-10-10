""" This module contains functionality for managing sessions.
"""

# ToDo: Socket Container
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

    def __init__(self, client_address, client_uuid):
        """ Initialize session.
        """

        self.client_address = client_address
        self.client_uuid = client_uuid

        self.__command = None

        self.__last_recv_time = time.time()
        self.__last_sent_time = time.time()

        self.__status = SessionStatus.active

    @property
    def last_recv_time(self):
        return self.__last_recv_time

    @property
    def last_sent_time(self):
        return self.last_sent_time

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
        # ToDo: VALIDATION
        if not isinstance(value, object):
            raise AttributeError()
        self.__command = value

    def update_recv_time(self):
        """ Update time from last recive packet.
        """

        self.__last_recv_time = time.time()

    def update_sent_time(self):
        """ Update time from last sent packet.
        """

        self.__last_sent_time = time.time()


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

    def create_session(self, client_address, uuid):
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

        session = Session(client_address, uuid)
        self._sessions.append(session)
        return session

    def get_all_active_sessions(self):
        """ Find and return sessions with active status.
        """

        active_sessions = [session for session in self._sessions if session.status == SessionStatus.active]
        return active_sessions


    def get_all_sockets(self):
        """
        """

        raise NotImplementedError()
