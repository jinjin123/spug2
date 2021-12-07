/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import ReactDOM from 'react-dom';

import { observer } from 'mobx-react';
import { Steps, Collapse, PageHeader, Spin, Tag, Button, Icon } from 'antd';
import { http, history, X_TOKEN } from 'libs';
import { AuthDiv } from 'components';
import OutView from './OutView';
import styles from './index.module.css';
import store from './store';
import lds from 'lodash';

@observer
class Ext2Rancher extends React.Component {
  constructor(props) {
    super(props);
    this.timer = null;
    this.id = props.match.params.id;
    this.log = props.match.params.log;
    this.state = {
      fetching: true,
      loading: false,
      iFrameHeight: '0px'

    }
  }

  // componentDidMount() {
  //   this.fetch()
  // }

  // componentWillUnmount() {
  //   if (this.socket) this.socket.close();
  //   if (this.timer) clearTimeout(this.timer);
  //   store.request = {targets: [], server_actions: [], host_actions: []};
  //   store.outputs = {};
  // }


  fetch = () => {
    if (!this.timer) this.setState({fetching: true});
    http.get(`/api/deploy/request/${this.id}/`, {params: {log: this.log}})
      .then(res => {
        store.request = res;
        const outputs = {};
        while (res.outputs.length) {
          const msg = JSON.parse(res.outputs.pop());
          if (!outputs.hasOwnProperty(msg.key)) {
            const data = msg.key === 'local' ? ['读取数据...        '] : [];
            outputs[msg.key] = {data}
          }
          this._parse_message(msg, outputs)
        }
        store.outputs = outputs;
        if (store.request.status === '2') {
          this.timer = setTimeout(this.fetch, 2000)
        } else {
          this.timer = null
        }
      })
      .finally(() => this.setState({fetching: false}))
  };

  _parse_message = (message, outputs) => {
    outputs = outputs || store.outputs;
    const {key, data, step, status} = message;
    if (data !== undefined) {
      outputs[key]['data'].push(data);
    }
    if (step !== undefined) outputs[key]['step'] = step;
    if (status !== undefined) outputs[key]['status'] = status;
  };

  handleDeploy = () => {
    this.setState({loading: true});
    http.post(`/api/deploy/request/${this.id}/`)
      .then(({token, outputs}) => {
        store.request.status = '2';
        store.outputs = outputs;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.socket = new WebSocket(`${protocol}//${window.location.host}/api/ws/exec/${token}/?x-token=${X_TOKEN}`);
        this.socket.onopen = () => {
          this.socket.send('ok');
        };
        this.socket.onmessage = e => {
          if (e.data === 'pong') {
            this.socket.send('ping')
          } else {
            this._parse_message(JSON.parse(e.data))
          }
        }
      })
      .finally(() => this.setState({loading: false}))
  };

  getStatus = (key, n) => {
    const step = lds.get(store.outputs, `${key}.step`, -1);
    const isError = lds.get(store.outputs, `${key}.status`) === 'error';
    const icon = <Icon type="loading"/>;
    if (n > step) {
      return {key: n, status: 'wait'}
    } else if (n === step) {
      return isError ? {key: n, status: 'error'} : {key: n, status: 'process', icon}
    } else {
      return {key: n, status: 'finish'}
    }
  };

  getStatusAlias = () => {
    if (Object.keys(store.outputs).length !== 0) {
      const {targets, host_actions} = store.request;
      for (let item of [{id: 'local'}, ...(host_actions.length > 0 ? targets : [])]) {
        if (lds.get(store.outputs, `${item.id}.status`) === 'error') {
          return <Tag color="red">发布异常</Tag>
        } else if (lds.get(store.outputs, `${item.id}.step`, -1) < 100) {
          return <Tag color="blue">发布中</Tag>
        }
      }
      return <Tag color="green">发布成功</Tag>
    } else {
      return <Tag>{store.request['status_alias'] || '...'}</Tag>
    }
  };

  render() {
    // const {app_name, env_name, status, server_actions, host_actions} = store.request;
    return (
        <div>aa</div>
    )
  }
}

export default Ext2Rancher
