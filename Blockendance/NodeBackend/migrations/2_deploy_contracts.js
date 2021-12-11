const Attendance = artifacts.require("Attendance.sol");
module.exports = async function (deployer,network,addresses) {
    const [admin,professor,_] = addresses;

    if(network == "develop")
    {
        await deployer.deploy(Attendance,admin);
    }
    else
    {
        const ADMIN_ADDRESS ="";
        await deployer.deploy(Attendance,ADMIN_ADDRESS);
    }
};
