/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable } from "mobx";
import http from 'libs/http';

class Store {
  @observable records = [];
  @observable confrecords = [];
  @observable apps = [];

  @observable record = {};
  @observable toppj = [];
  @observable rancherpj = [];
  @observable nsname = [];

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
  fetchConfig = () => {
    return http.get('/api/app/deploy/svc/all/')
    .then(({pj,svc,rj,ns,app,cmap,pvc,nodes})=>{
      this.confrecords = svc;
      this.toppj = pj;
      this.rancherpj = rj;
      this.nsname = ns;
      this.apps = app;
    })
    .finally(() => this.isFetching = false)
  }

  showForm = (info = {}) => {
    this.formVisible = true;
    this.record = info
  }
}

export default new Store()
