import "./App.css";

import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import HomePage from "./HomePage";
import AddressPage from "./HomePage";

function App() {
	return (
		<Router>
			<div>
				<Switch>
					<Route exact path="/" component={HomePage} />
					<Route path="/addresses" component={AddressPage} />
				</Switch>
			</div>
		</Router>
	);
}

export default App;
