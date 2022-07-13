import { put, all, call, select, takeEvery } from 'redux-saga/effects';
import {
  types,
  getNerData,
  getRelationData,
} from '../reducers/editstate';
import axios from 'axios';
import { initialLayout } from '../utils/layout';
import { initialOverviewLayout } from '../utils/overviewLayout';

// Posts the updated relation data to the backend and returns the updated network data.
const apiPostNetwork = (data) => {
  const formData = new FormData();
  formData.append('relationData', JSON.stringify(data));
  return axios.post('http://localhost:5000/updateNetwork', formData);
};

// Dispatches the action UPDATED_NETWORK_DATA to update the redux store with the new network data based on the file that was changed.
function* updateNetworkHelper({ data, currentFileName }) {
  const res = yield call(apiPostNetwork, data);
  const networkData = res.data;
  yield put({
    type: types.UPDATED_NETWORK_DATA,
    payload: networkData,
    currentFileName: currentFileName,
  });
}


// Dispatches the action UPLOADED_CORPUS_DATA to update the redux store with the new corpus data.
function* setCorpusData({ data }) {
  yield put({
    type: types.UPLOADED_CORPUS_DATA,
    payload: data,
  });
}

// Dispatches the action SET_FILENAMES and SET_LAYOUT based on the object keys of the corpus data.
function* setFileNames({ data }) {
  const fileNames = Object.keys(data);
  yield put({
    type: types.SET_FILENAMES,
    payload: fileNames,
  });
  var layouts = {};
  if (fileNames.length > 1) {
    fileNames
      .filter((e) => e !== 'Overview')
      .forEach((e) => (layouts[e] = initialLayout));
    layouts['Overview'] = initialOverviewLayout;
  } else {
    layouts[fileNames[0]] = initialLayout;
  }
  yield put({
    type: types.SET_LAYOUT,
    payload: layouts,
  });
}

// Posts the uploaded files to the backend and returns the output.
const apiPost = (payload) => {
  const formData = new FormData();
  console.log("payload: ", payload)
  var fileNames = [];
  for (var i = 0; i < payload.files.length; i++) {
    formData.append('file'.concat(i.toString()), payload.files[i]);
    fileNames.push(payload.files[i].name);
  }
  fileNames = JSON.stringify(fileNames);
  formData.append('fileNames', fileNames);
  formData.append('length', payload.files.length);

  console.log("payload files ", payload.files)
  
  var configFile = JSON.stringify(payload.config)
  formData.append('config', configFile);

  console.log("config: ", configFile)

  // inspect formData
  for (var pair of formData.entries()) {
      console.log(pair[0]+ ', ' + pair[1]); 
  }

  return axios.post('http://uploadfile-sme-project.apps.kw.projectinnovate.sg/uploadFile', formData);
};

// Posts the JSON document to the backend and returns the output.
const apiPostJson = (payload) => {
  const formData = new FormData();
  formData.append('existingFile', payload);
  // 'http://loadexistingfile-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/loadExistingFile'
  return axios.post('http://loadexistingfile-sme-project.apps.kw.projectinnovate.sg/loadExistingFile', formData);
};

// Posts the ObjectID of the document and returns the output from the MongoDB entry corresponding
// to that ObjectID.
const apiPostDb = (payload) => {
  // 'http://loaddbfile-alice.apps.8d5714affbde4fa6828a.southeastasia.azmosa.io/loadDbFile'
  return axios.post('http://localhost:5000/loadDbFile', {ID: payload});
}


// Posts the webscape request to the backend and returns the output.
const apiScrape = (payload) => {
  /*
  Have to convert the dictionary to a compatible object form for Flask to receive properly
  however, an array will still be received as a string by Flask so
  manipulate the data form at the scraper side instead
  see here for more info https://stackoverflow.com/questions/54892531/axios-data-coming-up-as-immutablemultidict-when-sent-to-flask-post-route-bu
  */
  
  const params = new URLSearchParams();
  const keys = Object.keys(payload);
  for (let key of keys) {
      params.append(key, payload[key]);
  }

  //return axios.post('http://localhost:5000/scrape', params);
  return axios.post('http://scrape-sme-project.apps.kw.projectinnovate.sg/scrape', params);
  };


var download_url = null;

export function get_download_url() {
  return download_url;
}

// Uploads the data to the backend to call the respective webscraper API in the backend
// dispatches the action SCRAPING_SUCCESS or SCRAPING_FAILURE depending
// on the status of the upload.
export function* scrapeData({ payload }) {
  try {
    let res;
    console.log(payload);
    res = yield call(apiScrape, payload);

    console.log('response', res);
    download_url = res.data;

    yield put({
      type: types.SCRAPING_SUCCESS,
    });
  } catch (error) {
    yield put({
      type: types.SCRAPING_FAILURE,
    });
    console.log('Error while scraping', error);
  }
}
 

