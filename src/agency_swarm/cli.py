#!/usr/bin/env python3
"""
Agency Swarm CLI - Command line interface for agency-swarm framework
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click


@click.group()
@click.version_option()
def cli():
    """Agency Swarm - Multi-agent collaboration framework."""
    pass


@cli.command("create-agent-template")
@click.option(
    "--name",
    required=True,
    help="Name of the agent (e.g., 'Developer', 'CEO')"
)
@click.option(
    "--description", 
    required=True,
    help="Brief description of the agent's role"
)
@click.option(
    "--path",
    default=".",
    help="Path where to create the agent folder (default: current directory)"
)
@click.option(
    "--use-txt",
    is_flag=True,
    help="Use .txt extension for instructions file instead of .md"
)
def create_agent_template(name: str, description: str, path: str, use_txt: bool):
    """Create a new agent template with the recommended folder structure."""
    try:
        create_agent_template_structure(name, description, path, use_txt)
        click.echo(f"✅ Agent template '{name}' created successfully!")
    except Exception as e:
        click.echo(f"❌ Error creating agent template: {e}", err=True)
        sys.exit(1)


def create_agent_template_structure(name: str, description: str, base_path: str, use_txt: bool = False):
    """
    Create the agent template folder structure.
    
    Args:
        name: Name of the agent
        description: Brief description of the agent's role
        base_path: Base directory to create the agent folder in
        use_txt: Whether to use .txt extension for instructions
    """
    # Sanitize the agent name for folder/file names
    agent_name = name.strip().replace(" ", "")
    
    # Create base agent directory
    agent_path = Path(base_path) / agent_name
    
    if agent_path.exists():
        raise ValueError(f"Agent directory '{agent_path}' already exists!")
    
    # Create directory structure
    agent_path.mkdir(parents=True, exist_ok=True)
    (agent_path / "files").mkdir(exist_ok=True)
    (agent_path / "schemas").mkdir(exist_ok=True)
    (agent_path / "tools").mkdir(exist_ok=True)
    
    # Create __init__.py
    init_content = f'"""Agent module for {agent_name}."""\n\nfrom .{agent_name} import {agent_name}\n\n__all__ = ["{agent_name}"]\n'
    (agent_path / "__init__.py").write_text(init_content)
    
    # Create agent class file
    agent_class_content = f'''from agency_swarm import Agent


class {agent_name}(Agent):
    def __init__(self):
        super().__init__(
            name="{agent_name}",
            description="{description}",
            instructions="./instructions.{"txt" if use_txt else "md"}",
            files_folder="./files",
            schemas_folder="./schemas", 
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
'''
    
    (agent_path / f"{agent_name}.py").write_text(agent_class_content)
    
    # Create instructions file
    instructions_ext = "txt" if use_txt else "md"
    instructions_content = f'''# {agent_name} Agent Instructions

## Role
You are a {agent_name} agent responsible for {description.lower()}.

## Goals
- Define the main objectives of this agent
- List specific tasks this agent should accomplish
- Outline how this agent contributes to the overall agency

## Process
1. How to handle incoming requests
2. When and how to use available tools
3. How to collaborate with other agents
4. Any specific workflows or procedures

## Tools
- List and describe the tools available to this agent
- Explain when and how to use each tool
- Include any tool-specific guidelines

## Communication
- How to communicate with other agents
- What information to share and when
- Protocols for handoffs and coordination
'''
    
    (agent_path / f"instructions.{instructions_ext}").write_text(instructions_content)
    
    # Create example tool file
    example_tool_content = f'''from agency_swarm.tools import BaseTool
from pydantic import Field


class ExampleTool(BaseTool):
    """
    An example tool for the {agent_name} agent.
    Replace this with your actual tools.
    """
    
    example_field: str = Field(
        ..., 
        description="Description of what this field is used for"
    )
    
    def run(self):
        """
        Execute the tool's main functionality.
        """
        # Implement your tool logic here
        return f"Tool executed with: {{self.example_field}}"
'''
    
    (agent_path / "tools" / "example_tool.py").write_text(example_tool_content)
    (agent_path / "tools" / "__init__.py").write_text("")


if __name__ == "__main__":
    cli()
