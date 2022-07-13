import React from 'react';
import './NavBar.css';

const NavBar = () => {
    return(
        <nav>
             <div>
                <a href="/Home" className="Home">Home</a>
                <a href="/Analysis" className="analysisclass">Analysis</a>
                <a href="/Dashboard" className="dashboardclass">Dashboard</a>

                <a href="BELOW OPTIONS">ffeef</a>
                <a href="/UploadUsingDropzoneContainer">Upload using dropzone</a>
             </div>
        </nav>
    )
}
export default NavBar;