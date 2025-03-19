import MainHeader from "../components/MainHeader/MainHeader";
import { Outlet } from "react-router-dom";
function RootLayout() {
    return (
        <>
            <MainHeader></MainHeader>
            <Outlet />
        </>
    );
}

export default RootLayout;