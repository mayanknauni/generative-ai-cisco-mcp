# Claude MCP Cisco Demo

Welcome to the **Claude MCP Cisco Demo**!  
This project demonstrates how you can use [Claude Desktop](https://www.anthropic.com/claude), the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), and Python to manage Cisco routers using natural language and automation.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Lab Topology](#lab-topology)
- [Features](#features)
- [Getting Started](#getting-started)
  - [1. Requirements](#1-requirements)
  - [2. Clone & Set Up](#2-clone--set-up)
  - [3. Configure Your Routers](#3-configure-your-routers)
  - [4. MCP Server Setup](#4-mcp-server-setup)
  - [5. Claude Desktop Integration](#5-claude-desktop-integration)
  - [6. Run & Test](#6-run--test)
- [Usage Examples](#usage-examples)
- [Security Notes](#security-notes)
- [FAQ & Troubleshooting](#faq--troubleshooting)
- [License](#license)

---

## Overview

This repo shows how to:
- Connect Claude Desktop to Cisco routers via the Model Context Protocol (MCP)
- Run show commands, retrieve configs, and push changes—all via natural language
- Scale the approach to your entire IT infrastructure

All code and instructions are included.  
**All scripts and diagrams are open source—see [LICENSE](#license).**

---

## Architecture

**MCP Architecture Flow**

![MCP Architecture Flow](image.jpg)

- **Claude Desktop**: User interacts with AI
- **MCP Client**: Bridges Claude with the MCP server
- **MCP Server**: Exposes tools/resources, translates requests
- **Netmiko/SSH**: Secure connection to Cisco routers
- **Routers**: Managed devices

---

## Lab Topology

**GNS3 Lab Topology**

![GNS3 Topology](Topology.JPG)

- **PC1**: Runs Claude Desktop and MCP server
- **R2, R1**: Cisco routers (can be real or emulated)
- **Cloud**: Simulates WAN/Internet

---

## Features

- **Natural Language Network Management**: Use Claude to interact with your routers
- **Python MCP Server**: Powered by [FastMCP](https://pypi.org/project/fastmcp/) and [Netmiko](https://github.com/ktbyers/netmiko)
- **Multi-Device Support**: Easily add more routers
- **Secure SSH Automation**: All actions over SSH

---

## Getting Started

### 1. Requirements

- Python 3.10+
- Claude Desktop (see [Anthropic](https://www.anthropic.com/claude))
- Cisco routers (real or GNS3/Packet Tracer/CSR1000v)
- [GNS3](https://www.gns3.com/) (optional, for emulation)
- SSH enabled on routers

### 2. Clone & Set Up

