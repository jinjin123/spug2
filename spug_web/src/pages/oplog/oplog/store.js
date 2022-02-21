/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable } from "mobx";
import http from 'libs/http';
import { message,Modal } from 'antd';

class Store {
  @observable records = [];
  @observable zones = [];
  @observable permRecords = [];
  @observable record = {};
  @observable idMap = {};
  @observable isFetching = false;
  @observable formVisible = false;
  @observable importVisible = false;




  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/deploy/request/oplogs')
      .then(({data}) => {
        this.records = data;

      })
      .finally(() => this.isFetching = false)
  };


  showForm = (info = {}) => {
    this.formVisible = true;
    this.record = info
  }


}

export default new Store()
