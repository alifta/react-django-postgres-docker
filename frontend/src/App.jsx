import "./App.css";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import AddressPage from "./AddressPage";

function App() {
	return (
		<Router>
			<div>
				<Routes>
					<Route path="/" element={<HomePage />} />
					<Route path="/addresses" element={<AddressPage />} />
				</Routes>
			</div>
		</Router>
	);
}

export default App;
