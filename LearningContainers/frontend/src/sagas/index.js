import { all } from 'redux-saga/effects';
import editStateSaga from './editstate';

function* rootSaga() {
  yield all([...editStateSaga]);
}

export default rootSaga;
