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
  @observable modifypwdkey=[];


  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/host/resource/host/')
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
    // console.log(this.tpjj,this.chjj,this.f_zone,this.otp,this.pvd,this.csst,
    //   this.wzz,this.f_ip) 
      let formData={}
      // if(this.tpjj){
      //   formData["top_project"] = this.tpjj
      // }
      // if(this.chjj){
      //   formData["child_project"] = this.chjj
      // }
      // if(this.f_zone){
      //   formData["zone"] = this.f_zone
      // }
      // if(this.otp){
      //   formData["otp"] = this.otp
      // }
      // if(this.pvd){
      //   formData["provider"] = this.pvd
      // }
      // if(this.csst){
      //   formData["cluster"] = this.csst
      // }
      // if(this.wzz){
      //   formData["work_zone"] = this.wzz
      // }
      // if(this.f_ip){
      //   formData["f_ip"] = this.f_ip
      // }
      // console.log(this.tmpExcel)
      formData["data"] = this.tmpExcel
      // return http.post('/api/file/excel/host',formData)
    return http.post(
        '/api/file/excel/host',formData,
        {responseType:'blob'},)
    .then(res => {
      if(res){
        let url = window.URL.createObjectURL(new Blob([res.data]));
        let link = document.createElement("a");
        link.style.display = "none";
        link.href = url;
        link.setAttribute("download", "主机信息汇总.xlsx");
        link.click();
        message.success('下载成功');
      }
    })
    .finally(() => this.isFetching = false)
  }
  modifypwd = () => {
    // let FormData = {}
    // FormData["data"] = this.modifypwdkey
    if((this.modifypwdkey).length === 0) {
      Modal.confirm({
        title: '修改密码确认',
        content:  `没有选中则默认修改所有主机密码，谨慎操作！`,
        // content: `确定要回收【${text['ipaddress']}】?`,
        onOk: () => {
          return http.post('/api/host/updatepwd/', {data: []})
            .then(() => {
              this.isFetching = true
              message.success('修改密码中。。。1分钟后改完');

              setTimeout(() => {
                this.isFetching = false
                this.fetchRecords()
              },15000)

            })
        }
      })
    }else{
      Modal.confirm({
        title: '修改密码确认',
        content:  `修改【${(this.modifypwdkey).length}】台主机密码，谨慎操作！`,
        // content: `确定要回收【${text['ipaddress']}】?`,
        onOk: () => {
          return http.post('/api/host/updatepwd/', {data: this.modifypwdkey})
            .then(() => {
              this.isFetching = true
              message.success('修改密码中。。。1分钟后改完');

              setTimeout(() => {
                this.isFetching = false
                this.fetchRecords()
              },15000)
            })
        }
      })
    }
  }
  //   return http.post(
  //     '/api/host/updatepwd/', FormData
  //   )
  //   .then(res => {
  //       message.success('异步任务改密中。。。1分钟后密码即可生效');
  //   })
  //   .finally(() => this.isFetching = false)
  // } 
}

export default new Store()
