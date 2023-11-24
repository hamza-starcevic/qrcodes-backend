import React, { useState } from "react";

const Predavanja = () => {
  const [inputData, setInputData] = useState({
    naziv: "",
    godina_studija: 0,
    // Other fields...
  });

  const [displayData, setDisplayData] = useState({
    naziv: "",
    godina_studija: 0,
    // Other fields...
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleCreatePredmet = async () => {
    // Validate form data here (e.g., check if naziv is not empty)

    try {
      // Add loading state here (optional)
      const response = await fetch("http://127.0.0.1:8000/api/predmet/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputData),
      });

      const data = await response.json();
      console.log(data); // Handle the response from the backend

      // Clear input fields and update the state with the received data
      setInputData({
        naziv: "",
        godina_studija: 0,
        // Other fields...
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
        <input type="text" name="naziv" value={inputData.naziv} onChange={handleInputChange} placeholder="Naziv" />
        <input type="text" name="godina_studija" value={inputData.godina_studija} onChange={handleInputChange} placeholder="Godina studija" />
        {/* Add more input fields as needed */}
        <button onClick={handleCreatePredmet}>Kreiraj Predmet</button>
      </div>
      {/* Display the received data */}
      <div>
        <h1 className="H1-title">Kreirani Predmeti</h1>
        <table>
          <thead>
            <tr>
              <th>Naziv</th>
              <th>Godina Studija</th>
              
            </tr>
          </thead>
          <tbody>
            
              <tr>
                <td>{displayData.naziv}</td>
                <td>{displayData.godina_studija}</td>
              
              </tr>
            
          </tbody>
        </table>
        {/* Display other fields as needed */}
      </div>
    </div>
  );
};

export default Predavanja;
