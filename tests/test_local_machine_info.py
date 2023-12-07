from monkeytypes import OperatingSystem

from agentpluginapi.local_machine_info import LocalMachineInfo

LOCAL_MACHINE_INFO_OBJECT = LocalMachineInfo(
    operating_system=OperatingSystem.WINDOWS,
    temporary_directory="temp/o/rary",
)

LOCAL_MACHINE_INFO_DICT = {
    "operating_system": "windows",
    "temporary_directory": "temp\\o\\rary",
}


def test_local_machine_info__serialization():
    assert LOCAL_MACHINE_INFO_OBJECT.to_json_dict() == LOCAL_MACHINE_INFO_DICT


def test_local_machine_info__deserialization():
    assert LocalMachineInfo(**LOCAL_MACHINE_INFO_DICT) == LOCAL_MACHINE_INFO_OBJECT
