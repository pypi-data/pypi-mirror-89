Agent
=======

Spotinst Agent executor provides a mechanism to run remote shutdown scripts on machine using polling architecture.

Note:
The agent must have token to communicate with spotinst API.
The credentials ini that holds the token file must be located at: '/root/.spotinst/credentials'

Application
===========

Manual Executing
~~~~~~~~~~~~~~~~
The simplest way to run the agent is by './agent' that start and write basic logs to /var/log/messages/agent.log

Otherwise, you can use the following options:

Usage:  ./agent [options]

-c --config            Use alternate configuration yml file.
-l --log               Use alternate Log file for output.
-t --test              Test run.  Do not run remote script.
-v --verbose           verbose log
--stdout               redirect output to stdout
--debug                run with dummy credentials for debug purposes

Configuration
~~~~~~~~~~~~~
There are two levels of configuration representing in yml files.
The global configuration 'agent.yml' is responsible of the agent framework and necessary params.
The worker configuration, located at the workers folder is responsible of the specific workers parameters.


MAKEFILE
~~~~~~~~~~~~~
run 'make release'
output file is located in the /dist folder

Documentation
=============
