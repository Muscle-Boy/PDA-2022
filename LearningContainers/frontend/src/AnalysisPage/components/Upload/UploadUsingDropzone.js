import React from 'react';
import './uploaddropzone.css';
import { Row, Col } from 'react-bootstrap';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import { TiDeleteOutline } from 'react-icons/ti';
import DropzoneContainer from '../dropbox/DropzoneContainer';
import Options from './Options';
import { css, ThemeProvider } from 'styled-components';
import { base, DocumentPdf, DocumentTxt } from 'grommet-icons';
import { deepMerge } from 'grommet-icons/utils';
import { useState, useEffect } from "react";
import Modal from 'react-bootstrap/Modal'


const UploadUsingDropzone = (props) => {
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
  const{ files, setFiles, uploadFiles, deleteFile, setConfig, config} = props;
  const[show,setShow] = useState(false);
  const handleShow = () => setShow(true);
  const handleClose = () => setShow(false);

  const handleToggle = () => setShow(!show);

  // const random = () => {
  //   if(blah){
  //     hdd
  //   } else {
  //     haha
  //   }

  // }

  // useEffect(()=>{
  //   if(show){
  //     document.getElementById('id01').style.display = "block";
  //   } else {
  //     document.getElementById('id01').style.display = "none";
  //   }
  // }, [show])

  return(

    <React.Fragment>
      <h1>hi</h1>
      <DropzoneContainer/>
      <section id="theanalysispagetoppart">

      {/* <div className="upload-column" lg={7} md={7} sm={12} xs={12}>
        <div className="uploaded-files">
          <div className="uploaded-files-header">
            <h4>Uploaded Files</h4>
            <div className="uploaded-files-subheader">
              <span>{files.length} Files</span>
              <span>
                {(
                  files.reduce((acc, e) => acc + e.size, 0.0) / 1000000
                ).toFixed(2)}{' '}
                MB
              </span>
            </div>
          </div>
          <Divider className="divider" />


          {files.map((file, index) => {
            return (
              <div className="uploaded-file-container" key={index}>
                <div className="uploaded-file">
                  <ThemeProvider theme={customColorTheme}>
                    {file.name.substring(
                      file.name.lastIndexOf('.') + 1,
                      file.name.length
                    ) === 'pdf' ? (
                      <DocumentPdf color="brand" />
                    ) : (
                      <DocumentTxt color="brand" />
                    )}
                  </ThemeProvider>
                  <div className="uploaded-file-details">
                    <span>File Name: {file.name}</span>
                    <span>File Size: {(file.size / 1000000).toFixed(2)}MB</span>
                  </div>
                </div>
                <div className="delete-uploaded-file">
                  <TiDeleteOutline
                    size={30}
                    color="red"
                    onClick={() => deleteFile(index)}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div> */}


      </section>

      
    </React.Fragment>

  )
}
export default UploadUsingDropzone;
// const customColorTheme = deepMerge(base, {
//   global: {
//     colors: {
//       icons: '#333333',
//     },
//   },
//   icon: {
//     extend: css`
//       ${(props) =>
//         props.color === 'brand' &&
//         `
//         fill: #64FFDA;
//         stroke: #64FFDA;
//       `}
//     `,
//   },
// });

// const UploadUsingDropzone = (props) => {
//   const { files, setFiles, uploadFiles, deleteFile, setConfig, config } = props;

//   // for the modal 
//   const [show, setShow] = useState(false);

//   // const handleClose = () => setShow(false);
//   // const handleShow = () => setShow(true);

//   const handleShow = () => {

//   }

//   const handleClose = () => {
    
//   }

//   // check file type
  
//   const isJson = (fileType) => {
//     if (fileType == 'json') {
//       return true;
//     } else {
//       return false;
//     }
//   };

//   // for process button 
//   const handleClick = (file) => {
//     if (file.length===1){
//       var fileType = file[0].path.split('.').slice(-1)[0];
//       if (isJson(fileType)) {
//         uploadFiles();
//       } else {
//         handleShow();
//       }
//     } else {
//       handleShow();
//     }
//     // console.log(file)
//   }  

//   // for button style
//   // const useStyles = makeStyles(theme => ({
//   //   outlined: {
//   //     color: 'rgb(3, 155, 144)',
//   //     border: '1px solid',
//   //     margin: '8px',
//   //     "&:hover": {
//   //       color: '#b1fdf8'
//   //     }
//   //   }
//   // }));
//   // const classes = useStyles();

//   return (
//     <Row className="upload-row" lg={2} md={2} sm={1} xs={1}>
//       <Col className="upload-column" lg={5} md={5} sm={12} xs={12}>
//         {/* <DropzoneContainer files={files} setFiles={setFiles} /> */}

//         <div className="upload-button">
//           <Button
//             variant="outlined"
//             // onClick={() => handleClick(files)}
//             // className={classes.outlined}
//           >
//             <span>PROCESS</span>
//           </Button>
//         </div>
//         {/* <Modal
//           show={show}
//           onHide={handleClose}
//           backdrop="static"
//           // keyboard={false}
//           >
          
//           <Modal.Header closeButton>
//             <Modal.Title>What would you like to analyse?</Modal.Title>
//           </Modal.Header>
//           <Modal.Body>
//              Import option form here 
//             <Options setConfig={setConfig} uploadFiles={uploadFiles}/>
//           </Modal.Body>
//           <Modal.Footer>
//             <Button variant="secondary" onClick={handleClose}>CLOSE</Button>
//             <Button variant="primary" onClick={uploadFiles}>SUBMIT</Button>
//           </Modal.Footer>
//         </Modal> */}
//       </Col>

//       <Col className="upload-column" lg={7} md={7} sm={12} xs={12}>
//         <div className="uploaded-files">
//           {/* <div className="uploaded-files-header">
//             <h4>Uploaded Files</h4>
//             <div className="uploaded-files-subheader">
//               <span>{files.length} Files</span>
//               <span>
//                 {(
//                   files.reduce((acc, e) => acc + e.size, 0.0) / 1000000
//                 ).toFixed(2)}{' '}
//                 MB
//               </span>
//             </div>
//           </div> */}
//           {/* <Divider className="divider" /> */}


//           {
//           // files.map((file, index) => {
//           //   return (
//           //     <div className="uploaded-file-container" key={index}>
//           //       <div className="uploaded-file">
//           //         <ThemeProvider theme={customColorTheme}>
//           //           {/* {file.name.substring(
//           //             file.name.lastIndexOf('.') + 1,
//           //             file.name.length
//           //           ) === 'pdf' ? (
//           //             <DocumentPdf color="brand" />
//           //           ) : (
//           //             <DocumentTxt color="brand" />
//           //           )} */}
//           //         </ThemeProvider>
//           //         <div className="uploaded-file-details">
//           //           <span>File Name: {file.name}</span>
//           //           <span>File Size: {(file.size / 1000000).toFixed(2)}MB</span>
//           //         </div>
//           //       </div>
//           //       <div className="delete-uploaded-file">
//           //         <TiDeleteOutline
//           //           size={30}
//           //           color="red"
//           //           // onClick={() => deleteFile(index)}
//           //         />
//           //       </div>
//           //     </div>
//           //   );
//           // })
//           }
//         </div>
//       </Col>
//     </Row>
//   );
// };

