/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable } from "mobx";
import http from 'libs/http';
import { message } from 'antd';

class Store {
  @observable records = [];
  @observable zones = [];
  @observable permRecords = [];
  @observable record = {};
  @observable idMap = {};
  @observable isFetching = false;
  @observable formVisible = false;
  @observable winformVisible = false;
  @observable importVisible = false;

  @observable f_name;
  @observable f_zone;
  @observable f_host;
  @observable f_ip;

  @observable res_t= [];
  @observable w_z =[];
  @observable provider=[];
  @observable ostp=[];
  @observable tpj=[];
  @observable pvd;
  @observable otp;
  @observable rtp;
  @observable tpjj;
  @observable csst;
  @observable wzz;

  @observable chjj;
  @observable cs=[];
  @observable wz=[];
  @observable zz=[];
  @observable svbag=[];
  @observable polist=[];
  @observable dvpo=[];
  @observable cuser=[];
  @observable rset=[];
  @observable pj=[];
  @observable envs=[];


  @observable tmpExcel=[];

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/host/dbresource/db/')
      .then(({hosts, zones, perms, res_t,w_z,provider,ostp,tp,cs, wz, zz, svbag,polist,dvpo,cuser,rset,pj,envs}) => {
        this.records = hosts;
        this.zones = zones;
        this.res_t = res_t;
        this.tpj = tp;
        this.w_z = w_z;
        this.ostp = ostp;
        this.provider = provider;

        this.cs = cs;
        this.wz = wz;
        this.zz = zz;
        this.svbag = svbag;
        this.polist = polist;
        this.dvpo = dvpo;
        this.cuser = cuser;
        this.rset = rset;
        this.pj = pj;
        this.envs = envs;
        this.permRecords = hosts.filter(item => perms.includes(item.id));
        for (let item of hosts) {
          this.idMap[item.id] = item
        }
      })
      .finally(() => this.isFetching = false)
  };
  // fetchAllConfig  = () => {
  //   this.isFetching = true;
  //   return http.get('/api/config/hostall/')
  //     .then(({cs, wz, zz, svbag,polist,dvpo,cuser,rset,pj,envs}) => {
  //       this.cs = cs;
  //       this.wz = wz;
  //       this.zz = zz;
  //       this.svbag = svbag;
  //       this.polist = polist;
  //       this.dvpo = dvpo;
  //       this.cuser = cuser;
  //       this.rset = rset;
  //       this.pj = pj;
  //       this.envs = envs;

  //     })
  //     .finally(
  //       () => this.isFetching = false
  //     )
  // }

  showForm = (info = {}) => {
    this.formVisible = true;
    this.record = info
  }
  downExcel = () => {
    let formData={}
    formData["data"] = this.tmpExcel
    this.isFetching = true
    return http.post(
        '/api/file/dbmexcel/host', formData,
        {responseType:'blob'},)
    .then(res => {
      if(res){
        let url = window.URL.createObjectURL(new Blob([res.data]));
        let link = document.createElement("a");
        link.style.display = "none";
        link.href = url;
        link.setAttribute("download", "数据库信息汇总.xlsx");
        link.click();
        message.success('下载成功');
      }
    })
    .finally(() => this.isFetching = false)
  }
}

export default new Store()
