# Improvements

## Resuming a conversation

Say you are using the project manager, and you return to the project you were managing, the agent will not automatically understand the context when you get back; the workspace instruction is not injected in the context as it is when you start a conversation. This is critical and needs to be fixed.

## init takes long

Init takes a long time to run, this should either be optimized or at least give some kind of feedback the process is running.

## MCP scope

After installing MCP the scope will stay within the project it was installed in the first time.
So if I start a new workspace, the MCP is there, but it's actually scoped to a different project.
This happens with claude

## Versioning

Cortext itself does not have a clear semver version number
