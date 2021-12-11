pragma solidity ^0.8.10;

contract Attendance {
    address public admin;
    string public attendants;

    event AttendanceCompleted(
        address professorAddress,
        string attendants,
        uint256 attendanceId,
        uint256 date
    );
    constructor(address adminAddress) public{
        admin = adminAddress;
    }
    function completeAttendance(string memory attendants, uint256 attendanceId) external {
        emit AttendanceCompleted(msg.sender,attendants,attendanceId,block.timestamp);
    }
}