import React, { useState } from 'react';

const Prisustvo = () => {
  const [students, setStudents] = useState([
    { indexNumber: '123456', name: 'Anes', surname: 'Zilić', status: 'Prisutan' },
    { indexNumber: '789012', name: 'Amila', surname: 'Starčević', status: 'Odsutan' },
    { indexNumber: '345678', name: 'Nermin', surname: 'Omerhodzic', status: 'Prisutan' },
    { indexNumber: '123456', name: 'Anes', surname: 'Zilić', status: 'Prisutan' },
    { indexNumber: '789012', name: 'Amila', surname: 'Starčević', status: 'Odsutan' },
    { indexNumber: '345678', name: 'Nermin', surname: 'Omerhodzic', status: 'Prisutan' }, { indexNumber: '123456', name: 'Anes', surname: 'Zilić', status: 'Prisutan' },
    { indexNumber: '789012', name: 'Amila', surname: 'Starčević', status: 'Odsutan' },
    { indexNumber: '345678', name: 'Nermin', surname: 'Omerhodzic', status: 'Prisutan' },
    { indexNumber: '123456', name: 'Anes', surname: 'Zilić', status: 'Prisutan' },
    { indexNumber: '789012', name: 'Amila', surname: 'Starčević', status: 'Odsutan' },
    { indexNumber: '345678', name: 'Nermin', surname: 'Omerhodzic', status: 'Prisutan' }
    
  ]);

  const handleStatusChange = (index, newStatus) => {
    setStudents((prevStudents) => {
      const updatedStudents = [...prevStudents];
      updatedStudents[index].status = newStatus;
      return updatedStudents;
    });
  };

  return (
    <div>
      <h1>Prisutvo studenata na Predavanju 10.1.2024</h1>
      <table>
        <thead>
          <tr>
            <th>Broj Indexa</th>
            <th>Ime</th>
            <th>Prezime</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student, index) => (
            <tr key={index}>
              <td>{student.indexNumber}</td>
              <td>{student.name}</td>
              <td>{student.surname}</td>
              <td>{student.status}</td>
              
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Prisustvo;
