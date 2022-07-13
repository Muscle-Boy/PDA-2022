import React from 'react';
import './Dropzone.css';
import Dropzone from 'react-dropzone';

const DropzoneContainer = (props) => {
 // Checks whether the file passed in is a json
 const isJson = (fileType) => {
  if (fileType == 'json') {
    return true;
  } else {
    return false;
  }
};

// Check whether a json file has been uploaded previously. 
// This is for consequtive uploads before pressing process
const checkHistoryForJson = (history) => {
  for (var i = 0; i < history.length; i++) {
    var fileType = history[i].path.split('.').slice(-1)[0]
    if (isJson(fileType)) {
      return true;
    } else {
      return false; 
    }
  }
}
 
  return (
    

    <h1>fef</h1>
    // <Dropzone>
      
    // </Dropzone>
    // <Dropzone
    //   onDrop={(acceptedFiles) =>{
    //     if (acceptedFiles.length===1){
    //       var fileType = acceptedFiles[0].path.split('.').slice(-1)[0];
    //       if (isJson(fileType)) { 
    //         props.setFiles(acceptedFiles);
    //       } else {
    //         props.setFiles([...props.files, ...acceptedFiles]);
    //       }
    //     } else {
    //       try{
    //         for (var i=0; i<acceptedFiles.length; i++){
    //           var fileType = acceptedFiles[i].path.split('.').slice(-1)[0];      
    //           if (isJson(fileType)) {
    //             alert("Only 1 .json file is accepted!")
    //             throw TypeError;
    //           }
    //         }
    //         //check for json in history
    //         var history = props.files
    //         if (checkHistoryForJson(history)) {
    //           alert("Only 1 .json file is accepted!")
    //         } else {
    //           props.setFiles([...props.files, ...acceptedFiles]);
    //         }
    //       } 
    //       catch(TypeError) {
    //         console.log("incorrect input")
    //       }
    //     }
        
    //   }
    // }
    // accept="application/pdf,text/plain,application/json,.csv,application/vnd.ms-excel"

    // >
    //   {({
    //     getRootProps,
    //     getInputProps,
    //     isDragAccept,
    //     isDragActive,
    //     isDragReject,
    //   }) => {
    //     const acceptClass = isDragAccept ? 'acceptStyle' : '';
    //     const rejectClass = isDragReject ? 'rejectStyle' : '';
    //     const activeClass = isDragActive ? 'activeStyle' : '';
    //     return (
    //       <div
    //         {...getRootProps({
    //           className: `dropzone ${acceptClass} ${rejectClass} ${activeClass}`,
    //         })}
    //       >
    //         <input {...getInputProps()} />
    //         <img
    //           id='logo-image'
    //           className='logo-image'
    //           src={require('../../../images/logo.png')}
    //           alt="Sentir logo"
    //         />
    //         {isDragAccept && <span>All files will be accepted</span>}
    //         {isDragReject && <span>Some files will be rejected</span>}
    //         {!isDragActive && <span>Drop some files here!</span>}
    //         <div className="footnote-text">
    //           <span>.json, .pdf, .csv and .txt files accepted</span>
    //         </div>
    //       </div>
    //     );
    //   }}
    // </Dropzone>
  );
};

export default DropzoneContainer;
