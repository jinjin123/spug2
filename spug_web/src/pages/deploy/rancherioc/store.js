/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable } from "mobx";
import http from 'libs/http';

class Store {
  @observable records = [];
  @observable cmaprecords = [];
  @observable pvcrecords = [];

  @observable toppj = [];
  @observable rancherpj = [];
  @observable nsname = [];
  @observable apps = [];
  @observable record = {};
  @observable deploy = {};
  @observable page = 0;
  @observable loading = {};
  @observable isReadOnly = false;
  @observable isFetching = false;
  @observable formVisible = false;
  @observable addVisible = false;
  @observable ext1Visible = false;
  @observable ext2Visible = false;
  @observable deployForm =false;
  @observable f_name;
  @observable f_desc;
  @observable project;
  @observable ns;
  @observable app;
  @observable fullmode=[false];
  @observable fullmode_flag=0;
  @observable envname;
  @observable volume;
  @observable topproject;
  @observable rj;
  @observable pbtype = 1;
  @observable rancherPublish = false;
  @observable addRancherVisible = false;

  @observable rancherenv=[{}];
  @observable rancherport=[{}];
  @observable rancherVolume=[];
  @observable rancherCallhost=[];
  // @observable rancherCallhost=[{"itemid":1,"iteminput":"","itemdata":[]},
  // {"itemid":2,"itemdata":
  // [{"itemid":1,"itemtitle":"必须","itemk":"","itemtype":"","itemv":""},
  // {"itemid":2,"itemtitle":"最好","itemk":"","itemtype":"","itemv":""},
  // {"itemid":3,"itemtitle":"首选","itemk":"","itemtype":"","itemv":""}]}];


  // @observable loadings = [];

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/app/deploy/svc/ioc/')
      .then(({pj,svc,rj,ns,app,cmap,pvc})=>{
        this.records = svc;
        this.toppj = pj;
        this.rancherpj = rj;
        this.nsname = ns;
        this.apps = app;
        this.cmaprecords =  cmap;
        this.pvcrecords =  pvc;
      })
      .finally(() => this.isFetching = false)
  };

  showAddForm = () => {
    this.deployForm = true;
  }
  showRancerExtForm = (e, app_id, info, isClone, isReadOnly = false) => {
    if (e) e.stopPropagation();
    this.page = 0;
    this.app_id = app_id;
    this.isReadOnly = isReadOnly
    if (info) {
      if (info.extend === '1') {
        this.ext1Visible = true
      } else {
        this.ext2Visible = true
      }
      isClone && delete info.id;
      this.deploy = info
    } else {
      this.addRancherVisible = true;
      this.rancherPublish = true;
    }
  };
  showFullMode = (index,status) => {
    if(this.fullmode_flag === 0 ){
      this.fullmode[index] = true;
      this.fullmode_flag = 1;
    }else{
      this.fullmode_flag=0;
      this.fullmode[index]=false
    }
  }
}

export default new Store()