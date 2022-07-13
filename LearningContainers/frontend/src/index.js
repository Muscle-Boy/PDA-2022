import 'react-app-polyfill/ie11';
import 'react-app-polyfill/stable';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route,Routes } from 'react-router-dom';

// import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import * as serviceWorker from './serviceWorker';
import App from './App';
import 'bootstrap/dist/css/bootstrap.css';

import Upload from './AnalysisPage/components/Upload/UploadBox';
import NavBar from './globalstuff/components/NavBar/NavBar';
// import Nav from './Nav/components/index'
import MyDropzone from './mydropzone/MyDropzone'


// import Dropzone from './AnalysisPage/components/dropbox/DropzoneContainer';
import DropzoneAlicia from './AnalysisPage/components/Upload/UploadUsingDropzoneContainer';
// import UploadForm from "./test/containers/UploadForm";
// import TestTest from "./test2/components/index"
// import About from './components/FrontPage/About';
// import Home from './components/FrontPage/Home';
// import Preview from './components/FrontPage/SaveAndPreview';
// import DataSource from './components/FrontPage/DataSource'

import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import createSagaMiddleware from 'redux-saga';
import { Provider } from 'react-redux';

import reducers from './reducers';
import rootSaga from './sagas';

// // create the saga middleware
const sagaMiddleware = createSagaMiddleware();
// mount it on the Store
const store = createStore(
  reducers,
  composeWithDevTools(applyMiddleware(sagaMiddleware))
);

sagaMiddleware.run(rootSaga);


ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <Routes>
        {/* <Route path="/dashboard">
          <App />
        </Route> */}
         <Route path="/" element={<App/>}/> 
         <Route path="/upload" element={<Upload/>}/>
         {/* <Route path="/nav" element={<Nav/>}/> */}
         {/* <Route path="/dropzone" element={<Dropzone/>}/> */}
         <Route path="/MyDropzone" element={<MyDropzone/>}/>
         {/* <Route path="/UploadForm" element={<testtest/>}/> */}
         <Route path="/navbar" element={<NavBar/>}/>
        
      
        {/* <Route path="/about" component={About} />
        <Route path="/upload" component={Upload} />
        <Route path="/preview" component={Preview} />
        <Route path="/datasource" component={DataSource} /> */}
        {/* <PrivateRoute path="/test" component={testLogin} /> */}

        {/* <Route path="/" component={Upload} /> */}
      </Routes>
     
    </BrowserRouter>

    </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

module.hot.accept();
