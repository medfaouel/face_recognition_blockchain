const Koa = require("koa");
const Router = require("@koa/router");
const cors = require("@koa/cors");
const ethers = require("ethers");
const Attendance = require("../build/contracts/Attendance.json");

const app = new Koa();
const router = new Router();

app.use(cors()).use(router.routes()).use(router.allowedMethods());

app.listen(4000, ()=>{
    console.log("Server running on port 4000");
});

const listenToEvents = () => {
    const provider = new ethers.providers.JsonRpcProvider(
    "http://127.0.0.1:9545"
    );
    const networkId = "5777";
    const attendance = new ethers.Contract(
        Attendance.networks[networkId].address,
        Attendance.abi,
        provider
    );
    attendance.on("AttendanceCompleted",async (professor,attendants,attendanceId,date) => {
        console.log(`
            Attendance list has been successfully added to the blockchain !
            Attendance was marked for professor ${professor}
            attendanceId = ${attendanceId}
            with attendants : ${attendants}
            date : ${new Date(date.toNumber()*1000).toLocaleString()}
        `);
    })

}
listenToEvents();