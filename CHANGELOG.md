# Changelog
All notable changes to this project will be documented in this
file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
the [PEP 440 version scheme](https://peps.python.org/pep-0440/#version-scheme).

## [v0.9.0] - 2024-06-11
### Added
- ILinuxAgentCommandBuilder.build_set_permissions_command().
  https://github.com/guardicore/monkey/issues/4187

## [v0.8.0] - 2024-06-10
### Changed
- `ReservationID` from a UUID to a string.
  https://github.com/guardicore/monkey/issues/4187

## [v0.7.0] - 2024-05-14
### Changed
- The `agent_binary_transform` parameter to `agent_binary_wrapper_template` in
  `IHTTPAgentBinaryServerRegistrar.reserve_download()`. #8

## [v0.6.0] - 2024-03-14
### Fixed
- An issue in TargetHost that caused ports_status to be shared amongst all
  TargetHosts. #7

## [v0.5.0] - 2024-03-08
### Added
- Implementation for \[NetworkProtocol\] getter in TargetHostPorts. #6
- PortScanDataDict.get_open_service_ports(). #6


## [v0.4.0] - 2024-03-14
### Added
- IAgentEventPublisher. #4

## [v0.3.0] - 2024-02-13
### Added
- A command builder interface including IAgentCommandBuilderFactory,
  ILinuxAgentCommandBuilder, IWindowsAgentCommandBuilder that allows plugins to
  quickly and easily build agent download/run commands.

## [v0.2.0] - 2024-01-18
### Added
- `AgentBinaryTransform` to exported components (__init__.py) #2
- `ReservationID` to exported components (__init__.py) #2
