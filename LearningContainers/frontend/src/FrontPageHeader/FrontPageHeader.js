import React from 'react';
import './frontpageheader.css';

const FrontPageHeader = () => {
  return (
    <nav className="front-page-header fixed-top">
      <a className="logo-container" href="/home">
        <img src={require('../../src/images/Sentir.png')} width="100" alt="SENTIR logo" />
      </a>
      <div className="front-page-link-container">
      <a href="/about">
          <span className="front-page-link-text">About</span>
        </a>
        <a href="/upload">
          <span className="front-page-link-text">Upload</span>
        </a>
        <a href="/datasource">
          <span className="front-page-link-text">WebScraping</span>
        </a>
      </div>
    </nav>
  );
};

export default FrontPageHeader;
