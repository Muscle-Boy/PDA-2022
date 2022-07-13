// import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from "react";


import NavBar from './globalstuff/components/NavBar/NavBar';
import Upload from './AnalysisPage/components/Upload/Upload';
import MyDropzone from './mydropzone/MyDropzone'

function App() {
  const [check, setCheck] = useState(false);
  const [getMovies, setMovies] = useState([]);


  // get request
  useEffect(()=> {
    fetch("http://127.0.0.1:5000/movies").then(response =>
      response.json().then(data=> {
       setMovies(data);
      console.log(data)
  })
  );
},[check]

  );

  return (
    <><NavBar/>
    {/* <MyDropz one></MyDropzone></> */}
  
  </>

  );
}



export default App;
