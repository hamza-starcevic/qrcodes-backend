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
  }, []);

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
      const response = await fetch("http://127.0.0.1:8000/api/predavanja/create", {
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
      <div className="Predmet wrapper-4">
        <input type="text" name="predmet" value={inputData.predmet} onChange={handleInputChange} placeholder="Predmet" />
        <input type="text" name="title" value={inputData.title} onChange={handleInputChange} placeholder="Title" />
        <textarea name="description" value={inputData.description} onChange={handleInputChange} placeholder="Description" />
        <button onClick={handleCreatePredavanje}>Kreiraj Predavanje</button>
      </div>
      <h1 className="H1-title">Predavanja</h1>
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
