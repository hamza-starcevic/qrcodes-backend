import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Modal from "react-modal";
import QRCodeModal from "./QRCodeModal";
import QRCode from "qrcode.react";

const Predavanja = () => {
  const [inputData, setInputData] = useState({
    predmet: "",
    title: "",
    description: "",
  });

  const [tableData, setTableData] = useState([]);
  const [qrcodeData, setQRCodeData] = useState(null);
  const [isQRCodeModalOpen, setQRCodeModalOpen] = useState(false);

  useEffect(() => {
    // Fetch data from your database API here
    const fetchData = async () => {
      try {
        const response = await fetch("your-api-endpoint-for-predavanja");
        const data = await response.json();
        setTableData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []); // The empty dependency array ensures that this effect runs only once when the component mounts

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleCreatePredavanje = async () => {
    try {
      // Make a POST request to your database API to create a new predavanje
      const response = await fetch("your-api-endpoint-for-creating-predavanje", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          predmet: inputData.predmet,
          title: inputData.title,
          description: inputData.description,
        }),
      });

      const createdPredavanje = await response.json();

      setTableData((prevTableData) => [...prevTableData, createdPredavanje]);
      setInputData({
        predmet: "",
        title: "",
        description: "",
      });
    } catch (error) {
      console.error("Error creating Predavanje:", error);
    }
  };

  const handleCreateQRCode = (predavanjeId) => {
    setQRCodeData(predavanjeId);
    setQRCodeModalOpen(true);
  };

  const closeQRCodeModal = () => {
    setQRCodeModalOpen(false);
    setQRCodeData(null);
  };

  return (
    <div className="container">
      {/* ... (rest of the component remains the same) */}
      <div className="predmet-card">
        <table>
          <thead>
            <tr>
              <th>Naziv</th>
              <th>Opis</th>
              <th>Predmet</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tableData.map((row) => (
              <tr key={row.id}>
                <td>{row.naziv}</td>
                <td>{row.opis}</td>
                <td>{row.predmet}</td>
                <td>
                  <button onClick={() => handleCreateQRCode(row.id)}>Kreiraj QR kod</button>
                  <Link to={`/prisustvo/${row.id}`}>
                    <button>Prisustvo</button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <QRCodeModal isOpen={isQRCodeModalOpen} onRequestClose={closeQRCodeModal} qrcodeData={qrcodeData} />
    </div>
  );
};

export default Predavanja;