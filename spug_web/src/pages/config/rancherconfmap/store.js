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
  @observable configMap = [];

  @observable f_name;
  @observable fullmode=false;
  @observable fullmode_flag=0;
  @observable project;
  @observable pjtips = [];
  @observable pjtip;
  @observable nstips = [];
  @observable nstip;
  @observable configname;
  @observable envname;
  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/config/rsconfagg/')
      .then(res=> {
        this.records =res
        if((this.pjtips).length<1){
          let tmp = [];
          this.records.map((item) =>{
            tmp.push(item.project)
          })
          this.pjtips = [...new Set(tmp)]
        }
        if((this.nstips).length<1){
          let tmp = [];
          this.records.map((item) =>{
            tmp.push(item.namespace)
          })
          this.nstips = [...new Set(tmp)]
        }
      })
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
  showFullMode = (status = {}) => {
    if(this.fullmode_flag == 0 ){
      this.fullmode = !status ? false : true;
      this.fullmode_flag = 1;
    }else{
      this.fullmode_flag=0;
      this.fullmode=false
    }
  }
  showAddForm = () => {
    this.formVisible = true;
    this.record = {};
    this.codeRead = false;
  }

}

export default new Store()
