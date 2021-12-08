/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import ReactDOM from 'react-dom';

import { observer } from 'mobx-react';
import { Steps, Collapse, PageHeader, Spin, Tag, Button, Icon,Input } from 'antd';
import { http, history, X_TOKEN } from 'libs';
import { AuthDiv, SearchForm } from 'components';
import OutView from './OutView';
import styles from './index.module.css';
import store from './store';
import lds, { times } from 'lodash';

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
      iFrameHeight: '0px',
      tmplog: null,
      status:null
    }
  }

  componentDidMount() {
    this.fetch()
  }

  // componentWillUnmount() {
  //   if (this.socket) this.socket.close();
  //   if (this.timer) clearTimeout(this.timer);
  //   store.request = {targets: [], server_actions: [], host_actions: []};
  //   store.outputs = {};
  // }


  fetch = () => {
    if (!this.timer) this.setState({fetching: true});
    http.get(`/api/deploy/request/2/${this.id}/`)
      .then((data) => {
        this.state.tmplog = JSON.stringify(data.data,undefined, 4)
        var s = (this.state.tmplog).search(/"state": "active"/g)
        if(s == 0){
          this.state.status = "red"
        }else{
          this.state.status = "#52c41a"

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

  render() {
    const { TextArea } = Input;
    const { tmplog,status } = this.state;
    return (
      <>
              <SearchForm>
                  <SearchForm.Item span={4} style={{textAlign: 'right'}}>
                    <Button type="primary" icon="sync" onClick={()=>this.fetch()}>刷新重新获取结果</Button>
                  </SearchForm.Item>
                <SearchForm.Item span={4} style={{textAlign: 'right'}}>
                      发布结果：<Icon type="check-circle" theme="twoTone" twoToneColor={status} />
                </SearchForm.Item>
              </SearchForm>
              <TextArea 
              value={tmplog}
              
              placeholder="Autosize height based on content lines" autoSize />

      </>
    )
  }
}

export default Ext2Rancher
