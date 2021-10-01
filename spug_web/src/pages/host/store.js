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
  @observable importVisible = false;

  @observable f_name;
  @observable f_zone;
  @observable f_host;
  @observable f_ip;

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/host/')
      .then(({hosts, zones, perms}) => {
        this.records = hosts;
        this.zones = zones;
        this.permRecords = hosts.filter(item => perms.includes(item.id));
        for (let item of hosts) {
          this.idMap[item.id] = item
        }
      })
      .finally(() => this.isFetching = false)
  };

  showForm = (info = {}) => {
    this.formVisible = true;
    this.record = info
  }
  downExcel = () => {
    return http.get(
        '/api/file/excel/host',
        {responseType:'blob'},)
    .then(res => {
      if(res){
        let url = window.URL.createObjectURL(new Blob([res.data]));
        let link = document.createElement("a");
        link.style.display = "none";
        link.href = url;
        link.setAttribute("download", "资产信息汇总.xlsx");
        link.click();
        message.success('下载成功');
      }
    })
    .finally(() => this.isFetching = false)
  }
}

export default new Store()
