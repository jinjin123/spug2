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
  @observable noderecords = [];

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
  @observable pvcForm =false;
  @observable cmpForm =false;
  @observable codeRead = false;
  // @observable fullmode=[];
  @observable historyVisible = false;
  @observable historyDetailVisible = false;
  @observable restartVisible = false;
  @observable restartrecord;
  @observable versiontmp = [];
  @observable f_name;
  @observable f_desc;
  @observable project;
  @observable ns;
  @observable app;
  @observable cmapsearch;
  @observable pvcsearch;
  @observable fullmode=[false];
  @observable fullmode_flag=0;
  @observable envname;
  @observable volume;
  @observable topproject;
  @observable rj;
  @observable pbtype = 1;
  @observable rancherPublish = false;
  @observable addRancherVisible = false;
  @observable desccomment;

  @observable ranchercmp=[{"k":"","v":""}];
  @observable rancherenv=[];
  @observable rancherport=[];
  @observable rancherVolume=[];
  @observable rancherCallhost=[];
  @observable cmaprecord = {};
  @observable historytmpdetail = {};
  @observable clonedeploy = null;

  // @observable rancherCallhost=[{"itemid":1,"iteminput":"","itemdata":[]},
  // {"itemid":2,"itemdata":
  // [{"itemid":1,"itemtitle":"必须","itemk":"","itemtype":"","itemv":""},
  // {"itemid":2,"itemtitle":"最好","itemk":"","itemtype":"","itemv":""},
  // {"itemid":3,"itemtitle":"首选","itemk":"","itemtype":"","itemv":""}]}];


  // @observable loadings = [];

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/app/deploy/svc/ioc/')
      .then(({pj,svc,rj,ns,app,cmap,pvc,nodes})=>{
        this.records = svc;
        this.toppj = pj;
        this.rancherpj = rj;
        this.nsname = ns;
        this.apps = app;
        this.cmaprecords =  cmap;
        this.pvcrecords =  pvc;
        this.noderecords = nodes
      })
      .finally(() => this.isFetching = false)
  };

  showAddForm = () => {
    this.deployForm = true;
  }
  showAddPvcForm = () => {
    this.pvcForm = true;
  }
  showAddCmpForm = () => {
    this.cmpForm = true;
    this.cmaprecord = {};
    this.fullmode=[false];
    this.ranchercmp=[{"k":"","v":"占位填充，需要自行删除------------------------------------------>"}]
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
  showForm = (info,status = {}) => {
    console.log(info)
    this.historyDetailVisible = true;
    this.historytmpdetail = info;
    this.codeRead = !status ? false : true;
  }
  onChange = ({ target: { value } }) => {
    this.desccomment =  value ;
  };
}

export default new Store()
