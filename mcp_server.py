"""Cisco Router MCP Server
A Model Context Protocol server for managing Cisco routers via Claude Desktop
"""

from fastmcp import FastMCP
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import requests
import json
import logging
from typing import Dict, List, Optional, Any
import os
from dataclasses import dataclass
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RouterConfig:
    """Configuration for a Cisco router"""
    host: str
    username: str
    password: str
    device_type: str = "cisco_ios"
    port: int = 22
    secret: str = ""  # Enable password

class CiscoRouterManager:
    """Manages connections and operations with Cisco routers"""

    def __init__(self):
        self.routers: Dict[str, RouterConfig] = {}
        self.executor = ThreadPoolExecutor(max_workers=5)

    def add_router(self, name: str, config: RouterConfig):
        """Add a router to the managed devices"""
        self.routers[name] = config
        logger.info(f"Added router {name}: {config.host}")

    def _connect_router(self, router_name: str) -> ConnectHandler:
        """Establish SSH connection to router"""
        if router_name not in self.routers:
            raise ValueError(f"Router {router_name} not found")

        config = self.routers[router_name]
        device_config = {
            'device_type': config.device_type,
            'host': config.host,
            'username': config.username,
            'password': config.password,
            'port': config.port,
            'secret': config.secret,
            'timeout': 20,
            'session_timeout': 60,
        }

        try:
            connection = ConnectHandler(**device_config)
            return connection
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            logger.error(f"Failed to connect to {router_name}: {str(e)}")
            raise

    async def run_command(self, router_name: str, command: str) -> str:
        """Execute a command on specified router"""
        loop = asyncio.get_event_loop()
        try:
            def _execute():
                with self._connect_router(router_name) as conn:
                    return conn.send_command(command)
            return await loop.run_in_executor(self.executor, _execute)
        except Exception as e:
            logger.error(f"Command failed on {router_name}: {str(e)}")
            return f"Error: {str(e)}"

# Initialize MCP Server
mcp = FastMCP("CiscoRouterMCP")
router_manager = CiscoRouterManager()

# Add your routers (replace IPs with actual values)
router_manager.add_router("R1", RouterConfig(
    host="1.1.1.1",
    username="admin",
    password="Cisco123"
))

router_manager.add_router("R2", RouterConfig(
    host="2.2.2.2",
    username="admin",
    password="Cisco123"
))

@mcp.tool("run_command", "Execute CLI command on router")
async def run_command(router: str, command: str) -> str:
    """Example usage: run_command('R1', 'show ip interface brief')"""
    return await router_manager.run_command(router, command)

@mcp.tool("get_config", "Retrieve running configuration")
async def get_config(router: str) -> str:
    """Example usage: get_config('R2')"""
    return await router_manager.run_command(router, "show run")

@mcp.tool("configure_interface", "Configure network interface")
async def configure_interface(router: str, interface: str, ip_address: str, subnet: str) -> str:
    """Example: configure_interface('R1', 'Gig0/1', '192.168.1.1', '255.255.255.0')"""
    commands = [
        f"interface {interface}",
        f"ip address {ip_address} {subnet}",
        "no shutdown"
    ]
    return await router_manager.run_command(router, "\n".join(commands))

if __name__ == "__main__":
    logger.info("Starting Cisco MCP Server...")
    mcp.run()
