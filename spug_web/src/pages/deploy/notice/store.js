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
  @observable toppj = [];
  @observable rancherpj = [];
  @observable isFetching = false;
  @observable formVisible = false;
  @observable topproject;
  @observable ns;
  @observable rj;
  @observable app;
  @observable user;
  @observable f_name;
  @observable f_status;

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/app/deploy/svc/notice')
      .then(({pj,rj,data})=>{
        this.records = data;
        this.toppj = pj;
        this.rancherpj = rj;
      })
      .finally(() => this.isFetching = false)
  };

  showForm = (info = {}) => {
    this.formVisible = true;
    this.record = info
  }
}

export default new Store()
