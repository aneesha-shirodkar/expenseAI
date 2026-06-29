import Budgets from "./pages/Budgets";
import Dashboard from "./pages/Dashboard";
import ReceiptDetails from "./pages/ReceiptDetails";
import { BrowserRouter,Routes, Route } from "react-router-dom";

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard/>} />
        <Route path="/receipts/:id"element={<ReceiptDetails/>} />
        <Route path="/budgets" element={ <Budgets/> }/>
      </Routes>
    </BrowserRouter>

  );
}

export default App;