import React, { useState } from 'react';

const Ucenici = () => {
    const [inputData, setInputData] = useState({
        email: "",
        ime: "",
        prezime: "",
        password: "",
    });

    const [displayData, setDisplayData] = useState({
        email: "",
        ime: "",
        prezime: "",
        password: "",
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setInputData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleCreateUcenik = async () => {
        // Validate form data here (e.g., check if email, ime, prezime, and password are not empty)

        try {
            // Add loading state here (optional)
            const response = await fetch("http://127.0.0.1:8000/api/ucenik/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    ...inputData,
                    role: "ucenik",
                }),
            });

            const data = await response.json();
            console.log(data); // Handle the response from the backend

            // Clear input fields and update the state with the received data
            setInputData({
                email: "",
                ime: "",
                prezime: "",
                password: "",
            });

            setDisplayData(data);
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <div className="container">
            <div className="Predmet wrapper-4">
                {/* Input fields for inputData */}
                <input type="email" name="email" value={inputData.email} onChange={handleInputChange} placeholder="Email" />
                <input type="text" name="ime" value={inputData.ime} onChange={handleInputChange} placeholder="Ime" />
                <input type="text" name="prezime" value={inputData.prezime} onChange={handleInputChange} placeholder="Prezime" />
                <input type="password" name="password" value={inputData.password} onChange={handleInputChange} placeholder="Password" />
                <button onClick={handleCreateUcenik}>Kreiraj Ucenika</button>
            </div>
            {/* Display the received data */}
            <div>
                <h1 className="H1-title">Kreirani Ucenici</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Email</th>
                            <th>Ime</th>
                            <th>Prezime</th>
                            <th>Password</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{displayData.email}</td>
                            <td>{displayData.ime}</td>
                            <td>{displayData.prezime}</td>
                            <td>{displayData.password}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Ucenici;
