import logging
from os import environ

from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller

import subprocess, time

ip_port_regex = r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,5}'


class UserAgentManager:
    __TOR_SOCKS_PORT: int = int(environ['TOR_SOCKS_PORT'])
    __TOR_CONTROL_PORT: int = int(environ['TOR_CONTROL_PORT'])
    __TOR_PASSWORD: str = environ['TOR_PASSWORD']

    def __init__(self, logger_level: int = logging.INFO) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logger_level)
        
        self.user_agent: UserAgent = UserAgent()
        self.proxy: str = f'socks5://localhost:{UserAgentManager.__TOR_SOCKS_PORT}'

        subprocess.Popen(['tor'])
        time.sleep(5)

    def get_random_user_agent(self) -> str:
        return self.user_agent.random
    
    def get_proxy(self) -> str:
        self.update_route()
        return self.proxy
    
    def update_route(self) -> None:
        with Controller.from_port(port=UserAgentManager.__TOR_CONTROL_PORT) as controller:
            controller.authenticate(UserAgentManager.__TOR_PASSWORD)
            
            # Проверяем состояние Tor
            status = controller.get_info("status/circuit-established")
            if status == '1':
                self.logger.info(f'Tor is connected.')
            else:
                self.logger.error(f'Tor is NOT connected.')
            
            controller.signal(Signal.NEWNYM)

