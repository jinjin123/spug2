/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable } from "mobx";
import http from 'libs/http';

class Store {
  @observable records = [];
  @observable record = {};
  @observable isFetching = false;
  @observable formVisible = false;
  @observable historyVisible = false;
  @observable env = {};
  @observable codeRead = false;
  @observable vrecords = [];

  @observable f_name;

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/config/rsconfagg/')
      .then(res => this.records = res)
      .finally(() => this.isFetching = false)
  };

  showForm = (info,status = {}) => {
    this.formVisible = true;
    this.record = info;
    this.codeRead = !status ? false : true;
  }
  showHistory = (info = {}) => {
    this.isFetching = true;
    this.historyVisible = true;
    this.record = info;
    return http.get('/api/config/rsconfig/',{params:{configid: info.configid,old_id: info.id}})
    .then(res => this.vrecords = res)
    .finally(() => this.isFetching = false)
  }
}

export default new Store()
