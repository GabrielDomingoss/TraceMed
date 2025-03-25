import { Route, Routes } from "react-router-dom";
import { Login } from "./pages/login";
import { Dashboard } from "./pages/dashboard";
import { DefaultLayout } from "./layout";
import { ResetPassword } from "./pages/resetPassword";
import { Users } from "./pages/users";
import { Materials } from "./pages/materials";
import { Tracebility } from "./pages/traceability";

export function Router() {
    return (
        <Routes>
            <Route path="/login" element={<Login />}></Route>
            <Route path="/resetPassword" element={<ResetPassword />}></Route>
            <Route path="/" element={<DefaultLayout />}>
                <Route path="/dashboard" element={<Dashboard />}></Route>
                <Route path="/users" element={<Users />}></Route>
                <Route path="/materials" element={<Materials />}></Route>
                <Route path="/traceability" element={<Tracebility />}></Route>
            </Route>
        </Routes>
    )
}