// Uploads the data to the backend based on the input type and
// dispatches the action UPLOAD_SUCCESS or UPLOAD_FAILURE depending
// on the status of the upload.
// If the document uploaded is an existing one (JSON or MongoDB ObjectID),
// the function dispatches the action SET_EXISTING_DOCUMENT.
export function* uploadData({ payload }) {
  try {
    let res;
    if (payload.existing) {
      if (payload.docId) {
        res = yield call(apiPostDb, payload.docId);
        console.log(payload)
        console.log(res)
      } else {
        res = yield call(apiPostJson, payload.files);
      }
      console.log(payload)
      console.log(res)
      const existingData = res.data;

      // Remove bugs related to network graph when loading existing file
      existingData.fileNames.forEach((document) => {
        console.log(existingData);
        console.log(existingData.corpusData[document]);
        if (existingData.corpusData[document].network.links.length > 0) {
          if (existingData.corpusData[document].network.links[0].source.id) {
            existingData.corpusData[document].network.links.forEach((link) => {
              link.source = link.source.id;
              link.target = link.target.id;
              delete link.__indexColor;
              delete link.__controlPoints;
              delete link.__photons;
              delete link.index;
            });

            existingData.corpusData[document].network.nodes.forEach((node) => {
              delete node.index;
              delete node.x;
              delete node.y;
              delete node.vx;
              delete node.vy;
              delete node.__indexColor;
            });
          }
        }
      });

      yield put({
        type: types.SET_EXISTING_DOCUMENT,
        payload: existingData,
      });
    } else {
      console.log("apipost payload", payload);
      res = yield call(apiPost, payload);
      const newData = res.data;
      if (Object.keys(newData).length === 0) {
        throw new Error('Document could not be processed');
      }

      // Remove bugs related to network graph when generating new data
      Object.keys(newData.corpusData).forEach((document) => {
        console.log(newData);
        console.log(newData.corpusData[document]);
        if (newData.corpusData[document].network.links.length > 0) {
          if (newData.corpusData[document].network.links[0].source.id) {
            newData.corpusData[document].network.links.forEach((link) => {
              link.source = link.source.id;
              link.target = link.target.id;
              delete link.__indexColor;
              delete link.__controlPoints;
              delete link.__photons;
              delete link.index;
            });

            newData.corpusData[document].network.nodes.forEach((node) => {
              delete node.index;
              delete node.x;
              delete node.y;
              delete node.vx;
              delete node.vy;
              delete node.__indexColor;
            });
          }
        }
      });
      const args = { data: newData.corpusData };
      yield all([call(setCorpusData, args), call(setFileNames, args)]);
    }
    yield put({
      type: types.UPLOAD_SUCCESS,
    });
  } catch (error) {
    yield put({
      type: types.UPLOAD_FAILURE,
    });
    console.log('ERROR', error);
  }
}

// Dispatches the action UPDATED_NER_DATA to update the redux store with the new NER data based on the file that was changed.
// // Updates the relation and network data based on the new changes.
function* updateNer({ payload }) {
  const { newNer, nerToRelation, currentFileName } = payload;
  const currentNerData = yield select(getNerData, [currentFileName]);
  const text = currentNerData.text;
  const currentRelationData = yield select(getRelationData, currentFileName);
  var newRelationData;
  if (nerToRelation[3] === 'DELETE') {
    newRelationData = currentRelationData.filter((e) => {
      return (
        (e.e1 !== nerToRelation[0] || e.e1_id !== nerToRelation[1]) &&
        (e.e2 !== nerToRelation[0] || e.e2_id !== nerToRelation[1])
      );
    });
  } else {
    newRelationData = currentRelationData.map((e) => {
      if (e.e1 === nerToRelation[0] && e.e1_id === nerToRelation[1]) {
        e.e1_label = nerToRelation[2];
      } else if (e.e2 === nerToRelation[0] && e.e2_id === nerToRelation[1]) {
        e.e2_label = nerToRelation[2];
      }
      return e;
    });
  }

  yield put({
    type: types.UPDATED_NER_DATA,
    payload: {
      text: text,
      ents: newNer,
    },
    currentFileName: currentFileName,
  });
  const args = { data: newRelationData, currentFileName: currentFileName };
  yield all([
    call(updateRelationHelper, args),
    call(updateNetworkHelper, args),
  ]);
}

// Dispatches the action UPDATED_RELATION_DATA to update the redux store with the new relation data based on the file that was changed.
function* updateRelationHelper({ data, currentFileName }) {
  yield put({
    type: types.UPDATED_RELATION_DATA,
    payload: data,
    currentFileName: currentFileName,
  });
}

// Updates the relation and network data based on the new changes.
function* updateRelation({ payload }) {
  const { newRelation, currentFileName } = payload;
  const args = { data: newRelation, currentFileName: currentFileName };
  yield all([
    call(updateRelationHelper, args),
    call(updateNetworkHelper, args),
  ]);
}

export default [
  takeEvery(types.UPLOADING_DATA, uploadData),
  takeEvery(types.SCRAPING_DATA, scrapeData),
  takeEvery(types.UPDATING_NER_DATA, updateNer),
  takeEvery(types.UPDATING_RELATION_DATA, updateRelation),
];
