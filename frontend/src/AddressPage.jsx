import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const AddressPage = () => {
	const [addresses, setAddresses] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		const fetchAddresses = async () => {
			try {
				const response = await axios.get("/api/addresses/");
				// "http://localhost:8000/api/hello-world/"
				setAddresses(response.data);
			} catch (err) {
				setError(err);
			} finally {
				setLoading(false);
			}
		};

		fetchAddresses();
	}, []);

	if (loading) return <div>Loading...</div>;
	if (error) return <div>Error: {error.message}</div>;

	return (
		<div>
			<h1>Addresses</h1>
			<ul>
				{addresses.map((address) => (
					<li key={address.id}>
						{address.street}, {address.city}, {address.state},{" "}
						{address.zipcode}
					</li>
				))}
			</ul>
		</div>
	);
};

export default AddressPage;
