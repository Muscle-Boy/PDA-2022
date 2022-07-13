import React from 'react';
import './uploaddropzone.css';
// import { Row, Col } from 'react-bootstrap';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import { TiDeleteOutline } from 'react-icons/ti';
import DropzoneContainer from '../dropbox/DropzoneContainer';
import Options from './Options';
import { css, ThemeProvider } from 'styled-components';
import { base, DocumentPdf, DocumentTxt } from 'grommet-icons';
import { deepMerge } from 'grommet-icons/utils';
import { useState } from "react";
// import 'bootstrap/dist/css/bootstrap.css';
import Modal from 'react-bootstrap/Modal'
import 'antd/dist/antd.css';
import { Col, Row } from 'antd';

const customColorTheme = deepMerge(base, {
  global: {
    colors: {
      icons: '#333333',
    },
  },
  icon: {
    extend: css`
      ${(props) =>
        props.color === 'brand' &&
        `
        fill: #64FFDA;
        stroke: #64FFDA;
      `}
    `,
  },
});

const Test = (props) => {
  const { files, setFiles, uploadFiles, deleteFile, setConfig, config } = props;

  // for the modal 
  const [show, setShow] = useState(false);

  

  return (
    <div style={{ display: 'block', width: 700, padding: 30 }}>
      <h4>React-Bootstrap Col Component</h4>
      <Row gutter={16}>
      <Col className="gutter-row" span={6}>
        <div>col-6</div>
      </Col>
      <Col className="gutter-row" span={6}>
        <div>col-6</div>
      </Col>
      <Col className="gutter-row" span={6}>
        <div>col-6</div>
      </Col>
      <Col className="gutter-row" span={6}>
        <div>col-6</div>
      </Col>
    </Row>
    </div>
  );
};

export default Test;


