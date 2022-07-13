import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// import { with } from 'react-router-dom';
import { connect } from 'react-redux';
import './uploaddropzone.css';
import { uploadingData, resetState} from '../../../reducers/editstate';
import FrontPageHeader from '../../../FrontPageHeader/FrontPageHeader';
import UploadUsingDropzone from './UploadUsingDropzone.js';
// import FooterPage from '../Footer/FooterPage';
import Test from "./Test"

class ErrorBoundary extends React.Component {
    constructor(props) {
      super(props);
      this.state = { error: null, errorInfo: null };
    }
    
    componentDidCatch(error, errorInfo) {
      // Catch errors in any components below and re-render with error message
      this.setState({
        error: error,
        errorInfo: errorInfo
      })
      // You can also log error messages to an error reporting service here
    }
    
    render() {
      if (this.state.errorInfo) {
        // Error path
        return (
          <div>
            <h2>Something went wrong.</h2>
            <details style={{ whiteSpace: 'pre-wrap' }}>
              {this.state.error && this.state.error.toString()}
              <br />
              {this.state.errorInfo.componentStack}
            </details>
          </div>
        );
      }
      // Normally, just render children
      return this.props.children;
    }  
  }
const UploadUsingDropzoneContainer = (props) => {
  const [files, setFiles] = useState([]);
  const [config, setConfig] = useState({platform: "Dark Web", visualisations: ["Fake News", 
  "Stance Detection", "Summary", "Word Cloud","Topic Modelling", "NER and Relation"]});
  const { resetState } = props;

  useEffect(() => {
    // resetState();
  }, [resetState]);

  const deleteFile = (event) => {
    setFiles(files.filter((_, i) => i !== event));
  };
  useNavigate(UploadUsingDropzoneContainer)
  const uploadFiles = () => {
    var fileType = files[0].path.split('.').slice(-1)[0];

    console.log(fileType)
    console.log(files)
    console.log(files[0])

    if (fileType === 'json') {
      if (files.length === 1) {
        props.uploadingData({ files: files[0], existing: true});
        // props.history.push('/dashboard');
      } else {
        alert('No document uploaded');
      }
    } else { // not json
      if (files.length !== 0) {
        props.uploadingData({ files: files, config: config, existing: false});
        props.history.push('/dashboard');
      } else {
        alert('No files uploaded');
      }
    }
  };

  // console.log('Uploaded Files', files, config);

  return (
    <div className="wholeThing" id="wholeThing">
      <div className="upload-container">
        {/* <ErrorBoundary> */}
            <FrontPageHeader />
        {/* </ErrorBoundary> */}
        {/* <ErrorBoundary> */}
            {/* <UploadUsingDropzone
                // files={files}
                // setFiles={setFiles}
                // uploadFiles={uploadFiles}
                // deleteFile={deleteFile}
                // setConfig={setConfig}
                // config={config}
            /> */}
            <UploadUsingDropzone/>
        {/* </ErrorBoundary> */}
      </div>
      {/* <div className="d-md-flex flex-md-equal w-100 my-md-1 pl-md-5 pr-md-5 px-md-5">
        <div className="px-md-5">
          <FooterPage />
        </div>
      </div> */}
    </div>

  );
};

const mapDispatchToProps = (dispatch) => ({
  uploadingData: (payload) => dispatch(uploadingData(payload)),
  resetState: (payload) => dispatch(resetState(payload)),
});

export default UploadUsingDropzoneContainer;
