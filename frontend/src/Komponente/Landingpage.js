import React from 'react';

const LandingPage = () => {
    return (
        <>
            <section className='hero'>
                <div className="container">
                    <div className='content-wrapper'>
                        <img className='pozadinskaSlika' src="pozadina.png" alt="pozadina" />
                        <div className='text-wrapper'>
                            <h1 className='big'>Revolucija u oblasti praćenja prisustva</h1>
                            <p>Pratite prisustvo sa jednim skeniranjem</p>
                            <button className='bigbutton'>Počnite sada</button>
                        </div>
                    </div>
                </div>
            </section>
            <section className='sekundarni'>
                <div className="container">
                    <div className='content-wrapper-2'>
                        <div className='text-wrapper-2'>
                            <h1 className='big'>Olakšajte praćenje prisustva</h1>
                            <p>Efikasno i tačno praćenje</p>
                            <a href='/'><button className='bigbutton'>Prijavite se</button></a>
                        </div>
                    </div>
                </div>
            </section>
            <section className='Tim'>
                <div className='row '>
                    <div className='column-left'>
                        <div className='card-1'>
                            <img src="slika1.png" alt="slika1" />
                            <div className='container'>
                                <h3 className='card'>Jasmin Azemovic</h3>
                                <p className='title'>Stručnjak za baze i sigurnost</p>

                            </div>
                        </div>
                        <div className='card-1'>
                            <img src="slika2.png" alt="slika2" />
                            <div className='container'>
                                <h3 className='card'>Nevzudin Buzađija</h3>
                                <p className='title'>Prodekan</p>

                            </div>
                        </div>
                        <div className='card-1'>
                            <img src="slika3.png" alt="slika3" />
                            <div className='container'>
                                <h3 className='card'>Mujo Hodžić</h3>
                                <p className='title'>Profesor razvoja sistema</p>

                            </div>
                        </div>
                        <div className='card-1'>
                            <img src="slika4.png" alt="slika4" />
                            <div className='container'>
                                <h3 className='card'>Enes Saletović</h3>
                                <p className='title'>Profesor</p>

                            </div>
                        </div>
                    </div>
                    <div className='column-right'>
                        <img className="full-height" src="slika5.png" alt="slika5" />
                    </div>
                </div>
            </section>
            <section className='plava-pozadina'>
                <div className='container'>
                    <h3 className='zadnji'>Naš cilj<br></br>Cilj nam je da pojednostavimo praćenje prisusustva za fakultete i univerzitete putem našeg sistema baziranog na QR kodu, osiguravajući tačnost i efikasnost u svakom trenutku.</h3>
                    <p>Inovativno rješenje</p>
                </div>
            </section>
        </>
    );
};

export default LandingPage;