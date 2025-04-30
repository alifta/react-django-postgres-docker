import { createContext, useState } from "react";

const AuthContext = createContext(null);

export AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

}
